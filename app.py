from datetime import datetime
import json
from pathlib import Path

from flask import Flask, jsonify, request
from flask_cors import CORS


# Create the Flask application.
app = Flask(__name__)

# Allow the future browser dashboard to access API endpoints.
CORS(app, resources={r"/api/*": {"origins": "*"}})


# Store courses.json next to this app.py file.
DATA_FILE = Path(__file__).parent / "courses.json"

# Courses may only use one of these status values.
VALID_STATUSES = (
    "Not Started",
    "In Progress",
    "Completed",
)

# Fields required when creating a course.
REQUIRED_FIELDS = (
    "name",
    "description",
    "target_date",
    "status",
)


def initialise_json_file():
    """Create courses.json with an empty list if it does not exist."""
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]\n", encoding="utf-8")


def load_courses():
    """Load and return all courses stored in courses.json."""
    initialise_json_file()

    try:
        content = DATA_FILE.read_text(encoding="utf-8")
        courses = json.loads(content)

        if not isinstance(courses, list):
            raise ValueError("courses.json must contain a JSON list.")

        return courses

    except json.JSONDecodeError as error:
        raise ValueError(
            f"courses.json contains invalid JSON: {error}"
        ) from error

    except OSError as error:
        raise OSError(
            f"Could not read courses.json: {error}"
        ) from error


def save_courses(courses):
    """Save the complete course list to courses.json."""
    try:
        DATA_FILE.write_text(
            json.dumps(courses, indent=2) + "\n",
            encoding="utf-8",
        )

    except OSError as error:
        raise OSError(
            f"Could not write to courses.json: {error}"
        ) from error


def get_next_id(courses):
    """Return an ID one greater than the largest existing ID."""
    return max(
        (course["id"] for course in courses),
        default=0,
    ) + 1


def validate_target_date(target_date):
    """Check that a target date uses a valid YYYY-MM-DD format."""
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
        return True
    except (TypeError, ValueError):
        return False


def validate_course_data(data, require_all_fields=True):
    """
    Validate input sent when creating or updating a course.

    Returns:
        None when the input is valid.
        A string containing an error message when it is invalid.
    """
    if not isinstance(data, dict):
        return "Request body must contain a valid JSON object."

    if require_all_fields:
        missing_fields = [
            field
            for field in REQUIRED_FIELDS
            if field not in data
            or not isinstance(data[field], str)
            or not data[field].strip()
        ]

        if missing_fields:
            return (
                "Missing or empty required fields: "
                + ", ".join(missing_fields)
            )

    for field in ("name", "description"):
        if field in data:
            if not isinstance(data[field], str) or not data[field].strip():
                return f"{field} must be a non-empty string."

    if "target_date" in data:
        if not validate_target_date(data["target_date"]):
            return "target_date must be a valid date in YYYY-MM-DD format."

    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return (
                "status must be one of: "
                + ", ".join(VALID_STATUSES)
            )

    return None


@app.get("/")
def index():
    """Return a simple response showing that the API is running."""
    return jsonify(
        {
            "success": True,
            "message": "CodeCraftHub API is running.",
        }
    ), 200


@app.get("/api/courses")
def get_all_courses():
    """Return all courses."""
    try:
        courses = load_courses()

        return jsonify(
            {
                "success": True,
                "count": len(courses),
                "courses": courses,
            }
        ), 200

    except (OSError, ValueError) as error:
        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500


@app.get("/api/courses/<int:course_id>")
def get_course(course_id):
    """Return one course identified by its ID."""
    try:
        courses = load_courses()

        course = next(
            (
                course
                for course in courses
                if course["id"] == course_id
            ),
            None,
        )

        if course is None:
            return jsonify(
                {
                    "success": False,
                    "error": "Course not found.",
                }
            ), 404

        return jsonify(
            {
                "success": True,
                "course": course,
            }
        ), 200

    except (OSError, ValueError) as error:
        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500


@app.post("/api/courses")
def add_course():
    """Create and store a new course."""
    data = request.get_json(silent=True)

    validation_error = validate_course_data(
        data,
        require_all_fields=True,
    )

    if validation_error:
        return jsonify(
            {
                "success": False,
                "error": validation_error,
            }
        ), 400

    try:
        courses = load_courses()

        new_course = {
            "id": get_next_id(courses),
            "name": data["name"].strip(),
            "description": data["description"].strip(),
            "target_date": data["target_date"],
            "status": data["status"],
            "created_at": datetime.now().isoformat(timespec="seconds"),
        }

        courses.append(new_course)
        save_courses(courses)

        return jsonify(
            {
                "success": True,
                "message": "Course added successfully.",
                "course": new_course,
            }
        ), 201

    except (OSError, ValueError) as error:
        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500


@app.put("/api/courses/<int:course_id>")
def update_course(course_id):
    """Update fields on an existing course."""
    data = request.get_json(silent=True)

    if not data:
        return jsonify(
            {
                "success": False,
                "error": "Provide at least one field to update.",
            }
        ), 400

    validation_error = validate_course_data(
        data,
        require_all_fields=False,
    )

    if validation_error:
        return jsonify(
            {
                "success": False,
                "error": validation_error,
            }
        ), 400

    try:
        courses = load_courses()

        course = next(
            (
                course
                for course in courses
                if course["id"] == course_id
            ),
            None,
        )

        if course is None:
            return jsonify(
                {
                    "success": False,
                    "error": "Course not found.",
                }
            ), 404

        allowed_fields = (
            "name",
            "description",
            "target_date",
            "status",
        )

        for field in allowed_fields:
            if field in data:
                value = data[field]

                if isinstance(value, str):
                    value = value.strip()

                course[field] = value

        save_courses(courses)

        return jsonify(
            {
                "success": True,
                "message": "Course updated successfully.",
                "course": course,
            }
        ), 200

    except (OSError, ValueError) as error:
        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500


@app.delete("/api/courses/<int:course_id>")
def delete_course(course_id):
    """Delete an existing course."""
    try:
        courses = load_courses()

        course = next(
            (
                course
                for course in courses
                if course["id"] == course_id
            ),
            None,
        )

        if course is None:
            return jsonify(
                {
                    "success": False,
                    "error": "Course not found.",
                }
            ), 404

        courses.remove(course)
        save_courses(courses)

        return jsonify(
            {
                "success": True,
                "message": "Course deleted successfully.",
                "deleted_course": course,
            }
        ), 200

    except (OSError, ValueError) as error:
        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500


# Create the data file as soon as the application starts.
initialise_json_file()


if __name__ == "__main__":
    app.run(debug=True)
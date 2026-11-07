import json
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "courses.json"

VALID_STATUSES = [
    "Not Started",
    "In Progress",
    "Completed",
]


def initialise_data_file():
    """Create the data directory and JSON file if they do not exist."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]\n", encoding="utf-8")


def read_courses():
    """Read and return all courses from the JSON file."""
    initialise_data_file()

    try:
        content = DATA_FILE.read_text(encoding="utf-8")

        if not content.strip():
            return []

        courses = json.loads(content)

        if not isinstance(courses, list):
            raise ValueError("Course data must be stored as a JSON list.")

        return courses

    except json.JSONDecodeError as error:
        raise ValueError(
            f"The course data file contains invalid JSON: {error}"
        ) from error


def write_courses(courses):
    """Write the complete course list to the JSON file."""
    initialise_data_file()

    DATA_FILE.write_text(
        json.dumps(courses, indent=2),
        encoding="utf-8",
    )


def get_all_courses():
    """Return every stored course."""
    return read_courses()
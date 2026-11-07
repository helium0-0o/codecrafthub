from flask import Flask, jsonify
from flask_cors import CORS

from courses import get_all_courses, initialise_data_file


app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*",
        }
    },
)

initialise_data_file()


@app.get("/")
def index():
    return jsonify(
        {
            "success": True,
            "message": "CodeCraftHub API is running.",
        }
    ), 200


@app.get("/api/courses")
def list_courses():
    try:
        courses = get_all_courses()

        return jsonify(
            {
                "success": True,
                "data": courses,
                "count": len(courses),
            }
        ), 200

    except (OSError, ValueError) as error:
        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500


if __name__ == "__main__":
    app.run(debug=True)
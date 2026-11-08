# CodeCraftHub

CodeCraftHub is a beginner-friendly REST API for managing a personalised list of programming courses.

The application allows users to create, view, update and delete courses. Course information is stored in a JSON file, so no database is required.

This project was created to practise:

- Python and Flask
- REST API design
- CRUD operations
- JSON file storage
- HTTP methods and status codes
- Input validation
- API testing with curl
- Cross-Origin Resource Sharing (CORS)

## Features

- Create a new course
- View all courses
- View one course by ID
- Update an existing course
- Delete a course
- Automatically generate numeric course IDs
- Automatically generate creation timestamps
- Validate required fields
- Validate target dates using the `YYYY-MM-DD` format
- Restrict course status to predefined values
- Return consistent JSON success and error responses
- Store data in a local JSON file
- Automatically create `courses.json` if it does not exist
- Enable CORS for a browser-based frontend

## Course data model

Each course contains the following fields:

| Field | Type | Description |
|---|---|---|
| `id` | Integer | Automatically generated unique identifier |
| `name` | String | Required course name |
| `description` | String | Required course description |
| `target_date` | String | Required date in `YYYY-MM-DD` format |
| `status` | String | Required course status |
| `created_at` | String | Automatically generated creation timestamp |

The allowed status values are:

- `Not Started`
- `In Progress`
- `Completed`

Example course:

```json
{
  "id": 1,
  "name": "Python Fundamentals",
  "description": "Learn core Python programming concepts",
  "target_date": "2026-12-15",
  "status": "Not Started",
  "created_at": "2026-11-08T13:21:11"
}
```

## Project structure

```text
codecrafthub/
├── app.py
├── courses.json
├── requirements.txt
├── README.md
└── .gitignore
```

### File descriptions

- `app.py`: Contains the Flask application, API routes, validation and JSON file operations.
- `courses.json`: Stores course records as a JSON array.
- `requirements.txt`: Lists the Python packages required by the project.
- `README.md`: Contains the project documentation.
- `.gitignore`: Prevents local and generated files from being committed to Git.

The local `.venv` directory is not committed because each developer should create their own virtual environment.

## Prerequisites

Before running the project, make sure the following tools are available:

- Python 3
- pip
- Git
- curl
- Visual Studio Code or another code editor

Check the installed versions:

```bash
python3 --version
git --version
curl --version
```

## Installation

### 1. Open the project directory

```bash
cd "/path/to/codecrafthub"
```

Replace `/path/to/codecrafthub` with the actual location of the project.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

On macOS or Linux:

```bash
source .venv/bin/activate
```

When the environment is active, the terminal prompt should start with:

```text
(.venv)
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Check the Flask installation

```bash
python -m flask --version
```

## Running the application

Make sure the virtual environment is active. Then run:

```bash
python -m flask --app app:app run --debug
```

The development server should start at:

```text
http://127.0.0.1:5000
```

Open the root endpoint in a browser or test it with:

```bash
curl -i http://127.0.0.1:5000/
```

Expected response:

```json
{
  "message": "CodeCraftHub API is running.",
  "success": true
}
```

Press `Ctrl+C` in the server terminal to stop the application.

> The Flask development server and debug mode are intended for local development only.

## API endpoints

The API base URL is:

```text
http://127.0.0.1:5000
```

### Create a course

**Method:** `POST`  
**Endpoint:** `/api/courses`

All four input fields are required.

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python Fundamentals",
    "description": "Learn core Python programming concepts",
    "target_date": "2026-12-15",
    "status": "Not Started"
  }'
```

Expected status:

```text
201 Created
```

Example response:

```json
{
  "course": {
    "created_at": "2026-11-08T13:21:11",
    "description": "Learn core Python programming concepts",
    "id": 1,
    "name": "Python Fundamentals",
    "status": "Not Started",
    "target_date": "2026-12-15"
  },
  "message": "Course added successfully.",
  "success": true
}
```

### Get all courses

**Method:** `GET`  
**Endpoint:** `/api/courses`

```bash
curl -i http://127.0.0.1:5000/api/courses
```

Expected status:

```text
200 OK
```

Example response:

```json
{
  "count": 1,
  "courses": [
    {
      "created_at": "2026-11-08T13:21:11",
      "description": "Learn core Python programming concepts",
      "id": 1,
      "name": "Python Fundamentals",
      "status": "Not Started",
      "target_date": "2026-12-15"
    }
  ],
  "success": true
}
```

When no courses exist:

```json
{
  "count": 0,
  "courses": [],
  "success": true
}
```

### Get a specific course

**Method:** `GET`  
**Endpoint:** `/api/courses/<course_id>`

Example using course ID `1`:

```bash
curl -i http://127.0.0.1:5000/api/courses/1
```

Expected status:

```text
200 OK
```

If the course does not exist, the API returns:

```text
404 Not Found
```

```json
{
  "error": "Course not found.",
  "success": false
}
```

### Update a course

**Method:** `PUT`  
**Endpoint:** `/api/courses/<course_id>`

Only the fields that need to change must be provided.

```bash
curl -i -X PUT http://127.0.0.1:5000/api/courses/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "In Progress",
    "target_date": "2026-12-20"
  }'
```

Expected status:

```text
200 OK
```

Example response:

```json
{
  "course": {
    "created_at": "2026-11-08T13:21:11",
    "description": "Learn core Python programming concepts",
    "id": 1,
    "name": "Python Fundamentals",
    "status": "In Progress",
    "target_date": "2026-12-20"
  },
  "message": "Course updated successfully.",
  "success": true
}
```

The `id` and `created_at` fields cannot be updated through this endpoint.

### Delete a course

**Method:** `DELETE`  
**Endpoint:** `/api/courses/<course_id>`

```bash
curl -i -X DELETE http://127.0.0.1:5000/api/courses/1
```

Expected status:

```text
200 OK
```

Example response:

```json
{
  "deleted_course": {
    "created_at": "2026-11-08T13:21:11",
    "description": "Learn core Python programming concepts",
    "id": 1,
    "name": "Python Fundamentals",
    "status": "In Progress",
    "target_date": "2026-12-20"
  },
  "message": "Course deleted successfully.",
  "success": true
}
```

## Testing error scenarios

Start the Flask server before running these tests. Use a second terminal for the curl commands.

### Missing required fields

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Incomplete Course"
  }'
```

Expected status:

```text
400 Bad Request
```

Example response:

```json
{
  "error": "Missing or empty required fields: description, target_date, status",
  "success": false
}
```

### Invalid status

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask Basics",
    "description": "Build a REST API",
    "target_date": "2026-12-30",
    "status": "Almost Finished"
  }'
```

Expected status:

```text
400 Bad Request
```

Example response:

```json
{
  "error": "status must be one of: Not Started, In Progress, Completed",
  "success": false
}
```

### Invalid target date

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flask Basics",
    "description": "Build a REST API",
    "target_date": "30-12-2026",
    "status": "Not Started"
  }'
```

Expected status:

```text
400 Bad Request
```

Example response:

```json
{
  "error": "target_date must be a valid date in YYYY-MM-DD format.",
  "success": false
}
```

### Invalid JSON request

```bash
curl -i -X POST http://127.0.0.1:5000/api/courses \
  -H "Content-Type: application/json" \
  -d 'not valid JSON'
```

Expected status:

```text
400 Bad Request
```

### Course not found

```bash
curl -i http://127.0.0.1:5000/api/courses/999
```

Expected status:

```text
404 Not Found
```

Example response:

```json
{
  "error": "Course not found.",
  "success": false
}
```

## HTTP status codes

The API uses the following status codes:

- `200 OK`: A GET, PUT or DELETE operation succeeded.
- `201 Created`: A new course was created.
- `400 Bad Request`: The request contains missing or invalid data.
- `404 Not Found`: The requested course does not exist.
- `500 Internal Server Error`: The application could not read or write the data file.

## Data storage

Course data is stored in `courses.json`.

An empty data file contains:

```json
[]
```

After courses are created, the file contains a JSON array of course objects. The application reads this file before each operation and writes the updated course list back after creating, updating or deleting a course.

This JSON storage approach is suitable for learning and small local projects. It is not intended to replace a database in a production application.

## CORS

CORS is enabled for routes under `/api/*`.

This allows a browser-based frontend running from another local origin to send requests to the API. This configuration will be used by the CodeCraftHub dashboard.

## Troubleshooting

### `ModuleNotFoundError: No module named 'flask'`

Make sure the virtual environment is active:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### Flask cannot find the application

Run Flask explicitly with the module and application object:

```bash
python -m flask --app app:app run --debug
```

Make sure the command is run from the directory containing `app.py`.

### Port 5000 is already in use

Stop the other process using port 5000 or run the application on another port:

```bash
python -m flask --app app:app run --debug --port 5001
```

When using another port, update the curl URLs accordingly.

### `courses.json` contains invalid JSON

For a fresh local test, stop the server and reset the file:

```bash
printf "[]\n" > courses.json
```

This deletes all existing course records.

Restart the application after resetting the file.

### Changes do not appear

Check that the file was saved in the editor. When debug mode is active, Flask should restart automatically after a saved code change.

### curl cannot connect to the server

Make sure the Flask server is still running in the first terminal and that the curl command uses the same host and port shown by Flask.

## Development workflow

A useful workflow for making changes is:

```text
Write → Save → Check syntax → Run → Test with curl → Commit
```

Check the Python syntax:

```bash
python -m py_compile app.py
```

Check the repository:

```bash
git status
```

Commit completed changes:

```bash
git add .
git commit -m "Describe the completed change"
```

## Future development

The next stage of CodeCraftHub is a browser-based dashboard that consumes this REST API. The dashboard will allow administrative users to create, view, update and delete courses through a visual interface.
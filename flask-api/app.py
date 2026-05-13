# ==============================================================
# DevOps Open Book Exam Flask Template
# Student: EDIT_YOUR_NAME_HERE
# Roll No: EDIT_YOUR_ROLL_NO_HERE
# Description: Complete Flask CRUD API + health check + search + stats
# Port: 5000
# ============================================================== 

from flask import Flask, jsonify, request, render_template_string

# Optional CORS support. If flask-cors is installed, browser frontend calls work.
try:
    from flask_cors import CORS
except ImportError:
    CORS = None

app = Flask(__name__)
if CORS:
    CORS(app)

# -----------------------------
# In-memory database
# -----------------------------
# This data resets whenever the server/container restarts.
students = [
    {"id": 1, "name": "Ali", "grade": "A", "course": "DevOps", "city": "Topi"},
    {"id": 2, "name": "Sara", "grade": "B", "course": "DevOps", "city": "Islamabad"},
]
next_id = 3
VALID_GRADES = {"A", "B", "C", "D", "F"}

# -----------------------------
# Helper functions
# -----------------------------
def find_student(student_id):
    """Return student dictionary by ID, or None if not found."""
    return next((student for student in students if student["id"] == student_id), None)


def get_json_body():
    """Safely read JSON body from request."""
    data = request.get_json(silent=True)
    if data is None:
        return None
    return data


def error_response(message, status_code):
    """Return consistent JSON error response."""
    return jsonify({"success": False, "error": message}), status_code


def success_response(data=None, message="success", status_code=200):
    """Return consistent JSON success response."""
    payload = {"success": True, "message": message}
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status_code


# -----------------------------
# Basic / documentation routes
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    """Simple browser homepage showing available endpoints."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DevOps Flask API</title>
        <style>
            body { font-family: Arial, sans-serif; background: #eef2f7; padding: 30px; }
            .card { background: white; padding: 25px; border-radius: 10px; max-width: 900px; margin: auto; box-shadow: 0 2px 10px #ccc; }
            h1 { color: #1F3864; }
            code { background: #f4f4f4; padding: 3px 6px; border-radius: 4px; }
            li { margin: 8px 0; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>DevOps Flask API is Running ✅</h1>
            <p>This template covers common exam tasks: Flask, REST API, CRUD, JSON, validation, status codes, health checks, and curl testing.</p>
            <h2>Useful Endpoints</h2>
            <ul>
                <li><code>GET /api/health</code></li>
                <li><code>GET /api/students</code></li>
                <li><code>GET /api/students/&lt;id&gt;</code></li>
                <li><code>POST /api/students</code></li>
                <li><code>PUT /api/students/&lt;id&gt;</code></li>
                <li><code>PATCH /api/students/&lt;id&gt;</code></li>
                <li><code>DELETE /api/students/&lt;id&gt;</code></li>
                <li><code>GET /api/students/count</code></li>
                <li><code>GET /api/students/search?grade=A</code></li>
                <li><code>GET /api/students/search?name=Ali</code></li>
                <li><code>GET /api/stats</code></li>
                <li><code>GET /api/system</code></li>
            </ul>
        </div>
    </body>
    </html>
    """
    return render_template_string(html), 200


@app.route("/api/health", methods=["GET"])
def health_check():
    """Standard DevOps health-check endpoint."""
    return jsonify({"status": "ok", "message": "Flask is running"}), 200


@app.route("/api/info", methods=["GET"])
def api_info():
    """Return project/API metadata."""
    return jsonify({
        "app": "DevOps Flask Exam Template",
        "version": "1.0",
        "port": 5000,
        "endpoints": [
            "GET /api/health",
            "GET /api/students",
            "GET /api/students/<id>",
            "POST /api/students",
            "PUT /api/students/<id>",
            "PATCH /api/students/<id>",
            "DELETE /api/students/<id>",
            "GET /api/students/count",
            "GET /api/students/search?grade=A",
            "GET /api/stats",
            "GET /api/system"
        ]
    }), 200


# -----------------------------
# CRUD API routes
# -----------------------------
@app.route("/api/students", methods=["GET"])
def get_students():
    """READ ALL students."""
    return jsonify(students), 200


@app.route("/api/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    """READ ONE student by ID."""
    student = find_student(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student), 200


@app.route("/api/students", methods=["POST"])
def create_student():
    """CREATE a new student. Required JSON fields: name, grade."""
    global next_id
    data = get_json_body()

    if not data:
        return error_response("JSON body is required", 400)

    name = data.get("name")
    grade = data.get("grade")
    course = data.get("course", "DevOps")
    city = data.get("city", "Unknown")

    if not name or not grade:
        return error_response("name and grade are required", 400)

    grade = str(grade).upper()
    if grade not in VALID_GRADES:
        return error_response("Invalid grade. Allowed grades: A, B, C, D, F", 400)

    new_student = {
        "id": next_id,
        "name": str(name),
        "grade": grade,
        "course": str(course),
        "city": str(city)
    }
    students.append(new_student)
    next_id += 1

    return jsonify(new_student), 201


@app.route("/api/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """UPDATE/replace student fields by ID."""
    student = find_student(student_id)
    if not student:
        return error_response("Student not found", 404)

    data = get_json_body()
    if not data:
        return error_response("JSON body is required", 400)

    if "name" in data:
        if not data["name"]:
            return error_response("name cannot be empty", 400)
        student["name"] = str(data["name"])

    if "grade" in data:
        grade = str(data["grade"]).upper()
        if grade not in VALID_GRADES:
            return error_response("Invalid grade. Allowed grades: A, B, C, D, F", 400)
        student["grade"] = grade

    if "course" in data:
        student["course"] = str(data["course"])

    if "city" in data:
        student["city"] = str(data["city"])

    return jsonify(student), 200


@app.route("/api/students/<int:student_id>", methods=["PATCH"])
def patch_student(student_id):
    """PARTIAL UPDATE. PATCH works same as PUT here for exam convenience."""
    return update_student(student_id)


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """DELETE student by ID."""
    global students
    student = find_student(student_id)
    if not student:
        return error_response("Student not found", 404)

    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "Deleted successfully", "deleted": student}), 200


# -----------------------------
# Extra exam-friendly endpoints
# -----------------------------
@app.route("/api/students/count", methods=["GET"])
def count_students():
    """Return total number of students."""
    return jsonify({"count": len(students)}), 200


@app.route("/api/students/search", methods=["GET"])
def search_students():
    """
    Search students using query parameters.
    Examples:
    /api/students/search?grade=A
    /api/students/search?name=ali
    /api/students/search?city=topi
    """
    grade = request.args.get("grade")
    name = request.args.get("name")
    city = request.args.get("city")
    course = request.args.get("course")

    results = students

    if grade:
        results = [s for s in results if s["grade"].lower() == grade.lower()]
    if name:
        results = [s for s in results if name.lower() in s["name"].lower()]
    if city:
        results = [s for s in results if city.lower() in s.get("city", "").lower()]
    if course:
        results = [s for s in results if course.lower() in s.get("course", "").lower()]

    return jsonify(results), 200


@app.route("/api/stats", methods=["GET"])
def stats():
    """Return small summary/report of students by grade."""
    grade_counts = {}
    for student in students:
        grade = student["grade"]
        grade_counts[grade] = grade_counts.get(grade, 0) + 1

    return jsonify({
        "total_students": len(students),
        "valid_grades": sorted(list(VALID_GRADES)),
        "grade_counts": grade_counts
    }), 200


@app.route("/api/system", methods=["GET"])
def system_status():
    """Simple server/app status endpoint useful for DevOps demos."""
    return jsonify({
        "server": "running",
        "framework": "Flask",
        "database": "in-memory list",
        "port": 5000,
        "note": "Use docker ps, docker logs, df -h, free -h, uptime on EC2 for server investigation."
    }), 200


# -----------------------------
# Error handlers
# -----------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Route not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"success": False, "error": "Method not allowed for this endpoint"}), 405


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500


if __name__ == "__main__":
    # host='0.0.0.0' is REQUIRED on EC2/Docker so the app is reachable from outside.
    # debug=False is safer for deployment. For local practice you can temporarily use debug=True.
    app.run(host="0.0.0.0", port=5000, debug=False)

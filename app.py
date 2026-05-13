from flask import Flask, render_template, jsonify, abort, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super-secret-key"

courses = [
    {
        "id": 0,
        "title": "Introduction to SQL",
        "image": "database",
        "description": "Learn SQL basics, queries, and data filtering.",
        "action": "Start Course",
        "lessons": [
            "What is SQL and why it matters",
            "SELECT queries for table data",
            "Filtering and sorting with WHERE and ORDER BY"
        ]
    },
    {
        "id": 1,
        "title": "Python Programming",
        "image": "python",
        "description": "Build Python skills with real examples and exercises.",
        "action": "Start Course",
        "lessons": [
            "Python syntax and variables",
            "Functions, loops, and conditionals",
            "Working with lists and dictionaries"
        ]
    },
    {
        "id": 2,
        "title": "Data Science",
        "image": "data",
        "description": "Explore data analysis, visualization, and modeling.",
        "action": "Start Course",
        "lessons": [
            "Cleaning data with pandas",
            "Creating charts with matplotlib",
            "Intro to model evaluation"
        ]
    },
    {
        "id": 3,
        "title": "SQL Mastery",
        "image": "database",
        "description": "Advance your SQL skills with deeper query patterns.",
        "action": "Start Course",
        "lessons": [
            "JOINs and subqueries",
            "Grouping and aggregation",
            "Window functions and optimization"
        ]
    }
]

practice_cards = [
    {
        "title": "Upgrade to unlock all features",
        "dark": True,
        "action": ""
    },
    {
        "title": "SQL Practice",
        "image": "sql",
        "xp": "250 XP",
        "action": "Practice"
    },
    {
        "title": "Python Practice",
        "image": "python",
        "xp": "250 XP",
        "action": "Practice"
    }
]

assessments = [
    {
        "id": 0,
        "title": "SQL Test",
        "image": "database",
        "description": "Practice SQL queries and database logic.",
        "xp": "100 XP",
        "action": "Start Assessment",
        "questions": [
            {
                "question": "What does SELECT * do?",
                "options": ["Returns all columns", "Deletes all rows", "Updates all records"],
                "answer": 0
            },
            {
                "question": "Which clause filters rows?",
                "options": ["GROUP BY", "ORDER BY", "WHERE"],
                "answer": 2
            }
        ]
    },
    {
        "id": 1,
        "title": "Python Quiz",
        "image": "python",
        "description": "Test your Python fundamentals and problem solving.",
        "xp": "150 XP",
        "action": "Start Assessment",
        "questions": [
            {
                "question": "How do you start a function in Python?",
                "options": ["func myfunc()", "def myfunc():", "function myfunc()"],
                "answer": 1
            },
            {
                "question": "Which is a list?",
                "options": ["{1,2,3}", "[1,2,3]", "(1,2,3)"],
                "answer": 1
            }
        ]
    },
    {
        "id": 2,
        "title": "Data Analysis",
        "image": "analytics",
        "description": "Assess your data science and analytics knowledge.",
        "xp": "200 XP",
        "action": "Start Assessment",
        "questions": [
            {
                "question": "What is pandas used for?",
                "options": ["Web design", "Data analysis", "Mobile apps"],
                "answer": 1
            },
            {
                "question": "What does visualization help with?",
                "options": ["Hiding data", "Understanding trends", "Slowing performance"],
                "answer": 1
            }
        ]
    }
]

@app.route("/")
def dashboard():
    return render_template(
        "index.html",
        title="StudySync Dashboard",
        topbar_placeholder="Search...",
        courses=courses,
        practice_cards=practice_cards,
    )

@app.route("/courses")
def course_list():
    return render_template(
        "courses.html",
        title="Courses",
        topbar_placeholder="Search courses...",
        courses=courses,
    )

@app.route("/course/new", methods=["GET", "POST"])
def create_course():
    error = None
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        image = request.form.get("image", "").strip() or "course"
        lessons_text = request.form.get("lessons", "").strip()
        lessons = [line.strip() for line in lessons_text.splitlines() if line.strip()]

        if not title or not description:
            error = "Please provide a title and description for the course."
        else:
            new_id = max((c["id"] for c in courses), default=-1) + 1
            new_course = {
                "id": new_id,
                "title": title,
                "image": image,
                "description": description,
                "action": "Start Course",
                "lessons": lessons or ["Lesson 1"],
            }
            courses.append(new_course)
            return redirect(url_for("course_detail", course_id=new_id))

    return render_template(
        "new_course.html",
        title="Add New Course",
        error=error,
    )

@app.route("/assessments")
def assessment_list():
    return render_template(
        "assessments.html",
        title="Assessments",
        topbar_placeholder="Search assessments...",
        assessments=assessments,
    )

@app.route("/course/<int:course_id>")
def course_detail(course_id):
    course = next((c for c in courses if c["id"] == course_id), None)
    if course is None:
        abort(404)
    return render_template(
        "course_detail.html",
        title=course["title"],
        course=course,
    )

@app.route("/assessment/<int:assessment_id>")
def assessment_detail(assessment_id):
    assessment = next((a for a in assessments if a["id"] == assessment_id), None)
    if assessment is None:
        abort(404)
    return render_template(
        "assessment_detail.html",
        title=assessment["title"],
        assessment=assessment,
    )

@app.route("/course/<int:course_id>/continue")
def course_content(course_id):
    course = next((c for c in courses if c["id"] == course_id), None)
    if course is None:
        abort(404)
    return render_template(
        "course_content.html",
        title=f"Continue {course['title']}",
        course=course,
    )

@app.route("/assessment/<int:assessment_id>/start")
def assessment_start(assessment_id):
    assessment = next((a for a in assessments if a["id"] == assessment_id), None)
    if assessment is None:
        abort(404)
    return render_template(
        "assessment_start.html",
        title=f"{assessment['title']} - Start",
        assessment=assessment,
    )

@app.route("/assessment/<int:assessment_id>/submit", methods=["POST"])
def assessment_submit(assessment_id):
    assessment = next((a for a in assessments if a["id"] == assessment_id), None)
    if assessment is None:
        abort(404)

    score = 0
    results = []
    for idx, question in enumerate(assessment["questions"]):
        selected = request.form.get(f"question_{idx}")
        selected_index = int(selected) if selected is not None else None
        correct = selected_index == question["answer"]
        if correct:
            score += 1
        results.append({
            "question": question,
            "selected": selected_index,
            "correct": correct,
        })

    return render_template(
        "assessment_result.html",
        title=f"{assessment['title']} Result",
        assessment=assessment,
        score=score,
        total=len(assessment["questions"]),
        results=results,
    )

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    plans = {
        "Pro": {"price": "$9.99", "description": "Unlock all courses, unlimited assessments, and certificates."},
        "Premium": {"price": "$19.99", "description": "Get 24/7 support, mentorship, and a custom learning path."}
    }
    plan = request.args.get("plan", request.form.get("plan", "Pro")).title()
    if plan not in plans:
        plan = "Pro"
    error = None

    if request.method == "POST":
        card_name = request.form.get("card_name", "").strip()
        card_number = request.form.get("card_number", "").strip()
        expiry = request.form.get("expiry", "").strip()
        cvv = request.form.get("cvv", "").strip()

        if not card_name or not card_number or not expiry or not cvv:
            error = "Please enter all payment details to proceed."
        else:
            session["premium"] = True
            session["premium_plan"] = plan
            session["premium_features"] = [
                "Unlimited access to all courses",
                "Unlimited assessments and practice",
                "Certificates of completion",
                "Priority support and mentorship",
                "Custom learning path recommendations"
            ]
            return redirect(url_for("premium"))

    return render_template(
        "checkout.html",
        title=f"Checkout - {plan}",
        plan=plan,
        price=plans[plan]["price"],
        description=plans[plan]["description"],
        error=error,
    )

@app.route("/premium")
def premium():
    if not session.get("premium"):
        return redirect(url_for("upgrade"))

    return render_template(
        "premium.html",
        title="Premium Features",
        plan=session.get("premium_plan", "Premium"),
        features=session.get("premium_features", []),
    )

@app.route("/upgrade")
def upgrade():
    plans = [
        {
            "name": "Free",
            "price": "$0",
            "period": "/month",
            "features": [
                "3 Courses",
                "2 Assessments",
                "Basic Support"
            ],
            "button_text": "Current Plan",
            "button_disabled": True,
        },
        {
            "name": "Pro",
            "price": "$9.99",
            "period": "/month",
            "features": [
                "All Courses",
                "Unlimited Assessments",
                "Priority Support",
                "Certificates"
            ],
            "button_text": "Upgrade Now",
            "button_disabled": False,
        },
        {
            "name": "Premium",
            "price": "$19.99",
            "period": "/month",
            "features": [
                "All Courses",
                "Unlimited Assessments",
                "24/7 Support",
                "Certificates",
                "Mentorship",
                "Custom Learning Path"
            ],
            "button_text": "Upgrade Now",
            "button_disabled": False,
        }
    ]
    return render_template(
        "upgrade.html",
        title="Upgrade to StudySync Pro",
        plans=plans,
    )

@app.route("/search")
def search():
    query = request.args.get('q', '').lower()
    if not query:
        return redirect(url_for('dashboard'))
    
    # Search in courses
    matching_courses = [c for c in courses if query in c['title'].lower() or query in c['description'].lower()]
    
    # Search in assessments
    matching_assessments = [a for a in assessments if query in a['title'].lower() or query in a['description'].lower()]
    
    return render_template(
        "search.html",
        title=f"Search Results for '{query}'",
        query=query,
        courses=matching_courses,
        assessments=matching_assessments,
    )

@app.route("/practice")
def practice():
    return render_template(
        "practice.html",
        title="Practice",
        topbar_placeholder="Search practice...",
        practice_cards=practice_cards,
    )

@app.route("/practice/sql")
def practice_sql():
    return render_template(
        "practice_sql.html",
        title="SQL Practice",
    )

@app.route("/practice/python")
def practice_python():
    return render_template(
        "practice_python.html",
        title="Python Practice",
    )

@app.route("/api/courses")
def api_courses():
    return jsonify(courses)

@app.route("/api/courses/<int:course_id>")
def api_course_detail(course_id):
    course = next((c for c in courses if c["id"] == course_id), None)
    if course is None:
        abort(404)
    return jsonify(course)

@app.route("/api/assessments")
def api_assessments():
    return jsonify(assessments)

if __name__ == "__main__":
    app.run(debug=True)

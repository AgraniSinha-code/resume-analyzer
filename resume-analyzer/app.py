from flask import Flask, request, render_template
import PyPDF2

app = Flask(__name__)

skills_db = {
    "web developer": ["html", "css", "javascript", "react"],
    "backend developer": ["python", "java", "sql"],
    "data analyst": ["python", "sql", "excel"]
}

def analyze_resume(text):
    found_skills = []

    for role_skills in skills_db.values():
        for skill in role_skills:
            if skill in text.lower():
                found_skills.append(skill)

    found_skills = list(set(found_skills))  # remove duplicates

    score = len(found_skills) * 20

    all_skills = set(sum(skills_db.values(), []))
    missing_skills = list(all_skills - set(found_skills))

    return found_skills, score, missing_skills


def job_match(found_skills, role):
    required_skills = skills_db.get(role, [])

    if not required_skills:
        return 0

    match = sum(1 for skill in required_skills if skill in found_skills)
    return int((match / len(required_skills)) * 100)


def get_suggestion(score):
    if score >= 80:
        return "Excellent Resume 👍"
    elif score >= 50:
        return "Good but needs improvement"
    else:
        return "Add more skills and projects"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['resume']
        role = request.form['role']

        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        skills, score, missing_skills = analyze_resume(text)
        match_percent = job_match(skills, role)
        suggestion = get_suggestion(score)

        return render_template("result.html",
                               skills=skills,
                               score=score,
                               missing_skills=missing_skills,
                               suggestion=suggestion,
                               match_percent=match_percent,
                               role=role)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template, jsonify
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "students.csv"

app = Flask(__name__)

def load_students():
    df = pd.read_csv(DATA_FILE)
    numeric = ["StudyHours", "Attendance", "Assignments", "InternalMarks"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Result"] = df["Result"].astype(str)
    return df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/dashboard")
def dashboard():
    df = load_students()
    pass_count = int((df["Result"].str.lower() == "pass").sum())
    fail_count = int((df["Result"].str.lower() == "fail").sum())
    total = len(df)

    response = {
        "kpis": {
            "total_students": total,
            "average_marks": round(float(df["InternalMarks"].mean()), 2),
            "average_attendance": round(float(df["Attendance"].mean()), 2),
            "pass_percentage": round((pass_count / total * 100) if total else 0, 2),
        },
        "result": {"pass": pass_count, "fail": fail_count},
        "students": df.to_dict(orient="records"),
        "marks": {
            "labels": df["Name"].tolist(),
            "values": df["InternalMarks"].fillna(0).tolist()
        },
        "study_vs_marks": {
            "study_hours": df["StudyHours"].fillna(0).tolist(),
            "marks": df["InternalMarks"].fillna(0).tolist(),
            "names": df["Name"].tolist()
        },
        "attendance": {
            "labels": df["Name"].tolist(),
            "values": df["Attendance"].fillna(0).tolist()
        },
        "averages": {
            "study_hours": round(float(df["StudyHours"].mean()), 2),
            "attendance": round(float(df["Attendance"].mean()), 2),
            "assignments": round(float(df["Assignments"].mean()), 2),
            "internal_marks": round(float(df["InternalMarks"].mean()), 2),
        }
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

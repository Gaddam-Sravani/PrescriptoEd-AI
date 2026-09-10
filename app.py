from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import os
import numpy as np

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

MODEL_FILE = "student_risk_model.pkl"
model = joblib.load(MODEL_FILE) if os.path.exists(MODEL_FILE) else None

# --- SINGLE SOURCE OF TRUTH (Central Database with Subject-Wise Metrics for 3 Subjects) ---
STUDENT_DATABASE = {
    "STU1042": {
        "rollNo": "STU1042",
        "pass": "pass1042",
        "name": "Sravani Gaddam",
        "batch": "B.Tech CSE - Section A",
        "phone": "+91 98495-10422",
        "email": "gsravani90455@gmail.com",
        "parentPhone": "+91 94401-88210",
        "parentEmail": "guardian.sharma@gmail.com",
        "subjects": {
            "CS301": {"name": "Design & Analysis of Algorithms", "attendance": 38.0, "midterm": 20.0, "assignment": 30.0},
            "CS302": {"name": "Database Management Systems", "attendance": 65.0, "midterm": 47.0, "assignment": 70.0},
            "CS303": {"name": "Computer Networks", "attendance": 80.0, "midterm": 68.0, "assignment": 60.0}
        },
        "backlogs": 0,
        "feeDue": "₹15,000",
        "dueDate": "2026-09-35",
        "feeDelay": 30
    },
    "STU1045": {
        "rollNo": "STU1045",
        "pass": "pass1045",
        "name": "Rahul Sharma",
        "batch": "B.Tech CSE - Section A",
        "phone": "+91 97001-22334",
        "email": "rahul.s@prescriptoed.edu",
        "parentPhone": "+91 94402-99881",
        "parentEmail": "guardian.gupta@gmail.com",
        "subjects": {
            "CS301": {"name": "Design & Analysis of Algorithms", "attendance": 92.0, "midterm": 85.0, "assignment": 90.0},
            "CS302": {"name": "Database Management Systems", "attendance": 88.0, "midterm": 78.0, "assignment": 92.0},
            "CS303": {"name": "Computer Networks", "attendance": 85.0, "midterm": 80.0, "assignment": 88.0}
        },
        "backlogs": 0,
        "feeDue": "₹0 (Paid)",
        "dueDate": "N/A",
        "feeDelay": 0
    },
    "STU1088": {
        "rollNo": "STU1088",
        "pass": "pass1088",
        "name": "Vikram Rao",
        "batch": "B.Tech CSE - Section B",
        "phone": "+91 91234-56789",
        "email": "vikram.r@prescriptoed.edu",
        "parentPhone": "+91 98765-43210",
        "parentEmail": "guardian.rao@gmail.com",
        "subjects": {
            "CS301": {"name": "Design & Analysis of Algorithms", "attendance": 75.0, "midterm": 65.0, "assignment": 70.0},
            "CS302": {"name": "Database Management Systems", "attendance": 72.0, "midterm": 60.0, "assignment": 75.0},
            "CS303": {"name": "Computer Networks", "attendance": 70.0, "midterm": 58.0, "assignment": 65.0}
        },
        "backlogs": 1,
        "feeDue": "₹5,000",
        "dueDate": "2026-10-10",
        "feeDelay": 10
    },
    "STU1091": {
        "rollNo": "STU1091",
        "pass": "pass1091",
        "name": "Neha Verma",
        "batch": "B.Tech CSE - Section B",
        "phone": "+91 99887-66554",
        "email": "neha.v@prescriptoed.edu",
        "parentPhone": "+91 93322-11445",
        "parentEmail": "guardian.verma@gmail.com",
        "subjects": {
            "CS301": {"name": "Design & Analysis of Algorithms", "attendance": 50.0, "midterm": 35.0, "assignment": 40.0},
            "CS302": {"name": "Database Management Systems", "attendance": 52.0, "midterm": 38.0, "assignment": 45.0},
            "CS303": {"name": "Computer Networks", "attendance": 48.0, "midterm": 30.0, "assignment": 50.0}
        },
        "backlogs": 2,
        "feeDue": "₹0 (Paid)",
        "dueDate": "N/A",
        "feeDelay": 0
    }
}

faculty_database = {
    "FAC001": {
        "id": "FAC001",
        "pass": "passFac1",
        "name": "Dr. K. Srinivas",
        "role": "faculty",
        "department": "Computer Science",
        "email": "srinivas.k@prescriptoed.edu"
    }
}

dean_database = {
    "DEAN001": {
        "id": "DEAN001",
        "pass": "passDean1",
        "name": "Dr. R. V. Rao",
        "role": "dean",
        "department": "Academic Administration",
        "email": "dean.rao@prescriptoed.edu"
    }
}

# --- HTML Page Serving Routes ---
@app.route("/")
def serve_login():
    return send_from_directory('.', 'login.html')

@app.route("/student1.html")
def serve_student():
    return send_from_directory('.', 'student1.html')

@app.route("/faculty.html")
def serve_faculty():
    return send_from_directory('.', 'faculty.html')

@app.route("/admin.html")
def serve_dean():
    return send_from_directory('.', 'admin.html')
# --- Static File Serving Routes ---
@app.route("/admin.css")
def serve_admin_css():
    return send_from_directory('.', 'admin.css')

@app.route("/admin.js")
def serve_admin_js():
    return send_from_directory('.', 'admin.js')

# --- Unified Authentication Route ---
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    role = data.get("role")
    user_id = data.get("user_id")
    password = data.get("password")
    
    if role == "student":
        user = STUDENT_DATABASE.get(user_id)
        if user and user["pass"] == password:
            safe = {k: v for k, v in user.items() if k != "pass"}
            safe["role"] = "student"
            return jsonify({"status": "success", "user": safe, "redirect": "student1.html"})
            
    elif role == "faculty":
        user = faculty_database.get(user_id)
        if user and user["pass"] == password:
            safe = {k: v for k, v in user.items() if k != "pass"}
            safe["role"] = "faculty"
            return jsonify({"status": "success", "user": safe, "redirect": "faculty.html"})
            
    elif role == "dean":
        user = dean_database.get(user_id)
        if user and user["pass"] == password:
            safe = {k: v for k, v in user.items() if k != "pass"}
            safe["role"] = "dean"
            return jsonify({"status": "success", "user": safe, "redirect": "admin.html"})
            
    return jsonify({"status": "error", "message": "Invalid Credentials or Selected Role"}), 401

@app.route("/get_student/<roll_no>", methods=["GET"])
def get_student(roll_no):
    student = STUDENT_DATABASE.get(roll_no)
    if student:
        safe_profile = {k: v for k, v in student.items() if k != "pass"}
        return jsonify({"status": "success", "student": safe_profile})
    return jsonify({"status": "error", "message": "Student not found"}), 404

@app.route("/update_metrics", methods=["POST"])
def update_metrics():
    data = request.get_json()
    roll_no = data.get("roll_no")
    
    if roll_no not in STUDENT_DATABASE:
        return jsonify({"status": "error", "message": "Student not found"}), 404
        
    subject_code = data.get("subject_code")
    if subject_code and subject_code in STUDENT_DATABASE[roll_no]["subjects"]:
        if "attendance" in data: STUDENT_DATABASE[roll_no]["subjects"][subject_code]["attendance"] = float(data["attendance"])
        if "midterm" in data: STUDENT_DATABASE[roll_no]["subjects"][subject_code]["midterm"] = float(data["midterm"])
        if "assignment" in data: STUDENT_DATABASE[roll_no]["subjects"][subject_code]["assignment"] = float(data["assignment"])
        
    if "backlogs" in data: STUDENT_DATABASE[roll_no]["backlogs"] = int(data["backlogs"])
    if "feeDelay" in data: STUDENT_DATABASE[roll_no]["feeDelay"] = int(data["feeDelay"])
    if "feeDue" in data: STUDENT_DATABASE[roll_no]["feeDue"] = data["feeDue"]
    if "dueDate" in data: STUDENT_DATABASE[roll_no]["dueDate"] = data["dueDate"]
    
    safe_profile = {k: v for k, v in STUDENT_DATABASE[roll_no].items() if k != "pass"}
    return jsonify({"status": "success", "student": safe_profile})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    roll_no = data.get("roll_no")
    student = STUDENT_DATABASE.get(roll_no)
    
    if not student:
        return jsonify({"status": "error", "message": "Student not found"}), 404

    # Calculate average metrics across the 3 subjects for prediction
    subs = student["subjects"].values()
    attendance = sum(s["attendance"] for s in subs) / len(subs)
    midterm = sum(s["midterm"] for s in subs) / len(subs)
    assignment = sum(s["assignment"] for s in subs) / len(subs)
    backlogs = student["backlogs"]
    fee_delay = student["feeDelay"]

    if model:
        features = np.array([[attendance, midterm, assignment, backlogs, fee_delay]])
        risk_score = round(float(model.predict_proba(features)[0][1] * 100), 1)
    else:
        risk_score = round(min(max(100.0 - (attendance * 0.35 + midterm * 0.35 + assignment * 0.15) + (backlogs * 6.0), 5.0), 98.0), 1)

    alert_log = []
    if risk_score >= 70.0:
        risk_level = "Critical Zone (Danger)"
        alert_log.append({
            "recipient": f"Parent ({student['parentEmail']} | {student['parentPhone']})",
            "channel": "Secure Email & SMS Simulator",
            "status": "DISPATCHED - URGENT DANGER",
            "message": f"URGENT: Student {student['name']} ({roll_no}) is in Critical Danger Zone (Risk: {risk_score}%). Immediate parent intervention required."
        })
    elif risk_score >= 40.0:
        risk_level = "Watchlist Zone"
        alert_log.append({
            "recipient": f"Student ({student['email']} | {student['phone']})",
            "channel": "Secure Email & SMS Simulator",
            "status": "DISPATCHED - WATCHLIST ADVISORY",
            "message": f"Advisory: Your academic risk score is {risk_score}% (Watchlist Zone). Please review your recovery pathways."
        })
    else:
        risk_level = "Safe Zone"
        alert_log.append({
            "recipient": f"Student ({roll_no})",
            "channel": "None",
            "status": "STABLE",
            "message": "Student trajectory is stable."
        })

    return jsonify({
        "status": "success",
        "risk_score": risk_score,
        "risk_level": risk_level,
        "alert_dispatch_log": alert_log
    })

@app.route("/generate_peer_groups", methods=["POST"])
def generate_peer_groups():
    student_list = list(STUDENT_DATABASE.values())
    
    student_profiles = []
    for s in student_list:
        sub_scores = {}
        for code, sub in s["subjects"].items():
            score = (sub["midterm"] + sub["assignment"]) / 2.0
            sub_scores[code] = score
        
        sorted_subs = sorted(sub_scores.items(), key=lambda item: item[1])
        weakest_sub = sorted_subs[0]
        strongest_sub = sorted_subs[-1]
        
        avg_score = sum(sub_scores.values()) / len(sub_scores)
        if avg_score < 50 or s["backlogs"] >= 2:
            tier = "Danger Zone"
        elif avg_score < 75 or s["backlogs"] == 1:
            tier = "Watchlist Zone"
        else:
            tier = "Safe Zone"
        
        student_profiles.append({
            "rollNo": s["rollNo"],
            "name": s["name"],
            "tier": tier,
            "avg_score": avg_score,
            "strongest": strongest_sub[0],
            "weakest": weakest_sub[0],
            "sub_scores": sub_scores
        })

    groups = []
    paired_rolls = set()
    pod_counter = 1

    for i in range(len(student_profiles)):
        s1 = student_profiles[i]
        if s1["rollNo"] in paired_rolls:
            continue
            
        best_match = None
        for j in range(i + 1, len(student_profiles)):
            s2 = student_profiles[j]
            if s2["rollNo"] in paired_rolls:
                continue
                
            is_complementary = (s1["strongest"] == s2["weakest"]) or (s2["strongest"] == s1["weakest"])
            is_remedial_mix = (s1["tier"] != s2["tier"])
            
            if is_complementary or is_remedial_mix:
                best_match = s2
                break
        
        if not best_match and len(student_profiles) > i + 1:
            for j in range(i + 1, len(student_profiles)):
                if student_profiles[j]["rollNo"] not in paired_rolls:
                    best_match = student_profiles[j]
                    break

        if best_match:
            paired_rolls.add(s1["rollNo"])
            paired_rolls.add(best_match["rollNo"])
            
            focus_text = f"Cross-Domain Synergy: {s1['name']} & {best_match['name']}"
            rationale = (f"Matched based on dynamic skill evaluation: {s1['name']} excels in {s1['strongest']} (needs support in {s1['weakest']}), "
                         f"while {best_match['name']} excels in {best_match['strongest']} (needs support in {best_match['weakest']}).")
            
            groups.append({
                "group_id": f"POD-SYNAPSE-{pod_counter}",
                "focus": focus_text,
                "members": [
                    {"name": s1["name"], "tier": s1["tier"], "strength": s1["strongest"], "weakness": s1["weakest"]},
                    {"name": best_match["name"], "tier": best_match["tier"], "strength": best_match["strongest"], "weakness": best_match["weakest"]}
                ],
                "rationale": rationale
            })
            pod_counter += 1

    return jsonify({
        "status": "success",
        "total_pods": len(groups),
        "peer_groups": groups
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

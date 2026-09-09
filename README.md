# PrescriptoEd AI

PrescriptoEd AI is an intelligent institutional management and predictive academic intervention platform designed to monitor student trajectories, automate early-risk detection, and bridge performance gaps through targeted peer guidance.

## Core Features

* **Multi-Role Authentication**: Secure login portals supporting **Students**, **Faculty Members**, and **Deans/Administrators** with role-based routing.
* **Student Dashboard**: 
  * Live risk assessment ring gauge with real-time zone categorization (**Safe Zone**, **Watchlist**, **Danger Zone**).
  * Overall attendance projection and target simulator.
  * Subject-wise performance tracking (attendance, midterms, assignments).
  * Active backlogs and fee tracking (due amount and due date).
* **Faculty Dashboard**:
  * Real-time synchronized student roster oversight.
  * Automated Peer-to-Peer Guidance Engine combining top-tier students with support candidates based on dynamic skill matrices.
* **Admin Intelligence Workspace**:
  * Institutional macro-metrics (monitored students, critical risk ratios, average faculty ratings).
  * Faculty scorecards and departmental student risk directories.

## Tech Stack

* **Backend**: Python, Flask, Flask-CORS, Joblib, NumPy
* **Frontend**: HTML5, Modern CSS (Glassmorphism UI), JavaScript (ES6)
* **Machine Learning**: Predictive risk evaluation models with fallback heuristics

## Getting Started

1. Clone the repository:
2. 
   git clone [https://github.com/Gaddam-Sravani/PrescriptoEd-AI.git](https://github.com/Gaddam-Sravani/PrescriptoEd-AI.git)
   
   cd PrescriptoEd-AI

4. Install dependencies:

pip install flask flask-cors joblib scikit-learn numpy pandas


3. Run the Flask application:
   
python3 app.py


5. Access the workspace locally in your browser at `http://127.0.0.1:5000`.

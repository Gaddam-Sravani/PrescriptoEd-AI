const adminDatabase = {
  departments: [
    { code: "CSE", name: "Computer Science & Engineering" },
    { code: "ECE", name: "Electronics & Communication Engineering" },
    { code: "MECH", name: "Mechanical Engineering" }
  ],
  faculty: [
    { id: "FAC101", name: "Dr. K. Srinivas", department: "CSE", subjectCode: "CS301", subjectName: "Design & Analysis of Algorithms", targetStudents: ["STU1042", "STU1043", "STU1045"] },
    { id: "FAC102", name: "Dr. P. Sharma", department: "CSE", subjectCode: "CS302", subjectName: "Database Management Systems", targetStudents: ["STU1042", "STU1044"] },
    { id: "FAC103", name: "Prof. S. Rao", department: "CSE", subjectCode: "CS303", subjectName: "Operating Systems", targetStudents: ["STU1042", "STU1043", "STU1044"] },
    { id: "FAC104", name: "Dr. M. Joseph", department: "CSE", subjectCode: "CS304", subjectName: "Computer Networks", targetStudents: ["STU1042", "STU1045"] },
    { id: "FAC105", name: "Prof. N. Murthy", department: "CSE", subjectCode: "MA301", subjectName: "Discrete Mathematics", targetStudents: ["STU1042", "STU1043", "STU1044"] },
    { id: "FAC106", name: "Dr. Ananya Roy", department: "ECE", subjectCode: "EC301", subjectName: "Digital Signal Processing", targetStudents: ["STU2001", "STU2002"] },
    { id: "FAC107", name: "Prof. Vikram Reddy", department: "ECE", subjectCode: "EC302", subjectName: "VLSI Design & Architecture", targetStudents: ["STU2001", "STU2002"] },
    { id: "FAC108", name: "Dr. R. Verma", department: "MECH", subjectCode: "ME301", subjectName: "Thermodynamics & Heat Transfer", targetStudents: ["STU3001"] }
  ],
  students: [
    { rollNo: "STU1042", name: "Rahul Sharma", department: "CSE", batch: "2024–2028 (Year 3)", backlogs: 2, riskScore: 78 },
    { rollNo: "STU1043", name: "Pooja Verma", department: "CSE", batch: "2024–2028 (Year 3)", backlogs: 0, riskScore: 22 },
    { rollNo: "STU1044", name: "Karthik Subramanian", department: "CSE", batch: "2024–2028 (Year 3)", backlogs: 1, riskScore: 54 },
    { rollNo: "STU1045", name: "Sneha Patel", department: "CSE", batch: "2024–2028 (Year 3)", backlogs: 3, riskScore: 84 },
    { rollNo: "STU2001", name: "Arjun Nambiar", department: "ECE", batch: "2024–2028 (Year 3)", backlogs: 0, riskScore: 18 },
    { rollNo: "STU2002", name: "Meera Nair", department: "ECE", batch: "2024–2028 (Year 3)", backlogs: 1, riskScore: 42 },
    { rollNo: "STU3001", name: "Tanmay Deshmukh", department: "MECH", batch: "2024–2028 (Year 3)", backlogs: 0, riskScore: 28 }
  ]
};

function computeTeacherAnalytics(teacher) {
  const cohort = adminDatabase.students.filter(s => teacher.targetStudents.includes(s.rollNo));
  if (cohort.length === 0) return { meanRisk: 0, rating: 5.0, stars: "★★★★★", status: "Unassigned" };

  const totalRisk = cohort.reduce((acc, curr) => acc + curr.riskScore, 0);
  const meanRisk = Math.round(totalRisk / cohort.length);
  const normalizedRating = Math.max(1.0, Math.min(5.0, +(5.0 - (meanRisk / 100) * 4).toFixed(1)));

  let stars = "★".repeat(Math.round(normalizedRating));
  let status = "";
  let statusClass = "";

  if (normalizedRating >= 4.0) {
    status = "Exemplary";
    statusClass = "status-safe";
  } else if (normalizedRating >= 2.8) {
    status = "Standard";
    statusClass = "status-watch";
  } else {
    status = "Intervention Target";
    statusClass = "status-crit";
  }

  return { meanRisk, rating: normalizedRating, stars, status, statusClass, studentCount: cohort.length };
}

function renderFacultyTable() {
  const tbody = document.getElementById("faculty-table-body");
  tbody.innerHTML = "";
  let totalRatings = 0;

  adminDatabase.faculty.forEach(teacher => {
    const analytics = computeTeacherAnalytics(teacher);
    totalRatings += analytics.rating;

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>
        <b style="color:#ffffff;">${teacher.name}</b>
        <div style="font-size:0.7rem; color:var(--text-muted); font-family:monospace;">${teacher.id}</div>
      </td>
      <td><span class="dept-pill">${teacher.department}</span></td>
      <td>
        <span class="tag-code">${teacher.subjectCode}</span>
        <div style="font-weight:600; margin-top:2px;">${teacher.subjectName}</div>
      </td>
      <td>${analytics.studentCount} Assigned</td>
      <td>
        <b style="color:${analytics.meanRisk >= 65 ? "var(--rose)" : (analytics.meanRisk >= 40 ? "var(--amber)" : "var(--emerald)")}">
          ${analytics.meanRisk}%
        </b>
      </td>
      <td>
        <b>${analytics.rating.toFixed(1)}</b>
        <span class="rating-stars">${analytics.stars}</span>
      </td>
      <td>
        <span class="status-badge ${analytics.statusClass}">${analytics.status}</span>
      </td>
    `;
    tbody.appendChild(tr);
  });

  const avgInstRating = (totalRatings / adminDatabase.faculty.length).toFixed(1);
  document.getElementById("kpi-avg-rating").innerText = `${avgInstRating} / 5.0`;
}

function renderStudentsTable(deptFilter = "ALL") {
  const tbody = document.getElementById("students-table-body");
  tbody.innerHTML = "";

  const filtered = deptFilter === "ALL" 
    ? adminDatabase.students 
    : adminDatabase.students.filter(s => s.department === deptFilter);

  filtered.forEach(s => {
    let riskBadgeClass = s.riskScore >= 70 ? "status-crit" : (s.riskScore >= 40 ? "status-watch" : "status-safe");
    let statusText = s.riskScore >= 70 ? "Remedial Plan" : (s.riskScore >= 40 ? "Monitored" : "On Track");

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><span class="tag-code">${s.rollNo}</span></td>
      <td><b style="color:#ffffff;">${s.name}</b></td>
      <td><span class="dept-pill">${s.department}</span></td>
      <td>${s.batch}</td>
      <td style="color:${s.backlogs > 0 ? "var(--rose)" : "inherit"}; font-weight:${s.backlogs > 0 ? "700" : "400"}">
        ${s.backlogs} Arrear${s.backlogs === 1 ? "" : "s"}
      </td>
      <td>
        <b style="color:${s.riskScore >= 65 ? "var(--rose)" : (s.riskScore >= 40 ? "var(--amber)" : "var(--emerald)")}">
          ${s.riskScore}%
        </b>
      </td>
      <td>
        <span class="status-badge ${riskBadgeClass}">${statusText}</span>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function filterStudentsByDept(dept) {
  renderStudentsTable(dept);
}

function updateKPICounters() {
  const totalStudents = adminDatabase.students.length;
  const criticalCount = adminDatabase.students.filter(s => s.riskScore >= 65).length;

  document.getElementById("kpi-total-students").innerText = totalStudents;
  document.getElementById("kpi-critical-students").innerText = `${criticalCount} (${Math.round((criticalCount / totalStudents) * 100)}%)`;
  document.getElementById("kpi-total-faculty").innerText = adminDatabase.faculty.length;
}

function switchAdminTab(tabId) {
  document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(panel => panel.classList.remove("active"));

  document.querySelector(`[data-tab="${tabId}"]`).classList.add("active");
  document.getElementById(tabId).classList.add("active");
}

document.addEventListener("DOMContentLoaded", () => {
  updateKPICounters();
  renderFacultyTable();
  renderStudentsTable("ALL");
});

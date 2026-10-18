let dashboardData = null;
const charts = {};

function makeCharts(data){
    const common = {responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}};

    charts.marks = new Chart(document.getElementById("marksChart"), {
        type:"bar",
        data:{labels:data.marks.labels,datasets:[{label:"Internal Marks",data:data.marks.values,borderRadius:5}]},
        options:{...common,scales:{y:{beginAtZero:true,max:100}}}
    });

    charts.result = new Chart(document.getElementById("resultChart"), {
        type:"doughnut",
        data:{labels:["Pass","Fail"],datasets:[{data:[data.result.pass,data.result.fail]}]},
        options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:"bottom"}}}
    });

    charts.study = new Chart(document.getElementById("studyChart"), {
        type:"scatter",
        data:{datasets:[{label:"Students",data:data.study_vs_marks.study_hours.map((x,i)=>({x:x,y:data.study_vs_marks.marks[i]})),pointRadius:6}]},
        options:{...common,scales:{x:{title:{display:true,text:"Study Hours"}},y:{beginAtZero:true,max:100,title:{display:true,text:"Internal Marks"}}}}
    });

    charts.attendance = new Chart(document.getElementById("attendanceChart"), {
        type:"line",
        data:{labels:data.attendance.labels,datasets:[{label:"Attendance",data:data.attendance.values,tension:.25,fill:false}]},
        options:{...common,scales:{y:{beginAtZero:true,max:100}}}
    });
}

function renderTable(rows){
    const tbody=document.getElementById("studentTable");
    tbody.innerHTML=rows.map(s=>`
        <tr>
            <td>${s.StudentID}</td><td>${s.Name}</td><td>${s.StudyHours}</td>
            <td>${s.Attendance}%</td><td>${s.Assignments}</td><td>${s.InternalMarks}</td>
            <td class="${String(s.Result).toLowerCase()==="pass"?"result-pass":"result-fail"}">${s.Result}</td>
        </tr>`).join("");
}

async function loadDashboard(){
    const res=await fetch("/api/dashboard");
    if(!res.ok) throw new Error("Unable to load dashboard data");
    dashboardData=await res.json();
    const k=dashboardData.kpis;
    document.getElementById("totalStudents").textContent=k.total_students;
    document.getElementById("averageMarks").textContent=k.average_marks;
    document.getElementById("averageAttendance").textContent=k.average_attendance+"%";
    document.getElementById("passRate").textContent=k.pass_percentage+"%";
    renderTable(dashboardData.students);
    makeCharts(dashboardData);
}
document.getElementById("searchInput").addEventListener("input", e=>{
    if(!dashboardData)return;
    const q=e.target.value.toLowerCase().trim();
    renderTable(dashboardData.students.filter(s=>String(s.Name).toLowerCase().includes(q)||String(s.StudentID).includes(q)||String(s.Result).toLowerCase().includes(q)));
});
loadDashboard().catch(err=>{
    console.error(err);
    document.getElementById("totalStudents").textContent="Error";
});

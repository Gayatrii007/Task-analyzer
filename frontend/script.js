let tasks = [];

function addTask() {
    const title = document.getElementById("title").value;
    const due_date = document.getElementById("due_date").value;
    const estimated_hours = document.getElementById("estimated_hours").value;
    const importance = document.getElementById("importance").value;
    const dependencies = document.getElementById("dependencies").value
        .split(",")
        .map(x => x.trim())
        .filter(x => x);

    if (!title) return alert("❗ Title required");

    tasks.push({
        title,
        due_date: due_date || null,
        estimated_hours: estimated_hours ? Number(estimated_hours) : null,
        importance: importance ? Number(importance) : 5,
        dependencies,
    });

    showTaskList();
    clearInputFields();

    alert("✔ Task added successfully!");
}


function clearInputFields() {
    document.getElementById("title").value = "";
    document.getElementById("due_date").value = "";
    document.getElementById("estimated_hours").value = "";
    document.getElementById("importance").value = "";
    document.getElementById("dependencies").value = "";
}
function showTaskList() {
    const output = document.getElementById("output");
    
    if (tasks.length === 0) {
        output.innerHTML = "<p>No tasks added yet.</p>";
        return;
    }

    output.innerHTML = "<h3>📝 Tasks You Added</h3>";

    tasks.forEach((t, index) => {
        output.innerHTML += `
            <div style="border:1px solid #ccc;padding:10px;margin:5px;border-radius:6px;display:flex;justify-content:space-between;align-items:center;">
                <div>
                    <strong>${index + 1}. ${t.title}</strong><br>
                    ⏳ Due: ${t.due_date ?? "Not set"}<br>
                    ⏱ Hours: ${t.estimated_hours ?? "-"}<br>
                    ⭐ Importance: ${t.importance}<br>
                    🔗 Depends on: ${t.dependencies.length ? t.dependencies.join(", ") : "None"}
                </div>

                <button 
                    onclick="deleteTask(${index})" 
                    style="padding:6px 10px;background:red;color:white;border:none;border-radius:5px;cursor:pointer;">
                    Delete
                </button>
            </div>
        `;
    });
}



function getPayload() {
    const text = document.getElementById("jsonInput").value.trim();
    return text ? JSON.parse(text) : tasks;
}


async function analyzeTasks() {
    document.getElementById("output").innerHTML = "<p>⏳ Processing...</p>";

    const payload = getPayload();
    const strategy = document.getElementById("strategy").value;

    const response = await fetch(
        `http://127.0.0.1:8000/api/tasks/analyze/?strategy=${strategy}`, {
            method: "POST",
            headers: { "Content-Type": "application/json"},
            body: JSON.stringify(payload)
        }
    );

    const result = await response.json();

    if (result.results) {
        displayResults(result.results);
    } else {
        alert("⚠ Backend error: Check console");
        console.log(result);
    }
}


async function suggestTasks() {
    const payload = getPayload();
    const strategy = document.getElementById("strategy").value;

    const response = await fetch(
        `http://127.0.0.1:8000/api/tasks/suggest/?strategy=${strategy}`, {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (result.suggested_tasks) {
        displayResults(result.suggested_tasks);
    } else {
        alert("⚠ Backend error: Check logs");
        console.log(result);
    }
}

function displayResults(arr) {
    const output = document.getElementById("output");

    if (!arr || arr.length === 0) {
        output.innerHTML = "<p>No results to display.</p>";
        return;
    }

    output.innerHTML = "<h2>📌 Analysis Result</h2>";

    arr.forEach(task => {
        const priorityClass = 
            task.score > 70 ? "high" :
            task.score > 40 ? "medium" : "low";

        output.innerHTML += `
            <div class="task-card ${priorityClass}">
                <strong>${task.title}</strong><br>
                🔢 Score: <b>${task.score}</b><br>
                🧠 Reason: ${task.explanation}
            </div>
        `;
    });

    window.scrollTo({ top: document.body.scrollHeight, behavior: "smooth" });
}


function updateStats(tasks) {
    document.getElementById("totalTasks").innerText = tasks.length;

    let high = tasks.filter(t => t.priority === "high").length;
    document.getElementById("highPriority").innerText = high;

    document.getElementById("suggested").innerText = Math.min(3, tasks.length);
}

function deleteTask(index) {
    tasks.splice(index, 1);
    showTaskList();
}

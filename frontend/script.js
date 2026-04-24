const API_URL = "http://98.82.122.41:5000/tasks";

// Load tasks when page opens
window.onload = fetchTasks;

async function fetchTasks() {
    const res = await fetch(API_URL);
    const tasks = await res.json();

    const list = document.getElementById("taskList");
    list.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");
        li.innerHTML = `
            ${task.text}
            <button onclick="deleteTask('${task.id}')">❌</button>
        `;
        list.appendChild(li);
    });
}

async function addTask() {
    const input = document.getElementById("taskInput");
    const text = input.value.trim();

    if (!text) return;

    await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
    });

    input.value = "";
    fetchTasks(); // refresh list
}

async function deleteTask(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    fetchTasks(); // refresh list
}

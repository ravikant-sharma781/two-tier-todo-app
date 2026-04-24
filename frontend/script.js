const API_URL = `${window.location.protocol}//${window.location.hostname}:5000/tasks`;

// Load tasks on page load
window.onload = fetchTasks;

// =========================
// Fetch Tasks
// =========================
async function fetchTasks() {
    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error("Failed to fetch tasks");
        }

        const tasks = await response.json();

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

    } catch (error) {
        console.error("Error fetching tasks:", error);
    }
}

// =========================
// Add Task
// =========================
async function addTask() {
    try {
        const input = document.getElementById("taskInput");
        const text = input.value.trim();

        if (!text) {
            alert("Task cannot be empty");
            return;
        }

        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });

        if (!response.ok) {
            throw new Error("Failed to add task");
        }

        input.value = "";
        fetchTasks();

    } catch (error) {
        console.error("Error adding task:", error);
    }
}

// =========================
// Delete Task
// =========================
async function deleteTask(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Failed to delete task");
        }

        fetchTasks();

    } catch (error) {
        console.error("Error deleting task:", error);
    }
}

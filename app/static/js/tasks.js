document.addEventListener("DOMContentLoaded", () => {
    const taskList = document.getElementById("task-list");
    const modal = document.getElementById("task-modal");
    const modalTitle = document.getElementById("modal-title");
    const closeModalBtn = document.querySelector(".close-modal");
    const newTaskBtn = document.getElementById("new-task-btn");

    const form = document.getElementById("task-form");
    const taskId = document.getElementById("task-id");
    const taskName = document.getElementById("task-name");
    const taskDueDate = document.getElementById("task-due-date");
    const taskDesc = document.getElementById("task-desc");

    // Delete confirmation modal
    const deleteModal = document.getElementById("delete-modal");
    const deleteConfirmBtn = document.getElementById("btn-delete-confirm");
    const deleteCancelBtn = document.getElementById("btn-delete-cancel");
    const closeDeleteModalBtn = document.querySelector(".modal-close-delete");

    let taskIdToDelete = null;

    const openModal = (edit = false, task = null) => {
        modal.classList.remove("hidden");
        if (edit && task) {
            modalTitle.textContent = "Editar Tarefa";
            taskId.value = task.id;
            taskName.value = task.name;
            taskDueDate.value = task.due_date;
            taskDesc.value = task.description;
        } else {
            modalTitle.textContent = "Nova Tarefa";
            taskId.value = "";
            form.reset();
        }
    };

    const closeModal = () => {
        modal.classList.add("hidden");
        form.reset();
    };

    const openDeleteModal = (id) => {
        taskIdToDelete = id;
        deleteModal.classList.remove("hidden");
    };

    const closeDeleteModal = () => {
        taskIdToDelete = null;
        deleteModal.classList.add("hidden");
    };

    closeModalBtn.onclick = closeModal;
    closeDeleteModalBtn.onclick = closeDeleteModal;
    deleteCancelBtn.onclick = closeDeleteModal;

    newTaskBtn.onclick = () => openModal(false);

    form.onsubmit = async (e) => {
        e.preventDefault();
        const data = {
            name: taskName.value,
            due_date: taskDueDate.value,
            description: taskDesc.value,
        };

        const method = taskId.value ? "PUT" : "POST";
        const url = taskId.value ? `/api/tasks/${taskId.value}` : "/api/tasks";

        try {
            await fetch(url, {
                method,
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data),
            });
            closeModal();
            loadTasks();
        } catch (err) {
            alert("Erro ao salvar tarefa.");
        }
    };

    const deleteTask = (id) => {
        openDeleteModal(id);
    };

    deleteConfirmBtn.onclick = async () => {
        if (!taskIdToDelete) return;

        try {
            await fetch(`/api/tasks/${taskIdToDelete}`, {method: "DELETE"});
            closeDeleteModal();
            loadTasks();
        } catch (err) {
            alert("Erro ao deletar.");
        }
    };

    const editTask = async (id) => {
        try {
            const res = await fetch(`/api/tasks/${id}`);
            const task = await res.json();
            openModal(true, task);
        } catch (err) {
            alert("Erro ao carregar tarefa.");
        }
    };

    const loadTasks = async () => {
        taskList.innerHTML = "<p>Carregando...</p>";
        try {
            const res = await fetch("/api/tasks");
            const tasks = await res.json();

            if (tasks.length === 0) {
                taskList.innerHTML = "<p>Sem tarefas no momento.</p>";
                return;
            }

            taskList.innerHTML = "";
            tasks.forEach(task => {
                const taskEl = document.createElement("div");
                taskEl.className = "task-item";
                taskEl.style.backgroundColor = getTaskColor(task.due_date);
                taskEl.innerHTML = `
                    <h3>${task.name}</h3>
                    <p><strong>Data:</strong> ${task.due_date}</p>
                    <p>${task.description}</p>
                    <button onclick="editTask(${task.id})">Editar</button>
                    <button onclick="deleteTask(${task.id})">Excluir</button>
                `;
                taskList.appendChild(taskEl);
            });
        } catch (err) {
            taskList.innerHTML = "<p>Erro ao carregar tarefas.</p>";
        }
    };

    const getTaskColor = (dueDate) => {
        const now = new Date();
        const taskDate = new Date(dueDate);
        const timeDiff = taskDate - now;

        if (timeDiff < 0) {
            return "#f8d7da";
        } else if (timeDiff < 86400000) {
            return "#fff3cd";
        } else {
            return "#d4edda";
        }
    };

    window.editTask = editTask;
    window.deleteTask = deleteTask;

    loadTasks();
});

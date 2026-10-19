"use strict";

const listEl = document.getElementById("task-list");
const emptyEl = document.getElementById("empty");
const formEl = document.getElementById("task-form");
const titleEl = document.getElementById("title");
const descEl = document.getElementById("description");
const toastEl = document.getElementById("toast");

let allTasks = [];
let currentFilter = "all";
let editingId = null;

function showError(message) {
  toastEl.textContent = message;
  toastEl.hidden = false;
  setTimeout(() => { toastEl.hidden = true; }, 3000);
}

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Terjadi kesalahan");
  return data;
}

async function loadTasks() {
  try {
    allTasks = await api("/tasks");
    render();
  } catch (err) {
    showError(err.message);
  }
}

function formatDate(iso) {
  return new Date(iso).toLocaleString("id-ID", { dateStyle: "medium", timeStyle: "short" });
}

function makeButton(label, className, handler) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.className = className;
  btn.textContent = label;
  btn.addEventListener("click", handler);
  return btn;
}

function buildTaskItem(task) {
  const li = document.createElement("li");
  li.className = "task" + (task.done ? " done" : "");

  const check = document.createElement("input");
  check.type = "checkbox";
  check.checked = task.done;
  check.addEventListener("change", () => updateTask(task.id, { done: check.checked }));

  const body = document.createElement("div");
  body.className = "task-body";

  if (editingId === task.id) {
    const input = document.createElement("input");
    input.type = "text";
    input.className = "task-edit";
    input.value = task.title;
    input.maxLength = 100;
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter") saveEdit(task.id, input.value);
      if (e.key === "Escape") { editingId = null; render(); }
    });
    body.appendChild(input);
    setTimeout(() => input.focus(), 0);
  } else {
    const title = document.createElement("div");
    title.className = "task-title";
    title.textContent = task.title;
    body.appendChild(title);
    if (task.description) {
      const desc = document.createElement("div");
      desc.className = "task-desc";
      desc.textContent = task.description;
      body.appendChild(desc);
    }
    const date = document.createElement("div");
    date.className = "task-date";
    date.textContent = formatDate(task.created_at);
    body.appendChild(date);
  }

  const actions = document.createElement("div");
  actions.className = "actions";
  if (editingId === task.id) {
    actions.appendChild(makeButton("Batal", "icon-btn", () => { editingId = null; render(); }));
  } else {
    actions.appendChild(makeButton("Ubah", "icon-btn", () => { editingId = task.id; render(); }));
    actions.appendChild(makeButton("Hapus", "icon-btn danger", () => deleteTask(task.id)));
  }

  li.append(check, body, actions);
  return li;
}

function render() {
  const done = allTasks.filter((t) => t.done).length;
  document.getElementById("stat-total").textContent = allTasks.length;
  document.getElementById("stat-done").textContent = done;
  document.getElementById("stat-active").textContent = allTasks.length - done;

  const visible = allTasks.filter((t) => {
    if (currentFilter === "done") return t.done;
    if (currentFilter === "active") return !t.done;
    return true;
  });

  listEl.replaceChildren(...visible.map(buildTaskItem));
  emptyEl.hidden = visible.length > 0;
}

async function updateTask(id, changes) {
  try {
    await api("/tasks/" + id, { method: "PUT", body: JSON.stringify(changes) });
    await loadTasks();
  } catch (err) {
    showError(err.message);
    await loadTasks();
  }
}

async function saveEdit(id, newTitle) {
  editingId = null;
  await updateTask(id, { title: newTitle });
}

async function deleteTask(id) {
  if (!window.confirm("Hapus tugas ini?")) return;
  try {
    await api("/tasks/" + id, { method: "DELETE" });
    await loadTasks();
  } catch (err) {
    showError(err.message);
  }
}

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  try {
    await api("/tasks", {
      method: "POST",
      body: JSON.stringify({ title: titleEl.value, description: descEl.value }),
    });
    formEl.reset();
    titleEl.focus();
    await loadTasks();
  } catch (err) {
    showError(err.message);
  }
});

document.querySelectorAll(".filter").forEach((btn) => {
  btn.addEventListener("click", () => {
    currentFilter = btn.dataset.filter;
    document.querySelectorAll(".filter").forEach((b) => b.classList.toggle("active", b === btn));
    render();
  });
});

loadTasks();

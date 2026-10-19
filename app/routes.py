"""Endpoint REST API untuk Task Manager."""
from flask import Blueprint, current_app, jsonify, render_template, request

from .utils import (
    parse_bool,
    sanitize_text,
    validate_description,
    validate_title,
)

bp = Blueprint("tasks", __name__)


def _store():
    return current_app.extensions["task_store"]


def _error(message: str, status: int):
    return jsonify({"error": message}), status


@bp.get("/")
def index():
    """Halaman antarmuka web."""
    return render_template("index.html")


@bp.get("/health")
def health():
    return jsonify({"status": "ok", "total_tasks": _store().count()})


@bp.get("/tasks")
def list_tasks():
    done_param = request.args.get("done")
    only_done = parse_bool(done_param) if done_param is not None else None
    tasks = _store().list_all(only_done=only_done)
    return jsonify([t.to_dict() for t in tasks])


@bp.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    err = validate_title(data.get("title"))
    if err:
        return _error(err, 400)
    description = data.get("description", "")
    err = validate_description(description)
    if err:
        return _error(err, 400)
    task = _store().add(sanitize_text(data["title"]), sanitize_text(description))
    return jsonify(task.to_dict()), 201


@bp.get("/tasks/<int:task_id>")
def get_task(task_id: int):
    task = _store().get(task_id)
    if task is None:
        return _error("task tidak ditemukan", 404)
    return jsonify(task.to_dict())


@bp.put("/tasks/<int:task_id>")
def update_task(task_id: int):
    data = request.get_json(silent=True) or {}
    changes = {}
    if "title" in data:
        err = validate_title(data["title"])
        if err:
            return _error(err, 400)
        changes["title"] = sanitize_text(data["title"])
    if "description" in data:
        err = validate_description(data["description"])
        if err:
            return _error(err, 400)
        changes["description"] = sanitize_text(data["description"])
    if "done" in data:
        if not isinstance(data["done"], bool):
            return _error("done harus berupa boolean", 400)
        changes["done"] = data["done"]
    task = _store().update(task_id, **changes)
    if task is None:
        return _error("task tidak ditemukan", 404)
    return jsonify(task.to_dict())


@bp.delete("/tasks/<int:task_id>")
def delete_task(task_id: int):
    if not _store().delete(task_id):
        return _error("task tidak ditemukan", 404)
    return "", 204

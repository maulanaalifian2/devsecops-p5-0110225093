"""Task Manager API - application factory."""
from flask import Flask

from .models import TaskStore
from .routes import bp


def create_app() -> Flask:
    """Buat dan konfigurasi instance Flask."""
    application = Flask(__name__)
    application.extensions["task_store"] = TaskStore()
    application.register_blueprint(bp)
    return application

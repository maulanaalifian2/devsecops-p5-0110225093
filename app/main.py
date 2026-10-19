"""Entry point aplikasi Task Manager API."""
import os

from . import create_app

app = create_app()


def run() -> None:
    """Jalankan server pengembangan.

    Mode debug HANYA aktif jika FLASK_DEBUG=1 (default: mati) dan
    server hanya mengikat ke localhost agar aman.
    """
    debug_mode = os.getenv("FLASK_DEBUG", "0") == "1"
    port = int(os.getenv("PORT", "5000"))
    app.run(host="127.0.0.1", port=port, debug=debug_mode)


if __name__ == "__main__":
    run()

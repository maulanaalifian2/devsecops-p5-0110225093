"""Model data dan penyimpanan in-memory untuk Task."""
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    done: bool = False
    created_at: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict:
        return asdict(self)


class TaskStore:
    """Penyimpanan tugas sederhana di memori (CRUD)."""

    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1

    def add(self, title: str, description: str = "") -> Task:
        task = Task(id=self._next_id, title=title, description=description)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def list_all(self, only_done: Optional[bool] = None) -> List[Task]:
        tasks = list(self._tasks.values())
        if only_done is None:
            return tasks
        return [t for t in tasks if t.done == only_done]

    def update(self, task_id: int, **changes) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if task is None:
            return None
        for key in ("title", "description", "done"):
            if key in changes:
                setattr(task, key, changes[key])
        return task

    def delete(self, task_id: int) -> bool:
        return self._tasks.pop(task_id, None) is not None

    def count(self) -> int:
        return len(self._tasks)

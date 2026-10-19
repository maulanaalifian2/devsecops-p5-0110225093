from app.models import TaskStore


def test_add_and_get():
    store = TaskStore()
    task = store.add("Belajar DevSecOps", "Kerjakan praktikum 5")
    assert task.id == 1
    assert store.get(1).title == "Belajar DevSecOps"


def test_ids_increment():
    store = TaskStore()
    assert store.add("A").id == 1
    assert store.add("B").id == 2


def test_update_and_filter():
    store = TaskStore()
    store.add("A")
    store.add("B")
    store.update(1, done=True)
    assert len(store.list_all(only_done=True)) == 1
    assert len(store.list_all(only_done=False)) == 1


def test_delete():
    store = TaskStore()
    store.add("A")
    assert store.delete(1) is True
    assert store.delete(1) is False
    assert store.count() == 0

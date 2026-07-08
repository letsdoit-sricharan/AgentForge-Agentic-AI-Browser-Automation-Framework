from app.runtime.memory import RuntimeMemory, RuntimeVariable


def test_set_and_get():
    memory = RuntimeMemory()

    memory.set(RuntimeVariable.MOVIE, "Interstellar")

    assert memory.get(RuntimeVariable.MOVIE) == "Interstellar"


def test_contains():
    memory = RuntimeMemory()

    memory.set(RuntimeVariable.CITY, "Chennai")

    assert memory.contains(RuntimeVariable.CITY)


def test_remove():
    memory = RuntimeMemory()

    memory.set(RuntimeVariable.CITY, "Chennai")
    memory.remove(RuntimeVariable.CITY)

    assert not memory.contains(RuntimeVariable.CITY)


def test_clear():
    memory = RuntimeMemory()

    memory.set(RuntimeVariable.CITY, "Chennai")
    memory.set(RuntimeVariable.MOVIE, "Interstellar")

    memory.clear()

    assert memory.size == 0


def test_snapshot():
    memory = RuntimeMemory()

    memory.set(RuntimeVariable.CITY, "Chennai")

    snapshot = memory.snapshot()

    assert snapshot["city"] == "Chennai"
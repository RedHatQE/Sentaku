import pytest

from todo_example import api as todo_api
from todo_example import pseudorpc, spec
from todo_example import ux as todo_ux


@pytest.fixture()
def api() -> spec.TodoAPI:
    return spec.TodoAPI.from_api(todo_api.TodoApp())


@pytest.mark.parametrize(
    "impl", [todo_api.TodoApp, todo_ux.TodoUX, pseudorpc.PseudoRpc]
)
def test_simple(api: spec.TodoAPI, impl: object) -> None:
    with api.use(impl):
        assert api.implementation_chooser.current.elements == (impl,)
        collection = api.create_collection(name="test")
        item = collection.create_item(name="buy ham")
        # assert collection.all()[0] == item

        try:
            assert not item.completed
        except LookupError:
            pass  # rpc
        item.completed = True

        try:
            assert item.completed
        except LookupError:
            pass  # rpc
        collection.clear_completed()
        assert collection.get_by(name="buy ham") is None

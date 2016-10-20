import pytest

from todo_example import spec, api as todo_api


@pytest.fixture
def api():
    return spec.TodoApi.from_api(todo_api.TodoApp())


@pytest.mark.parametrize('impl', [spec.ViaAPI, spec.ViaUX, spec.ViaRPC])
def test_simple(api, impl):
    with api.use(impl):
        assert api.implementation_chooser.current.elements == (impl, )
        collection = api.create_collection(name='test')
        item = collection.create_item(name='buy ham')
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
        assert collection.get_by(name='buy ham') is None

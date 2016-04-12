import pytest
from todo_example import spec, api as todo_api


@pytest.fixture
def api():

    return spec.TodoApi(app=todo_api.TodoApp())


@pytest.mark.parametrize('impl', [spec.ViaAPI, spec.ViaUX])
def test_simple(api, impl):
    with api.use(impl):
        collection = api.create_collection(name='test')
        item = collection.create_item(name='buy ham')
        # assert collection.all()[0] == item
        item.completed = True
        collection.clear_completed()

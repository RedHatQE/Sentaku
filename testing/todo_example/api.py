import attr


class TodoApp(object):
    pass


@attr.s
class TodoUX(object):
    app = attr.ib()

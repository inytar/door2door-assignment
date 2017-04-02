import morepath

from .app import App


def factory():
    morepath.autoscan()
    App.commit()
    return App()


app = factory()

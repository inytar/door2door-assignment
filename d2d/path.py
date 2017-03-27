from .app import App
from . import model


@App.path(model=model.Data, path='/')
def get_data(app):
    return model.Data()

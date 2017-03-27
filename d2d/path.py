import os

from .app import App
from . import model


@App.path(model=model.Map, path='/')
def get_map(app):
    return model.Map()


@App.path(model=model.Analysis, path='/analysis')
def get_analysis(app):
    return model.Analysis()

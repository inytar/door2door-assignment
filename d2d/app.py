import os

from more.chameleon import ChameleonApp
from more.marshmallow import MarshmallowApp

from webob.static import DirectoryApp

from .import model


class App(ChameleonApp, MarshmallowApp):

    def __init__(self):
        model.Data.load_data()

    static_path = 'static'


@App.template_directory()
def get_template_directory():
    return 'templates'


@App.tween_factory(name='static')
def make_static_tween(app, handler):
    """A tween to serve static files."""
    # TODO allow turning off.
    # TODO Get path from config.
    static_app = DirectoryApp(
        os.path.join(os.path.dirname(__file__), app.static_path),
        index_page=None
    )

    def static_tween(request):
        if request.path_info_peek() == 'static':
            request.path_info_pop()
            return static_app(request)
        return handler(request)

    return static_tween

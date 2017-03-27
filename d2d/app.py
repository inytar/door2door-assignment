import os

from more.chameleon import ChameleonApp
import morepath

from webob.static import DirectoryApp

from .model import Analysis


class App(ChameleonApp):

    def __init__(self):
        Analysis.load_data()

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

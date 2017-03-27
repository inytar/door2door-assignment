from .app import App
from . import model


@App.html(model=model.Map, template='map.pt')
def view_map(self, request):
    return {
        'bounding_box': []
    }


# TODO Should work on post, so we can easily send a html form.
@App.json(model=model.Analysis)
def view_analysis(self, request):
    self.analyse(**request.params)
    return {
        'greeting': 'hello '
    }

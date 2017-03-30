from .app import App
from . import model


@App.html(model=model.Data, template='map.pt')
def view_map(self, request):
    return {
        'bounds': self.bounds
    }


# TODO Should work on post, so we can easily send a html form.
@App.json(model=model.Data, name='data')
def view_analysis(self, request):
    result = self.analyse(**request.params)
    return model.Data.json_parsable(result)

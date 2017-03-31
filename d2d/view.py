from more.marshmallow import loader

from .app import App
from . import model
from .schemas import AnalysisSchema


@App.html(model=model.Data, template='map.pt')
def view_map(self, request):
    return {
        'bounds': self.bounds
    }


load_analyse_params = loader(AnalysisSchema)


@App.json(model=model.Data, name='data',
          load=load_analyse_params)
def view_analysis(self, request, analyse_params):
    result = self.analyse(**analyse_params)
    return model.Data.json_parsable(result)

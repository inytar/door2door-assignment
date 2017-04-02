from more.marshmallow import Error

from .app import App
from . import model
from .schemas import AnalysisSchema


@App.html(model=model.Data, template='map.pt')
def view_map(self, request):
    return {
        'bounds': self.bounds
    }


schema = AnalysisSchema()


def load_analyse_params(request):
    if request.content_type == 'application/json':
        data = request.json
    else:
        data = parse_params(request.params)
    data, errors = schema.load(data)
    if errors:
        raise Error(errors)
    return data


def parse_params(params):
    """Parse parameters into a dictionary with sub dicts."""
    data = []
    for item in params.items():
        item = split_item(*item)
        data.append(item)
    return merge(data)


def merge(data):
    if not data:
        return None
    if len(data) == 1:
        return data[0]
    return merge_dicts(data[0], merge(data[1:]))


def merge_dicts(d1, d2):
    """Merge two dicts and any subdicts they might have."""
    result = d1.copy()
    for key, val in d2.items():
        if key not in result:
            result[key] = val
        else:
            result[key] = merge_dicts(result[key], val)
    return result


def split_item(key, value):
    """Split an item like ('key[subkey]', 'value') into
    {'key': {'subkey': 'value'}}.
    """
    split_key = key.rsplit('[', 1)
    if len(split_key) == 1:
        return {split_key[0]: value}
    key = split_key[0]
    value = {split_key[1][:-1]: value}
    return split_item(key, value)


@App.json(model=model.Data, request_method='POST', load=load_analyse_params)
def view_analysis(self, request, analyse_params):
    result = self.analyse(**analyse_params)
    return model.Data.json_parsable(result)

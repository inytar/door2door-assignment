class Map(object):

    @property
    def binding_box(self):
        return []


class Analysis(object):

    data = None

    @classmethod
    def load_data(cls):
        cls.data = {}

    def analyse(self, **kwargs):
        pass


class Static(object):

    def __init__(self, path):
        self.path = path

import os

import geopandas as gpd


class Data(object):

    _data = None

    @property
    def bounds(self):
        return self._data.total_bounds

    @classmethod
    def load_data(cls):
        cls._data = gpd.read_file(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'static/data/activity_points.geojson'
            )
        )

    def analyse(self, **kwargs):
        pass

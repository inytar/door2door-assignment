import logging
import os

import geopandas as gpd

import numpy as np

import pandas as pd


class Data(object):

    _points = None
    _routes = None
    time_column = 'dt_created_at'

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.points = self._points.copy()
        self.routes = self._routes.copy()

    @property
    def bounds(self):
        return self.points.total_bounds

    @staticmethod
    def load_points():
        log = logging.getLogger(__name__)
        data = gpd.read_file(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'static/data/activity_points.geojson'
            )
        )
        data.set_index('id', inplace=True, drop=False)
        data['dt_timestamp'] = pd.to_datetime(data.timestamp)
        data['dt_created_at'] = pd.to_datetime(data.created_at)
        log.debug('Total points %s', len(data))
        log.debug('Points crs: %s', data.crs)
        log.debug('Points dtypes:\n%s', data.dtypes)
        return data

    @staticmethod
    def load_routes():
        log = logging.getLogger(__name__)
        data = gpd.read_file(
            os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                'static/data/routes.geojson'
            )
        )
        log.debug('Total routes: %s', len(data))
        log.debug('Routes crs: %s', data.crs)
        log.debug('Routes dtypes:\n%s', data.dtypes)
        return data

    @classmethod
    def load_data(cls):
        cls._points = cls.load_points()
        cls._routes = cls.load_routes()

    def period(self, *, shift=1, duration=30):
        return pd.DateTimeIndex(
            self.points[self.time_column]
        ).shift(shift, freq='T').to_period(freq='{}T'.format(duration))

    def points_near_time(self, row, *, data=None):
        if data is None:
            data = self.points
        period = row.dt_period
        return data[(period.start_time <= data[self.time_column]) &
                    (data[self.time_column] <= period.end_time)]

    def points_near_space(self, row, *, decimal=2, data=None):
        if data is None:
            data = self.points
        return data[data.geom_almost_equals(row.geometry, decimal=decimal)]

    def distance_to_route(self):
        result = pd.Series(np.nan, index=self.points.index)
        for row in self.routes.itertuples():
            series = self.points.distance(row.geometry)
            result.update(series[result.isnull() | (series < result)])
        return result

    def analyse(self, **kwargs):
        pass

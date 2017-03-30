import logging
import os

import geopandas as gpd

import numpy as np

import pandas as pd


class Data(object):

    _points = None
    _routes = None
    time_column = 'created_at'

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
        data.timestamp = pd.to_datetime(data.timestamp)
        data.created_at = pd.to_datetime(data.created_at)
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

    def points_near_time(self, period, *, data=None):
        if data is None:
            data = self.points
        return data[(period.start_time <= data[self.time_column]) &
                    (data[self.time_column] <= period.end_time)]

    def points_near_space(self, geometry, *, decimal=2, data=None):
        if data is None:
            data = self.points
        return data[data.geom_almost_equals(geometry, decimal=decimal)]

    def distance_to_route(self):
        result = pd.Series(np.nan, index=self.points.index)
        for row in self.routes.itertuples():
            series = self.points.distance(row.geometry)
            result.update(series[result.isnull() | (series < result)])
        return result

    def count_points_near_space_time(self, *, time_shift=1, time_duration=30,
                                     space_decimal=2):
        # Create dataframe with period and geometry.
        period = self.period(shift=time_shift, duration=time_duration)
        data = gpd.GeoDataFrame({'period': period,
                                 'geometry': self.data.geometry})
        result = pd.Series(0, index=self.points.index)
        for row in data.itertuples():
            points_time = self.points_near_time(row.period)
            result[row.id] = len(self.points_near_space(row.geometry,
                                                        decimal=space_decimal,
                                                        data=points_time))
        return result

    @staticmethod
    def json_parsable(data):
        geo = {'type': 'FeatureCollection',
               'crs': {'type': 'name',
                       'properties': {'name': data.crs['init']}},
               'features': []}
        # loop through all properties, and make sure datetime like objects
        # are converted to strings.
        for feature in data.iterfeatures():
            props = {}
            for name, value in feature['properties'].items():
                if isinstance(value, np.datetime64, pd.Period):
                    value = str(value)
                props['name'] = value
            feature['properties'] = props
            geo['features'].append(feature)
        return geo

    def normalize_speed(self):
        # Get average speed of in_vehicle not 0
        # make this 50 km/h.
        # https://www.lonelyplanet.com/tanzania/dar-es-salaam/transportation/dar-rapid-transit/a/poi-tra/1498335/355642
        # Recalculate all speeds.
        pass

    def calc_probability(self):
        probability = pd.Series(0, index=self.data.index)
        # anything closer than 0.004 to route gets +100
        probability += (self.distance_to_route() < 0.0004) * 100
        # anything with 1 or more points close in time and space gets +50
        probability += (self.count_points_near_space_time() > 1) * 50
        # # anything with 2 or more points close in space gets +50
        # anything with 'still' as current activity gets confidance * 10
        probability += (self.data['current_dominating_activity'] ==
                        'still') & \
            (self.data['current_dominating_activity_confidence'] * 10)
        # anything with not with 'still' as current act gets confidance * -5
        probability += (self.data['current_dominating_activity'] !=
                        'still') & \
            (self.data['current_dominant_activity_confidence'] * -5)
        # # anything with normalized speed > 5 km/h gets - 20
        return probability

    def analyse(self, **kwargs):
        probability = self.calc_probability()
        return gpd.GeoDataFrame({'probability': probability,
                                 'geometry': self.data.geometry})

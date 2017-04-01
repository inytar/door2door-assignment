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
        return pd.DatetimeIndex(
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
                                     space_distance=100):
        # Create dataframe with period and geometry.
        period = self.period(shift=time_shift, duration=time_duration)
        data = gpd.GeoDataFrame({'period': period,
                                 'geometry': self.points.geometry})
        result = pd.Series(0, index=self.points.index)
        for row in data.itertuples():
            points_time = self.points_near_time(row.period)
            result[row.Index] = len(
                self.points_near_space(row.geometry,
                                       decimal=to_decimal(space_distance),
                                       data=points_time)
            )
        return result

    @classmethod
    def json_parsable(cls, data):
        crs = data.crs or cls._points.crs
        geo = {'type': 'FeatureCollection',
               'crs': {'type': 'name',
                       'properties': {'name': crs['init']}},
               'features': []}
        # loop through all properties, and make sure datetime like objects
        # are converted to strings.
        for feature in data.iterfeatures():
            props = {}
            for name, value in feature['properties'].items():
                if isinstance(value, (np.datetime64, pd.Period)):
                    value = str(value)
                props[name] = value
            feature['properties'] = props
            geo['features'].append(feature)
        return geo

    def normalize_speeds(self):
        # Get average speed of in_vehicle not 0
        # make this 50 km/h.
        # https://www.lonelyplanet.com/tanzania/dar-es-salaam/transportation/dar-rapid-transit/a/poi-tra/1498335/355642
        fifty = self.points[(self.points['current_dominating_activity'] ==
                             'in_vehicle')]['speed']
        fifty = fifty[fifty > 0].mean()
        # Recalculate all speeds.
        return self.points['speed'] / fifty * 50

    def calc_probability(self, distance, space_time, current_activity, speed):
        # Create result series.
        probability = pd.Series(0, index=self.points.index)

        # Calculate distance points. Distances closer than
        # distance['distance'] get distance['points']
        probability += (self.distance_to_route() <
                        to_degrees(distance['distance'])) * \
            distance['points']

        # Calculate space time closeness points. Anything with more than
        # space_time['min_count'] points get space_time['points']
        space_time_count = space_time.pop('min_count')
        space_time_points = space_time.pop('points')
        probability += (self.count_points_near_space_time(**space_time) >
                        space_time_count) * space_time_points

        # Calculate dominating activity points. Still get activity['still']
        # points times confidence. Not still get -activity['other'] points
        probability += (self.points['current_dominating_activity'] ==
                        'still') * \
            (self.points['current_dominating_activity_confidence'] *
             current_activity['still_points'])
        probability += (self.points['current_dominating_activity'] !=
                        'still') * \
            (self.points['current_dominating_activity_confidence'] * -1 *
             current_activity['other_points'])

        # Look at speed, speed is more than penalty_speed get
        # -penalty_points. If speed is less than max_speed and accuracy is
        # higher than 0 get speed_points.
        speeds = self.normalize_speeds()
        probability += (speeds >= speed['penalty_speed']) * -1 * \
            speed['penalty_points']
        probability += ((speeds <= speed['max_speed']) &
                        (self.points['accuracy'] > 0)) * speed['speed_points']

        # Min probability is 0.
        probability[probability < 0] = 0
        # Normalize probability
        max_probability = distance['points'] + space_time_points + \
            100 * current_activity['still_points'] + speed['speed_points']
        probability = probability / max_probability * 100

        return probability

    def analyse(self, **kwargs):
        probability = self.calc_probability(**kwargs)
        return gpd.GeoDataFrame({'probability': probability,
                                 'geometry': self.points.geometry})


def to_degrees(meters):
    """Estimate the distance in degrees from distance in meters.

    To simplify this we assume that for our location and crs 1 degree
    is 100 km.
    """
    return meters / 10**5


def to_decimal(meters):
    """Estimate the decimal place of degrees from distance in meters."""
    return -1 * np.log10(to_degrees(meters))

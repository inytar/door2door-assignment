import morepath
import d2d

from webtest import TestApp as Client


def test_root():
    morepath.scan(d2d)
    morepath.commit(d2d.App)

    client = Client(d2d.App())
    root = client.get('/')

    assert root.status_code == 200
    assert b'id="map"' in root.body


def test_data():
    morepath.scan(d2d)
    morepath.commit(d2d.App)

    client = Client(d2d.App())
    response = client.post('/')

    assert response.status_code == 200
    assert 'crs' in response.json
    assert response.json['type'] == 'FeatureCollection'
    features = response.json['features']
    feature = features[0]
    assert feature['type'] == 'Feature'
    assert 'geometry' in feature
    properties = feature['properties']
    assert 'probability' in properties
    geometry = feature['geometry']
    assert geometry['type'] == 'Point'
    assert 'coordinates' in geometry

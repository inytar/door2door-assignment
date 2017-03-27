import morepath
import d2d

from webtest import TestApp as Client


def test_root():
    morepath.scan(d2d)
    morepath.commit(d2d.App)

    client = Client(d2d.App())
    root = client.get('/')

    assert root.status_code == 200
    assert len(root.json['greetings']) == 2

import pytest

from d2d import view


@pytest.mark.parametrize('in_item, expected', [
    (('key', 'value'), {'key': 'value'}),
    (('key[subkey]', 'value'), {'key': {'subkey': 'value'}}),
    (('key', {'subkey': 'value'}), {'key': {'subkey': 'value'}}),
    (('key[subkey0][subkey1]', 'value'), {'key': {'subkey0':
                                                  {'subkey1': 'value'}}}),
])
def test_split_item(in_item, expected):
    assert view.split_item(*in_item) == expected


@pytest.mark.parametrize('d1, d2, expected', [
    ({}, {}, {}),
    ({'k': 'v'}, {}, {'k': 'v'}),
    ({'k0': 'v0'}, {'k1': 'v1'}, {'k0': 'v0', 'k1': 'v1'}),
    ({'k0': {'k0.0': 'v0'}}, {'k0': {'k0.1': 'v1'}},
     {'k0': {'k0.0': 'v0', 'k0.1': 'v1'}}),
    ({'k0': {'k0.0': 'v0'}}, {'k0': {'k0.1': 'v1'}, 'k1': 'v2'},
     {'k0': {'k0.0': 'v0', 'k0.1': 'v1'}, 'k1': 'v2'}),
    ({'k0': {'k0.0': 'v0'}}, {'k0': {'k0.1': 'v1'}, 'k1': {'k0.0': 'v2'}},
     {'k0': {'k0.0': 'v0', 'k0.1': 'v1'}, 'k1': {'k0.0': 'v2'}}),
])
def test_merge_dicts(d1, d2, expected):
    assert view.merge_dicts(d1, d2) == expected
    # Test that order of dicts does not matter.
    assert view.merge_dicts(d2, d1) == expected


@pytest.mark.parametrize('data, expected', [
    ([], {}),
    ([{}], {}),
    ([{}, {}], {}),
    ([{'k': 'v'}], {'k': 'v'}),
    ([{'k0': 'v0'}, {'k1': 'v1'}], {'k0': 'v0', 'k1': 'v1'}),
    ([{'k0': 'v0', 'k1': 'v1'}, {'k2': 'v2'}],
     {'k0': 'v0', 'k1': 'v1', 'k2': 'v2'}),
    ([{'k0': 'v0'}, {'k1': 'v1', 'k2': 'v2'}],
     {'k0': 'v0', 'k1': 'v1', 'k2': 'v2'}),
    ([{'k0': 'v0'}, {'k1': 'v1'}, {'k2': 'v2'}],
     {'k0': 'v0', 'k1': 'v1', 'k2': 'v2'}),
])
def test_merge(data, expected):
    assert view.merge(data) == expected


@pytest.mark.parametrize('params, expected', [
    ({}, {}),
    ({'k0': 'v0'}, {'k0': 'v0'}),
    ({'k0': 'v0', 'k1': 'v1'}, {'k0': 'v0', 'k1': 'v1'}),
    ({'k0[k0.0]': 'v0'}, {'k0': {'k0.0': 'v0'}}),
    ({'k0[k0.0]': 'v0', 'k0[k0.1]': 'v1'},
     {'k0': {'k0.0': 'v0', 'k0.1': 'v1'}}),
    ({'k0[k0.0]': 'v0', 'k1[k1.0]': 'v1'},
     {'k0': {'k0.0': 'v0'}, 'k1': {'k1.0': 'v1'}}),
    ({'k0[k0.0][k0.0.0]': 'v0'}, {'k0': {'k0.0': {'k0.0.0': 'v0'}}}),
])
def test_parse_params(params, expected):
    assert view.parse_params(params) == expected

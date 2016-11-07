import pytest

import pytry


class DummyTrial(pytry.Trial):
    def params(self):
        self.param('a', a=0)
        self.param('b', b=0.0)
        self.param('c', c='')
        self.param('d', d=True)
        self.param('e', e=False)

    def evaluate(self, p):
        return {}


def test_parse_valid():
    t = DummyTrial()

    p = t.parse_args('--a 1 --b 0.5 --c hi --d False --e'.split())
    assert p['a'] == 1
    assert p['b'] == 0.5
    assert p['c'] == 'hi'
    assert p['d'] is False
    assert p['e'] is True

    p = t.parse_args([])
    assert p['a'] == 0
    assert p['b'] == 0.0
    assert p['c'] == ''
    assert p['d'] is True
    assert p['e'] is False


def test_parse_unknown_param():
    t = DummyTrial()

    with pytest.raises(SystemExit):
        t.parse_args('--x 1'.split())


def test_parse_invalid_value():
    t = DummyTrial()

    with pytest.raises(SystemExit):
        t.parse_args('--a hi'.split())
    with pytest.raises(SystemExit):
        t.parse_args('--a 1.5'.split())
    with pytest.raises(SystemExit):
        t.parse_args('--b hi'.split())
    with pytest.raises(SystemExit):
        t.parse_args('--d 1.2'.split())

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
        return dict(ra=p.a, rb=p.b, rc=p.c, rd=p.d, re=p.e)

def test_set_param():
    t = DummyTrial()
    
    assert t.run(a=1)['ra'] == 1
    assert t.run(b=1)['rb'] == 1
    assert t.run(b=1.5)['rb'] == 1.5
    assert t.run(c='hi')['rc'] == 'hi'
    assert t.run(d=False)['rd'] == False
    assert t.run(e=True)['re'] == True

    with pytest.raises(AttributeError):
        t.run(q=0)

def test_param_override():
    class BadTrial(pytry.Trial):
        def params(self):
            self.param('seed', seed=1)

    with pytest.raises(ValueError):
        BadTrial()


def test_param_creation():
    class BadTrial(pytry.Trial):
        def params(self):
            self.param('seed')

    with pytest.raises(ValueError):
        BadTrial()

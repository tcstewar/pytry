import os
import shutil

import numpy as np

import pytry


class DummyTrial(pytry.Trial):
    def params(self):
        self.param('a', a=0)
        self.param('b', b=0.0)
        self.param('c', c='')
        self.param('d', d=True)
        self.param('e', e=False)
    def evaluate(self, p):
        return dict(
            aa=p.a,
            bb=p.b,
            cc=p.c,
            dd=p.d,
            ee=p.e)

def test_save_txt():
    DummyTrial().run(data_dir='tmp', data_filename='tmp')
    values = {}
    with open('tmp/tmp.txt') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) > 0:
                k, v = line.split(' = ')
                values[k] = eval(v)
    assert isinstance(values['a'], int)
    assert isinstance(values['b'], float)
    assert isinstance(values['c'], str)
    assert isinstance(values['d'], bool)
    assert isinstance(values['e'], bool)
    assert isinstance(values['aa'], int)
    assert isinstance(values['bb'], float)
    assert isinstance(values['cc'], str)
    assert isinstance(values['dd'], bool)
    assert isinstance(values['ee'], bool)

    assert values['a'] == values['aa']
    assert values['b'] == values['bb']
    assert values['c'] == values['cc']
    assert values['d'] == values['dd']
    assert values['e'] == values['ee']


def test_save_npz():
    DummyTrial().run(data_dir='tmp', data_filename='tmp',
                     data_format='npz')
    values = {}
    f = np.load('tmp/tmp.npz')
    for k in f.files:
        values[k] = f[k]
    assert values['a'].dtype.kind == 'i'
    assert values['b'].dtype.kind == 'f'
    assert values['c'].dtype.kind == 'S' or values['c'].dtype.kind == 'U'
    assert values['d'].dtype.kind == 'b'
    assert values['e'].dtype.kind == 'b'
    assert values['aa'].dtype.kind == 'i'
    assert values['bb'].dtype.kind == 'f'
    assert values['cc'].dtype.kind == 'S' or values['cc'].dtype.kind == 'U'
    assert values['dd'].dtype.kind == 'b'
    assert values['ee'].dtype.kind == 'b'

    assert values['a'] == values['aa']
    assert values['b'] == values['bb']
    assert values['c'] == values['cc']
    assert values['d'] == values['dd']
    assert values['e'] == values['ee']

def test_read():
    for data_format in ['txt', 'npz']:
        if os.path.exists('tmp2'):
            shutil.rmtree('tmp2')

        for seed in range(3):
            DummyTrial().run(data_dir='tmp2',
                             data_format=data_format, seed=seed)
        data = pytry.read('tmp2')
        assert len(data) == 3
        for values in data:
            assert values['a'] == values['aa']
            assert values['b'] == values['bb']
            assert values['c'] == values['cc']
            assert values['d'] == values['dd']
            assert values['e'] == values['ee']

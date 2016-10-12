import pytry

class Simple(pytry.Trial):
    def params(self):
        self.param('first number', x=1)
        self.param('second number', y=1)
        self.param('operation to compute', op='plus')

    def evaluate(self, p):
        if p.op == 'plus':
            result = p.x + p.y
        if p.op == 'minus':
            result = p.x - p.y
        return dict(result=result)

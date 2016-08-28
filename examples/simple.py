import pytry

class Simple(pytry.Trial):
    def params(self):
        self.param('first number', x=1)
        self.param('second number', y=1)
        self.param('operation to compute', op='plus')

    def evaluate(self, p, plt):
        if p.op == 'plus':
            result = p.x + p.y
        if p.op == 'minus':
            result = p.x - p.y
        return dict(result=result)

if __name__ == '__main__':
    Simple().run(x=1, y=2)

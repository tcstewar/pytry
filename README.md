# pytry: Running trials with parameter variation

Pytry is a light-weight Python package for defining something that you want
to try, some parameters you'd like to vary while you try it, and some
measurement that you want to do each time you try it.

For example, suppose you have some complicated simulation you want to run
and measure how well it performs.  You might write code that looks like
this:

```python
model = create_my_large_model(a=3, b=7)
data = model.run()
average_value = numpy.mean(data)
final_value = data[-1]
```

But now you want to explore what happens as you adjust parameter values.
Sometimes you just want to do this by hand, changing ```a``` and ```b``` and
seeing what happens.  Sometimes you want to do this more rigorously, by
automatically varying the parameter values over some range.  And you probably
what to record those results of the individual runs.

Pytry lets you slightly reorganize the code to look like this:

```python
import pytry

class MyModel(pytry.Trial):
    def params(self):
        self.param('the first parameter', a=3)
        self.param('the second parameter', b=7)
    def evaluate(self, p, plt):
        model = create_my_large_model(a=p.a, b=p.b)
        data = model.run()
        return dict(
            average_value=numpy.mean(data),
            final_value=data[-1],
            )
```

Now you can run the Trial in one of two ways.  First, you can use ```pytry```
itself from the command line.  Just do:

```
pytry filename.py --a 5 --b 8
```

from the command line and your model will be run with your new parameter
settings.  Second, you can run it from a separate script:

```python
for a in [3, 5, 7, 9]:
    for b in [3, 5, 7, 9]:
        MyModel().run(a=a, b=b)
```

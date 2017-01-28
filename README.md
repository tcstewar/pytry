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
class MyModel(pytry.Trial):
    def params(self):
        self.param('the first parameter', a=3)
        self.param('the second parameter', b=7)
    def evaluate(self, p):
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

This will run the model 16 times with all combinations of parameter settings

## Command line interaction

When you use ```pytry``` from the command line, you can give the ```--help```
argument to see the various options.  This will include the defined parameters
of the model.  For example, for the model above you will see:

```
usage: pytry [-h] [--a <X>] [--b <X>] [--seed <X>] [--data_dir <X>]
             [--data_filename <X>] [--verbose <X>]
             FILE

pytry: Run Trials with parameters

positional arguments:
  FILE                 .py file containing Trial object

optional arguments:
  -h, --help           show this help message and exit
  --a <X>              the first parameter (default=3)
  --b <X>              the second parameter (default=7)
  --seed <X>           random number seed (default=1)
  --data_dir <X>       data directory (default='data')
  --data_filename <X>  filename for data (default=None)
  --verbose <X>        print progress information (default=True)
```

The parameters ```a``` and ```b``` are determined from the ```Trial``` you
defined, but the other parameters are automatically generated.  They are:

 - ```seed```, which sets the random number seeds for the standard ```random```
   random number generator, as well as the ```numpy.random``` random number
   generator
 - ```data_dir```, which indicates the directory to store the results of the
   trial in.
 - ```data_filename```, the filename to use for this trial.  If it is not
   set, it defaults to ```<ModelName>#<timestamp>-<UUID>```.
 - ```verbose```, whether information will be printed to the screen

All of these parameters are also available when running from a script.  For
example, you can do:

```python
MyModel().run(a=3, b=5, seed=2, verbose=False)
```

## Recorded data files

Each trial is saved as a separate file.  By default, it uses a simple text
format, including both the parameter settings and the evaluation results.
For example, the above model will create files like this:

```
a = 3
b = 7
seed = 1

average_value = 3.4240799645298909
final_value = 7.8862242385055321
```

You can change the save format using the ```data_format``` option.  The
currently known formats are ```txt``` (the default text format) and
```npz``` (the numpy ```savez``` format).


You can also load all the data from all the trials in a directory:

```python
data = pytry.read('data')
```

This will give you a list of dictionaries, with each dictionary containing
the contents of one trial.  Since this is the same format used by common
data management packages such as ```pandas```, you can do this to get it
into a pandas DataFrame:

```python
df = pandas.DataFrame(pytry.read('data'))
```

## Plotting data

You may want to generate plots in addition to the raw results from running
the trial.  To do this, use ```pytry.PlotTrial``` rather than
 ```pytry.Trial```.  This adds three new parameters:

```
  --plt                display plot (default=False)
  --plt_save           save plot (default=False)
  --plt_overlay        show overlay on figures (default=False)
```

 - ```plt```, whether to show the plot on the screen
 - ```plt_save```, whether those plots should be saved to a file
 - ```plt_overlay```, whether the plots should have the parameter values
   and results written on them as well

When using the ```pytry.PlotTrial```, the ```evaluate``` function will get
a ```plt``` argument passed into it.  This will be the ```matplotlib.pyplot```
object (or ```None``` if neither the ```plt``` nor ```plt_save```
parameters are set).  

```python
class MyModel(pytry.PlotTrial):
    def params(self):
        self.param('the first parameter', a=3)
        self.param('the second parameter', b=7)
    def evaluate(self, p, plt):
        model = create_my_large_model(a=p.a, b=p.b)
        data = model.run()

        if plt is not None:
            plt.plot(data)

        return dict(
            average_value=numpy.mean(data),
            final_value=data[-1],
            )
```

If ```plt``` is set, this plot will be shown on the screen.  If
```plt_save``` is set, this plot will be saved as a ```.png``` file in the
data directory.  These parameters are dependent on ```matplotlib``` being
installed.

## Custom Trial type: NengoTrial

By subclassing ```pytry.Trial``` you can make customized ```Trial```s for
different circumstances.  ```pytry``` has one of these built-in that is
suitable for use with ```nengo```, a package for producing large-scale
neural simulations.

The ```pytry.NengoTrial``` class introduces new parameters and separates
```evaluate``` into two stages (making the model and running the model).
This works as follows:

```python
class NengoSimple(pytry.NengoTrial):
    def params(self):
        self.param('number of neurons', N=100)
        self.param('number of dimensions', D=2)

    # define the model
    def model(self, p):
        model = nengo.Network()
        with model:
            stim = nengo.Node([0]*p.D)
            ens = nengo.Ensemble(n_neurons=p.N, dimensions=p.D)
            nengo.Connection(stim, ens)
            self.probe = nengo.Probe(ens, synapse=0.01)
        return model

    # run the model and evaluate the results
    def evaluate(self, p, sim, plt):
        sim.run(1)

        if plt is not None:
            plt.plot(sim.trange(), sim.data[self.probe])

        rmse = np.sqrt(np.mean((sim.data[self.probe])**2))
        return dict(rmse=rmse)
```

This also adds three new parameters (in addition to the three introduced
by ```pytry.PlotTrial```:

```
  --backend <X>        nengo backend to use (default='nengo')
  --dt <X>             nengo timestep (default=0.001)
  --gui                run in nengo GUI (default=False)
```

 - ```backend``` allows you to run the neural model using different
   implementations of the neural simulator (such as nengo_ocl or
   nengo_spinnaker)
 - ```dt``` specifies the time step of the simulation
 - ```gui``` does not run the simulation.  Instead, it creates the model and
   then starts the ```nengo_gui``` interactive simulation environment, allowing
   you to directly interact with the model.

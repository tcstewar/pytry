import os


def read(path):
    data = []
    if os.path.exists(path):
        for fn in os.listdir(path):
            if fn.endswith('.txt'):
                with open(os.path.join(path, fn)) as f:
                    text = f.read()
                d = dict()
                try:
                    exec(text, d)
                except:
                    continue
                del d['__builtins__']
                data.append(d)
    return data

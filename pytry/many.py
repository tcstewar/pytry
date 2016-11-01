import sys
import os


def execute(cmd, checked=None):
    if checked is None:
        checked = []
    if len(cmd) == 0:
        os.system(' '.join(checked))
    else:
        c = cmd.pop(0)
        if c.startswith('[') and c.endswith(']'):
            if ':' in c:
                start, end = c[1:-1].split(':', 1)
                opts = ['%d' % x for x in range(int(start), int(end))]
            else:
                opts = c[1:-1].split('~')
            for opt in opts:
                execute(list(cmd), checked + [opt])
        else:
            execute(cmd, checked + [c])


def run_many():
    if len(sys.argv) < 2:
        print('Usage: pytry-many filename.py --param1 [v1~v2~v3] --p2 [v1~v2]')
        print('   or: pytry-many <runner> file.py --p1 [v2~v3] --p2 [v1~v2]')
        sys.exit()

    cmd = sys.argv[1:]

    if os.path.exists(sys.argv[1]) and sys.argv.endswith('.py'):
        cmd = ['pytry'] + cmd

    execute(cmd)

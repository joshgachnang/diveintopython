import re
import subprocess
import sys


INTERPRETERS = ['python2.7']


def run_file(match):
    """ Run the file through all the configured interpreters
    :return:
    """
    indent = len(match.group('indent'))
    with open('/tmp/py', 'w') as f:
        for line in match.group('code').split('\n'):
            f.write(line[indent:])
            f.write('\n')

    outputs = []
    for interp in INTERPRETERS:
        try:
            out = subprocess.check_output([interp, f.name],
                                          stderr=subprocess.STDOUT)
            print 'out', out
        except subprocess.CalledProcessError:
            print "{} failed command: \n{}".format(
                interp, open(f.name, 'r').read())
            continue
        outputs.append(out)
    if not outputs:
        return None
    else:
        return outputs[0]


def run_interpreter(match):
    indent = len(match.group('indent'))
    with open('/tmp/py', 'w') as f:
        for line in match.group('code').split('\n'):
            f.write(line[indent:])
            f.write('\n')
    a = execfile('/tmp/py')
    print "run intp", a
    return a


def replace(match):
    if match.group('args') == 'file':
        return run_file(match)
    elif match.group('args') == 'interpreter':
        return run_interpreter(match)


def template(filename):
    with open(filename, 'r') as f:
        lines = f.read()
    # print lines
    lines = re.sub(r'(?P<indent>[ ]*){\%\s*(?P<args>[A-Za-z0-9_,]+)\s*\n(?P<code>\s*.+)\s*\%}',
           replace, lines, flags=re.DOTALL)
    # print lines

if __name__ == '__main__':
    template(sys.argv[1])
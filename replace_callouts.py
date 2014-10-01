"""Find all instances of {{1}} and replace them with the matching callout img"""
import glob
import re


def find_html_files(directory):
    return glob.glob('{}/*/*.html'.format(directory))


def replace_callouts(html_file):
    with open(html_file, 'r') as f:
        newlines = []
        for line in f.readlines():
            matches = re.search(r'\{\{(?P<num>\d)\}\}', line)
            if matches:
                line = line.replace(
                    matches.group(), '<img src="images/callouts/{}.png">'
                    .format(matches.groups()[0]))

            newlines.append(line)

    with open(html_file, 'w') as f:
        for line in newlines:
            f.write(line)


if __name__ == '__main__':
    for f in find_html_files('website/'):
        replace_callouts(f)
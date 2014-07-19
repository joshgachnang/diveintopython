import re
import sys


def replace(input, output=None):
    output = output = input
    text = open(input).read()
    text = re.sub('You are here.+creativeASIN=B001GIOFN8\)', '', text, flags=re.S)
    text = re.sub('\[\\\<\\\<.+Josh Gachnang\.', '', text, flags=re.S)
    text = re.sub('\|\|', '', text, flags=re.S)
    text = re.sub('\n\|', '\n', text, flags=re.S)
    text = re.sub('\|', ' ', text, flags=re.S)
    text = re.sub('\s\[\]\n', '\n', text, flags=re.S)
    text = re.sub('\n\[\!\[', '\n\n[![', text, flags=re.S)


    with open(output, 'w') as output_file:
        output_file.write(text)

if __name__ == '__main__':
    replace(sys.argv[1])
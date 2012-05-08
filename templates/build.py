from jinja2 import Environment, FileSystemLoader
from jinja2 import TemplateNotFound
import os

#>>> with open('/home/josh/programming/diveintopython/templates/dv.html', 'w') as f:
#...     f.write(template.render({'site_url': 'http://www.diveintopython.net/', 'support_email': 'josh@servercobra.com'}).encode('utf8'))


template_dir = os.getcwd()
output_dir = os.path.join(template_dir, '../demo')

# Must be http://DOMAIN.TLD/. Trailing slash is important.
site_url = 'http://www.diveintopython.net/'
support_email = 'josh@servercobra.com'

ignore = ('chapter_base.html', 'chapter_page_template.html', 'footer.html', 'google_analytics.html', 'google_search.html')

env = Environment(loader=FileSystemLoader(template_dir))

def render_file(in_file, out_file, input_directory=None, output_directory=None):
    '''
    Takes the given input file, renders it, and places it in the named 
    output_file in output_directory inside output_dir
    '''
    if input_directory is None:
        input_file = os.path.join(template_dir, in_file)
    else:
        input_file = os.path.join(template_dir, input_directory, in_file)
    if output_directory is None:
        output_file = os.path.join(output_dir, out_file)
    else:
        output_file = os.path.join(output_dir, output_directory, out_file)
    if not os.path.exists(input_file) or not os.path.isfile(input_file):
        print "Input file %s doesn't exist or isn't a file." % input_file
        return

    if in_file in ignore:
        return
    try:
        with open(output_file, 'w') as out:
            if input_directory is None:
                template = env.get_template(in_file)
            else:
                template = env.get_template(os.path.join(input_directory, in_file))
            out.write(template.render({'site_url': site_url, 'support_email': support_email}).encode('utf8'))
            print "Rendered %s to %s" % (in_file, out_file)
            return

    except TemplateNotFound as e:
        print "Could not find template %s" % input_file
        return
    except OSError as e:
        print "Error writing to output file %s, error" % (output_file), e.value
        return

def render_all_html():
    for ob in os.listdir(template_dir):
        if os.path.isfile(os.path.join(template_dir, ob)) and ob[-5:] == '.html':
            # Is a file, send to render_file
            #print "rendering %s" % ob
            render_file(ob, ob,)

        elif os.path.isdir(os.path.join(template_dir, ob)):
            dirname = ob
            # Is directroy, list files, send to render_file
            for f in os.listdir(ob):
                if os.path.isfile(os.path.join(template_dir, dirname, f)) and f[-5:] == '.html':
                    #print "rendering %s" % f
                    render_file(f, f, dirname, dirname)


if __name__ == '__main__':
    render_all_html()
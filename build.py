from jinja2 import Environment, FileSystemLoader
from jinja2 import TemplateNotFound
import os

#>>> with open('/home/josh/programming/diveintopython/templates/dv.html', 'w') as f:
#...     f.write(template.render({'site_url': 'http://www.diveintopython.net/', 'support_email': 'josh@servercobra.com'}).encode('utf8'))

root_dir = os.getcwd()
template_dir = os.path.join(root_dir, 'templates')
output_dir = os.path.join(root_dir, 'new')

# Must be http://DOMAIN.TLD/. Trailing slash is important.
site_url = 'http://www.diveintopython.net/'
support_email = 'josh@servercobra.com'

ignore = ('new_chapter_base1.html', 'chapter_base.html', 'chapter_page_template.html', 'footer.html', 'google_analytics.html', 'google_search.html', 'new_chapter_page_template.html', 'new_chapter_base.html', 'snippets.html')

env = Environment(loader=FileSystemLoader(template_dir))

#def render_file1(in_file, out_file, input_directory=None, output_directory=None):
    #'''
    #Takes the given input file, renders it, and places it in the named 
    #output_file in output_directory inside output_dir
    #'''
    #if input_directory is None:
        #input_file = os.path.join(template_dir, in_file)
    #else:
        #input_file = os.path.join(template_dir, input_directory, in_file)
    #if output_directory is None:
        #output_file = os.path.join(output_dir, out_file)
    #else:
        #output_file = os.path.join(output_dir, output_directory, out_file)
    #if not os.path.exists(input_file) or not os.path.isfile(input_file):
        #print "Input file %s doesn't exist or isn't a file." % input_file
        #return

    #if in_file in ignore:
        #return
    #try:
        #with open(output_file, 'w') as out:
            #if input_directory is None:
                #template = env.get_template(in_file)
            #else:
                #template = env.get_template(os.path.join(input_directory, in_file))
            #out.write(template.render({'site_url': site_url, 'support_email': support_email}).encode('utf8'))
            #print "Rendered %s to %s" % (in_file, out_file)
            #return

    #except TemplateNotFound as e:
        #print "Could not find template %s" % input_file
        #return
    #except OSError as e:
        #print "Error writing to output file %s, error" % (output_file), e.value
        #return

def render_file(infile):
    ''' Takes in file, renders it to the output directory. Only works for folders that are at most one deep.'''
    if not os.path.exists(infile):
        print "File does not exist: %s" % (infile)
        return
    out_dir = infile.split('/')[-2]
    out_filename = infile.split('/')[-1]
    
    template_path = os.path.join(template_dir, out_dir, out_filename)
    output_file = os.path.join(output_dir, out_dir, out_filename)
    
    if out_filename in ignore:
        return
    #print out_dir, out_filename, template_path, output_file
    try:
        with open(output_file, 'w') as out:
            t = os.path.join(out_dir, out_filename)
            #print t
            template = env.get_template(t)
            out.write(template.render({'site_url': site_url, 'support_email': support_email}).encode('utf8'))
            print "Rendered %s to %s" % (infile, output_file)
            return

    #except TemplateNotFound as e:
        #print "Could not find template %s" % infile
        #print e
        #return
    except OSError as e:
        print "Error writing to output file %s, error" % (output_file), e.value
        return
    
def render_all_html():
    for ob in os.listdir(template_dir):
        if os.path.isfile(os.path.join(template_dir, ob)) and ob[-5:] == '.html':
            # Is a file, send to render_file
            #print "rendering %s" % ob
            render_file(os.path.join(template_dir, ob))

        elif os.path.isdir(os.path.join(template_dir, ob)):
            dirname = os.path.join(template_dir, ob)
            #print dirname
            # Is directroy, list files, send to render_file
            for f in os.listdir(dirname):
                if os.path.isfile(os.path.join(dirname, f)) and f[-5:] == '.html':
                    #print "rendering %s" % f
                    render_file(os.path.join(dirname, f))


if __name__ == '__main__':
    render_all_html()

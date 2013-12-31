"""
This file takes the original HTML and creates a build system using Jinja2. It also filters out the old
diveintopyton.org links and switches them to diveintopython.net. I'm also switching the email to my own, because
Mark is unreachable.
"""

from bs4 import BeautifulSoup
import os
from jinja2 import Environment, FileSystemLoader
from jinja2 import TemplateNotFound
import shutil
import distutils

root_dir = os.getcwd()
template_dir = os.path.join(root_dir, 'templates')
output_dir = os.path.join(root_dir, 'pages')
original_dir = os.path.join(root_dir, 'original/html')


def convert(old_dir, page, new_dir):
    """
    Converts a page from the static HTML to a Jinja2 template
    Page is a filename to convert.
    The file will be read from old_dir (either full path or reachable relative path), and written to new_dir.
    """
    # Load up the file into soup
    with open(os.path.join(old_dir, page), 'r') as f:
        soup = BeautifulSoup(f.read())
    # Save some important stuff that's on every page
    data = {
        'title': soup.title.string,
        'document_links': link_builder(soup.findAll(rel="previous", href=True, title=True)),
        'previous': link_builder(soup.findAll(rel="previous", href=True, title=True)),
        'next': link_builder(soup.findAll(rel="next", href=True, title=True)),
        'up': link_builder(soup.findAll(rel="up", href=True, title=True)),
        'breadcrumb': encode(soup.findAll(id="breadcrumb")),
        'navigation': encode(soup.findAll(id="navigation")),
        'footer': encode(soup.findAll("table", class_="Footer")),
        'titlepage': encode(soup.findAll("div", class_="titlepage")),
        'toc': encode(soup.findAll("div", class_="toc")),
        'abstract': encode(soup.findAll("div", class_="abstract")),
        'section': encode(soup.findAll("div", class_="section"))
    }
    # print soup.prettify()
    # print "data", data['section']
    if data['section'] is not None:
        if data['titlepage'] is not None and data['titlepage'] in data['section']:
            # print "title in section"
            data['titlepage'] = None
        if data['abstract'] is not None and data['abstract'] in data['section']:
            # print "abs in sectionr"
            data['abstract'] = None
    # print 'prev', data['previous']['href']
    # for k, v in data.items():
    #     print k
    #     for item in v:
    #         print item
    env = Environment(loader=FileSystemLoader(template_dir))
    output_file = os.path.join(output_dir, new_dir, page)
    with open(output_file, 'w') as out:
        template = env.get_template("page_template.html")
        html = template.render(data).encode("utf-8")
        # print "writing to ", old_dir, page, new_dir
        out.write(html)


def link_builder(soup):
    """
    Gets the first item in the list as a link dict and returns it, or returns None.
    """
    if len(soup) == 0:
        return None
    else:
        # print "hreftitle", soup[0]['href'], soup[0]['title'], soup[0]['rel']
        return {
            "href": soup[0]['href'].encode('ascii', 'ignore'),
            "title": soup[0]['title'].encode('ascii', 'ignore'),
        }


def encode(soup):
    if len(soup) == 0:
        return None
    return soup[0].encode('ascii')


def convert_all(root_directory):
    # print os.listdir(root_directory)
    # return
    for ob in os.listdir(root_directory):
        # print "ob", ob, os.path.isfile(os.path.join(root_directory, ob))
        # return
        if os.path.isdir(os.path.join(root_directory, ob)):
            directory = os.path.join(root_directory, ob)
            # print "directory", directory
            for f in os.listdir(directory):
                filename = os.path.join(directory, f)
                if os.path.isfile(filename):
                    if filename[-5:] == ".html":
                        # print "Converting", directory, f, os.path.join(output_dir, ob)
                        if not os.path.exists(os.path.join(output_dir, ob)):
                            os.mkdir(os.path.join(output_dir, ob))
                        convert(directory, f, os.path.join(output_dir, ob))
                    else:
                        shutil.copyfile(filename, os.path.join(output_dir, ob, f))
                else:
                    # nested directory
                    # print "other file", f

                    if os.path.exists(os.path.join(output_dir, ob, f)):
                        shutil.rmtree(os.path.join(output_dir, ob, f))
                    shutil.copytree(filename, os.path.join(output_dir, ob, f))

        elif os.path.isfile(os.path.join(root_directory, ob)):
            # print "root file", ob
            filename = ob
            # print "root file", filename
            if filename[-5:] == ".html":
                # print "Converting", root_directory, filename, output_dir
                convert(root_directory, filename, output_dir)
                # return
            else:
                source = os.path.join(root_directory, ob)
                destination = os.path.join(output_dir, ob)
                shutil.copyfile(source, destination)


def copy_replacements():
    # Copy over all the replacement files from templates/additions. Easy way to build and modify things like css.
    for f in os.listdir(os.path.join(template_dir, 'additions')):
        filename = os.path.join(template_dir, 'additions', f)
        if os.path.isfile(filename):
            shutil.copyfile(filename, os.path.join(output_dir, f))
        else:
            for subf in os.listdir(filename):
                # print "sub", subf
                subfilename = os.path.join(template_dir, 'additions', f, subf)
                shutil.copyfile(subfilename, os.path.join(output_dir, f, subf))
            # Change to merge files.
            # shutil.copytree(filename, os.path.join(output_dir, f))


if __name__ == "__main__":
    convert_all('original/html')
    copy_replacements()
    # convert("or/html/native_data_types", "lists.html", output_dir)
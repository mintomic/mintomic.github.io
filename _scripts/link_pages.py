# This script updates the YAML front matter of all documentation pages.
# It requires each page to have a valid title and next link (if any).
# From this, it will update the prev, prev_title, up, up_title, and next_title variables.
# Also generates _includes/toc.html

from collections import OrderedDict
import re
import os
import sys
import cgi
import StringIO

# Set ROOT to the parent folder
ROOT = os.path.normpath(os.path.join(sys.argv[0], '..', '..'))

def pathToUrl(*paths):    
    """ Simply join some paths and convert to forward slashes if necessary. """
    return os.path.normpath(os.path.join(*paths)).replace('\\', '/')

class Page:
    """ Represents a page of documentation.
        Stores its URL, the raw contents of its .md file, and its YAML front matter as a dictionary.
        Also stores "level" which is how deeply nested it is in subfolders.
        Has next, up and prev links. """

    def __init__(self, url):
        assert '\\' not in url
        self.url = url
        self.level = len([c for c in self.url.split('/') if c]) + 1
        lines = open(self.localPath(), 'r').readlines()
        assert lines[0] == '---\n'
        div = lines.index('---\n', 1)
        self.yaml = OrderedDict(re.match('(\\w+): (.*)', l).groups() for l in lines[1:div])
        self.body = lines[div+1:]
        self.next = None
        self.up = None
        self.prev = None

    def localPath(self):
        return os.path.join(ROOT, os.path.relpath(self.url, '/'), 'index.md')
    
    def __repr__(self):
        return 'Page(%s, %s)' % (self.url, repr(self.yaml['title']))

    def updateYaml(self):
        """ Update the YAML dictionary to reflect changes to the next, up and prev links.
            Also store the titles of previous/next pages. """        
        for x in ['prev', 'up', 'next']:
            if getattr(self, x):
                self.yaml[x] = getattr(self, x).url
                self.yaml[x + '_title'] = getattr(self, x).yaml['title']
            else:
                if x in self.yaml:
                    del self.yaml[x]
                if x + '_title' in self.yaml:
                    del self.yaml[x + '_title']

    def save(self):
        """ Resave the .md file locally. """   
        header = ['---\n'] + ['%s: %s\n' % (k, v) for k, v in self.yaml.items()] + ['---\n']
        open(self.localPath(), 'w').writelines(header + self.body)

def writeTOC(f, page, indent=''):
    """ Traverse a hierarchy of pages starting at the given root and output a nested
        list of HTML <ul> & <li> elements with hyperlinks. This gets written to
        _includes/toc.html. """
    level = 0
    while page:
        if level >= page.level:
            while level > page.level:
                level -= 1
                f.write('    ' * level + '  </li>\n')
                f.write('    ' * level + '</ul>\n')
            f.write('    ' * (level - 1) + '  </li><li>\n')
        else:
            while level < page.level:
                f.write('    ' * level + '<ul>\n')
                f.write('    ' * level + '  <li>\n')
                level += 1            
        if not page:
            break
        f.write('    ' * level + '<a href="%s">%s</a>\n' % (page.url, cgi.escape(page.yaml['title'])))
        page = page.next
    while level > 0:
        level -= 1
        f.write('    ' * level + '  </li>\n')
        f.write('    ' * level + '</ul>\n')

def sweepPages():
    """ Perform a pass through the available pages, repairs the prev & up links in the YAML,
        stores the titles of previous/up/next links, resaves them and writes a new
        _includes/toc.html. Requires all the next links and titles to already be valid. """
    # Make doubly-linked next/prev list
    p = Page('/')
    pages = [p]
    print('Reading pages...')
    while p.yaml.has_key('next'):
        p.next = Page(p.yaml['next'])
        p.next.prev = p
        p = p.next
        pages.append(p)
        
    # Make up links
    print('%d pages found. Fixing links...' % len(pages))
    url2page = dict((p.url, p) for p in pages)
    for p in pages[1:]:
        url = pathToUrl(p.url, '..')
        p.up = url2page[url]
        
    # Update yamls and re-save
    print('Resaving...')
    for p in pages:
        p.updateYaml()
        p.save()

    # Make TOC
    print('Generating _includes/toc.html...')
    toc = StringIO.StringIO()
    writeTOC(toc, pages[0])
    open(os.path.join(ROOT, '_includes', 'toc.html'), 'w').write(toc.getvalue())

sweepPages()

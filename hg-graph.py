#!/usr/bin/env python
"""
Run it:
hg log -r c54441866584::default --template "{node} {children} <branch>{branch}</branch> <date>{date|isodate}</date> <desc>{desc}</desc> <user>{author}</user>\n" | hg-graph.py | dot -Tpng -o1.png
"""

import cgi
import re
import sys

def print_rev(rev, branch, date, user, desc):
    print (
        "\"{0}\" [shape=box, margin=0, label=<<table border=\"0\">"
        "<tr><td align=\"right\">changeset</td><td align=\"left\">{0}</td></tr>"
        "<tr><td align=\"right\">branch</td><td align=\"left\">{1}</td></tr>"
        "<tr><td align=\"right\">date</td><td align=\"left\">{2}</td></tr>"
        "<tr><td align=\"right\">user</td><td align=\"left\">{3}</td></tr>"
        "<tr><td align=\"right\">desc</td><td align=\"left\">{4}</td></tr>"
        "</table>>];"
        .format(rev, cgi.escape(branch), cgi.escape(date), cgi.escape(user), cgi.escape(desc))
    )

MAIN_RE = re.compile(
    r'^([a-f0-9]{12})[a-f0-9]{28}((?:\s\d+\:[a-f0-9]{12})*)'
    r'\s<branch>(.*)</branch>'
    r'\s<date>(.*)</date>'
    r'\s<desc>(.*)</desc>'
    r'\s<user>(.*)</user>'
    '.*$', re.I)
REV_RE = re.compile(r'\s\d+:([a-f0-9]{12})', re.I)

seen = set()

print 'digraph G {'
for i in sys.stdin:
    m = MAIN_RE.search(i)
    if m:
        rev = m.group(1)
        if rev not in seen:
            seen.add(rev)
            branch = m.group(3)
            date = m.group(4)
            desc = m.group(5)
            user = m.group(6)
            print_rev(rev, branch, date, user, desc)
            
        if m.group(2):
            for c in REV_RE.findall(m.group(2)):
                child = c[-12:]
                print "\"{}\" -> \"{}\";".format(rev, child)
print '}'

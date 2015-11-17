#!/usr/bin/env python
#
# Copyright 2015
# Johannes K. Fichte, Vienna University of Technology, Austria
#
# gml2htdecomp.py is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.  gml2htdecomp.py is
# distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.  You should have received a copy of the
# GNU General Public License along with gml2htdecomp.py.  If not, see
# <http://www.gnu.org/licenses/>.
#
from os import path as os_path
import logging
import logging.config
logging.config.fileConfig('%s/logging.conf'%os_path.dirname(os_path.realpath(__file__)))

from itertools import imap, izip
import contextlib
import networkx as nx
import optparse
import sys

def options():
    usage  = "usage: %prog [options] [files]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-o", "--output", dest="out", type="string", help="Output file", default=None)
    opts, files = parser.parse_args(sys.argv[1:])
    if len(files)>1:
        raise ValueError('Supports at most one input file.')
    return opts, files[0]


@contextlib.contextmanager
def selective_output(filename=None):
    if filename and filename != '-':
        fh = open(filename, 'w')
    else:
        fh = sys.stdout
    try:
        yield fh
    finally:
        if fh:
            fh.close()

def replace_chars(x):
    return x.replace(',','').replace('%','').replace('.','').replace('-','').replace('+','')

def write_htdecomp(G,output):
    output.write('<defVar : %s>\n' %' , '.join(imap(lambda x: replace_chars(str(x)), G.nodes_iter())))
    output.write('<defRel : %s>\n' %' , '.join(imap(lambda x: replace_chars(str(x)) + '/2', xrange(G.number_of_edges()))))
    output.write('\n')
    n = 0
    num_edges=G.number_of_edges()
    for e,i in izip(G.edges_iter(),xrange(num_edges)):
        #print 'e0=', replace_comma(e[0]), 'e1=', replace_comma(e[1])
        output.write('%i (%s,%s)' %(i,replace_chars(e[0]),replace_chars(e[1])))
        if i<num_edges-1:
            output.write(',\n')
        else:
            output.write('.\n')
            output.flush()
        #exit(1)

def parse_and_run(filename,output):
    logging.info('Reading gml file...')
    G=nx.read_gml(filename)
    logging.info('Reading done')
    logging.info('Exporting Graph to htdecomp format')
    write_htdecomp(G,output)

if __name__ == '__main__':
    opts,filename=options()
    s=None
    with selective_output(opts.out) as s:
        parse_and_run(filename,s)
    exit(1)

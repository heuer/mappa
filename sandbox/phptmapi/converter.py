# -*- coding: utf-8 -*-
#
#    ====================================
#    Topic Maps source -> PHPTMAPI script
#    ====================================
#
#    Donated to the public domain by Lars Heuer - Semagia <http://www.semagia.com/>.
#
"""\
Converts a topic map into a PHP script.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      Public Domain
"""
from optparse import OptionParser
import codecs
try:
    import phptmapi
except ImportError:
    import sys
    sys.path.append('..')
from phptmapi.miohandler import PHPTMAPIMapHandler
from tm import Source
from tm.mio import create_deserializer

def _generate_phpfilename(source):
    filename = source + '.php'
    slash_idx = filename.rfind('/')
    if slash_idx:
        filename = filename[slash_idx+1:]
    return filename

def _extract_format(source):
    dot_idx = source.rfind('.')
    if dot_idx == -1:
        return None
    return source[dot_idx+1:]

def main():
    usage = usage = 'usage: %prog args'
    parser = OptionParser(usage)
    parser.add_option('-s', '--source', dest='source',
                      help='Specifies the source')
    parser.add_option('-o', '--out', dest='output',
                      help='Specifies the output file name')
    parser.add_option('-f', '--format', dest='format',
                      help='Specifies the Topic Maps syntax name of the source, i.e. xtm. '
                      'If the format is not specified, the format will be extracted from '
                      'the source filename')
    parser.add_option('-b', '--base', dest='base',
                      help='Specifies the IRI against which the identifiers are resolved')
    (options, args) = parser.parse_args()
    if not options.source:
        parser.error('No source specified')
    out_filename = options.output or _generate_phpfilename(options.source)
    format = options.format or _extract_format(options.source)
    if not format:
        parser.error('The format was not specified and cannot be detected')
    deser = create_deserializer(format=format)
    if not deser:
        parser.error('Cannot find a deserializer for "%s"' % format)
    src = Source(file=open(options.source, 'rb'), iri=options.base or options.source)
    out = codecs.open(out_filename, 'wb', 'utf-8')
    deser.handler = PHPTMAPIMapHandler(out)
    deser.parse(src)
    out.close()
    

if __name__ == '__main__':
    main()

====================================
Topic Maps source -> PHPTMAPI script
====================================

This script converts a topic map source into a PHP script which
uses PHPTMAPI to create a topic map.

Usage::

  converter.py -s pokemon.ltm -b http://www.example.org/map


Use::

  converter.py --help 

to get help.

Requirements:
- Python >= 2.4
- tm.reader.* packages

Install Python and then install all available topic map readers via:

  easy_install -U tm.reader.ctm tm.reader.xtm tm.reader.jtm tm.reader.tmxml tm.reader.ltm


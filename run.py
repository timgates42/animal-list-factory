#!/usr/bin/env python
"""\
%(app)s

Usage:
   %(cmd)s [options] <wordset_dictionary_path>
   %(cmd)s (-h | --help)
   %(cmd)s --version

Options:
  -h --help              Show this screen
  --version              Show version

"""
# vi:syntax=python

from __future__ import print_function, division

# System Imports
import sys
import os
import io
import json
# External Imports
import docopt

__version__ = '0.1'
__appname__ = 'animal-word-factory'

def main():
    """
    Read command line options and pass to the main command line entry point.
    """
    appname = __appname__ if __appname__ else sys.argv[0]
    args = docopt.docopt(
        __doc__ % {
            'app': appname,
            'cmd': sys.argv[0],
        },
        version='%s %s' % (
            appname,
            __version__,
        )
    )
    run_main(args)

def get_basedir():
    """
    Locate the current directory of this file
    """
    return os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))

def run_main(args):
    """
    Main Command Line Entry Point
    """
    wordset_dictionary_path = args['<wordset_dictionary_path>']
    animal_kinds = [
        'mammal', 'invertebrate', 'reptile', 'fish', 'bird', 'amphibian',
    ]
    animals = []
    for letter in (chr(val) for val in range(ord('a'), ord('z') + 1)):
        fpath = os.path.join(wordset_dictionary_path, 'data', '%s.json' % (
            letter,
        ))
        with io.open(fpath, 'r', encoding='utf-8') as fobj:
            dictdata = json.load(fobj)
            for word in dictdata:
                worddetails = dictdata[word]
                meanings = worddetails.get('meanings', [])
                found = False
                for meaning in meanings:
                    if meaning['speech_part'] != 'noun':
                        continue
                    if any(
                                animalkind in meaning['def'].lower().split(' ')
                                    for animalkind in animal_kinds
                            ):
                        found = True
                        break
                if found:
                    animals.append(word)
    print('\n'.join(animals))

if __name__ == '__main__':
    main()

# vim: set ft=python:

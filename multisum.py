#!/usr/bin/env python3
"""multisum.

Usage:
multisum.py [--plain | --xml] [--one-game] [--mktxt] FILE ...

Options:
  -h, --help        Show this screen.
  -v, --version     Show version.
  -x, --xml         Output in xml datfile format.
  -p, --plain       Output in plain format.
  -o, --one-game    If format is xml,
  -t, --mktxt       Create ".multisum.txt" files for each hashed file.

"""
from docopt import docopt
import rhash
from pathlib import Path

format_strings={
'plain' : \
['',
'filename : {filename}\n'
'size     : {size}\n'
'crc32    : {crc32}\n'
'md5      : {md5}\n'
'sha1     : {sha1}\n'
'sha256   : {sha256}\n',
'\n',

''],

'xml': \
['<game name="{filename}">\n',

'<rom name="{filename}" size="{size}" crc="{crc32}" md5="{md5} '
'sha1="{sha1}" sha256="{sha256}"/>\n',
 
'</game>\n',

'\n']
}

def print_format_string(hasher,output_format,part):
    print(format_strings[output_format][part].format(
            filename='TODO',
            size='TODO',
            crc32=hasher.HEX(rhash.CRC32),
            md5=hasher.HEX(rhash.MD5),
            sha1=hasher.HEX(rhash.SHA1),
            sha256=hasher.HEX(rhash.SHA256)
            ),end='')

def main(arguments):
    hasher = rhash.RHash(rhash.CRC32 | rhash.MD5 | rhash.SHA1 | rhash.SHA256)
    if arguments['--xml']:
        output_format = 'xml'
    else:
        output_format = 'plain'
    for file in arguments['FILE']:
        hasher.update_file(file)
        print_format_string(hasher,output_format,0)
        print_format_string(hasher,output_format,1)
        print_format_string(hasher,output_format,2)
    print_format_string(hasher,output_format,3)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='multisum.py')
    main(arguments)

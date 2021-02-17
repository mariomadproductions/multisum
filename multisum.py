#!/usr/bin/env python3
"""multisum.

Usage:
multisum.py --format=<format> [--one-game] [--mktxt] <file> ...

Options:
  -h, --help               Show this screen.
  -v, --version            Show version.
  -f, --format=<format>    Format to output in.
                           Values:
                           gh - GameHeader
                           xml - xml datfile
                           plain - plain text
  -o, --one-game           If format is xml, and multiple files are selected,
                           put everything under one "game" tag.
  -t, --mktxt              Create ".multisum.txt" files for each file.

"""
from docopt import docopt
import rhash
from pathlib import Path

format_strings={
'gh': \
[
'',
'----| File Data |--------------------------------------------------\n'
'System:             Unknown File\n'
'Archive:            \n'
'File:               {filename}\n'
'Size (Bytes):       {size}\n'
'CRC32:              {crc32}\n'
'MD5:                {md5}\n'
'SHA1:               {sha1}\n'
'SHA256:             {sha256}\n'
'-------------------------------------------------------------------\n'
'\n',
'',
''
],

'xml': \
[
'<game name="{filename}">\n',
'<rom name="{filename}" size="{size}" crc="{crc32}" md5="{md5}" '
'sha1="{sha1}" sha256="{sha256}"/>\n',
'</game>\n',
'\n'
],

'plain' : \
[
'',
'filename : {filename}\n'
'size     : {size}\n'
'crc32    : {crc32}\n'
'md5      : {md5}\n'
'sha1     : {sha1}\n'
'sha256   : {sha256}\n',
'\n',
''
],
}

def print_format_string(filename,size,hasher,output_format,part):
    print(format_strings[output_format][part].format(
            filename=filename,
            size=size,
            crc32=hasher.HEX(rhash.CRC32),
            md5=hasher.HEX(rhash.MD5),
            sha1=hasher.HEX(rhash.SHA1),
            sha256=hasher.HEX(rhash.SHA256)
            ),end='')

def main(arguments):
    hasher = rhash.RHash(rhash.CRC32 | rhash.MD5 | rhash.SHA1 | rhash.SHA256)
    output_format = arguments['--format']
    for file in arguments['<file>']:
        filename = Path(file).name
        size = Path(file).stat().st_size
        hasher.update_file(file)
        print_format_string(filename,size,hasher,output_format,0)
        print_format_string(filename,size,hasher,output_format,1)
        print_format_string(filename,size,hasher,output_format,2)
    print_format_string(filename,size,hasher,output_format,3)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='multisum.py')
    main(arguments)

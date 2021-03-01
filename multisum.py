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
from zlib import crc32
from hashlib import sha1, sha256, md5
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


#This function is based on one by Icyelut
def hash_file(file_path):
    calculated_crc32 = 0
    calculated_md5 = md5()
    calculated_sha1 = sha1()
    calculated_sha256 = sha256()
    with open(file_path, "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            calculated_crc32 = crc32(data, calculated_crc32)
            calculated_md5.update(data)
            calculated_sha1.update(data)
            calculated_sha256.update(data)

    output_crc32 = ("%08X" % (calculated_crc32 & 0xffffffff)).upper()
    output_md5 = calculated_md5.hexdigest().upper()
    output_sha1 = calculated_sha1.hexdigest().upper()
    output_sha256 = calculated_sha256.hexdigest().upper()
    
    return output_crc32, output_md5, output_sha1, output_sha256

def print_format_string(filename,size,hashes,output_format,part):
    print(format_strings[output_format][part].format(
            filename=filename,
            size=size,
            crc32=hashes[0],
            md5=hashes[1],
            sha1=hashes[2],
            sha256=hashes[3]
            ),end='')

def main(arguments):
    output_format = arguments['--format']
    for file in arguments['<file>']:
        filename = Path(file).name
        size = Path(file).stat().st_size
        hashes = hash_file(file)
        print_format_string(filename,size,hashes,output_format,0)
        print_format_string(filename,size,hashes,output_format,1)
        print_format_string(filename,size,hashes,output_format,2)
    print_format_string(filename,size,hashes,output_format,3)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='multisum.py')
    main(arguments)

#!/usr/bin/env python3
"""multisum.

Usage:
multisum.py --format=<format> [--recursive] [--one-game] [--mktxt] <path> ...

Options:
  -h, --help               Show this screen.
  -v, --version            Show version.
  -f, --format=<format>    Format to output in.
                           Values:
                           gh - GameHeader
                           xml - xml datfile
                           plain - plain text
  -r, --recursive          Hash files recursively.
  -o, --one-game           If format is xml, and multiple files are selected,
                           put everything under one "game" tag.
  -t, --mktxt              Create ".multisum.txt" files for each file.

"""
from docopt import docopt
from zlib import crc32
from hashlib import md5, sha1, sha256
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

arguments = docopt(__doc__, version='multisum.py')
output_format = arguments['--format']
input_path = arguments['<path>']
recursive_mode = arguments['--recursive']

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

def print_format_string(filename,size,hashes,part):
    if part == 3:
        print(format_strings[output_format][part],end='')
    else:
        print(format_strings[output_format][part].format(
                filename=filename,
                size=size,
                crc32=hashes[0],
                md5=hashes[1],
                sha1=hashes[2],
                sha256=hashes[3]
                ),end='')

def process_file(path):
    if recursive_mode:
        filename = Path(path)
    else:
        filename = Path(path).name
    size = Path(path).stat().st_size
    hashes = hash_file(path)
    print_format_string(filename,size,hashes,0)
    print_format_string(filename,size,hashes,1)
    print_format_string(filename,size,hashes,2)

def main():
    path_not_dir_found = False
    for path_string in input_path:
        if Path(path_string).is_dir():
            if recursive_mode:
                for glob_path in Path(path_string).glob('**/*'):
                    try:
                        process_file(glob_path)
                    except IsADirectoryError:
                        pass
            else:
                for iterdir_path in Path(path_string).iterdir():
                    try:
                        process_file(iterdir_path)
                    except IsADirectoryError:
                        pass
        else:
            path_not_dir_found = True
            process_file(path_string)
    if path_not_dir_found:
        print_format_string(None,None,None,3)

if __name__ == '__main__':
    main()

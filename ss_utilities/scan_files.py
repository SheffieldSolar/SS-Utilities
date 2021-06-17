#!/usr/bin/python3
"""
Scan for all files of a particular file extension recursively and look for a particular string
inside.

- Jamie Taylor <jamie.taylor@sheffield.ac.uk>
- First Authored: 2020-04-07
"""

import os
import sys
import glob
import argparse

global quiet
quiet = True

def parse_options():
    """Parse command line options."""
    parser = argparse.ArgumentParser(description=("This is a command line interface (CLI) to "
                                                  "scan for files with a particular file extension "
                                                  "containing a particular string"),
                                     epilog="Jamie Taylor 2020-04-07")
    parser.add_argument("-e", "--extension", metavar="<file-extension>[ <file-extension2>]",
                        dest="extensions", action="store", nargs="*", type=str, required=False,
                        default=["*"], help="Specify a file extension (without the period '.'). "
                                            "Can specify multiple extensions separated by spaces.")
    parser.add_argument("-p", "--path", metavar="</an/absolute/path>", dest="path", action="store",
                        type=str, required=False, default=os.getcwd(),
                        help="Specify a path to search in (default is CWD).")
    parser.add_argument("-r", "--recursive", dest="recursive", action="store_true", required=False,
                        help="Specify to search for files recursively.")
    parser.add_argument("--find", metavar="<some-string>", dest="find", action="store",
                        type=str, required=False, default=None,
                        help="Specify a string to look for in matched files.")
    parser.add_argument("--replace", metavar="<some-string>", dest="replace", action="store",
                        type=str, required=False, default=None,
                        help="Specify a string to replace with in matched files (must be used in "
                             "conjunction with '--find'.")
    parser.add_argument("-o", "--outfile", metavar="</path/to/file>", dest="outfile",
                        action="store", type=str, required=False, default=None,
                        help="Specify a file to write results to (leave blank to print results to "
                             "stdout).")
    parser.add_argument("-q", "--quiet", dest="quiet", action="store_true",
                        required=False, help="Specify to not print anything to stdout.")
    parser.add_argument("--encoding", metavar="<character-encoding>", dest="encoding",
                        action="store", type=str, required=False, default="utf-8",
                        help="Specify the character encoding to use for find & replace (default is "
                             "utf-8).")
    options = parser.parse_args()
    def handle_options(options):
        """Extra validation of the options."""
        if not os.path.isdir(options.path):
            raise Exception(f"The path you specified ('{options.path}') does not exist.")
        return options
    return handle_options(options)

def print_results(results, filename=None):
    if filename is None:
        for file in results:
            print(file)
    else:
        with open(filename, "w") as fid:
            for file in results:
                fid.write(f"{file}\n")
        print(f"    -> Results were printed to '{filename}'")

def find_in_files(files, find, replace=None):
    if find is None:
        return files
    results = []
    for file in files:
        found = False
        with open(file, "r+b") as fid:
            # import pdb; pdb.set_trace()
            content = fid.read()
            if find in content:
                results.append(file)
                found = True
        if found and replace is not None:
            with open(file, "w+b") as fid:
                fid.write(content.replace(find, replace))
    return results

def myprint(msg):
    global quiet
    if not quiet:
        print(msg)

def scan_files(path, extensions=["*"], recursive=False, find=None, replace=None, outfile=None,
               encoding="utf-8"):
    myprint(f"Scanning '{path}' for files with extensions: {extensions}, recursive={recursive}...")
    path = os.path.join(path, "**") if recursive else path
    files = []
    for extension in extensions:
        files += glob.glob(os.path.join(path, f"*.{extension}"), recursive=recursive)
    myprint(f"    -> Found {len(files)} files matching the extension")
    find_ = find.encode(encoding) if find is not None else find
    replace_ = bytes(replace.encode(encoding)) if replace is not None else replace
    results = find_in_files(files, find_, replace_)
    if find is not None:
        myprint(f"    -> {len(results)} out of {len(files)} files contain the string '{find}'")
    print_results(results, outfile)

def main():
    opts = parse_options()
    quiet = opts.quiet
    scan_files(
        path=opts.path,
        extensions=opts.extensions,
        recursive=opts.recursive,
        find=opts.find,
        replace=opts.replace,
        outfile=opts.outfile,
        encoding=opts.encoding
    )

if __name__ == "__main__":
    main()


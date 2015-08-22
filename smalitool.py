#! /usr/bin/env python

import argparse
import sys
import os
import glob

# What we're looking for in the smali code
SMALI_CLASS = '.class'
SMALI_FIELD = '.field'
SMALI_INTERFACE = '.implements'
SMALI_METHOD_START = '.method'
SMALI_METHOD_END = '.end method'
SMALI_ANNOTATION_START = '.annotation'
SMALI_ANNOTATION_END = '.end annotation'

# What the user types
CLASS_ARG = 'class'
METHOD_ARG = 'method'
ANNOTATION_ARG = 'annotation'
FIELD_ARG = 'field'
INTERFACE_ARG = 'interface'

def find_declarations_in_file(fcontent, dec_type):
    matching_lines = [x for x in fcontent if dec_type in x]
    return matching_lines

def show_declarations(fcontent, dec_type):
    for line in find_declarations_in_file(fcontent, dec_type):
        print line.strip()

def show_info(fcontent):
    show_declarations(fcontent, SMALI_CLASS)
    show_declarations(fcontent, SMALI_INTERFACE)
    show_declarations(fcontent, SMALI_FIELD)
    show_declarations(fcontent, SMALI_METHOD_START)
    #show_declarations(fcontent ,SMALI_ANNOTATION_START)

def inspect_method(mname, fcontent):
    methods = []
    method = []
    inside_method = False

    for i in xrange(len(fcontent)):
        if inside_method:
            method.append(str(i+1) + ": " + fcontent[i])
            if fcontent[i].startswith(SMALI_METHOD_END):
                methods.append(method)
                method = []
                inside_method = False
        else:
            if fcontent[i].startswith(SMALI_METHOD_START) and (mname+"(" in fcontent[i]):
                method.append(str(i+1) + ": " + fcontent[i])
                inside_method = True
    
    for m in methods:
        for l in m:
            print l
        print "\n"

# Define which method shall be called by which parameter
dec_types = {CLASS_ARG:SMALI_CLASS, METHOD_ARG:SMALI_METHOD_START, FIELD_ARG:SMALI_FIELD, INTERFACE_ARG:SMALI_INTERFACE, ANNOTATION_ARG:SMALI_ANNOTATION_START}


def parse_info_cmd(args):
    # Read file content
    fcontent = args.file.readlines()
    fcontent = [x[:-1] for x in fcontent]

    # Choose what to do depending on the specified optional parameters
    if not (args.show or args.inspect):
        show_info(fcontent)
        sys.exit(0)

    # Call function corresponding to given arguments    
    elif args.show:
        results = show_declarations(fcontent, dec_types[args.show])
    elif args.inspect:
        results = inspect_method(args.inspect, fcontent)


def parse_find_cmd(args):
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            fname = os.path.join(root, file)
            if not fname.endswith('.smali'):
                continue
            f = open(fname, 'r')
            fcontent = f.readlines()
            f.close()
            fcontent = [x[:-1] for x in fcontent]
            res = find_declarations_in_file(fcontent, SMALI_CLASS)
            if args.name in res[0]:
                print args.name, "found in", fname
            

commands = {'info':parse_info_cmd, 'find':parse_find_cmd}

if __name__ == "__main__":

    # Define argument parser and its options
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    info_parser = subparsers.add_parser('info', help="Show information for given smali file.")

    group = info_parser.add_mutually_exclusive_group()
    info_parser.add_argument('file', type=argparse.FileType('rt'), help="Smali file that shall be parsed.")
    group.add_argument('-s', '--show', choices=(CLASS_ARG, METHOD_ARG, FIELD_ARG, INTERFACE_ARG, ANNOTATION_ARG), help="Show all declarations of specified type.")
    group.add_argument('-i', '--inspect', help="Display source code given method.")

    find_parser = subparsers.add_parser('find', help="Find smali file containing given class.")
    find_parser.add_argument('name', help="The name of the class that seeked.")
    # TODO: Option to find callers of method of class
    
    # Parse arguments
    args = parser.parse_args()

    # Execute command
    commands[args.command](args)





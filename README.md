# smalitool
A little stand-alone tool for simpler parsing of smali files and projects

## Usage

### Parsing a specific .smali file

Smalitool allows a user to extract the class, fields, methods, interfaces, and annotations from smali files by calling

    ./smalitool.py info test.smali --show method

You can quickly extract the method declaration of a method foo from test.smali with 

    ./smalitool.py info test.smali -i foo

### Searching through .smali files
Smalitool can also be used to search through folders of smali files to find a class declaration by calling

    ./smalitool.py find class_name --path path/to/search/dir

If no path is given, then the script caller's current directory will be used as the search directory root.
If you want to find all callers of a method bar of a class foo then type

    ./smalitool.py find foo --callee bar --path path/to/search/dir

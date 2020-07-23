# Guide to the markup-languages PML and SML

(c) 2019-2020

Updated 23 July 2020

These are two markup languages designed to take plain text and allow transformation to .docx

# What are these markup languages?

PML is a markup language that attempts to take a relatively clean text file and transform it into intermediate markup language (SML or 'styled markup language).

SML (styled markup language) can be transformed into a .docx file, even one that requires legal numbering.

# How to use?

Download this repository.

Run the scripts 
1. On your files from command line; or
2. Integrate your scripts with Visual Studio Code and run from there.

## Command line

At present, the proposed workflow and my python implementation consists of two main translation programs:

Conversion of .pml text files to .sml text --> use pml2sml.py

Conversion of .sml text to OOXML and ultimately to .docx ---> use sml2docx.py

### Example (PML)

pml2sml.py -n filename.pml

Options:

-n to specify 'notes on')

-o to specify an output folder.

In PML, double-forward-slash // can be used to indicate a comments (notes) line 

## Using Visual Studio code

To see a simple example of my implementation of this workflow in python, used within the Visual Studio Code text editor, follow [this note](/Demo/HowTo_PMLparser.md)

# Simple examples

See:

example.pml

example.sml



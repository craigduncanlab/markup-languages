# Styled Markup Language (SML) and Plain Markup Language (PML) Specifications

(c) 29 January 2020 Craig Duncan

# Introduction

This document contains a definition for the two markup languages I have created (and which are still in development).  

The languages are:

 - Plain Markup Language (PML)
 - Styled Markup Language (SML)
 
Presently, PML and SML and are useful when chained together in a sequence to translate PML text files into .doxc files.

In brief, you write simple documents in the 'PML' text format (example here) and then by running one or more programs, you can convert that into .docx files.  There is an intermediate markup format used called Styled Markup Language (SML).

I have provided a simple example of my implementation in python, used within the Visual Studio Code text editor in [this note](/VisualStudioCode/README.md)

# How it works

The proposed workflow and implementation in python is:

- Conversion of .pml text files to .sml text ; using pml2sml
- Conversion of .sml text to OOXML and ultimately to .docx : using sml2docx.py

The purpose of translating PML to SML first is to allow some automated algorithms to make the task of inserting markup easier for writers.   The purpose of SML is to convert style codes to the more complicated OOXML format which is needed to make Word (.docx) files.

Also, by writing in PML and markup up comments (notes), this can easily be turned on or off for the purpose of the finished .docx document.

Another feature of PML/SML is to be able to insert document breaks - allowing you to produce more than one .docx file from a single PML script file.

# Definitions

Both PML and SML are markup languages, but PML has far less markup definitions.  This does mean, however, that a PML to SML translator may have more work (translation algorithms) to do.

SML is a markup language that specifies the styles for output, in a precise line-by-line fashion (suitable for .OOXML and .docx for example).  

Used together, these markup languages can be used, for example, to translate simple text documents into rendered and styled output (for example in a .docx file).  

Some of the goals of such staged text translation are:

-  to bridge the inconvenient gap between simple markup and more complex object-orientated, serialised markup languages like OOXML (with another human-readable markup scheme); and
- to introduce additional markup language features such as document splitting and easy toggle of comments/notes content.

The last features (such as tighter control over notes) are enabled by the markup definitions, but it also requires the translation program to accept override instructions about whether notes should appear in the output or not.

# Plain Markup Language 

The aim of this markup language is minimalist, to avoid the need for markup except where it can assist with automated application of styles and rendering of new documents.

Consistent with this aim, the present definition of PML avoids the need for marking up plain text except for:
 - notes; 
 - punctuation to encode tabulation (e.g. vertical expansion of long legal sentences);
 - defining where new documents begin; and
 - metadata (kind of document  - to assist with automated SML generation).

Automated SML generation requires the translator to use algorithms and analysis of the PML text to produce more detailed markup encoding than exists in the PML.  

## Notes

One of the aims of PML is to give easy control over the inclusion of comments(notes) that will pass through to SML.  

## Document divisions

The document division '-n-' is currently the same as SML, but it could be changed if the PML to SML translator makes an appropriate substitution.

## Expansion of sentences by Plain English drafting rules

Rather than a tagging system, PML uses a sentence construction convention (or restriction), namely that sub-paragraphs and lists will not be written vertically in PML.

The intention is that the PML to translate to an intermediate markup language like SML can convert a sentence that is written as :

	This is a sentence that has lists, including: first item; second item; and third item.

into sml like this:

	This is a sentence that has lists, including:#IN

	first item;#H3

	second item; and#H3

	third item.#H3

which can ultimately appear in .docx as something like this:

	This is a sentence that has lists, including:

	(a) first item;

	(b) second item; and

	(c) third item;

There is a legal convention that can require that some components of sentences can be broken into separate lines (paragraphs) depending on the location of list items, which are then indicated not only by line breaks, but also by the colon and semi-colons.  This process is called 'tabulation' in academic legal drafting papers.

The exact hashcode applied in SML will depend on the currently chosen 'theme' of the document.  The parser will turn these into separate paragraphs and attempt to locate the 'and' on the correct line.

## Metadata (categories of document)

The instruction 'meta:' can be used to specify the style outline schemes to be used for PML to SML translation schemes.

For example, 

	meta:legaldoc
	meta:letter
	meta:defaultdoc
	meta:memo

Each of these will specify the specific hashcodes to be used in place of the 'default' styles detected by the program.

# Independent use of Styled Markup Language (SML)

SML can be used as the basis for a simple translater to OOXML.  I have implemented one such translator in python in conjunction with a predefined .docx template, with the names of styles captured in the text for which the relevant style is applied.

For example, in the demonstration template document (StylesTemplate.docx), the only text in the document is text naming styles for use with SML, like:

	H1
	Indent1

and each of these lines has the relevant style applied to allow OOXML conventions to be sampled and used.

The penultimate markup language for conversion to OOXML (in this case, SML) must be organised as if each line is a paragraph, and each paragraph needs a style, to conform to OOXML assumptions.

## Defining new document breakpoints for distinct .docx files 

A feature of SML not found in most markup/markdown languages is the ability to divide the output of the single input file (whether chained .pml or .sml).

The insertion of document divisions by the ```-n-``` code is retained by PML to SML translation but then processed by SML to OOXML translators as a document division code.

The following codes should be at the beginning of a line.

- New documents use ```-n-```
- Document sections use ```---``` (legacy)

Every ```-n-``` line in an sml file will create a new docx file when processed.

The ```-n-``` code must be followed by the proposed filename (e.g. for .docx file output)

e.g. ```-n-NewFilename```

If no ```-n-``` line appears in the file the file will be output as 'Demo'

## SML hashcodes syntax

All hash tags appear at the *end* of a line or relevant paragraph, before the carriage return (line feed).

e.g.

	This is a heading level 1#H1

	This is a sentence. This is another sentence.#LN

	This is a note#N

	This will be indented #IN

	This will be indent level 2#Indent2

## Simple line-based hashcodes to use

The prepareParagraph function in sml2docx.py matches sml #codes to the template style names.  The default template .docx file is  in LegalDocsTemplate.docx.

The following hashcodes used for .sml map to the Styles in LegalDocsTemplate.docx 
(see sml2docx.py prepareParagraph)

 | sml hashcode |	Equivalent StyleName | Description
 | :-------- | :-------------- | ------------|
 | LH | H1 | 
 | LHF			| Indent1 |
 | LC 			|   H2 | 
 | LCF			|  Indent1
 | LCFF		|  H3
 | H1 			|    H1 | A numbered, bold heading (level 1 heading)
 | H2 			|    H2 | A numbered, bold heading (level 2 heading)
 | H3 			|    H3 | A numbered, alphabetic heading (level 3 heading)
 | H4 			|    H4
 | H5 			|    H5
 | IN 			|  Indent1
 | Indent1	|	Indent1
 | Indent2	|	Indent2
 | Indent0	|	IndentNoSpace
 | GD			|  Indent1
 | LD 			|  Indent1
 | ST 			|  SUBTITLE
 | DT 			|  DocTitle
 | BC 			|  BoldCentred
 | CH 		  |	CentredHeading
 | Note 	  |	Note
 | None	  |	Note
 | NP 		  |	NumParas
 | NP2 	  |	NumParas2
 | NB 		  |	NumParasBold
 | B 		  |	BoldHeading
 | LDP0 	  |	LDP0
 | LDP1 	  |	LDP1
 | LDdate 	|	LDdate
 | LDB 	  |	LDB
 | LDBN 		| LDBN
 | LN 			|    LN
 | Sched1 	| SCHEDL1

```nb: The `Note` style in the LegalDocsTemplate.docx is highlighted and italicised.```

| SML hashcode | Breaks: |
| :------- | :--- |
| SB 		|	SectionBreak
| PB 		|	PageBreak
   
## SML's patterned hashcodes

The purpose of SML is to identify line by line styles, however it is often convenient to process a schema or pattern of different styles in a hierarchical way, to a given block of text, or a sequence of sentences.  This saves having to encode SML lines comprehensively.  In addition, this can, if convenient, be a feature taken into account by PML to SML translaters.

If there are multiple sentences in a paragraph, you can direct the parser to use a hashcode pattern within the paragraph by just placing one hashcode at the end  (see sml2docx.py function readRowsSpam)

If there are more than 3 sentences in the paragraph, the last hashcode pattern will repeat as often as necessary to complete the paragraph.  These are the patterned hashcodes currently implemented in sml2docx.py.


| Hashcode 		| SML hashcode pattern	|		Description
| ---------- | --------------- | ---------------------------------------
| BC 	|			["BC","BC","BC"]		|			All bold centred
| LH 	|			["LH","Indent1","H3"]	|			Heading 1, Indent para with (a)
| IP 	|			["Indent1","Indent1","Indent1"]	|	Indented paragraphs
| H3 	|			["H3","H3","H3"]		|			All H3 level
| LC 	|			["LC","LCF","LCFF"]	|				H2, Indent, H3 repeat
| BHP |			["B","NP","NP"]			|			Bold Heading with numbered paras (Witness st)
| PP 	|			["NP","NP","NP"]		|			All numbered paras
| PL 	|			["NP","NP2","NP2"]		|			Numbered paras with change of numbering
| LHC |			["LH","LC","LCF"]			|		H1,H2, Indent
| L2 	|			["H2","Indent1","H3","H3"]		|	H2 with an indent then (a) pattern

# Implementation of the PML to SML translation

PML to SML translator design is based on the premise that by knowing a specific document type, the conventions and writing patterns can be used to detect structure and use this for application of more detailed, line-by-line style codes.  This helps to convert relatively plain text into SML.  It can also be described as an Automatic SML Assistant.

The efficacy of the translator is based on domain-specific knowledge and the quality of inferences that can be made by the algorithms that it uses.

The currently implemented plain english markup pre-processor is : pml2sml.py. 

## 'Plain English' long sentence expansion

The use of in-line colons and semicolons without line breaks in a PML file can be converted into separate separate SML lines (plain english style) by the PML to SML translation program.  This conversion to separate lines in SML enables each of the sentence fragments to be styled, ultimately, in a .docx output format. 

## Auto-detection of features for automated markup of styles

The PML to SML program attempts to convert sentences or paragraphs into SML hashcodes based on text features (e.g. automatic detection of headings levels 1 and 2)

The hashcodes it is looking to add can be generalised as :
	h1code,	h2code, notescode and level names (e.g. ["LDP1","H3","H4","H5"])

The classification system is based on the assumption that different types of documents (e.g. legal documents) are written with structural and grammatical patterns that can be automatically detected.

The way in which the document is processed depends on the currently selected 'theme' (triggered by encountering the 'meta:' code in the file being processed).  e.g. if the code 'meta:legaldoc' is encountered it will process the file using the set of abstract hashcodes defined for legal documents.

## Translation of comments to SML

The initial PML parser to SML, pml2sml.py, recognises simple notes or comments encoded by a '//' at the start of the line (like some programming languages).   These will be converted to an SML hashcode #N for the next stage of text processing.

e.g.

```// can be used to indicate a comments (notes) line (i.e. #N) will be inserted by pml2sml.py```

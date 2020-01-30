-n-CoverLetter
meta:letter
//Here are some notes at the start of the letter.
//If I want these to be left out, I just select the Task without notes when I create the docx.

The Company Secretary
LawCoder Pty Ltd
41 Innovation Loop 
PERTH WA 6000

23 December 2019

Dear Sirs

My cover letter

This will create a letter and a legal document from one script.  All you have to do is run the Task in Visual Studio.

Another heading

This letter can have headings at any stage.  In the body of the letter, anything that looks like a heading will be numbered.  

If I want a tabulated list, like lawyers sometimes do, I include a colon: then it will create a new item after the next semicolon; and automatically spread the text.

Notes feature

This is the easiest way to include or exclude notes for your docx files.  Just choose the Task with the notes option 
//to include these notes, or to exclude them.

Tiny files

The whole script for both these documents can be stored in any folder, or on github or whatever.
It is just 6000 bytes, but it's the equivalent of a 35k one page (compressed) Word document. 

Easy to find

The output folders will be in the same folder as you lmd files (or you can choose 'output' subfolder in Tasks)

Ability to make multiple documents

This is not limited to one docx output from the same .lmd (legal markdown) file.  if I want to generate more than one docx file from one text file, all I have to do is insert the -n- (new document) break and it will create the two documents at once.
These documents can also be in completely different styles - one a letter, the other a legal document.

In any case, have a nice day.

Regards

Craig

-n-SimpleDemoLegalDoc
meta:legaldoc
//These are notes on the document.
MEMO

Date: 20 December 2019.

Author: Craig.

Topic:	New legal work tools.

START HERE

Created 19.12.2019
Uses concept of 'grammatical' or 'context aware' markup to prepare styling, then
sends that on to the markup processor.
The basic rules for the legal document scheme are:
Less than 10 words, not the document name (-n-), not ending in full stop and no existing code at end
= heading.  If all capitals, then H1 otherwise H2.
Default paragraph is Indent1.  Default level for : ; lists (plain English) is H3.
Everything else requires explicit use of for markup.

By applying different rules (style schemes) you can generate different markup codes, 
which in turn specify different Word paragraphs, and so influence
The look of the document.

It makes sense to turn notes on or off at this stage, or at any stage of pipeline?

EFFICIENCIES

This process of encoding the text with as little annotation complication as possible means you can use simple text files for both preparation and publication.   They are much smaller than a full word-processor file, yet the same output can be produced.  The program that makes this possible is current around 120 kilobytes (or about 4 paged Word document in size).

This illustrates an interesting point about encoding information, and utilising 
repeated processing of basic information.  e.g. a text file of 660 bytes contains enough information
to generate the content for a 32K word file.   That's a saving of around 5,000.   

Intelligent encoding schemes achieve outcomes that general compression algorithms cannot.  There are few compression algorithms that can do this?  A zipped Word document, for example, is ...

If we are satisfied that our text files actually contain more useful information (e.g. notes on preparation, content and so on), but are still smaller in size then our real savings are much greater.

The other advantage of test is that our source document material can be stored in ordinary code
version control systems, benefitting from tracking of the content and recovery of previous work stages.

Live Coding

If we could link the pipeline up so that it fed the updated text document directly into word, we'd see 'live coding' - the ability to produce a Word document with just a few keystrokes - even title pages.

We could do this in a browser by having it produce both 'intermediate markdown' and HTML at the same time.
This would be a pretty good approximation for what we see in Word.  The Word export is handled seamlessly.
So all we need is to be able to use a good javascript or php or some other language to generate the browser environment...(instead of text file and python alone.).

Will jupyter notebooks help?

Then if we can invoke the python code to get the Word output we are still there...

DO YOU LIKE PAGE BREAKS?
#PB

A page break can be inserted just with the hash-PB.

Plain English

If you wish to create a list broken up as plain English might recommend, then: you just include a semi-colon; and make sure you have good grammatical punctuation.

You can have longer lists, like: item 1; item 2; and item3.

Notes

//The ability to include notes in-context is a very useful form of knowledge management that allows information to be stored where it is needed most, without complicated systems.

The ease of turning notes off for final publication means you never have to spend time reworking the document.

Leveraging typing

One of the interesting assumptions about Word is that although it shows you WYSIWYG, it doesn't really

Have easy ways to leverage your typing efficiencies.  
What you really want is GMTYT - GET MORE THAN YOU TYPE.

Data awareness

Future improvements: the initial markup can include simple tags for data like dates (not just notes)

These can be processed before the application of styles.

Full Legal IDE

The goal will be to allow processing of the text file in such a way that it outdoes both Word and Google because it is suited to the needs of lawyers (in many ways not too dissimilar from programmers).   The difference is that lawyers could use something which infers the kind of styling from what they are typing (grammatical context), without the need for explicit marking up by the user (to avoid ambiguity, the program can do this in the background, so that by the time it comes to render, it is clear for every line/paragraph - especially since Word has the concept of paragraphs for everything, both sentences and sentences broken by punctuation like semi-colons.)

The backup of these files can be done through git.  This is good for record-keeping but it is also far more space efficient than Word docs (5000 times as small in some cases, because the program uses structural and grammatical information, which is a different type of encoding - already present in our language and conventions)

Repurposing code editors

If we can work mainly in text, then features of code editors (like highlighting, notes detection etc) can be utilised.  If we make the notes markings match common notes markings for code (e.g. the // and /* */ convention), then we instantly can use existing tools.  

Some may allow integration of the code (e.g. some 'Run' facility or integration with the 'Build' system), providing a GUI straight away (in which case, it is worth integrating the projects...?)

i.e. if the pipeline for working is similar to compilation (piping text data), then we may be able to work within that ...

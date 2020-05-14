# Threads and Conversations. (The "Text Weaver" Project)
(c) Craig Duncan 28.1.2020

# Aim of this note:

To bring several ideas together, the idea of including a markup category for 'notes' leads to the idea of functional mark language or similar, and requires some consideration of processing pipelines that transform text files into different file formats, including docx.

# Keywords

Digital humanities, legal markup languages, functional markup languages, data transforms, layouts and rendering.

# Defined need

Some of the goals of this project are relatively modest, but very useful

The defined need is for:
1.	 a simple and easy way to carry out data manipulation of text data in text files, where we define the text by different blocks or regions of information.   
2.	a way to make simple data substitutions in text documents; 
3.  a way to chain together these data transforms in a pipeline through to rendering
4. [sufficient confidence in ability to manipulate documents to rendering that the knowledge and precedents of a working office can be stored in relatively simple text files, on something like github server, and used to explain contract drafting as well]

We're looking for a simple language and algebra, but possibly one that can be achieved by implicit data structures and the application of programs that supply the operations (merge, sort etc).   This means minimal need for data preparation/cleaning by users, provided the context is known.  By allowing staged transforms, we can also decrease the need for complicated pre-determined logic. If we do chain the logic, then we have a simpler grammar for doing so.  (e.g. 'thread' logic - see below)

Why not have an interchange standard in something like XML?  cf NewsML.  

For now, I'm interested in the idea of a *fuzzy standard* i.e. one that can cope with how humans like to write, and recognises that in their own way, they already have structures, and the computation system can work them out.  *Maybe if we use the same markdown headings, level 1, we can process the same text together?  Or if we add annotations under a heading, we can make something a comment or a 'response'?  Or should we have different 'responses' that we can extract in different ways?


## Data manipulation/operations

We want to apply some of the basic operations that we would find in query languages like SQL, to the data structures found in some text documents, e.g. text versions of legal documents (even with minimal annotation);

## Data fields/types in text files

We want people to be more data-aware, without it becoming too strict.  

What are essentially "visual structures" in text documents are very useful (this is actually what distinguishes them from tables or RDBMS database schemes etc).  The more we can define these for our purposes, the more leverage we can get from existing structures (e.g. the flow of information defines what goes together...).  

The 'benefit' we get is that we can issue a direction or request to the computer like 'date sort this' and it will make some simple assumptions about how this is to be done (or you can tell it).  We aim to succeed in the simple data operations, then we deal separately with how we're going to handle the layout etc.  For most purposes, I'm going to assume that if we can handle data types, we already know enough to automate a lot of the layout questions.

Headings/topics are very often short sentences (not indented) ...we can exploit that on purpose.

e.g. putting dates (of any kind) on single lines above text, instead of within text, might be a useful structure.

This can be user-defined by simple markup or automatically detected.  It should also be possible to apply different data transforms in one or more steps by linking them together.  

Small input text file sizes can be compared to the 'resting' size of a docx program.  It illustrates the advantages of a staged pipeline with successive stages of translating from one format to another.

## Pipeline

Users can transform source files by utility programs without needing to see the intermediate functions

It should be possible to process a plain-ish text file through to docx.

## Barriers

Current markdown text processing or word processing pipelines offer few, if any, simple solutions.   Markdown is simple, but still focusses on layout and doesn't easily permit data categories (even notes/comments) to be define.  Word processor files involve complicated serialised versions of object-orientated software application data, and are not conducive to being an input (or even an output) of simple data-orientated text transforms.

Most users might not be too interested in the concepts and distinctions, but they are much more relevant to a text data scientist, and/or legal process optimiser, who wants to apply computing power to simple data tasks that only seem to be difficult because more complicated software design and application-specific file formats/conventions have got in the way.  They should also be of interest to someone who wants useful data-processing capabilities to be independent of the program chosen for final output or publication.   

To further complicate the software landscape, user-level applications in the legal software market have even used word-processing applications as the starting platform for simple data-manipulation (HotDocs).   These are truly domain-specific languages, sometimes requiring template-specific graphic user interfaces just for basic data insertions.  The substantive function of the templates, in some cases, is simply to make data substitutions.   The achievements of these programs are modest relative to the size of the application, the extra layer of complexity in file formats, and the interference with what are normally easier word-processing workflows. Working on data at the application-end of the pipeline seems a much less efficient exercise than doing data manipulation earlier using plain text files.

## Markup/markdown

In the early text stages of any data pipeline that works with plain text, CommonMark/Markdown is one of the options for introducing simple styling information (without needing embedded logic).  Markdown captures intention without needing any independent 'states' to be stored, although file meta-data approximates a record of state.  It was originally intended to help render HTML, by translating simpler encoding into more complex HTML.

However, this Markdown language does not devote much attention to classifying functional content like notes or authors, even for blocks of texts.  We therefore cannot reason about the inclusion or exclusion of notes using ordinary Markdown.

It is possible we could redefine the intent of the same Markdown encoding scheme, by changing what it does with a different parser.  e.g. an indent could be redefined to mean something else, instead of 'code text'.  Perhaps this is also convenient, by repurposing editors built for Markdown, in the short term.

## Operators for text manipulation that use text encoding schemes

What if, instead of generating HTML immediately, we wanted to do basic data operations on the text based on its content types (e.g. modify, merge, sort, filter or change layouts).

e.g. a program that can take two text files with dates inserted, and merged the text under each date, could be achieved with a single line like:

	mergedates file2 file2 output

or sort it by date order and output to another file:

	sort file1 output

My goal is to achieve this with the least amount of encoding within the stateless file formats.  Data types can be extracted into an intermediate database (which will then hold sequence, order or other attributes in a software system, but this does not need to be kept as a state: the final output has a new sequence, and the original document provides the content as a reference.)

## Serialised word processing file formats

At another level of complexity, word processors use file formats generated as serialised, object-orientated data structures designed to capture the state of visual representations of information on-screen.  They define the data structures solely by the goals of the software, not the potential data use cases of the users.  As a result, they are less easily interpreted in simple functional divisions.   

Also, the data structures do not assume that the sole or dominant form of encoding is associated with proposed data manipulation by the user.  They are data structures that for the most part are hidden from users and occur in-memory.  They are not a data format intended to be manipulated, or captured in independent form.  They are not even intended to be the final., sequenced output of the processing of any dynamic data representations.  

## Solutions at application level

Word-processing software and associated file structures impose their data structure, that achieves the final purpose, on the file format used from the beginning of the process, rather than the data structures and fields the user wants to use within their text (at the front end).  This is very restrictive, from a data processing point of view.  

A more flexible approach holds data in more general formats, that allows pre-processing of data, and then enables a suitable interface to the final rendering of data.   A less restrictive approach might use object-orientated approaches in-memory, but does not impose them when considering possible output formats for the text.   A helpful API would allow not merely a plain-text version of the document with no retained markup (as the 'clipboard' function does), but one that also retains some level of encoding that allows intelligent processing of the data.

# Repurposing VS Studio Code to help with these markup / text based workflows

See my separate article today : [Visual Studio](VSCodeConfig.md)

# Introducing the idea of conversations and threads

## Useful functional categories = ability to reason based on function

We need to study the different things people put into documents, and why, in order to increase the benefits of having that information in a computer.  If the computer can't work with distinctions in the type of data, you can't write functions or transformations that use those distinctions.  This is what computers do best, and they can do it fast and in bulk when you set up the problem correctly.

Most of the solution is recognising the problem.  The goal of keeping track of different threads in a text or markup document is itself going to provide a solution, even in a non-electronic world.  We're just aiming to give it a simple, elegant implementation that is easy to use.

## Conversations/threads vs 'notes'

Just talking about 'notes' isn't as useful as identifying the kinds of reasons we use notes, and how we use and prepare documents.  In a diverse text, notes are often responses to other things in the text (like a scrap of a lecture, a topic heading, a quote or some other initiating topic).   They are like conversations with ourselves, in that we are responding to textual stimuli already on the page.   In other cases, texts might capture separate conversations, like ordinary human conversation, or in a formal debate of some kind; a negotiation.

To me, it makes sense to view 'notes' as simply one example of the broader function of recording conversations and threads of related discussion.   This is one of the ways documents are used, and sometimes the sole reason for their preparation.

If conversations lend themselves to dividing up the content in a document, in sequence, with different authors, or purposes, they might be worth identifying in a text document as a fundamental data type (of the markup language).

Our aim is to:

- identify these conversations and threads (at least, those with independent authors) simply, by a minimal markup-language or similar;
- enable processing and manipulation of text documents, like sorting and filtering, based on source authors and categories; and
- to enable customised styling and layouts based on different source authors and functional categories. 

These aims can be contrasted to the more elaborate markup schemes that are used to embed mathematical operations in something like [MathML](https://www.w3.org/TR/REC-MathML/chap4_1.html)

As an example of some of the considerations that might go into making a new markup language, consider this [2013 example, by Michael Kay](https://www.balisage.net/Proceedings/vol10/html/Kay01/BalisageVol10-Kay01.html)

There is a useful overview of several different types of markup language [here](https://www.sciencedirect.com/topics/computer-science/markup-language).  A common theme seems to be that many derive from a desire to achieve tagging for print production.   There are more semantically-orientated languages, but data definitions, like in XML-based tags for tables, seem to involve fairly long strings (tags) to define each element of the data.  With a text document, I'd prefer to rely on the fairly established line breaks/spacing or other layout which defines the document itself, visually, as a kind of data structure.  The data structure is implicit, but predictable enough, we should be able to use it to manipulate documents through code.

If we can adopt some of the inherent structure in text documents for particular purposes, our attention can focus on more intelligent, computable ways to work with the information within it.  

# Context

## Visual representations of textual symbols

We are dealing with 'texts', which is a simple way of saying some record of symbols that have a conventional meaning, on a media that also involves conventions about placement and structure.

The human visual and cognitive system can attribute meaning to the placement of text, and other features of text.   We have written in this way for thousands of years.  Scrolls used a running spatial system in which text was written progressively, earliest first, and used symbols arranged on lines.  The implied order was obvious to those who had written the text, and to others they taught.

Loose paper pages provided another scheme for recording text, then they became bound in flat folios called books.

Word processors, discussed below, adopted a 'scrolling' 'window' (drawing upon two physical metaphors. 'Page' layout option became the third physical and visual metaphor. By using these familiar metaphors, or models for how it displayed visual information, the software did not have to do further interpretation: it leveraged what humans could already interpret visually.  Importantly, this included structural conventions in punctuation and paragraphs.

## 'Threads'

The context for this project is:
- documents are prepared as human records, and as such can involve more than one purpose, or information inserted at different times;
- a finished document may be a contribution of different sources, information recorded for different purposes, or a record of different tasks completed; and
- as a result, a finished document in traditional media may be an interwoven thread of text blocks, or authored text, in which the different purposes, authors and times are no longer obvious.  

Responsive text usually follows a proposition or sentence, or some source material.  This relies on the fact that most text documents, even in plain text, contain conventions that are releated to order and sequence (top to bottom, right to left etc).   It reflects the way we learn to process information visually and culturally.  People even apply this when making notes for themselves.

## Topics

Many conversations start with a particular topic, and we indicate a shift in topics by inserting new headings.

## Computer code and 'comments'

Computer code has used non-processed text regions to enable programmers to include comments.  The marked sections are ignored when the text is passed to the next program that intreprets its contents to turn them into an intermediate representation of information for the computer.  

From a functional point of view, it doesn't matter who the author is, because excluded text is concerned preventing that part of the text information reaching the next stage of processing. The excluded section could include any kind of text which is there for human reasons not for ultimate use by the computer.

## Notes

Notes is merely one type of functional annotation.  Seen in this way, 'notes' can be a response to a particular text, treating the original text as a conversation into which we insert our own responses: our own author's voice.  We could have more than one set of notes, in which more information is provided by different people.   The 'discussion' is, for some purposes, the most important element.  For other purposes, only the original thread of documentary material is always important.  A legal precedent is one such example.

Computer 'comments' sections in the computer code compiling pipeline are a possible source of inspiration for how to deal with comments in markdown (and some versions of markdown think of it this way).  However, to think of notes only as being 'excludable' may be too limited a view.  It might be useful to have different kinds of functional sections, which could be excluded or included, or styled differently, or filtered or sorted.  

# Legal documents as conversations and threads

Legal documents are refined versions of threaded conversations.   They might even just represent the end of the conversation, where both threads merge into a common statement of intention.  In other situations, some final statements remain more obviously in the tone or for the main purpose of one party, rather than the other. 

# Ways of identifying threads in text documents

## Old media

For convenience, old media used to put the responses (like a legal defence to a claim) in a separate document, because they were prepared afterwards.  Each author's contribution to the conversation was in a separate document.  The overall effect was as if there was one conversation, with each document being the author/actor's script of their contribution to the conversation. 

## Electronic media

The new electronic media offers the ability to amend the original document with its statements and insert the responses, to provide the integrated script for both participants.  In that case, all we need to do is allow insertion of the additional material (and, possibly, freeze the original content at that point).  If we can annotate each author's thread we can keep track of it and filter it as we want.

## Word processors

Word-processors also attempt to capture the different contributions and times of authoring documents by markup, which does not easily and simply capture the different contributions in a markup format.  There are some forensic advantages of taking these logs.

It also appears that most approaches to simple markup language creation have not taken into account these functional aspects of including the author.  It tends to be included as document-wide metadata, not an in-text attribute.  This makes certain assumptions about how documents are created.

Based on the assumption that documents are single-author creations, Word processors tend to work with representing responsive material as 'marginalised' text, in that comments or notes are often placed in small fonts, to the edge or bottom of the page.  However, this subtexting doesn't represent the flow or importance of many conversations, with ourselves or others:   
- Our notes may, for our own purposes, be just as important as the information they respond to.
- Legal submissions or pleadings require threaded conversations with responses of equal importance. 

Topics are caterered for in the sense that headings that have already had styles associated with them may be visible in an outline mode.  They are not denotated as 'topics' per se; this is implied to the reader by normal writing convetions.  This outline feature is also found in code or text editors that allow 'fold-ups' of lines of text.

Neither word processors nor markup languages have an easy method for pre-processing data and variables into documents prepared for layout purposes.  This ought to be an easily-achieved transformation function.

## Collaboration documents

Documents in tbe Google Drive system perhaps offer a better indication of who the author was, as might git.  This is because there is a platform that handles author identification (and holds it as a state).

With stateless systems, like markdown text, we have to provide some method of indicating who included the text.  That is, unless we can borrow some indication of state from the operating system and use this for inclusion (i.e. if you have a git program, it might do this without you even thinking about it). Nonetheless, such systems tend not to be explicit to allow discrete utility programs to work with that information.

## Social Media

Social media is big on threads, in fact many of the platforms like Twitter are based on providing convenient representations of sequences of text, and keeping the data structures necessary for doing so hidden from the users.   The block-style creation of text is an example of paying explicit attention to who is adding to the total flow of information.

This is what is needed on a document scale, but we also require something that doesn't involve a proprietary, enterprise-level solution to get the job done.  We really only require some simple level of annotation.   

## Computer code

The use of '//' line comments in computer programming is one example of a simple way to indicate a functional difference in the information that follows.However, it is a single category, rather than offering multiple options.  Can we extend this in some way?

## Content management (Wordpress)

Wordpress has recently opted for a block-style scheme which is closer to social media conversation units, in that the state of smaller units of text is held as a block, and different classes of block (quote, text, etc) can be applied to categorise that text.  It is unclear whether this has the capacity to record different authors, or work easily with it.  It does represent, however, an example of a non word processor, non social media application where data structures apply to specific document contents.

# Stateful or stateless computation

One of the main differences between markdown or markup and text edited within a specific software application is that there is no 'state', other than what might be modified by the stream of information in the document.

This stateless document (like traditional physical media), tends to increase the level of annotation needed to record additional information, for example if you are interested in capturing the source of information from varied sources.  If you assume that a document's text only has one author, you just indicate the author once, and that is taken care of.  If you want to identify which components are authored by different people, you either need an implicit test for who the author is (e.g. using a novel word each time), or you need to explicitly identify the parts of the text authored by each person.

Markup schemes that are inherently simple only pay attention to those things for which you want the state to vary (which for layout schemes, are things like headings, font styling rather than functional parts of the document).  It is relatively easy to think of computer programs as defining a few keywords, import statements and functions, and comments.  These functional divisions are automatically identified by examining the text, but rely on distinguishing characters or words to indicate them.

On the other hand, creating systems or platforms that hold 'state' can represent labour-saving systems for the task of annotating or recording the state in this 'stateless' data format.  For example, if the system holds details of the author, it might hold that information in-memory, and then write it to a more detailed file as and when needed.  The user, however, might not have to worry about seeing that in the raw annotated file.  The indirect representation of state (e.g. by colour etc) is done by encoding the state for each observation invisibly, then presenting only those aspects to the user that are needed.  

Another example is a cricket scorer that keeps the state of each ball of the match in memory and records it all, whilst requiring the user only to indicate ball by ball changes in state.   The scoring system might reflect current state, then accept input from the user to confirm that this state should be the one entered into the system.  The system holding state, if it has access to the log (historical data), might even be able to anticipate changes in state (e.g. the result of the last ball might allow the system to change the batter on strike for the next ball, without the user having to do it).

There must be a balancing point at which the effort in introducing more explicit annotation to a stateless information scheme is slightly outweighed by the convenience of running a program (e.g. in a text-editing program), whilst editing data, to hold state, in order to save the user having to expressly annotate every feature in the source file.  This is the point at which more complex software use-cases begin.  There are many text-editors for coders which make it appear that plain text encoding is being carried out, but additional features, based on holding state, and interpreting the contents of the files, are being done.  (Even the 'fold-up' option in something like 'Visual Code Studio' is a result of holding the changing the 'state' of what is visible from a particular line in the text file, even though based on the simpler annotations in the content).

The holding of a 'state' can occur in different types of interfaces.  FoOr some, the idea of a 'mode' is associated with a change of state.  For example, a program that appears to be the same for all users may still have a 'mode' setting to indicate who the author is, enabling content modified whilst in that mode to be associated with a particular author (or, in simpler cases, to associate any paragraph modified whilst in a particular mode with the last author).  The program could provide feedback on which paragraphs are associated with a particular author by showing a particular colour in the margin, or an annotation etc.   The same scheme of 'modes' could be used to specify a different purpose to the work being done (e.g. editing in 'notes' mode creates notes blocks, editing in 'defence' mode creates new paragraphs categorised as 'defence').  It might also be associated with restrictions on editing previous content associated with a previous author or function (e.g. non-notes cannot be edited whilst in notes mode; 'claim' paragraphs can't be edited whilst in 'defence' mode).   

A more complex state-storing idea is that a 'mode' could indicate the date or event being worked on, in different domains.  So a person working in a particular date mode (in addition to setting the 'author' state, might be able to modify a witness statement that applies to that date, whilst also doing the same in a different statement, in order to tie the two together.   If the working interface stores this state across different work domains, then it enables the link to be made later.  

# Recording state when merging different information

One example of where state can be noted, without placing the burden on individual authors, is where a document is authored for an explicit purpose, and then merged with another document.  In that case, the system can recognise the different sources, and write in explicit 'state' information in to the merged file format.

One of the goals of a simple marking language for distinguishing notes in a text document was to include notes without requiring cross-referencing (i.e. it relies on the flow of text in the document, and the fact that the notes appear in-text, if at all, to provide context and meaning.   To merge different notes from different sources requires each separate application identify the relevant content consistently, so as to insert the notes at an appropriate point.  Collaborative text programs must already do this to some degree.

Does Google Drive/Google Docs, for example, record the information in such a way that if there is more than one 'defence' to a statement of claim, that each author's response could appear in context, underneath the original paragraph?   In order to consider this, we've had to move away from a specific word processing application, looking for a suitable function.  

Such a system might be able to define functional types of text, but for limited purposes only, because there is a suitable convention and we can treat the identity of the author and the purpose as a single category (e.g. author 2 is, in that context, making responsive notes or a defence).  However, if we want to trade in combinations of both author and purpose, in a single document, then we need the ability to specify our own useful purposes for including text (not just rely on what states, like author, the system is recording).

--Purposeful text annotation; or recording of the reason for including parts of a document, as a specific state for that part of the document.

# Stateful or stateless working methods in legal contexts

In an even more complex situation, if transcript-writers, or trascript processors, can indicate the 'state' that evidence relates to, it can then be associated with the same events.   Some degree of automated transcript parsing and categorisation of text contents may be possible if there are, even in the current transcript-writing conventions, sufficient data to introduce a further file format to categorise state in the transcript.   

Current methods of writing cross-references into text would not be as useful as being able to tag regions, or blocks of text.  Perhaps some of the litigation-assisting technologies enable a degree of issue-tagging, but people would need to know it exists, and how to integrate it into other workflows, to use it properly.   Can it also be used to tag conventional WP documents as well?  i.e. the recording of 'state' across all work in a case is a useful exercise, but requires additional work, and if it involves steps after the documents are prepared, would seem to be wasteful.  

It would be useful if witness statements could be written inside an application that can already tie them to a central set of events that indicate the category that information belongs to.  Even if simple dates on a line could be read into a separate category field in a date format, that would allow sorting of the information.}

On the other hand, even some stateless schemes, like HTML, have benefitted from other simpler encoding systems which allow rule-based processing to automate the more sophisticated specification, and save the user some effort.  This pre-processing involves cruder definitions or simple grammar than the HTML language might permit, but in many cases that is all that is required.

# Functional formats or languages

A functional language for marking text documents may be neither a layout language, nor a complete ontological scheme.  Its purpose is to enable independent filtering or automated formatting of text by function or source.  This also makes it suitable as a pre-processing language for markup or markdown languages (including both Markdown and OpenOfficeXML) that are more concerned with layout and presentation.

## Thoughts about successful markdown/markup schemes

### The pros/cons of explicit markup

When will a designed form of encoding, for example a markup/markdown specification, be considered optimal or attractive?  I believe the efficacy of such a scheme works if it doesn't require too much effort to encode relative to the effect on the visual representation of the data.  I think it comes back to subjective human valuations of the effort of using any kind of encoding.  

People are conditioned to think typing is worthwhile, because it is so precise.  They are very happy when it seems that they are just typing, and the actual encoding of the state associated with text, to allow style or layout, is almost completely hidden from them.  This is a large factor in Microsoft Word's success - it hides layout encoding, and layout was primarily what people who were working on text documents were interested in.   They were less concerned with the function of information (and all the inefficient processes that went with trying to collate information related to the same function, even with the existence of word-processors).  The price for this is a large software application, and large files that do not transform plain text with encoding into something more complex.  Word was written without a desire for a multi-stage transformation pipeline.  It was not designed to be modular between simple input and rendered layout.

What about another layer of encoding on plain text, in which something like layout or content is expressly encoded to enable machine processing?  The human author is happy if the encoding doesn't feel like a waste of time, based on conventions that might even be unconscious.  If I have to keep marking up paragraphs as authored by me, it will feel superfluous, even if I know that later it might enable some filtering.  The 'might' is not enough motivation, in general (but may be for some things).   This is less likely to be a problem when we encode function if we also achieve the purpose of visual encoding as well.  

Here's another example.  In plain text documents, we do not need to put a hash (#) to indicate a title, if the computer could recognise that for us.  Most people using CommonMark, or Markdown do it because it seems like we get both a visual and a computer-recognisable encoding for a small price.  

Another example: if you can indent a text block, the visual representation changes. (In Markdown this is associated with a layout, e.g. for code, rather than a function, but you could regard it as both a layout and a category). 

Markdown's code system can be considered efficient if you have a finite set of functions, or you agree with the designer's prioritisation.  But what if you want to redefine the meaning of the layout/punctuation that is interpreted?  What if you want code to mean 'notes'?

If you also use that to define notes or quotes (according to your preference), then you can transform this into a layout markup downstream, without the user caring or knowing about it.  Your visual/structural encoding then becomes a symbolic encoding.  This relies on a computer being able to efficiently detect and transform the indented blocks.

### Other schemes

At the moment, there are some conventional design decisions being made about what to do in order to improve the ability to work with text or its contents:

- explicit markup
- record state within a stateful application; hide everything (use internal markup scheme, like OOXML, if required)
- use automated look-ups and search to 'find' text, prompt for substitutions (computer aided review)

To this, I believe we need to add: solving specific problems, in a particular context, by using computing to reduce our need to use explicit markup schemes, manuall encoded.

# Reducing the need for manual encoding schemes

Some practical questions I'd like to answer:

 - How do we lessen the burden for our ultimate task?
 - How to we avoid needing human labour to include explicit markup to identify the important functional information?
 - Can we identify different authors or functions of text just from the document? 
- Can we introduce an intermediate/explicit markup that helps simplify the programs that will transform the text for subsequent processing stages?

The more specific our context, the more this might be possible.  One of the assumptions of AI or machine learning or even expert reasoning is that we can build general reasoning systems using our existing programming languages.  For present, we might do better putting that to one side, and create solutions/tools for specific purposes.  

One way to break apart larger problems is to turn them into simler ones.   Arranging data transforms in stages can be a productive method of doing so.  We create data transform tools that operate on specific information, but then produce a more general solution that can use more general tools.  Such tools also lend themselves to individual use and flexibility, rather than monolithic enterprise solutions.

## Litigation documents with multiple authors; recognising the function of the parts of the text

Let's say we want to prepare a document that needs no cross-referencing because our response is immediately under the statement we are responding to.  We rely on visual layout to help us separate the aggregated data.  Can we achieve this and still be able to filter the information?

For example, if someone has written a document in which they have provided their response (in the form of a 'defence') to a statement of claim, just by writing their responses and/or notes following the relevant text in the original document (e.g. in a markdown file), how do we retain the ability to identify the new information, with minimal effort?

There is more than one way to achieve this, in a computing sense

### Differential approach

Staged differentiation (automatically comparing versions of a document) is one way.  We keep the original document as the base, then prepare the additional text.  The computer then selects function by difference.  If we approach this in stages, we can keep track of each version's functional differences (in a stateful system, we could just switch to different modes, in order to work on the amended documents).   For this to work easily, we'd have to work on different text independently (i.e. not varying the text that is in another functional mode, so there are no overlaps and we can access them in any order).

The visual benefits we want to retain are being able to see the text from the previous version, so that we do not have to keep manually looking from one place to another, or introducing any other cross-referencing scheme.

We might save effort for the second author in this way:

- apply an automated encoding of the first file (i.e. markup the text that was received); and
- thereby allow the next person's additions, without markup, to be the differentiated text.
(we can do this in successive stages)

We might also be able to distinguish between the substantive defensive text and notes by having the second user encode the notes with //, thereby allowing the rest of the text to be treated as the substantive content.

### More semantic approaches

This staged 'differential' approach simplifies the need for simultaneously distinguishing different sources, and reflects the 'conversation' better.   However, there may be other more semantic methods.  FOr example, if we wanted to explicitly markup text for a particular function, perhaps there would be features of a defence, or 'prefatory words' that help distinguish it e.g. "As to paragraph ... of the claim,..." or "As to topic X of the claim...". or even "the Second Respondent says..." (which helps identify the text as being a statement of a particular respondent, to the claim).  It may help that much of legal conversation is written in this formal way, with explicit attention to who is saying something (a kind of formal speech we wouldn't find in ordinary conversation)

# Document transform pipelines

## Stateless stages in processing pipelines

If the processing of functional encoding also results in a stateless format, then it also provides a seamless transformation stage between unannotated text and markdown languages.

## Notes on the usefulness of OOP/OOXML

The use of OOXML is a stateless representation, but that does not mean it assumes a mostly stateful, computer-assisted environment for the creation of OOXML.   OOXML is hardly human-readable for the average user.  

OOXML is not a consumer or user-level markup scheme. OOXML is human-readable to a programmer or developer that is very invested in learning it.  It also comes in an object-orientated environment, and working with it involves programming languages that are built very heavily on the same object-orientated mindset.   The programmers are so full of the implied and predetermined data structures for hiding layouts in the Word application, that they can barely think any differently, or at any different level of abstraction. 

To prepare OOXML by hand would be a serious case of losing sight of the trees for the forest.  Developers who work with OOXML are drawn into the same world of OOP and working with enterprise-level assumptions about the use of a stateful software application.   They frequently deal in the minutiae of how to encode state into the layout of text at the paragraph level - an effort which can hardly pay off if you are designing many different, short templates, or want to flexibly change the contents of the documents.  For this reason, many of the examples seem to be high-use, static templates, in which the text doesn't change very often.

## Using OOXML in a data transformation pipeline

To get from plain text to docx, for example, you basically have to produce an intermediate OOXML document, to hold the 'state' of the main body of information that the software readers of docx will refer to.  

There will be more than one xml document required, because the final 'state' cannot be held in the document.xml file alone.  One of the complications of OOXML is that it assumes that there is a complex, stateful application generating it and reading it, rather than the simple parsing or translation of a single text document with a self-contained markup language.  

XML need not refer to a layout scheme at all, but the OOXML specification is mainly based on defining regions of a document so as to best define both the content and then directly (without abstraction) specify layout.  

OOXML arose out of the development of a stateful software application, which clearly influences its design.   OOXML is not really a general data processing format, or conducive to processing of data as text.  It is more precisely described as a 'serialisation' representation of an Object-Orientated data structure, created in a stateful software application for the purpose of visual representation.   As such, data is always encoded in a scheme of repeated 'instances' of data objects, rather than a tabular data structure of observations.

The level of abstraction for OOXML data, being object based, is not based on fields within observations.  Abstraction occurs at the level of the kinds of containers that hold textual layout elements, and whose state can be manipulated through the program.  It defines a system of data objects that repeatedly occur, like paragraphs, as units of the information.  As a result, OOXML does not easily lend itself to simple data transformations and stand-alone open source programs that can easily reason about the data structures to use.  There are layers of 'state' in OOXML that are based on the assumption that the information will primarily be used to layout and render the text for output on screen. 

OOXML does not assume that a sequential or abstract approach to building up that final rendered state, from a simple plain text representation: it rather assumes that all layout elements will be simultaneously used for rendering without concern for resulting modularity (or fragmentation) of the OOXML representation.  It was built to process individual objects (paragraph or table units, or objects within objects), rather than bulk-processing of particular kinds of data.   It does not use a modular or pipeline approach to rendering (as might be the case with OpenGL for example?). There are no 'shader' programs here?

There is no easy way to work on a OOXML and introduce a scheme for classifying content as by a particular author, or for a particular purpose.   Most classification functions assume that a person will have to style something in a particular way so as to classify it (e.g. the Heading1 style is used for outline mode.  In reverse, a '#'' in Markdown is often used to translate content into Heading1 style).   What OOXML does not encourage (because objects and layout are inherently bound together) is an intermediate level of encoding in which attributes of text can be added without concern for ultimate layout, at that stage.   The custom data types allowed for in the specification for OOXML are there on the assumption that they can only be accessed easily, or at all, through a stateful software application (i.e. for visual representation), not for some independent and general processing of the file format itself.  

There are few shortcuts with OOXML, if you want to use it as part of a data transformation pipeline, but I've done some work to overcome these difficulties.  If you want to transform text into OOXML easily, from a different type of stateless encoding, you need to make quite a few assumptions about the style and layout 'states' that you want to treat as constants for automated transforms into OOXML.   If you do this, you can create a pipeline in which simple markup schemes can be translated into OOXML (and then, in turn, into a docx document if that is your goal)

There are ways to avoid having to build the system inside a .NET or OOP environment, or with C# or another OOP language, but this is mostly discouraged by the makers of Microsoft Word, even though they have suggested OOXML is an open standard.

# Markup and conditional schemes at the application level

At another level of difficult entirely is a 'markup' scheme, on top of word processor representations of text, that is itself the input text for conditional logic, or possibly even a computer language.  It's hidden from the user that the superficial logic part of that markup has to be extracted and made 'contiguous' and removed entirely from the word processing context (it's inclusion in the docx or rtf format is purely for convenience to the user).  Such a scheme operates on top of an elaborate software program already designed to hide layout.  Ironically, the document assembly program does not attempt to 'hide' itself, but it might operate on the assumption that there will be user interfaces built that will hide both the content and how it is modified.  Its best use case is when there is hardly any change to information or systems.   It is rigid, and makes business sense in a rigid workplace.  That is because there is no clear separation of logic, layout and text.  The real 'input' is a hybrid of code and text, not a plain text document anymore, and to hide it you also need to construct custom interfaces.  For solicitors that want to work on actual content, and rearrange structure often, this system is an incredible burden, and will often force re-evaluation of the logical encoding from scratch.  The amount of effort to insert variables into a word processing text is quite high cmpoared to the effort that should be required to do so using simple computing languages operating on plain text.

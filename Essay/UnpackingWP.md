
# Unpacking word processing: how and what do we want to store in more efficient data structures?
Craig Duncan
22.1.2020

Our goal is to store legal information efficiently.  For present purposes, that means in the least space, but also in the leanest way that allows automation of the subsequent steps for different and varied output and reporting purposes.

In order to do this, we have to unpack many things that are current conventions caused by both the norms for legal drafting and the assumptions about how word processing tools will be used, leading to further dependencies that are built into the design assumptions.

This includes:

1.  'plain english' has invited legal drafters to adopt visual breaks in sentences (semi-colons, vertical separation aka 'tabulation'), which may provide logical divisions but they do not remove the need to read the whole sentence, in order to acquire the meaning of the whole sentence.    This is a sentence-level re-arrangement of the appearance of text which can be captured in a more traditional sentence structure by removing line breaks (these can be re-inserted if necessary, by algorithms).   

2.  Word processing features have been developed so that the default concept of a line break (new paragraph) is used for the plain-English inspired tabulation. These broken sentences are visually displayed by the Word Processor as a new vertical paragraph (text block). Similar styles are used to make them look, visually, connected to the neighbouring list items, and to distinguish them from the prefatory part of the sentence.  However, the Word processor's text blocks are all 'paragraphs', so that the data is internally stored based on the data needed for the visual layout/representation, rather than being linked to any data container (that would need to include the whole sentence and the parts into which it has been fragmented). 

3.  Groups of individual sentences that relate to the same topic are often given a lower heading 'level' and different styling or numbers.  This is a structural/visual navigation change.  In the word processor there is no connection, in a data sense, to neighbouring content. 

4.  Writers can use internal references to Word Processor-enabled numbering.  This adds a complication: the text is self-consciously written to be dependent on the current appearance and styles used for the document.  Despite there being no actual container to hold all the contents of a 'clause' or numbered item, the document will display references to the current numbering level of the other text that has been bookmarked.  In turn, self-updating features for cross-referencing in word processors encourage people to do so without fear that they will have to re-do the references, rather than avoid them altogether.  This is processed as an 'update' because the Word Processor is not, in fact, holding dynamic linked references in its paragraph meta-data.

From this it is apparent that to achieve computational control of these various elements, and to allow structural scaffolding and navigation ability, containers or indexes must exist so that text blocks and sentences can be linked to the hierarchical data structures that are routinely created by visual divisions in the document, apparent to human readers but not necessarily reflected in the word processing functions.  

*In other words, we need a way of structuring the data that is otherwise held in word processed documents.  It's almost an exact parallel to the goals for the pages of the internet in the 'Semantic Web' scheme.  (see schema.org and https://en.wikipedia.org/wiki/Semantic_Web)*   
nb references to schema.org in web sites are a reflection of some attempt to include semantic schemes?   See, for example, WordPress websites etc.  cf https://en.wikipedia.org/wiki/Computational_semantics. (This refers to an article by Blackburn: unfortunately, as soon as people say 'computational' they seem to require first-order logical representations and complexity, instead of just providing a data repository for library purposes, which for law might be useful for its own sake).   Semantic Web founders include Tim Berners Lee and James Hendler (Hendler's research interests[3][4] are in the semantic web[1][5] and artificial intelligence.[6][7]). (see also http://www.cs.cmu.edu/~softagents/DamlPaper/DAML-S/daml-s.pdf)

##. 

Consider this observation:
"The Semantic Web is not different from the World Wide Web. It is an enhancement that gives the Web far greater utility. It comes to life when people immersed in a certain field or vocation, whether it be genetic research or hip-hop music, agree on common schemes for representing information they care about. As more groups develop these taxonomies, Semantic Web tools allow them to link their schemes and translate their terms, gradually expanding the number of people and communities whose Web software can understand one another automatically." (http://www.thefigtrees.net/lee/sw/sciam/semantic-web-in-action; accessed 22 January 2020)

The additional requirement, for the present project, is that we want to take the text outside the word processing environment, as well as introduce data structures for semantic encoding (or at least, for being able to introduce some data fields to capture information).

## Semantic markup

A semantic markup scheme could be achieved by an XML scheme (this is what Tim Berners Lee and W3C originally had in mind for the 'semantic web'?), or some other text-based encoding.   

Once semantic meaning is marked up, it allows manipulation of semantically similar data, or application of stylistic information using automated functions.  Even plain English tabulation could be effected automatically, using repeatable functions.   

As compared to current Word processing files, these markup schemes are lean and simple.  They follow a different philosophy to OpenOfficeXML which is based on an ontology based around rendering of text blocks, without concern for which parts are related in meaning or purpose.   The encoding of semantic meaning still permits automated styling and content insertion for creation of word processing documents.

The data saving in preparing templates this way is enormous: 5000 times in some cases!  This kind of increase in efficiency is not the result of compression of random information per se, but identifying the absence of structured encoding.   Implicit in Word processing 'storage' is the assumption that each document will be manually and specifically arranged with its visual structure, precisely because of the absence of any concern for abstract representation of the structure of information.

## Criticisms of semantic markup schemes, in general

The implications of realising this scheme are that much information buried in docx format can be maintained as simple text information and exchanged over the internet, knowing it will slot into familiar structures.

This was also the dream of the Semantic Web, but the voluntary classification process was torched by Cory Doctorow (blogger) and others (see https://twobithistory.org/2018/05/27/semantic-web.html).  

The same article referred to protracted efforts to develop standards like RDF, and these made use of onotologies, defined in the article as "explicit specifications of what can and cannot be said within a specific domain."  Wiki for Semantic Web mentions RDF in this way: "To enable the encoding of semantics with the data, technologies such as Resource Description Framework (RDF)[2] and Web Ontology Language (OWL)[3] are used."

That doesn't mean it can't be revived in situations that call for it, or are essentially working with semantic information but haven't made it explicit to computers.  However, the main objection is that the alternatives are a lot easier to understand (and this includes the current paradigm of just using search engines).

The same arguments can be made for going to the trouble of introducing semantic schemes for legal documents.   Who will bother, and will it be worth it?

This is essentially one of the main obstacles, and lack of motivation, for doing anything about the capture of meaning (or even just plain old data structures) inside word processor documents.   Few can be bothered setting up and administering databases or separate text files to make the text itself the data, because they are happy to just type up the documents and hold the structure in a human-readable way.  They do see the benefit in combining templates with bulk inserts of addresses for mail-outs, but few other applications have leaped out.  Unless the extra effort to make the computer aware of the kinds of data that are included pays off in additional benefits, there is no obvious innovation here.

## Semantic web legacy

It should be noted that some of the semantic web project has forked in a different direction as "schema.org vocabularies, together with JSON-LD, are now used to drive features like Google’s Knowledge Graph."  and this: "What wasn’t possible in 2001 now is: You can easily build applications that make use of data from across the web. The difference is that you must sign up for each API one by one beforehand, which in addition to being wearisome also gives whoever hosts the API enormous control over how you access their data."  It also warns that Facebook's OpenGraph is something that has some semantic qualities, but it's still something that resides within Facebook's architecture, rather than underpinning the web as a whole.  And "why these technologies have succeeded and continue to be popular" is said to be because "Nobody wants to use a tool that can only be fully understood by reading a whole family of specifications."

## Schema and JSON-LD is taking off

https://www.3whitehats.co.nz/knowledge/guide-to-structured-data-seo/

Some of the Google boxes etc are using information that is being put into websites as 'structured data'

There is a small library of search engine contexts that peopl eare encouraged to insert structured data for:
Breadcrumbs
Local Business
Books

(also: Get eye catching results in search engines with the most popular schema markup plugin. Easy implementation of schema types like Review, Events, Recipes, Article, Products, Services etc
https://github.com/brainstormforce/all-in-one-schemaorg-rich-snippets)

What we need to do is to make legal documents this kind of document.  i.e. we put notes in as structured data, so that what you 'see' can be the final document, or you can replace the view with your content and notes, or you can see 'related' libraries which have similar data.

Does it rely on centralised schema?

Maybe.  If you start it, you can share.

Delivery?

On a page, with a docx output button on every page?  Written in...?

```
<script type='application/ld+json'>
	{
 
"@context": "http://schema.org",
 
"@type": "BreadcrumbList",

	The schema @type allows you to set things for the web.
	In our case, we can set @type to something like a type of document (e.g. lease) and then populate each clause inside it.
	This is an alternative to putting it in Word.
	Then we have general access to the data etc.
	We can read off JSON?

</script>
```
https://www.3whitehats.co.nz/knowledge/guide-to-structured-data-seo/
Schema is a collection of vocabularies that determine how the structured data in your website looks to search engines. To describe it simply, it is an agreed upon set of tags (microdata) that can be added to websites in order to improve the way search engines find and display your page on search results. Schema is a collaboration between Google, Bing, Yandex and Yahoo to come up with a universally recognised collection of tags so that information can be shared and re-used in different environments.

 Microdata is a way to tag certain elements of a page and inform search engines what they are. So, if you see a rich search result that includes a publication date, an author’s name or a product price – all of these are individual pieces of microdata. In this sense, you might say that pieces of microdata are used by schema to determine what is displayed on search results page listing.

 Microformats are another way of marking up structured data through, but unlike schema it is done by an open community process. Schema is the newer standard, but that doesn’t mean microformats are obsolete. Instead, they rely on HTML attribute tags to provide information about certain types of content.

 ...
 "JSON-LD (JavaScript Object Notation for Linked Data) is a linked data format that uses vocabularies such as schema.org to read and write structured data. Essentially, JSON-LD can be used to send information to search engines using semantic web technologies.

 Many web developers use JSON-LD because it doesn’t require any alteration to HTML code. It can simply be inserted into the site without disrupting anything, and used to send your structured data information to search engines.

 A simple way to look at it – structured data is the actual content you want search engines to see. JSON-LD is a way to get that information to the search engine.

Is Open Graph Structured Data? And What About Twitter Cards?
Open Graph could be considered a type of structured data, however not so much in the way we’ve been discussing. Our main focus has been how search engines use structured data to interact with websites. Open Graph is more related to social media."

## An interesting approach - but it's just Jekyll

This website (codemopolitan.com) includes script (javascript?) in which every single web page is defined in JSON variables.  i.e. the pages are hard coded.  Presumably, this also gets picked up by search engines.

It is data structure, with ID and body.   A possible template for writing legal docs too?
What's interesting is that the markup is VERY close to a punctuation (minimalist) scheme, in that it can distinguish between quotes, headings with very subtle differences.  Camel case seems to be associated with headings.   Quoted sections are hard to pick, maybe a double space.  Colons are used to indicate...  What is this?  Custom mark up or something?
Nope: the generator is Jekyll, and what it seems to do is place a list of all main document pages at the start, and then for each page, it will copy in the relevant HTML at the bottom.  Possibly useful for static pages, web search etc.  But what it is not doing is grammatical text parsing.

view-source:https://www.codemopolitan.com/development/

Author:  twitter.com/ctrlshifti

```
<script>
$(function() {
    $("#lunrsearchresults").on('click', '#btnx', function () {
        $('#lunrsearchresults').hide( 1000 );
        $( "body" ).removeClass( "modal-open" );
    });
});
    

var documents = [{
    "id": 0,
    "url": "https://www.codemopolitan.com/404/",
    "title": "",
    "body": " 404 Page not found :(  The requested page could not be found. "
    }, {
    "id": 1,
    "url": "https://www.codemopolitan.com/about/",
    "title": "About",
    "body": "              About:                 Oh, hi there! I'm loving what you did with your hair. Would you like some tea? Mimosa maybe?         Thanks for stopping by. I'm Kat, a full-time computer engineering student and infosec consultant. When I'm not studying or working, I run Codemopolitan and write tech jokes on Twitter. If you have any enquiries about the site, feel free to direct them there!             "
    },
</script>
```

## Tools the corporates are providing for non-coders to work with structured data

caution:
https://www.alexhudson.com/2020/01/13/the-no-code-delusion/

A web-based tool that converts information to the schema:
https://hallanalysis.com/json-ld-generator/

dwarfish: https://twitter.com/joehall
he says he's a postmodern developer:
"Using a flexible approach to SEO, Joe is able to craft highly aggressive SEO strategies that mitigate risk and ignore elements that aren’t going to increase the client’s ROI. Joe’s goal with each client is for them to reach their desired goal as quickly as possible with minimum budget allocation."

"Joe doesn’t use a basic marketing checklist, or free seo tools. His primary consulting product is a custom, advanced SEO audit that goes beyond looking for common seo errors, and develops a custom unbiased strategy to ranking."

https://hallanalysis.com/about/

Why not have a similar feature for generating legal markup?
i.e. it does grammatical analysis, then adds the markup for you?  Clause by clause.

## Less obstacles for legal documents than the web in general

To some degree, the goal of being able to meaningfully prepare semantic containers for information in legal documents involves preparing a legal knowledge graph, with information about the contents of certain classes of documents providing a higher-level way of defining the 'grammar' of information (reflecting legal language anyway).   If such a grammar helps with a general scheme, then it permits information sharing using these boxes.  This is a narrower, and possibly more achievable goal than the specifications to make the Semantic Web work.  

We have to suggest that the 'cognitive overhead' has, in part, already been invested because of the familiar ways in which knowledge for legal agreements has been embedded and incorporated into legal documents. i.e. part of the legal 'corpus' of knowledge of most lawyers is a knowledge of ontologies: structures or patterns of topics that are present in legal documents (agreements) of certain classes.   {*This gives rise to the possibility we could have a computer automatically learn these ontologies by being given access to training samples of documents which it can both automatically classify, using an independent scheme, and then analyse for the structural content*. i.e. two pass machine learning allows automatic tagging and learning of new information?}

This idea of having tools to acquire or record an existing semantic structure, at least in part, gives rise to the idea of a 'structural' document editor, that can create scaffolds, containers and sub-boxes inside documents (*with reference to semantic content, or topics*), without losing the hierarchical scheme.    That also allows:
1.  precise referencing to substantive content by topic (the containers at first level of the semantic scheme for documents)
2.  replacement of such content as a whole or for individual items.

## Overcoming these criticisms

One approach that I think is worth considering as a partial solution to these criticisms is asking computers to prepare the semantic schema, not as a one off search which is implicitly repeated by many people at different times, but something that thereafter allows the structure to be used.  

This is 'search+structure', a potentially new way of looking at the potential for machines to do some of the tasks that would once have been left to clerks.  Those tasks were still useful because the people working higher in the business could thereafter use the product of the work, and its organisation achieved an encoding that was useful.  The difference between chaos and order.   Search favours those who are too lazy to be organised, who want to find things, but who also might not appreciated that organisation has its own merits which outlast the initial effort to achieve it.

This enables content compression by symbolic representation, and symbolic manipulation of the contents of the document (an algebra).  

#!/usr/bin/env python
# above shebang line is to make sure we can execute this in python
# the 'env' program is used to allow it to find the python executable in the PATH
#
# This program will create OOXML content and .docx files from Styled Markup Language (SML) files
# and an appropriate template.
#
# The name 'Styled Markup Language' and this implementation (c) Craig Duncan
# Created 31 August 2019 by Craig Duncan
# (c) Craig Duncan 2019-2020


import xmlutil
import sys # for processing command line args
import csv # library for simple csv reading
import sqlite3 # to store our test text in a database


def makeNewDocBody(content):
    opentag="<w:body>"
    closetag="</w:body>"
    newbody=opentag+content+closetag
    return newbody

# function for a merge by swapping out the body of the old doc and the assembled <body> from script.  TO DO: unit tests
def docBodySwap(newstring,templatestring):
    opentag="<w:body>"
    closetag="</w:body>"
    libbody=xmlutil.getTagListInclusive(templatestring,opentag,closetag)
    oldbodystring=libbody[0] # 1 entry
    recbody=xmlutil.getTagListInclusive(newstring,opentag,closetag)
    rpstring=recbody[0] # 1 entry
    # replace the whole of the body part of olddocxstring with body part of rpstring
    result = templatestring.replace(oldbodystring,rpstring)
    return result

# takes argument as filename (local)
def csvinput(csvfile):
    
    table_name='facts'
    # the reader can split rows with delimiter or you can parse the file yourself
    # the csv.reader will split on rows using EOL.  So factor that into your parsing
    readRowsFromFile(csvfile)


# read in SML format from physical file
# Assumes only one code at end of each # at end of line
def readRowsFromFile(csvfile):
    output=[]
    with open(csvfile, 'r') as csvfile:
        # spamreader = csv.reader(csvfile)    
        spamreader = csv.reader(csvfile, delimiter='#', quotechar='|')
        for row in spamreader:
            output.append(row)
            print(row)
    # all rows are read now
    #print(output)
    return output

# read in lmd format from a string
def splitMDcodes(myArray):
    output=[]
    for item in myArray:
        first1=item[:1]
        #print(first1)
        items=item.split("#")
        if(first1=="-" and len(items)>=1):
            output.append(items)
        elif (len(items)>1):
            output.append(items)
        elif (len(items)==1):
            items.append("#NP")
            output.append(items)
    return output

# This function was originally to process SML patterns. 
# e.g. #text#text#H1
# Algo:
# 1. to turn text into line by line SML
# 2. Store SML lines in SQL database with appropriate fields (text, style, docname)
# database is used for later retrieval of individual documents.
# A 'visibility' state was also included.
#
# Inputs:
# This input array consists of list of arrays of varying length 
# length 2 if SML hashcode split off from end of line.  Length 1 for '-n-' newdoc lines.
#
# Output: updates the SQL database
# inserts each 'row' as a record in the global SQL database, for later use

def processRowsLMS(inputRows):
    print("processRowsLMS. Start")
    global db
    global cursor
    docname="Default Document"
    currentblockname="def"
    realinterpseq=0
    blockseq=0
    localseq=1
    interpseq=0
    blockcont="def"
    mycat='None'
    visible='TRUE'
    updateDB='FALSE'
   
    for row in inputRows:
        print(currentblockname,row)
        if (row is not None):
            #retrieve document name for use as field in db
            if (row[0][:3]=="-n-"):
                # update state not DB
                updateInterpretation(realinterpseq,docname) # update blockseq for interpretation clause
                docname=row[0][3:]
                print ("Found new document:",docname)
                # reset variables
                blockseq=1
                localseq=1
                interpseq=0 # hold this whilst parsing
                realinterpseq=0
                blockcont="def"
                mycat='None'
                visible='TRUE'
                updateDB='FALSE'
               
            elif (row[0][:3]=="---" or row[0][:3]=="-x-"):
                # update state not DB
                currentblockname=row[0][3:]
                blockseq=blockseq+1
                localseq=1
                if (currentblockname=="Interpretation"):
                    realinterpseq=blockseq  # currently not retrospective
                    #localseq=1  #priority in clause order
                visible='TRUE'
                if (row[0][:3]=="-x-"):
                    visible='FALSE'
            elif (row is not None and len(row)==1):
                print(row)
                print("Docmaker. ProcessRowsLMS. Problem with reading in style for this para")
                exit()

        # 'LH' or 'LC' successive para styles sequence: #heading#text#etc#LH (equivalent to H1, Indent1 formats)  
        if (row is not None and len(row)>2):
            colmax=len(row)-1
            mkdlist=[]
            updateDB='FALSE'
            visible='TRUE'
            myblockseq=blockseq
            myclname=currentblockname
            # Style sets
            if (row[colmax]=="BC"):
                mkdlist=["BC","BC","BC"]
            if (row[colmax]=="LH"):
                mkdlist=["LH","Indent1","H3"]
            if (row[colmax]=="IP"):
                mkdlist=["Indent1","Indent1","Indent1"]
            if (row[colmax]=="H3"):
                mkdlist=["H3","H3","H3"]
            elif (row[colmax]=="LC"):
                mkdlist=["LC","LCF","LCFF"]
            elif (row[colmax]=="BHP"):
                mkdlist=["B","NP","NP"]
            elif (row[colmax]=="PP"):
                mkdlist=["NP","NP","NP"]
            elif (row[colmax]=="PL"):
                mkdlist=["NP","NP2","NP2"]
            elif (row[colmax]=="LHC"):
                mkdlist=["LH","LC","LCF"]
            elif (row[colmax]=="L2"):
                mkdlist=["H2","Indent1","H3","H3"]
            # legal doc 3 tries to incorporate a cyclic style a heading and a paragraph
            #elif (row[colmax]=="L3"):
            #    styleitems = len(row)
            #    mkdlist=["H2","Indent1","H3","H3"]
            mmax=len(mkdlist)-1
            if (mmax>1):
                for idx in range(colmax):
                    myidx=idx    
                    if myidx>mmax:
                        myidx=mmax
                    # row entries taken in turn
                    blockcont=row[idx] # contents based on progressive row entries
                    mycat=mkdlist[myidx] # categories are a finite list
                    mylocalseq=localseq
                    cursor.execute('''INSERT INTO facts(docname,clname,block,blockseq,localseq,category,visible) VALUES (?,?,?,?,?,?,?)''', (docname,myclname,blockcont,myblockseq,mylocalseq,mycat,visible))
                    db.commit()
                    localseq=localseq+1
                    

        # longer general definition line syntax: #def#meaning#GD  
        # TO DO: put this into earlier translation process                
        if (row is not None and len(row)==3 and row[2]=="GD"):
            updateDB='TRUE'
            mycat="GD" # general definition
            blockcont='"'+row[0]+'" means '+row[1]
            visible='TRUE'
            # if not Interpretation clause yet will remain at 0

        elif (row is not None and len(row)==2):
            blockcont=row[0]
            mycat=row[1] # TO DO: semantic codes for clauses
            if (mycat=="I1"):
                mycat="Indent1"
            elif (mycat=="I2"):
                mycat="Indent2"
            elif (mycat=="N"):
                mycat="Note"
            
            # This will check whether semantic code at end of lmd line is in our database
            #TO DO: remove trailing white space before testing
            #TO DO: just look up database entries
            mylist=["LH","LHF","LC","LCF","LCFF","H1","H2","H3","H4","H5","IN","Indent1","Indent2","Indent0","GD","LD","ST","DT","BC","CH","Note","None","NP","NB","PL","B","SB","PB","LDP0","LDP1","LDdate","LDB","LDBN","LN","Sched1"] 
            try:
                if (mylist.index(mycat) is not None):
                    updateDB='TRUE'
            except ValueError:  #cf look before you leap in C programming
                print("Not in list. Ignored? Make it NP")
                mycat="NP"
                updateDB='TRUE'
        

        #elif (row is not None):
        #    print("Docmaker. ProcessRowsLMS. Not sure how we got here")
        #    print(row)
        #    exit()

        if (updateDB=='TRUE'): 
            mylocalseq=localseq
            myclname=currentblockname
            myblockseq=blockseq
            # All GDs go into same clause
            # Removed 8.11.2019 for Java GUI development
            #if (mycat=="GD"):
            #    myclname="Interpretation"
            #    mylocalseq=2
            #    myblockseq=interpseq  #set to whatever this is 
            cursor.execute('''INSERT INTO facts(docname,clname,block,blockseq,localseq,category,visible) VALUES (?,?,?,?,?,?,?)''', (docname,myclname,blockcont,myblockseq,mylocalseq,mycat,visible))
            db.commit()
            updateDB='false'
            localseq=localseq+1
        updateInterpretation(realinterpseq,docname) # last doc


# This interprets the current lmd format
# input: a csv file
# process: transforms 
# interprets semantic definitions and converts to style
# (simple).  To be expanded and improved
# TO DO: remove trailing whitespaces
# TO DO: store GD and CT rows, then write into database in preferred order/sequence at end
# 5.9.19: adopt a more inclusive capture of text blocks (requires more work to split out paragraphs for WP write-outs
# but simplify data structures)
def readRowsSpam(csvfile):
    global db
    global cursor
    with open(csvfile, 'r') as csvfile:
        # spamreader = csv.reader(csvfile)    
        spamreader = csv.reader(csvfile, delimiter='#', quotechar='|')
        docname="Default Document"
        currentblockname="def"
        realinterpseq=0
        blockseq=0
        localseq=1
        interpseq=0
        blockcont="def"
        mycat='None'
        visible='TRUE'
        updateDB='FALSE'
        for row in spamreader:
            print(currentblockname,row)
            if (row is not None and len(row)==1):
                if (row[0][:3]=="-n-"):
                    # update state not DB
                    updateInterpretation(realinterpseq,docname) # update blockseq for interpretation clause
                    docname=row[0][3:]
                    print ("Found new document:",docname)
                    # reset variables
                    blockseq=1
                    localseq=1
                    interpseq=0 # hold this whilst parsing
                    realinterpseq=0
                    blockcont="def"
                    mycat='None'
                    visible='TRUE'
                    updateDB='FALSE'

                   
                elif (row[0][:3]=="---" or row[0][:3]=="-x-"):
                    # update state not DB
                    currentblockname=row[0][3:]
                    blockseq=blockseq+1
                    localseq=1
                    if (currentblockname=="Interpretation"):
                        realinterpseq=blockseq  # currently not retrospective
                        #localseq=1  #priority in clause order
                    visible='TRUE'
                    if (row[0][:3]=="-x-"):
                        visible='FALSE'
                elif (len(row)==1):
                    print("Problem with reading in style for this para")
                    exit()
                else:
                    print("Not sure how we got here")
                    print(row)
                    exit()

            # 'LH' or 'LC' successive para styles sequence: #heading#text#etc#LH (equivalent to H1, Indent1 formats)  
            if (row is not None and len(row)>2):
                colmax=len(row)-1
                mkdlist=[]
                updateDB='FALSE'
                visible='TRUE'
                myblockseq=blockseq
                myclname=currentblockname
                # Style sets
                if (row[colmax]=="BC"):
                    mkdlist=["BC","BC","BC"]
                if (row[colmax]=="LH"):
                    mkdlist=["LH","Indent1","H3"]
                if (row[colmax]=="IP"):
                    mkdlist=["Indent1","Indent1","Indent1"]
                if (row[colmax]=="H3"):
                    mkdlist=["H3","H3","H3"]
                elif (row[colmax]=="LC"):
                    mkdlist=["LC","LCF","LCFF"]
                elif (row[colmax]=="BHP"):
                    mkdlist=["B","NP","NP"]
                elif (row[colmax]=="PP"):
                    mkdlist=["NP","NP","NP"]
                elif (row[colmax]=="PL"):
                    mkdlist=["NP","NP2","NP2"]
                elif (row[colmax]=="LHC"):
                    mkdlist=["LH","LC","LCF"]
                elif (row[colmax]=="L2"):
                    mkdlist=["H2","Indent1","H3","H3"]
                # legal doc 3 tries to incorporate a cyclic style a heading and a paragraph
                #elif (row[colmax]=="L3"):
                #    styleitems = len(row)
                #    mkdlist=["H2","Indent1","H3","H3"]
                mmax=len(mkdlist)-1
                if (mmax>1):
                    for idx in range(colmax):
                        myidx=idx    
                        if myidx>mmax:
                            myidx=mmax
                        # row entries taken in turn
                        blockcont=row[idx] # contents based on progressive row entries
                        mycat=mkdlist[myidx] # categories are a finite list
                        mylocalseq=localseq
                        cursor.execute('''INSERT INTO facts(docname,clname,block,blockseq,localseq,category,visible) VALUES (?,?,?,?,?,?,?)''', (docname,myclname,blockcont,myblockseq,mylocalseq,mycat,visible))
                        db.commit()
                        localseq=localseq+1
                        

            # longer general definition line syntax: #def#meaning#GD                  
            if (row is not None and len(row)==3 and row[2]=="GD"):
                updateDB='TRUE'
                mycat="GD" # general definition
                blockcont='"'+row[0]+'" means '+row[1]
                visible='TRUE'
                # if not Interpretation clause yet will remain at 0

            elif (row is not None and len(row)==2):
                blockcont=row[0]
                mycat=row[1] # TO DO: semantic codes for clauses
                if (mycat=="I1"):
                    mycat="Indent1"
                elif (mycat=="I2"):
                    mycat="Indent2"
                elif (mycat=="N"):
                    mycat="Note"
                
                # This will check whether semantic code at end of lmd line is in our database
                #TO DO: remove trailing white space before testing
                #TO DO: just look up database entries
                mylist=["LH","LHF","LC","LCF","LCFF","H1","H2","H3","H4","H5","IN","Indent1","Indent2","Indent0","GD","LD","ST","DT","BC","CH","Note","None","NP","NP2","NB","PL","B","SB","PB","LDP0","LDP1","LDdate","LDB","LDBN","LN"]
                try:
                    if (mylist.index(mycat) is not None):
                        updateDB='TRUE'
                except ValueError:  #cf look before you leap in C programming
                    print("Not in list. Ignored? Make it NP")
                    mycat="NP"
                    updateDB='TRUE'
               
            if (updateDB=='TRUE'): 
                mylocalseq=localseq
                myclname=currentblockname
                myblockseq=blockseq
                # All GDs go into same clause
                # Removed 8.11.2019 for Java GUI development
                #if (mycat=="GD"):
                #    myclname="Interpretation"
                #    mylocalseq=2
                #    myblockseq=interpseq  #set to whatever this is 
                cursor.execute('''INSERT INTO facts(docname,clname,block,blockseq,localseq,category,visible) VALUES (?,?,?,?,?,?,?)''', (docname,myclname,blockcont,myblockseq,mylocalseq,mycat,visible))
                db.commit()
                updateDB='false'
                localseq=localseq+1
            updateInterpretation(realinterpseq,docname) # last doc
        # all rows are read now
        

# specify that actual block seq of Interpretation clause for all 'general definitions'
def updateInterpretation(newblock,doc):
    global db
    global cursor
    myclause='Interpretation'
    cursor.execute('''UPDATE facts SET blockseq = (?) WHERE clname=(?) and docname=(?);''', (newblock,myclause,doc))
    db.commit()
    
# inputs: the paracode is the paracode detected in the paragraph
# the content is the text in the paragraph.
# uses the global blockdict to find the appropriate style
# also converts any semantic codes into style codes for this purpose
# If semantic code is "None" it will default to a 'Note' style
def prepareParagraph(paracode,content):
    global blockdict
    # Obtain parastyle from semantic code
    paratype="Indent1" # default
    mylist=["LH","LHF","LC","LCF","LCFF","H1","H2","H3","H4","H5","IN","Indent1","Indent2","Indent0","GD","LD","ST","DT","BC","CH","Note","None","NP","NP2","NB","B","SB","PB","LDP0","LDP1","LDdate","LDB","LDBN","LN","Sched1"]
    # These styles must be defined in the template used. TO DO: set them according to source file
    mystyles=["H1","Indent1","H2","Indent1","H3","H1","H2","H3","H4","H5","Indent1","Indent1","Indent2","IndentNoSpace","Indent1","Indent1","SUBTITLE","DocTitle","BoldCentred","CentredHeading","Note","Note","NumParas","NumParas2","NumParasBold","BoldHeading","SectionBreak","PageBreak","LDP0","LDP1","LDdate","LDB","LDBN","LN","SCHEDL1"]
    # What is the index number of the semantic code supplied?
    myindex=mylist.index(paracode)
    # What is the index number of the lmd style code for this paragraph?
    if (myindex is not None):
        paratype=mystyles[myindex]
    # What is the defined OOXML paragraph in our styles dictionary that contains 'XXX' in this style?
    samplepara=blockdict.get(paratype)
    if samplepara is None:
       print(blockdict,paratype,content)
       print("checks failed on samplepara")
       exit()
    #if (paracode=="IN"): #DT
    #    print("SamplePara:",samplepara)
    #   print("IN text:",content)
    # Prepare a new paragraph of the required style by replacing XXX with our content
    newcontent=samplepara.replace("XXX",content)
    #print("this:",samplepara,newcontent)
    # we must also escape any characters that will jeopardise XML
    cleancontent=xmlEscape(newcontent)
    return cleancontent

# replace user-level & with something XML won't have a problem with
# nb tag < > characters should be replaced BEFORE xml paras are added?
# .replace('<','&lt;').replace('>','&gt;').replace('\'','&apos;') 
def xmlEscape(myString):
    output=myString.replace('&','&amp;') # escape the character, but also have XML compliant
    print(output)
    return output

# loads up the docx template styles
# It then uses the document name argument (dn) to the 'makeWPdoc' function.
# (that function will call up just the OOXML lines relating to that doc name)
# It will use same docx file used for the template.
# It swaps in the new body text retrieved from the database, and writes back a new docx file.

def makeSomeDocs(templatepath,newpath,dn):
    #newpath=nbname+"_new."+suffix
    # get Styles to use and put in a dictionary of stylenames and OOXML text.
    # obtain the template's document.xml content from file
    templatestring=xmlutil.getDocxContent(templatepath)
    paralist=xmlutil.getParasInclusive(templatestring)
    global blockdict
    blockdict=identifyStyles(paralist)
    #make documents from database
    newbody=makeWPdoc(dn)
    if newbody is not None:
        makebody=docBodySwap(newbody,templatestring)
         # TO DO : resave. It uses the .docx styles document as the template for the new Word document too.
        xmlutil.writeNewFileZip(templatepath,newpath,makebody)
        print("Saved:"+newpath)
    else:
        print('No content')

# current function.  Retire 'makeSomeDocs' once dependencies are removed
def makeNewDocx(newpath,dn):
    stylepath="LegalDocsTemplate.docx"
    stylestring=xmlutil.getDocxContent(stylepath)
    updateDocxStyles(stylestring)
    #make documents from database
    newbody=makeWPdoc(dn)
    if newbody is not None:
        # put the new body into the template 
        makebody=docBodySwap(newbody,stylestring)
         # TO DO : resave. It uses the .docx styles document as the template for the new Word document too.
        xmlutil.writeNewFileZip(stylepath,newpath,makebody)
        print("Saved:"+newpath)
    else:
        print('No content')

# make a WP document from a named document in the database
# TO DO: different modes of construction depending on context
def makeWPdoc(mydoc):
    global db
    global cursor
    #cursor.execute('''select name from sqlite_master where type = 'table';''')
    #test=cursor.fetchone()  # fetch first row of SQL output (whatever it is)
    #with single variable you need to put , at end to make it a 'tuple'
    # or make it a list literal [mydoc]
    #
    # if visible condition not included this will output all clauses
    # cursor.execute('''select block,category from facts where docname=(?) AND visible='TRUE';''',(mydoc,))
    # docname,clname,block,category,visible
    # sort order will reflect input order (which is first entry in stream import first)
    cursor.execute('''select block,category,clname FROM facts WHERE docname=(?) AND visible='TRUE' ORDER BY blockseq ASC, localseq ASC, id ASC;''',(mydoc,))
    print("----------------Making WP DOCS---------------------")
    rows=cursor.fetchall()  # fetch first row of SQL output (whatever it is)
    if rows is not None:
        #print(rows)
        content=prepareParas(rows)
        newbody=makeNewDocBody(content)
        return newbody
        

# row is a tuple (block, category).  If select order changes, change this function
def prepareParas(row):
    newpara=""
    for item in row:
        paratext = item[0]
        paracode=item[1]
        # print(paratext,parastyle)
        newpara=newpara+prepareParagraph(paracode,paratext)
    return newpara    
    

# Take string input equivalent to a Word OpenXML <w:p> paragraph block
# This is only a temporary transformation of para data obtained using the xmlutil utility
# It is never working with the OpenXML file directly.
# Locates Word text tags <w:t>, and makes text from those tags contiguous
# Use: For text-based searches/replacements that require plain, readable text.
# nb do not rely on <w:t> tag: use <w:t for opening as there are variations in those tags.
# nb this is one of them: <w:t xml:space="preserve">

def makeContiguous(thispara):
    # print ("Trying to make this contiguous:")
    # print(thispara)
    # make para contiguous text
    output="" 
    stop = len(thispara)
    # print("in makeC, length:"+str(stop))
    newstart=0
    starttag="<w:t"
    starttagend=">" # to allow for insertion of attributes (Word). 
    endtag="</w:t>"
    while newstart<=stop:
        sindex=thispara.find(starttag,newstart,stop) 
        test=thispara[sindex+len(starttag):sindex+len(starttag)+1]
        if test==starttagend or test==" ":
            sindexend=thispara.find(starttagend,sindex,stop) 
            gap=sindexend-sindex
            findex=thispara.find(endtag,newstart,stop)
            # whenever we find end tag we capture internal w:t tags text
            if (findex!=-1):
                thistext=thispara[sindex+gap+1:findex]
                output=output+thistext
                newstart=findex+len(endtag)
            else:
                newstart=newstart+1
        else:
            newstart=newstart+1
    #print("new contig output:"+output)
    return output

# at the end of this function, we have a list with style names and pro forma paragraph text to use
#returns list as dictionary with key,value
def identifyStyles(paralist):
    blocklist=[]

    for thispara in paralist:
        # print("In findInserts.  Finding a user tag ref in a para.")
        contigtext=makeContiguous(thispara)
        print("contig text:"+contigtext)
        if len(contigtext)<1:
            print("no contig text in style template line")
            exit()
        else:
            # put in standard 'code' text to be replaced later
            # do not just replace contigtext if the text is same as actual style name in docx document
            tblock=">"+contigtext+"<" # avoids replacing OpenXML pstyle text if it has same name
            newtext=thispara.replace(tblock,">XXX<")
            if ("XXX" not in newtext):
                print("Problem with Style Template.  Name not contiguous")
                print(contigtext)
                print(newtext)
                exit()
            #hardcode page break.  Template file just needs "PageBreak" words and font
            if (contigtext=="PageBreak"):
                #pbcode=xmlutil.returnPageBreak()
               # a whole run with a break in it.
                pbcode='<w:r><w:br w:type="page"/></w:r>'
                dummytag="<w:r>" # This is now in the newtext para
                if (dummytag not in newtext):
                    print("Cannot setup page break properly. No run tag <w:r>")
                    exit()
                exttext=pbcode+dummytag # pbreak inserted before next run tag.
                #print(newtext)
                newtext=newtext.replace(dummytag,exttext)
                if (pbcode not in newtext):
                    print("Page break not inserted properly.")
                    print(pbcode)
                    print(newtext)
                    exit()
            blocklist.append((contigtext,newtext))  # store this paragraph for replacement with library ref
                # print("Appended insert blockref: "+str(blockref))
    #convert list to dictionary
    print("===============================",blocklist)
    styledict=dict(blocklist) # convert list to dict
    return styledict


# runs an SQL functon that creates a table
def dbReadDataFromFile(filename):
    global db
    global cursor
    cursor.execute(''' CREATE TABLE facts(id INTEGER PRIMARY KEY, docname TEXT, clname TEXT,block TEXT, blockseq INTEGER, localseq INTEGER, category TEXT,visible BOOLEAN)''')
    db.commit()
    #exit()
    table_name='facts'
    output=readRowsFromFile(filename)
    processRowsLMS(output)
    #csvinput(filename)

def dbReadDataFromArray(myArray):
    global db
    global cursor
    cursor.execute(''' CREATE TABLE facts(id INTEGER PRIMARY KEY, docname TEXT, clname TEXT,block TEXT, blockseq INTEGER, localseq INTEGER, category TEXT,visible BOOLEAN)''')
    db.commit()
    #exit()
    table_name='facts'
    # split end hashcodes so they are separate from string
    output=splitMDcodes(myArray)
    print(output)
    processRowsLMS(output)
    #csvinput(filename)


# Test this custom lmd file as the source for the document database
def demo():
    global db
    global cursor
    global outputfolder
    dbReadDataFromFile('demo.lmd')
    makeDocxFromDB()

# Test this custom lmd file as the source for the document database
# puts docname into SQL database, line by line?
# Then fetches those lines again, as an array ... 
def customFromFile(mdfile):
    try:
        dbReadDataFromFile(mdfile)
    except:
        print("Error reading file (custom function).")
    makeDocxFromDB()

# update global styles dictionary from styles in chosen template
def updateDocxStyles(stylestring):
    global blockdict
    paralist=xmlutil.getParasInclusive(stylestring)
    blockdict=identifyStyles(paralist)

def makeDocxFromDB():
    global db
    global cursor
    global outputfolder
    # names=["Testdoc","thirddoc","seconddoc"]
    cursor.execute('''select DISTINCT docname from facts;''')
    names=cursor.fetchall()  # fetch all rows of SQL output (whatever it is)
    # print(names)
    if names is not None:
        for dn in names:
            mydn=dn[0]
            #newpath="output/"+mydn+"_new.docx"
            newpath=outputfolder+mydn+"(2).docx"
            makeNewDocx(newpath,mydn)
    db.close()

# reads each line of the lmd file (now an array) but then stores it into the SQL database
# it calls the function to make docx documents AFTER it has updated the database ('db')
def docFromArray(myArray):
    # The first step reads in the script file and records separate documents with each line in db
    # If this succeeds, all the script data and styles is in a database we can use.
    try:
        dbReadDataFromArray(myArray)
    except:
        print("Error reading file (custom function).")
    #nbname="LegalDocsTemplate"
    makeDocxFromDB()

# START HERE
# Can be directly invoked with:  python3 docmaker.py fname

# global var for the styles
blockdict=dict()
outputfolder="output/"
db = sqlite3.connect(':memory:')   # this is RAM only.  Specify file to read from disk
cursor=db.cursor() # for command entry
 # this is from a file (create or open)
# db = sqlite3.connet('data/mydb')

# we are able to see how this code was invoked, and if called by another program, take no immediate action
# some prefer this technique for checking if this is the top-level or stand-alone source code run from command line:
# if __name__ == '__main__':

args=len(sys.argv)
#alternative way of checking how this is invoked
#progname=sys.argv[0]
#if (progname!="docmaker.py"):
#    print(progname)
#    exit()
if (args==2 and __name__ == '__main__'):
    nbname=sys.argv[1]
    if len(nbname)!=0:
        # remainder is optional for now:
        #
        nameonly,suffix=nbname.split('.')
        if (suffix=="txt" or suffix=="md" or suffix=="lmd"):    # or suffix=="odt":
            print("Name is "+nbname)
            customFromFile(nbname)
        else:
            print("This program requires .txt .md or .lmd extensions for the input (legal markup) file")
    else:
        doError()
if (args==3 and __name__ == '__main__'):
    outputfolder=sys.argv[1]
    nbname=sys.argv[2]
    if len(nbname)!=0:
        # remainder is optional for now:
        #
        nameonly,suffix=nbname.split('.')
        if (suffix=="txt" or suffix=="md" or suffix=="lmd"):    # or suffix=="odt":
            print("Name is "+nbname)
            customFromFile(nbname)
        else:
            print("This program requires .txt .md or .lmd extensions for the input lmd file")
    else:
        doError()

elif (args==1 and __name__ == '__main__'):
    demo()

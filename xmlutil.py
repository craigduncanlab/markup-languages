# OpenXML and .docx utility program
# (c) Craig Duncan 2019-2020
# v1.1 (c) by Craig Duncan 6/4/2019 updated 13/4/2019-1/5/2019 
# zipfile is in the python standard library but still need import statement
# This is written for python 3.6.5 (e.g. Anaconda version, not Ubuntu)
# useful ref (but in python 2.7): https://pymotw.com/2/zipfile/

import zipfile # the prefix for all functions.  Part of std python liubrary.
import datetime
import string # if you want to use string replace
import re # if you want to use regular expressions to replace in a single pass

testword = "";

def setTestWord(thisWord):
    global testword
    testword=thisWord

# private function to return contents of zipfile 
def _getZipInfo(filepath):
    myzf=zipfile.ZipFile(filepath,'r')
    print (myzf.namelist())
    return myzf.infolist()

# public function to return the document.xml content of a given .docx file
def getDocxContent(filepath):
    # part 1 - open .docx document from which clause (text/paragraphs) will be copied 
    mycontainerzipfile=zipfile.ZipFile(filepath,'r')
    worddoc='word/document.xml'
    inputdata = mycontainerzipfile.read(worddoc)
    worddata = inputdata.decode("utf-8") # convert binary data to a string in a specified text format
    return worddata

# public function to return the document.xml content of a given .docx file
# worddoc='word/document.xml'
# numberdoc='word/numbering.xml'
def extractDocxFile(filepath, filename):
    # part 1 - open .docx document from which clause (text/paragraphs) will be copied 
    mycontainerzipfile=zipfile.ZipFile(filepath,'r')
    if filename not in mycontainerzipfile.namelist():
        print (filename+" not in container.  Aborted")
        return -1 
    inputdata = mycontainerzipfile.read(filename)
    # allow for utf

    # can we test for utf8 directly?
    testxml=filename.find("xml",0,len(filename))
    testrels=filename.find("rel",0,len(filename))
    if testxml!=-1 or testrels!=-1:
        datanew = inputdata.decode("utf-8")
    else:
        datanew=inputdata
        myfile.open(fileout,'w')
    
    #if testrels!=-1:
    #    print("Unpacked a rels file:"+str(filename))
    #    print(datanew)
    # print("extracted")
    return datanew


# Takes a string as input, based on a Word OpenXML paragraph (<w:p> tags)
# The tag and tag end should be inclusive of quote chars
# Takes tag ends as input (these should bracket the 'value' portion)
# Returns only valid tag value found (str or int), otherwise -1 
# This function is overloaded in that it can return strings or ints

def _getTagStringValue(thispara, tag, tagend):
    result=thispara.find(tag,0,len(thispara)) # this will find open braces
    numdef=-1  # default is an integer
    if (result!=-1):
        start=result+len(tag)
        balance=thispara[start:]
        end=balance.find(tagend,0,len(balance)) # match,beg,end
        if (end!=-1):
            numdef=balance[0:end] # beg of balance should be start of digits.  
            if(len(numdef)==0):  
                numdef=-1
    return numdef

# Public function to read in ALL the file between OpenXML tag ends, inclusive of the tags&content
# The function allows you to specify as much or as little of the enclosing tags as needed.
# This could be specific to your OpenXML e.g. 
# opentag="<w:abstractNum w:abstractNumId="
# closetag="</w:abstractNum>" 
# Memory ? most Word docs have a document.xml file between 400kb and 700kb (<1 MB memory)
# if you use the <w:p> tags the list will include most of the file.

def getTagListInclusive(precstring,opentag,closetag):
    newstart=0
    if precstring==-1:
        return -1
    if precstring==None:
        return -1
    #starttagend=">"
    stop = len(precstring)
    anlist=[]
    # compare to dbutil.py makeContiguous function
    while newstart<stop:
        thispara=""
        sindex=precstring.find(opentag,newstart,stop)
        findex=precstring.find(closetag,newstart,stop)
        # if we find an end before the closing tag i.e. single open tag 
        if (findex!=-1):
            fin = findex+len(closetag)  # take up to end of tag
            thispara=precstring[sindex:fin] # enclose opening and closing tags
            if (len(thispara)>0):
                anlist.append(thispara)
            newstart=fin
            #print("fin")
        else:
            newstart=newstart+1
            #print("stop count:"+str(stop))
            #print(newstart)
    if len(anlist)==0:
        #print("No tags found")
        return -1
    else: 
        return anlist

# check for page break 
# cf <w:pageBreakBefore/> 
def getPageBreak(thispara):
    starttag="<w:lastRenderedPageBreak" # if page break is last thing 'rendered' on page
    endtag="/>"
    result=getTagAttribInclusive(thispara,starttag,endtag)
    #if (len(result)>0):
    #    return result
    return result

# function to return a page break for converting markdown
def returnPageBreak():
    return "<w:lastRenderedPageBreak/>"

# function to return a section break for converting markdown
# does this work or does it need some specification content?  Do we need to 'read' from a Style template?
def returnSectionBreak():
    return '<w:sectPr w:rsidR="00ED6065"><w:footerReference w:type="default" r:id="rId10"/><w:pgSz w:w="11906" w:h="16838" w:code="9"/><w:pgMar w:top="1134" w:right="1276" w:bottom="1134" w:left="1276" w:header="720" w:footer="720" w:gutter="0"/><w:pgNumType w:start="1"/><w:cols w:space="720"/><w:noEndnote/></w:sectPr>'


#check for a section break (this includes break that starts a new page but isn't tagged by OOXML as a page break)
def getSectionBreak(thispara):
    #section breaks will be included within a single 'para' object/string
    starttag="<w:sectPr"
    endtag="</w:sectPr>"
    result=getTagAttribInclusive(thispara,starttag,endtag)
    return result


def getParasInclusive(thispara):
    starttag="<w:p>"
    endtag="</w:p>"
    result=getTagAttribInclusive(thispara,starttag,endtag)
    return result

def getParasInclusiveStyle(thispara):
    starttag="<w:p>"
    endtag="</w:p>"
    result=getTagAttribInclusiveStyle(thispara,starttag,endtag)
    
    return result #result


def getTableRowsInclusive(thispara):
    starttag="<w:tr>"
    endtag="</w:tr>"
    result=getTagAttribInclusive(thispara,starttag,endtag)
    return result

def getTableCellsInclusive(thispara):
    starttag="<w:tc>"
    endtag="</w:tc>"
    result=getTagAttribInclusive(thispara,starttag,endtag)
    return result



# removes end of start tag so that included attributes section can be found
# e.g. <w:p> becomes <w:p and looks for > ahead.
# end tag is unaltered
# To do: use this to replace getTagListInclusive function
def getTagAttribInclusive(thispara,starttag,endtag):
    output=[] 
    stop = len(thispara)
    newstart=0
    starttagend=starttag[-1:] # this will be > in all cases
    starttag=starttag[:-1] # strip off closing >
    while newstart<=stop:
        sindex=thispara.find(starttag,newstart,stop)
        if sindex==-1:
            return output # nothing found to end = None?
        findex=thispara.find(endtag,sindex,stop)
        test=thispara[sindex+len(starttag):sindex+len(starttag)+1]
        if test==starttagend or test==" ":
            if (findex!=-1):
                thistext=thispara[sindex:findex+len(endtag)]
                output.append(thistext)
                newstart=findex+len(endtag)
            else:
                newstart=newstart+1
        else:
            newstart=newstart+1
    return output

# input: a full OOXML paragraph with appropriate tags
# processes the input string and identifies each Word 'paragraph' object (attribute)
# for each of these, detects the Word style string and returns an array pair with
# the full paragraph (for more processing) and the Style text isolated for processing
def getTagAttribInclusiveStyle(thispara,starttag,endtag):

    # now find the paragraph text inside the main paragraph tags
    output=[] 
    stop = len(thispara)
    newstart=0
    starttagend=starttag[-1:] # this will be > in all cases
    starttag=starttag[:-1] # strip off closing >
    count=0 # use this to keep track of the index values of paragraphs for later, even if filtered
    while newstart<=stop:
        sindex=thispara.find(starttag,newstart,stop)
        if sindex==-1:
            return output # nothing found to end = None?
        findex=thispara.find(endtag,sindex,stop)
        test=thispara[sindex+len(starttag):sindex+len(starttag)+1]
        if test==starttagend or test==" ":
            if (findex!=-1):
                thistext=thispara[sindex:findex+len(endtag)]
                # find the style part of the para identified.  This is OOXML for Word after....
                tag="<w:pStyle w:val=\""
                tagend="\"" # end quote
                style=getAttributeValue(thistext,tag,tagend)
                if (style=="Not found"):
                    style="Normal" # to align with Word.  Basically means no Style applied by user
                # find the outline part of the para identified.  ECMA376 part 1, page 234 (2016)
                # Probs: this is stored outside the w:p tag, so captured paras aren't wide enough.
                # Also, if there is a heading 'style' applied, the outline levels are in the style def only.
                # see https://docs.microsoft.com/en-us/office/vba/api/word.paragraph.outlinelevel
                tag="<w:outlineLvl w:val=\""
                tagend="\"" # end quote
                olevel=getAttributeValue(thistext,tag,tagend)
                if (olevel=="Not found"):
                    olevel=0 
                #if page break in para store for later
                pbreak=0
                pbreakstate=getPageBreak(thistext)
                if (len(pbreakstate)>0):
                    #print("pagebreakfound")
                    #print(pbreakstate)
                    pbreak=1
                #section breaks
                sbreak=0
                sbreakstate=getSectionBreak(thistext)
                if (len(sbreakstate)>0):
                    #print("sectionbreakfound")
                    #print(sbreakstate)
                    sbreak=1
                    #exit()
                #print("This para:%s" % thistext)
                #print("Style found:%s" % style)
                #style=getStyle(thistext)
                pair = [thistext,style,count,olevel,pbreak,sbreak] #keeping an index count for future reference
                output.append(pair)
                #output.append(thistext)
                newstart=findex+len(endtag)
                count=count+1
            else:
                newstart=newstart+1
        else:
            newstart=newstart+1
    return output
# NEXT
def getStyle(thisXMLpara):
    pair=[]
    global testword
    if (len(testword)<=0):
        testword="Heading"
    styletext="Normal" # not found is called 'Normal' by Word so adopt here.
    print("---Testing: "+testword)
    print("---Testing this: "+thisXMLpara)

    #if (test in thisXMLpara): #check for headingstyle 
    stop = len(thisXMLpara) # extend to next < or " etc
    result=""
    newstart=0
    count=0
    sindex=thisXMLpara.find(testword,0,stop)
    if (sindex!=-1):
        print(sindex)
        stop = sindex+len(testword)+1
        styletext=thisXMLpara[sindex:stop]
    print("style:"+styletext)
    if (len(styletext)==0):
        styletext="Normal" # not found is called 'Normal' by Word so adopt here.
    return styletext

# gets first tag pair match in the specified string
def getTagPair(precstring,opentag,closetag):
    print("GTP...")
    if precstring==-1:
        return -1
    stop = len(precstring)
    result=""
    newstart=0
    count=0
    sindex=precstring.find(opentag,0,stop)
    #print(precstring)
    if sindex!=-1:
        newstart=sindex+len(opentag)
        findex=precstring.find(closetag,sindex,stop)
        #closing tag
        if (findex!=-1):
            fin=findex+len(closetag)
            thispara=precstring[sindex:fin]
            if (len(thispara)>0):
                result=thispara
    if len(result)==0:
        print("No tags found")
        return -1
    else: 
        return result


# Typical use: tagend will be quote at end of value property
# e.g.tag="<w:numId w:val=\"" and tagend="\""
def getATagIntValue(thispara,tag,tagend):
    # print("_getATagIntValue (xml)")
    result=thispara.find(tag,0,len(thispara)) # this will find open braces
    numdef=-1  # default is an integer
    if (result!=-1):
        start=result+len(tag)
        balance=thispara[start:] # +1 not needed?
        end=balance.find(tagend,0,len(balance)) # match,beg,end
        if (end!=-1):
            numdef=balance[0:end] # beg of balance should be start of digits.  we capture end-1 as in OpenXML there are quoted vals!
            # print("this para in _getATagIntValue:"+str(thispara))
            if(len(numdef)>0): 
                numdef=int(numdef)
                #if (numdef>0):
                    #type checking?
                    # print("numdef in _getATagIntValue:"+str(numdef))
            else:
                numdef=-1
                # print(" Get A Tag Value.  Zero numdef for thispara:"+thispara)
                # print("balance:"+balance)
    return numdef

def getAttributeValue(thispara,tag,tagend):
    # print("_getATagIntValue (xml)")
    result=thispara.find(tag,0,len(thispara)) # this will find open braces
    myvalue="Not found"  # default is an integer
    if (result!=-1):
        start=result+len(tag)
        balance=thispara[start:] # +1 not needed?
        end=balance.find(tagend,0,len(balance)) # match,beg,end
        if (end!=-1):
            myvalue=balance[0:end] # beg of balance should be start of digits.  we capture end-1 as in OpenXML there are quoted vals!
            # print("this para in _getATagIntValue:"+str(thispara))
    return myvalue


# Appends entries to the target Content Types list where files did not previously exist in target.
# Currently only deals with numbering.xml TO DO: customXML files, etc

def writeContentsList(zipwrite,newtypes):
    contentfile=r'[Content_Types].xml'
    result=zipwrite.writestr(contentfile,newtypes)
    if result!=-1:
        print("write of Content_Types.xml successful")
    return result
 
# determine if source and destination have CustomXML 
def getCustomOption(libpath,insertpath):
    filename='[Content_Types].xml'
    insertflag=0
    libflag=0
    output=-1
    insertcontent=extractDocxFile(insertpath, filename)
    if insertcontent==-1:
        print ("getCustomOption.  Could not open Insert Content Types")
    libcontent=extractDocxFile(libpath, filename)
    if libcontent==-1:
        print ("getCustomOption.  Could not open Lib Content Types")
    
    insertflag=insertcontent.find("customXml",0,len(insertcontent))
    libflag=libcontent.find("customXml",0,len(libcontent))
    
    if libflag==-1:
        if insertflag==-1:
            print ("No customXML in either file")
            return 0
    else:
        if insertflag==-1: 
            return 1 #customXML in lib file only
        else:
            return 2 #custom XML in both files
    return output

# write customXML if it exists
# TO DO: just write all flags for content types then process together
# zipwrite object is an open zipfile object not closed by this function
# TO DO: check options again when writing Content_XLS and write in names of these files

def writeCustomXML(zipwrite,libpath,insertpath):
    option=getCustomOption(libpath,insertpath)
    packages=[]
    unziplib=0 # scope
    packages=0 # scope
    if option==0:
        return # nothing to do

    if option==1:
        packages=_getZipInfo(libpath)
        unziplib=zipfile.ZipFile(libpath,'r')
    if option==2:
        packages=_getZipInfo(insertpath)
        unziplib=zipfile.ZipFile(insertpath,'r')

    for item in packages:
        name=item.filename
        if name.find("custom",0,len(name))!=-1:
            data=unziplib.read(name)
            result=zipwrite.writestr(name,data)
            if result!=-1:
                print("Write of customXML... in target successful")


# write the styles lookup file from the lib packages to the destination 
def writeLibStyles(zipwrite,libpath):
    # write styles from lib to other (helpful in preserving "look and feel")
    unziplib=zipfile.ZipFile(libpath,'r')
    fname="word/styles.xml"
    data=unziplib.read(fname)
    content=data.decode("utf-8") # necessary?
    result=zipwrite.writestr(fname,content)
    if result!=-1:
        print("Write of lib styles.xml in target successful")

# Ensure data is UTF8 if necessary
# Ensure this code is run as python3 from command line

def utftest(filename,inputdata):
    testxml=filename.find("xml",0,len(filename))
    testrels=filename.find("rel",0,len(filename))
    if testxml!=-1 or testrels!=-1:
        datanew = inputdata.decode("utf-8")
        #print("utftest result xml:%d rels:%d" % (testxml,testrels))
        #print("decoded")
    else:
        datanew=inputdata
    return datanew

# inputs are the two filenames, and the new string representing document.xml content
def writeNewFileZip(nbpath,newname,docxml):

    maindoc='word/document.xml'
    excludednames = [maindoc] 
    nbpackages=_getZipInfo(nbpath) 
    unzipsrc=zipfile.ZipFile(nbpath,'r',zipfile.ZIP_DEFLATED)
    with zipfile.ZipFile(newname, 'w',zipfile.ZIP_DEFLATED) as zipwrite:
        
        # --- WRITE ALL EXISTING NOTEBOOK CONTENTS EXCEPT document.xml
        for item in nbpackages:
            if item.filename not in excludednames:  # no duplication
                print("saving notebook package:"+item.filename)
                insertdata = unzipsrc.read(item.filename)
                # check xml and rels strings are utf decoded/encoded
                newdata=utftest(item.filename,insertdata)
                zipwrite.writestr(item, newdata)  
            else: 
                print("notebook package not re-saved:"+item.filename)
                zipwrite.writestr(item,docxml)       
        zipwrite.close()

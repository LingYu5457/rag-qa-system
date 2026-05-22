

1
Interactive Data Public Test Suite, Version 77-260316, Page 1 of 32 
Interactive Data Public Test Suite 
Version 77-260316 
 
Contents 
1 
Goals .................................................................................................................................................. 2 
2 
Notation .............................................................................................................................................. 2 
3 
Versions .............................................................................................................................................. 2 
4 
Installation .......................................................................................................................................... 2 
5 
Library ................................................................................................................................................ 2 
5.1 
DTD and ENT files ........................................................................................................................ 2 
5.2 
Schemas and Style sheets ............................................................................................................. 2 
5.3 
Web Site Files Referenced by the Filer Manual.................................................................................. 3 
5.4 
Other files ................................................................................................................................... 3 
6 
Test Cases ........................................................................................................................................... 3 
6.1 
Required elements <creator>, <name> and <email>....................................................................... 4 
6.2 
Required element <number> ......................................................................................................... 4 
6.3 
Required element <name> ............................................................................................................ 4 
6.4 
Required element <description> .................................................................................................... 4 
6.5 
Optional repeating element <reference> ......................................................................................... 4 
7 
The <variation> element ...................................................................................................................... 4 
7.1 
Required attribute @id of <variation>............................................................................................. 4 
7.2 
Required element <name> of <variation> ...................................................................................... 5 
7.3 
Required element <description> of <variation> ............................................................................... 5 
7.4 
Optional repeating element <reference> of <variation> ................................................................... 5 
7.5 
Required element <data> of <variation> ........................................................................................ 5 
7.5.1 
Optional repeating element <parameter> of <data> ............................................................... 5 
7.5.2 
Required attribute @name of <parameter> ............................................................................ 5 
7.5.3 
Required attribute @datatype of <parameter> ........................................................................ 5 
7.5.4 
Required attribute @value <parameter> ................................................................................ 5 
7.5.5 
Parameter names, types and values currently in use ................................................................ 5 
7.6 
Optional repeating element <primary> ........................................................................................... 6 
7.6.1 
Optional attribute @docType of <primary> ............................................................................. 6 
7.7 
Required element <instance> ........................................................................................................ 6 
7.8 
Optional attribute @exhibitType of <instance> ................................................................................ 6 
7.9 
Optional repeating element <linkbase>........................................................................................... 6 
7.10 
Required repeating element <schema>........................................................................................... 7 
7.11 
Optional repeating element <exhibit>............................................................................................. 7 
7.11.1 
Optional attribute @docType of <exhibit> .............................................................................. 7 
7.12 
Required element <result>............................................................................................................ 7 
7.12.1 
Optional attribute @expected of <result> ............................................................................... 7 
7.13 
Optional repeating element <assert> ............................................................................................. 7 
7.14 
Optional repeating element <error> ............................................................................................... 7 
8 
The <assert> element .......................................................................................................................... 7 
8.1 
Required attribute @severity of <assert> ........................................................................................ 7 
8.2 
Required attribute @num of <assert> ............................................................................................. 7 
8.3 
Required attribute @name of <assert> ........................................................................................... 8 
8.4 
Optional attribute @frd of <assert> ................................................................................................ 8 
8.5 
Optional attribute @countSatisfied of <assert> ................................................................................ 8 
8.6 
Optional attribute @countNotSatisfied of <assert> ........................................................................... 8 
9 
Notes on the folder structure and file details ............................................................................................ 8 
10 
Notes on 6.16 Definition Syntax Subsections ...................................................................................... 8 
11 
Contacts ........................................................................................................................................ 9 
12 
Index .......................................................................................................................................... 10 
13 
Change Log .................................................................................................................................. 10 
 


2
Interactive Data Public Test Suite, Version 77-260316, Page 2 of 32 
1 
Goals 
The purpose of the public test suite is to assist developers of software that must validate Interactive Data prior to 
its submission to EDGAR. The test suite consists of many small Interactive Data instances, schemas and linkbases 
that are categorized as to whether they violate a validation check, and if so, what validation check they violate and 
whether that would be resulting a warning, or in an error that would cause the Interactive Data to be rejected. 
Filers that attach Interactive Data Exhibits to EDGAR submissions are responsible for compliance with all 
validations in the EDGAR XBRL Guide (“EXG”) and Chapter 5 of Volume II of the EDGAR Filer Manual (“the 
Manual”). Filers that attach Filing Fee Exhibits to EDGAR submissions are responsible for compliance with all 
validations in Filing Fee Inline XBRL Guide. Automated validation by preparation software can make it more 
efficient for filers to verify compliance before sending their filings to EDGAR itself. Nothing in this test suite is 
intended to create new requirements or change existing requirements for EDGAR submissions; filers should consult 
the Commission rules and the Manual for submission requirements. 
The organization of the test suite follows that of Chapter 6 of the Manual. Chapter 6 consists of subsections that 
each detail one or more Interactive Data validations, and these individual subsections are grouped into sections 
according to type of attachment (instance, schema, or linkbase) and whether the validations can be completely 
automated (called “syntax” sections) or whether they deal with the relationships that may require some manual 
review or accounting judgment (called “semantic” sections). 
Filing Fee Exhibit test variation are contained in directory conf/filing-fee-exhibit. The organization of this directory 
follows that of the Filing Fee Inline XBRL Guide. The Filing Inline XBRL Guide contains chapters pertaining to the 
applicable table for a Filing Fee Inline XBRL exhibit. Each chapter contains sections pertaining to the rules or 
elements that are being validated. The tests available in the test suite follow a similar hierarchy of Table →  Rule → 
Element. 
 
2 
Notation 
In this document, path names use forward slashes, although the tests work on any operating system. 
3 
Versions 
The major version number “77” refers to a specific version of Manual (draft or otherwise) and the minor version 
number “260316” is the date of the minor version, formatted as YYMMDD. 
4 
Installation 
The suite is distributed as a zip format archive. Extract the entire contents to any convenient location, preserving 
folder paths. It contains a top-level folder that corresponds to the version of the Manual. 
All files are encoded as 8-Bit Universal Transmission Format (UTF-8) or US ASCII. The suffix “.xsd” indicates an 
XML Schema file, “.xsl” indicates an XML Style Sheet (XSL) and suffix “.xml” indicates any other XML file type. 
There are no executables in the zip format archive except for XSL 1.0 files in subfolders “lib” and “conf”. 
The file index.htm is a file created to facilitate browsing the test files; it highlights testcase files containing remarks 
that may help developers. 
5 
Library 
The folder “lib” contains reference data and definitions used in multiple locations of the conf folder.   
5.1 DTD and ENT files 
An XML Document Type Definition (DTD) and three XML Entity Declaration (ENT) files used to validate the 
un-escaped content of Text Blocks and XBRL Footnotes. 
A Text Block is an XML element whose type is “textBlockItemType” in a namespace starting with 
“http://xbrl.us/us-gaap/”. 
An XBRL Footnote is an XML element named “footnote” in namespace “http://www.xbrl.org/2003/linkbase”. 
5.2 Schemas and Style sheets 
Files test.xsd, testcases.xsl and test.xsl are used to validate and view *-testcase.xml files in a browser, 
respectively.  The elements are all in the http://edgar/2009/conformance namespace. 


3
Interactive Data Public Test Suite, Version 77-260316, Page 3 of 32 
5.3 Web Site Files Referenced by the Filer Manual 
Section  File 
Related files 
6.5.43 
signwarnings.json 
 
6.5.44 
axiswarnings.json 
 
6.22 
edgartaxonomies.xml 
forbidden.xml, erxl.xsd 
5.4 Other files 
 
Content 
File 
Related files 
Error messages 
errors.xml 
xbrlerrors.htm 
Warning messages 
warnings.xml 
xbrlwarnings.htm 
External URL's used 
externals.txt 
 
Current Unit Type registry 
utr.xml 
 
 
6 
Test Cases 
A testcase file is an XML file used by software developers. The file names sets of files to be processed together and 
the expected results of that processing. The testcase XML file is typically transformed to produce a shell command 
script; the resulting command script invokes a validator on one file in each variation and stores the result of that 
validation. When a validator produces results identical to those expected, it is said to be “conforming”. 
All testcases and their test files are in the “conf” folder. The testcases are grouped by section with a sort code 
scheme that corresponds to the number and title of the section, for example: 
• 
Section 6.4 = Folder 604-filing-semantics 
• 
Section 6.5 = Folder 605-instance-syntax 
Within each section folder are subsection folders, following a similar coding scheme, for example: 
• 
Section 6.5.1 = 605-instance-syntax/605-01-identifier-scheme 
• 
Section 6.19.1 = 619-reference-semantics/619-01/619-01-no-standard-references 
Within each subsection is one testcase file whose name is prefixed the same as the folder. For example: 
• 
605-instance-syntax/605-01-entity-identifier-scheme/605-01-entity-identifier-scheme-testcase.xml 
Sections 6.24 and 6.25 of the filer manual are nested with an additional level of folders to distinguish "good" from 
"nogood" samples.   For example, the "good" variations of Section 6.24.2 are described here: 
• 
624-rendering/02-contexts/gd/02-contexts-testcase.xml 
It contains references to sample instances each in a different subfolder: 
• 
624-rendering/02-contexts/gd/000gd/r02000gd-20081231.xml 
• 
624-rendering/02-contexts/gd/001gd/r02001gd-20081231.xml 
Section 5.2.5 of the filer manual appears in 525-ix-syntax with an additional level of folders to distinguish tests 
that are Inline XBRL syntax tests that are "Not EDGAR Dependent" ("ned") versus those that are relevant to the 
EDGAR Filer Manual ("efm") versus those that cannot be unit tested but are "System Test Only" ("sto"): 
• 
525-ix-syntax/ned/01-format/i01001gd/i01001gd-20081231.xml 
• 
525-ix-syntax/efm/00-filing/i0200gd/i0200gd-20081231.xml 
• 
525-ix-syntax/sto/19-multiio/i19305ng/i19305ng-20181231.xml 
For Filing Fee Exhibits, all test cases are found under the “conf/filing-fee-exhibits” folder. The testcases are 
grouped by the chapter, section, and sub-section from the Filing Fee Inline XBRL Guide. For example: 
• 
Section 3.2.1 = Folder 300-offeringTable/02-Rule457(o)/01-PrevslyPdFlg 
• 
Section 4.2.2 = Folder 400-offsetTable/02-Rule0-11(a)(2)/02-OffsetPrrFilerNm 
Within each subsection folders, you will find a testcase xml file containing all the variations for this testcase. 


4
Interactive Data Public Test Suite, Version 77-260316, Page 4 of 32 
• 
Section 3.2.1 = Folder 300-offeringTable/02-Rule457(o)/01-PrevslyPdFlg/01-PrevslyPdFlg-testcase.xml 
The syntax of the testcase is a modification of the syntax typically used by the XBRL International consortium 
(http://www.xbrl.org) and so it retains some features that are not meaningful for this test suite. The schema at 
lib/test.xsd is for validating the syntax of each testcase. 
Each testcase file is XML that meant to be used for programming test harnesses and similar applications. Each 
testcase file also has an XML Processing Instruction referring to an XSL 1.0 style sheet lib/test.xsl for viewing it as 
HTML in a browser. 
The numbering of Manual sections is stable. The number and meaning of subsections will not change except to add 
additional subsections, or to mark subsections as “deleted” “reserved” or equivalent language. 
This version of the test suite contains an exception to the testcases structure.  EFM section 5.2.5 “Inline XBRL 
Documents” describes the handling of submissions containing more than one Inline XBRL Document Set (IXDS).  
Instead of the usual testcase XML file with the syntax detailed below, the 5.2.5 tests with multiple IXDS’s are 
provided with a shell script for executing the tests, in place of the usual testcase XML file. For Filing Fee Exhibits 
these tests are located here: conf/filing-fee-exhibit/000-multiinstance. 
6.1 Required elements <creator>, <name> and <email> 
These elements name the party responsible for the testcase, which for this test suite is always the Office of 
Structured Disclosure (OSD) at the SEC. 
6.2 Required element <number>  
By convention this is the sort code pattern “6[0-9]{2}-[0-9]{2}”, the sort code for a section as described above. 
“605-22” means section 6.5.22. 
An additional numbering convention used within 525-ix-syntax to ensure that no two leaf level test variations have 
the same name even if they are in different branches.  For example, test cases in ned/12-references/ will match 
i12000gd or i12100ng, while test cases in efm/12-references will match i12300gd or i12400ng.  This way, users 
may easily merge the folders and disregard the efm vs. ned distinction. 
6.3 Required element <name> 
The schema restricts this to contain a specific string that provides a human-readable reference back to the Manual: 
 
• 
EDGAR Filer Manual v{version} 6.{section}.{subsection} page 6-{page}  
6.4 Required element <description> 
This element has the text of the corresponding section of the Manual, but only for reference; EDGAR Filer Manual 
Volume II v53 is normative.  
This element also sometimes contains parenthetical additions such as (REMARK …) that indicates some 
implementation detail or related commentary, or a (TODO …) that indicates a known coverage gap or other 
deficiency in a draft version.  
6.5 Optional repeating element <reference> 
There can be any number of reference elements but each must have attribute @specification containing any useful 
string. 
7 
The <variation> element 
Each test case contains one or more variations. Each variation exposes just one aspect of the validation to be 
performed: either a “no good” variation that is meant to trigger exactly one validation error, or sometimes a 
“good” variation that is meant to illustrate either the base case or an edge case. 
All child elements of <variation> that denote filenames must have distinct contents within a single variation. For 
example, file "this.txt" cannot appear as both <primary> and as <exhibit>. 
7.1 Required attribute @id of <variation> 
By convention, this is in the format “_[0-9]{3}((gd)|(ng)|(gw))” in which “gd” always indicates a good (valid) 
variation, “ng” indicates a no good (invalid or triggering an error) variation and “gw” indicates that this variation is 
good with warning. A “gw” variation is intended as an example of a submission, which will be accepted with 
warnings, where a “ng” type submission with be suspended (not accepted).  


5
Interactive Data Public Test Suite, Version 77-260316, Page 5 of 32 
Concatenating the character “e”, the testcase number, and the portion of the @id occurring after the underscore, 
results in the base name of the files unique to that variation. For example, if the test number is 604-05 and there 
is a variation named “_003gd” then there will be data files with base name e60405003gd. 
The three digit number [0-9]{3} is often a zero based sequence, but may have gaps or some other iteration 
pattern.  
The numbering and meaning of individual variations within a testcase may change from release to release, 
although this is expected to be rare. 
7.2 Required element <name> of <variation> 
This contains free form plain text although by convention it begins with the section number and ends with either 
the token GOOD or NOGOOD. For example, these are the names of variations in 605-01-entity-identifier-scheme: 
• 
6.5.1, Scheme in instance is http://www.sec.gov/CIK, GOOD 
• 
6.5.1, Scheme in instance is http://www.sec.gov, NOGOOD 
7.3 Required element <description> of <variation> 
This contains free form plain text; again by convention it often duplicates the name element contents without the 
numeric prefix, and is always brief. 
7.4 Optional repeating element <reference> of <variation> 
There can be any number of reference elements but each must have attribute @specification containing any useful 
string. 
7.5 Required element <data> of <variation> 
The data element groups the Interactive Data files in the variation. This has instances, linkbases, and schemas. 
Although in principle the set of local files in the Discoverable Taxonomy Set (DTS) of the instance is discoverable 
from the instance, the testcase files also serve as a kind of manifest to ensure a set of files is complete without 
extraneous content. 
The DTS is described in detail along with other XBRL constructs in the XBRL 2.1 Specification at:  
http://www.xbrl.org/Specification/XBRL-2.1/REC-2003-12-31/XBRL-2.1-REC-2003-12-31+corrected-errata-2013-02-20.html  
7.5.1 Optional repeating element <parameter> of <data> 
Sometimes, validation requires an external input. For example, EDGAR uses the Central Index Key (CIK) number 
to identify filers.  
For example, variations in testcase 605-02-entity-identifier-match-cik requires that the CIK of the submission be 
provided as a parameter to the validation of an instance. 
7.5.2 Required attribute @name of <parameter> 
A QName that is the name of the parameter. In this test suite the QName content must have the empty 
namespace. 
7.5.3 Required attribute @datatype of <parameter> 
A QName that is the datatype of the parameter, usually xs:string. 
7.5.4 Required attribute @value <parameter> 
A string that is cast to the datatype specified and passed to the validator. 
7.5.5 Parameter names, types and values currently in use 
 
@name 
@datatype 
Sample value 
submissionType 
xs:string 
8-K 
cikList 
xs:string 
9876543210 
cikNameList 
xs:string 
9876543210,3333333333 
forceUtrValidation 
xs:boolean 
false 


6
Interactive Data Public Test Suite, Version 77-260316, Page 6 of 32 
ELOParams 
xs:string 
(JSON 
object) 
{"submissionType" : "S-1", 
"exTransitionPeriodFlag" : true,   
"emergingGrowthCompanyFlag" : true,  
"smallBusinessFlag" : false} 
 
Testcase e60524 uses parallel lists of CIK and entity names.  The delimiter for cikList is the comma character “,” 
and the delimiter for cikNameList is the seven character sequence “|Edgar|”.  Thus the following elements declare 
that the first CIK has company name “ABC & DEF LLC” and the second has company name “THI!S\$TR@NGE 
N#ME=:;.” 
<conf:parameter name="ELOparams" value="{&quot;periodOfReport&quot;: &quot;12-31-
2008&quot;, &quot;submissionType&quot;: &quot;8-K&quot;, 
&quot;cikList&quot;:&quot;9876543210,3333333333&quot;, &quot;cikNameList&quot;:&quot;ABC 
&amp; DEF LLC|Edgar|THI!S $TR@NGE N#ME=:;.&quot;}" 
xmlns="" 
xmlns:conf="http://edgar/2009/conformance" /> 
 
Testcase e60535 uses the parameter forceUtrValidation set to true, so that each instance will be validation with 
Unit Type Registry validation enabled no matter whether the instance DTS contains element “UTR” in a standard 
namespace. 
Majority of the test cases use the parameter ELOParams (EDGARLink Online Parameters), whose value is a JSON 
dictionary with the paired submission header element names and their values. The double-quote character must be 
represented in the xml file as &quot;. 
<conf:parameter xmlns="" xmlns:xs="http://www.w3.org/2001/XMLSchema" name="ELOparams" 
datatype="xs:string" value="{&quot;submissionType&quot; : &quot;S-1&quot; ,    
&quot;exTransitionPeriodFlag&quot; : true,  &quot;emergingGrowthCompanyFlag&quot; : 
true, &quot;smallBusinessFlag&quot; : false}"/> 
7.6 Optional repeating element <primary> 
The file name of a non-image file type unrelated to XBRL. Its file name may be any EDGAR compliant file name 
ending in .txt, .htm, or .pdf, and it is meant to indicate that the file is the primary document of an EDGAR 
submission. 
7.6.1 Optional attribute @docType of <primary> 
The document type (in the EDGAR submission sense) of the document, for example, "10-K", "485BPOS". 
7.7 Required element <instance> 
The local file name of the instance must be an EDGAR compliant file name (less than 24 characters, etc). By 
convention the name is formatted as: 
e6{section}{section}[0-9]{3}((gd)|(ng))-200(8|9)1231.xml 
For example e60501001ng refers to a no good instance violating Manual section 6.5.1. 
By convention, instances that have the date part 20081231 use the 1.0 DEI taxonomy and those with date part 
20091231 use the 2009 DEI taxonomy. 
The attribute @readMeFirst must be “true”. This attribute indicates to a test script that it is the instance file that is 
first opened by the validator being tested. 
7.8 Optional attribute @exhibitType of <instance> 
The exhibitType is a normalized string that defaults to and must be one of the exhibit types that names an XBRL 
instance, including: 
 
EX-100 
(This is an obsolete value) 
EX-101 
(This is the default value) 
EX-99.K SDR 
 
EX-99.L SDR 
 
 
7.9 Optional repeating element <linkbase> 
Every variation has linkbases named using the same naming convention as the instance.  


7
Interactive Data Public Test Suite, Version 77-260316, Page 7 of 32 
Many testcase variations have a set of common linkbases named edgar-20081231_*.* or edgar-20091231_*.*. 
Identically named “edgar-” linkbase files differ from folder to folder. 
7.10 Required repeating element <schema> 
Every variation has at least one schema with its own set of linkbases named using the same naming convention as 
the instance.  
Usually a variation has exactly one schema. Rarely, in section 608-schema-syntax or elsewhere, the nature of the 
testcase may necessitate more than one schema. 
Many testcase variations have a set of common schemas named edgar-20081231.xsd, edgar-20091231.xsd or 
edgar-20111231.xsd. Identically named “edgar-” files may differ from folder to folder. 
7.11 Optional repeating element <exhibit> 
The file name of a non-image file type unrelated to XBRL. Its file name may be any EDGAR compliant file name 
ending in .txt, .htm, or .pdf, and it is meant to indicate that the file is a non-primary document of an EDGAR 
submission. 
7.11.1 Optional attribute @docType of <exhibit> 
The document type (in the EDGAR submission sense) of the document, for example, "10-K", "485BPOS". 
7.12 Required element <result> 
For a “no good” variation the result element contains at least one <assert> element.  
For a "good" variation the result element may contain an <instance> element. 
The element is otherwise empty. 
7.12.1 Optional attribute @expected of <result> 
When the expected result is to be valid with no warnings or other messages, the @expected attribute may have 
the value "value". 
7.13 Optional repeating element <assert> 
The assert element contains information used to group information about the error or warning message expected 
upon validation.  
7.14 Optional repeating element <error> 
This element is used in the Filing Fee Exhibit test cases. The error element contains text indicating the expected 
validation code that a variation will produce. 
8 
The <assert> element 
The assert element declares the severity, associated EFM section and mnemonic error code to be generated. The 
element allows any other attributes to appear that the author of the variation may deem useful1. 
8.1 Required attribute @severity of <assert> 
There are two values, the most common one being “err” and the other “wrn” meaning a warning. In the EDGAR 
system, a warning does not cause the XBRL files to be stripped from a submission; an error does. 
8.2 Required attribute @num of <assert> 
The syntax is the same as the <number> element content without the dash. It is not identical because in rare 
cases the @num may differ from the testcase file where it appears, as for example when one error could not occur 
without triggering another. 
 
1 The syntax of <assert> is syntactically convertible to that used by the XBRL International Formula 1.0 Specification 
(http://www.xbrl.org/SpecRecommendations/). 


8
Interactive Data Public Test Suite, Version 77-260316, Page 8 of 32 
8.3 Required attribute @name of <assert> 
A mnemonic code with dash-separated proper case tokens such as “No-Presentation-Order”.  Tokens are strictly 
proper case, for example, “No-Xml-Base-Allowed” even for the error concerning attribute “xml:base”, or “Illegal-
Html” for errors concerning HTML. 
8.4 Optional attribute @frd of <assert> 
A two-letter code for a related group of assertions; this appears in error codes as reported by EDGAR, such as 
“60515-cp-No-Xml-Base-Allowed”. 
8.5 Optional attribute @countSatisfied of <assert> 
Defaulting to 0, this indicates the number of satisfied assertions in the variation. 
8.6 Optional attribute @countNotSatisfied of <assert> 
Defaulting to 1, this indicates the number of assertion violations in the variation. 
9 
Notes on the folder structure and file details 
There are a few exceptions to the mapping from Manual subsections to the test suite.  There are no test cases for 
sections of the manual marked “Reserved”. 
At this time, there is incomplete coverage of these syntax sections of the Manual: 
• 
603-filing-syntax (some subsections require information such as the attachment type (EX-100, EX-101) 
that is not available from the content of the XBRL files themselves. Some of these test variations are 
contained in directory sto – meaning these are for EDGAR system test only, and these cannot be validated 
using offline testing).  
• 
There are no separate tests for 605-06, 605-18, 605-26, 607-02, 607-05, 607-06, 609-02, 609-08, 610-
07, or 612-04 because these sections do not have their own unique error codes. 
Two files in folder 603-04-no-html-character-entities are not well-formed XML; this is intentional (e60304001ng, 
e60304002ng-20081231_lab.xml). 
There is no coverage of these semantic sections because they do not at this time result in EDGAR warning or error 
messages: 
• 
606-instance-semantics 
• 
608-schema-semantics 
• 
611-label-semantics 
• 
613-presentation-semantics 
• 
615-calculation-semantics 
• 
617-definition-semantics 
• 
619-reference-semantics 
There are no such subsections 6.22.1 through 6.22.4 in the Manual; these correspond, respectively, to the three 
issues covered by section 6.22 and the current contents of the 
http://www.sec.gov/info/edgar/edgartaxonomies.xml file. 
 
10 Notes on 6.16 Definition Syntax Subsections 
Subsections 6.16.4, 6.16.6, 6.16.7, and 6.16.8 can be difficult to interpret without further technical explanation.  
Their test cases are illustrated and explained in the figure below. 


9
Interactive Data Public Test Suite, Version 77-260316, Page 9 of 32 
6.16.4
6.16.5
6.16.7
6.16.8
X Disallowed 
→ Required
Remarks
Section text
All
R1
All
R1
HC1
HC2
P1
6.16.5 The DTS of an instance 
must contain in each base set, for 
each source element, at most one 
effective relationship with an 
xlink:arcrole attribute equal to 
‘http://xbrl.org/int/dim/arcrole/all’. 
This was intended to prevent 
unioning of hypercubes so as 
to simplify other constraints.
Because of primary item 
inheritance, this rule only rules 
out the simplest violations.
6.16.4 The xlink:arcrole attribute 
‘http://xbrl.org/int/dim/arcrole/
domain-member’ and 'http://
xbrl.org/int/dim/arcrole/dimension-
domain' must have no undirected 
cycles in any Directed Relationship 
Set as defined in XBRL 
Dimensions 1.0. 
This is called “no tangled 
domains”.  It applies to every 
DRS starting from a DimDom 
relationship.
DimDom relationships in 
different base sets can never 
be the source of a violation of 
this rule.
6.16.7 An axis of a negative table 
must appear in a positive table in a 
definitionLink having an equal 
value of xlink:role. 
An Axis cannot appear as an Axis 
of a negative hypercube (that is, 
axis excluded from a table) unless 
there are members of that Axis in a 
positive table. 
Formally, an axis element that is the 
target of an effective relationship 
with arcrole equal to ‘http://
xbrl.org/int/dim/arcrole/hypercube-
dimension’ that is consecutive from 
a relationship with arcrole ‘http://
xbrl.org/int/dim/arcrole/notAll’ 
must also be the target of an 
effective relationship in a 
link:definitionLink having the same 
value of xlink:role and which itself 
is consecutive from an effective 
relationship with xlink:arcrole 
attribute equal to ‘http://xbrl.org/
int/dim/arcrole/all’. 
6.16.8 The target of an effective 
relationship with an xlink:arcrole 
attribute equal to ‘http://xbrl.org/
int/dim/arcrole/notAll’ must not be 
the target of an effective arc with 
an xlink:arcrole attribute equal to 
‘http://xbrl.org/int/dim/arcrole/all’ 
in link:definitionLink elements 
having equal values of xlink:role. 
This rule ensures that a Table 
(hypercube) is not both positive 
and negative. 
This rule is intended to 
ensure that the notAll 
relationship does not forbid 
members of a dimension that 
is not even relevant to a 
hypercube. 
DomMbr relationships 
between P1 and P2 are not 
relevant, since neither all nor 
notAll are ever consecutive 
from DomMbr.
Note that the rule assumes, 
but does not require, that the 
target roles on HcDim1 and 
HcDim2 are different, so that 
the members of Dim1 are 
different in HC1 and HC2.
All
R3
→R2
NotAll1
R1
→R2
P2
HC2
P1
X
HC1
Dim1
HcDim1
R2
HcDim2
R2
NotAll
R1
All
R1
X
P1
HC1
P2
This rule complements 6.16.7 
by ensuring that HC1 and HC2 
are distinct.
The combination of this 
constraint, 6.16.4, and XBRL 
Dimensions 1.0 constraint’s 
prohibition of undirected cycles 
in HcDim relationships 
prevents using @targetRole to 
give the same HC element 
different members of the same 
axis.
→
DomMbr1
R1
DomMbr2
R1
→R2
M3
X
M1
M2
DomMbr3
R2
Dim1
DimDom1
R1
LEGEND
DimDom = dimension-domain
DomMbr = domain-member
HcDim = hypercube-dimension
R1,R2,R3 = Role
→R2 = Targetrole is R2
HC1 = Hypercube element
P1,P2 = Primary element
 
11 Contacts 
Developers with questions, bug reports, or suggestions for additional variations to improve coverage should 
contact StructuredData (at) sec.gov. 


10
Interactive Data Public Test Suite, Version 77-260316, Page 10 of 32 
The SEC cannot guarantee a response to every communication. Before sending a bug report, check for the latest 
version and check the Interactive Data FAQ (https://www.sec.gov/structureddata/FAQs).  
12 Index 
CIK, 5 
DEI taxonomy, 6 
DTD, 2 
DTS, 5 
ENT, 2 
EXG, 1 
Manual, the, 1 
OSD, 4 
testcase, 3 
Text Block, 2 
UTF-8, 2 
variation, 4 
XBRL Footnote, 2 
XSL, 2 
 
13 Change Log 
 
Version 
Changes 
13-
090917 
- 
13-
091021 
Change of namespace to http://edgar/2009/conformance. 
Addition of index.htm, testcases.xml, and errors.xml. 
Improved alignment of error codes listed in xbrlerrors.htm and the error codes in the testcase files.  
Change of @num on e60502000ng to agree with others in the same file. 
edbody.dtd: attribute ‘cite’ is no longer allowed on element ‘blockquote’.  
Remark added to e61404 due to discrepancy between wording in the manual and results of variation 
007gd. 
Remark added to e61006 to clarify the ‘normalized string’ requirement. 
Three new variations in e60516 to exercise validation of HTML text block bodies against the DTD. 
These test variations were corrected so that they are more likely to produce only the error being 
tested: 
e60306101ng 
e60306103ng 
e60502001ng 
e60502003ng 
e60523001ng 
e60523002ng 
e60903016gd 
e60904000gd 
e60904001ng 
e60907001ng 
e61003002ng 
e61003003ng 
e61004001gd 
e61004003ng 
e61403000gd 
e61404003gd 
e61602000gd 
e61603001ng 
e61604001ng 
e61604006gd 
e61604009gd 
e61608001gd 
e61609000gd 
e62202033ng 
13-
091128 
testcases.xml: removed references to nonexistent folders. 
e61403000gd: removed as unnecessary. 
e603061**: removed because redundant with e622***** variations. 
e603064**: removed because redundant with e622***** variations. 
e603115**: removed because redundant with e622***** variations. 
e60403004ng: corrected redundant labels. 
e60502001ng, e60502002ng: corrected irrelevant facts in instance. 
e61006002ng: corrected redundant labels. 


11
Interactive Data Public Test Suite, Version 77-260316, Page 11 of 32 
Version 
Changes 
e61609000gd: corrected so as not to have ineffectual arcs. 
edbody.dtd: corrected to disallow attributes cite, char, and charoff for consistency with EFM 5.2.2.2. 
e60516013ng, e60516014ng: corrected redundant labels. 
605-16-html-limited-testcase.xml: Corrected namespace and corrected e60516015ng and 
e60516016gd for consistency with edbody.dtd 
e60709: added variation e60709000gd to cover mark characters and variation e60709002ng to cover 
case-sensitivity. 
13-
091201 
e60403005ng and e60403006ng added to catch XBRL 2.1 validity. 
13-
100104 
Removed spurious <err> element from variation e60709000gd. 
13-
100303 
Removed e61602 because it is redundant with Dimensions 1.0. 
 
14-
100405 
Moved dei:EntityCommonSharesOutstanding tests from e60521 to e60526; warning conditions 
changed but code name unchanged. 
Renumbered e60520, e60521 variations and removed their dependence on the us-gaap 2008 element 
schema. 
Removed e60531 which required an order attribute on footnoteArc and removed error du-0531-
Footnote-Relationship-Order from xbrlerrors.htm. 
Updated e6220{1,2,3,4} to test for taxonomy RR 2010. 
Changed all dei:DocumentType contents to 8-K except in e605** test cases where dei:DocumentType 
is relevant to the rule. 
Tests e60511 corrected to remove unused unit declarations and added facts to use all declared units. 
*-testcase.xml: Updated to have XHTML-formatted equivalent of EFM v14 DRAFT contents. Added 
lib/descriptions.htm consolidating the HTML version of all rules in the suite. 
14-
100406 
e60704007ng: content corrected to use invalid ISO date “2009-9-12”. 
e60403007gd: added Dimensions 1.0 common domain test. 
14-
100409 
e60521***: Removed stray N-1A document type occurrences. 
/lib folder: From http://www.sec.gov/info/edgar/ folder, added edgartaxonomies.xml and erxl.xsd. 
14-
100630 
e60515005gd: DocumentType set to 8-K to avoid 6.5.26 violation. 
e60530000ng: DocumentType set to 8-K to avoid 6.5.26 violation. 
e60703: added missing <assert> elements to variations. 
e60703006ng: added ‘xbrl.sec.gov’ to reserved authority names. 
e60903017gd: Changed URI to not violate a ‘should’ condition in 6.7.9. 
e6100600*: DocumentType set to 8-K to avoid 6.5.26 violation. 
e6100800*: DocumentType set to 8-K to avoid 6.5.26 violation. 
e61603: Added remark regarding the need to evaluate with respect to primary items, not just presence 
of dimensions. 
e62202033ng, e62202054ng: Corrected Schema and XBRL 2.1 errors. 
e62203024ng, e62203034ng: Cases covering RR 2010 taxonomy. 
 
16-
110210 
For all variations in all test cases, removed unnecessary units, facts, and unnecessary dependencies 
on us-gaap taxonomy schemas. 
edgartaxonomies.xml: add XBRL International recommended roles, arc roles and types 
e60403: add variation 011ng formerly e60901001ng 
e60510: add variation clarifying that an instance has to be 24 hours and 1 second or more after the 
start of any duration 
e60510: correct testcase file which had incorrect files included 
e60515: new variations covering nonnum:textBlockItemType 
e60516: add variation for when an xmlns attribute appears 
e60523: add variation 004ng to test parameter – cik mismatch 
e60535: new test case and variations for new section 
e60713: add variation for fact-explanatoryFact 
e60714: remove variation 000gd 
e60728: new variations covering nonnum:domainItemType 
e60728: update to match edgartaxonomies.xml namespace authorities 
e60722: removed 


12
Interactive Data Public Test Suite, Version 77-260316, Page 12 of 32 
e60703: reflect changes in edgartaxonomies.xml 
e60704: reflect changes in edartaxonomies.xml 
e60901: move variation 001ng to e60403 as an xlink-level validation 
e60903: remove files not needed in variations 000, 004, 011 – 016 
e60904: remove 000gd and files not needed 
e61005: remove redundant variations for namesepace authorities 
e61604: add variations 014 – 018, removing 010 for clarification 
e61604: remove ‘good’ variations 006, 007, 008, 009 
e61604: add ‘nogood’ variations 010, 011, 012, 013 
e61605: use rr 2008 in preference to ici 2006 
lib/error.xml: add error codes 
Many schemas: add elementDefaultForm=’qualified’  
Many instances: change units for better alignment with forthcoming XBRL International Unit Type 
Registry 
Many files: change to encoding="US-ASCII" 
16-
110225 
Added detail in the ‘Library Files’ section of this document about the edgartaxonomies.xml file and 
others. 
Corrected EntityRegistrantName to match variation name in some 30 instance files. 
e60703, e60716, e62201: clarify that these tests use local copy of 
edgartaxonomies.xml. 
e60311: correct variation 512ng to use a smaller set of linkbases. 
e60403: correct instance to match variation 009gd’s intent. 
e60510: correct period date to avoid warning message. 
e60515, e60530, e61405: indicate where EFM has not yet been 
corrected to reflect validation intent. e60520: split variations into those which use 2008 dei taxonomy 
and 
those which use 2011 dei in which DocumentType is enumerated. 
e60521: remove EntityCommonSharesOutstanding variations. 
e60530: add remark confirming that EFM 16 has incorrect text. 
e60725: correct 001ng which had a schema validation error. 
e60728001ng: change context end date to avoid warnings. 
e60901: remove testcase entirely, it is now covered by e60403. 
e61203: correct variation 009 description. 
e62202, forbidden.xml: correct bad invest-doc linkbase reference. 
 
18-
111004 
e60302, e60521: Make the order of attribute values in assert elements of test case files consistent, to 
facilitate comparisons. 
e60302001ng: correct bad namespace prefix declaration. 
e60305: add a variation 003gd containing all allowed EDGAR characters and a variation 004ng 
containing the disallowed no-break space character. 
e60306: edit explanatory text for change made in EFM v17. 
e60403: add variation 012gd for prefix ‘dei’ assigned to a namespace other than a dei namespace, 
variation 016ng to catch empty xlink:href attribute, and variations 013, 014, 015 to test handling of 
default and fixed attributes on fact values and decimals attributes. 
e60507001ng: remove dei:DocumentReportType which was deprecated 
e60512: remove facts of deprecated dei:DocumentReportType 
e60513:  remove facts of deprecated dei:DocumentReportType 
e60514: change variations 001gd and 002gd to use en-US, add new variations 004ng and 005ng with 
the same instances, because those are now ng.  Remove dei:DocumentReportType facts. 
e60515: add three variations 013gd, 014ng in which there is an xml comment in the middle of a text 
block. 
e60516: add variation 024ng in which xml comment interferes with testing of prohibited EDGAR 
content.  Remove dei:DocumentReportType facts. 
e60519: in remarks, add 10-KT and 10-QT 
e60526: add variations covering 10-KT and 10-QT. 
e60530: remove remark that only applied to EFM v16.  Change variation filenames to be like all other 
testcases. 
e60536: add new testcase for newly added rule EFM 6.5.36. 
e60704: remove redundant variation and renumber removing 008ng. 
e60717: add variation to ensure that id for x:y is not x_y27. 
e60721: use element type xbrli:decimalItemType to avoid redundancy with syntax detail embedded in 
semantic rule 6.8.17. 
e60727: change testcase description text to match EFM text. 
e60729: add testcase for new syntax rule 6.7.29. 


13
Interactive Data Public Test Suite, Version 77-260316, Page 13 of 32 
e60730: add testcase for new syntax rule 6.7.30. 
e60903: correct typo in rule text. 
e61001: Add two new variations to test the heretofore untested case of a used fact (and member) with 
only an "en" language label. 
e61004: Change xml:lang of "fr" to "en" in variations to reinforce that the rule applies only to "en-US" 
labels.  Remove empty definition linkbase from variation e61004001gd. 
e61405: add variation 012gd to make explicit "any other element".  Remove remark regarding addition 
of the word "role" in the rule. 
e61603: correct capitalization in text of rule. 
e61604: add variation 019ng for tangled domain in primary items.  Change phrase "Domain (or 
Member)" to "domain members". Remove empty presentation linkbase from variation 002gd. 
e62203: add text to description of testcase to clarify testcase intent. 
asserts.xml: add new file consisting of all variation assertions. 
descriptions.htm: updated with descriptions to match EFM v18. 
errors.xml: comment out error for e60722 and correct typo in 6.22.0 
testcases.xml, testcases.htm: update with 6.5.36, 6.7.29, and 6.7.30 
test.xsd: relax restriction in EDGAR file names to allow URI’s ending in EDGAR file names.  Allow 
additional elements "info" "result" and open content model to the "variation" element. 
18-
111021 
e60403: edited text of rule to correspond with EFM text.  Removed variation 009gd until such time the 
UTR validation trigger condition can be included correctly; see 6.5.35. 
e60515: added variations 014, 015, and 016 with additional comment placements in text blocks, and 
removed definition linkbases. 
e60516: added variations 025, 026, and 027 with additional comment placement in text blocks, and 
removed definition linkbases. 
e60729: removed definition linkbases as irrelevant to the testcase. 
e60730: removed variations in which targetNamespace contained two-byte characters.  Removed 
definition linkbase as irrelevant to the test case.  Edited remarks. 
e60526: added variations in which there are no definition links. 
e60534: added variations 5 and 6 in which quoted but disallowed HTML appears harmlessly as strings; 
removed definition links. 
e60535: added variation 999gd to make explicit that 6.5.35 is relevant only when element “DTS” 
appears in a standard namespace.  Added remark that this means validators will not be able to 
distinguish the good from nogood variations until they are revised with a DTS element in a standard 
namespace.  Removed all definition linkbases as irrelevant to the testcase. 
18-
111122 
60305: Add variation 005ng with disallowed EDGAR circumflex (x5E). 
60403: Add variations 017gd and 018gd in which measures without namespaces are okay, and 019ng 
to test for gYear not 4 digits. 
60515: Use CDATA instead of ampersand quoting in text block. 
60516: Correct problem of missing text block text in 023ng. Use CDATA instead of ampersand quoting 
in text block. 
60520: Add 10-QT, 10-KT, POS AM to remarks 
60521: Add 10-QT, 10-KT to remarks and to variations 
60535: Add parameter forceUtrValidation to all variations but 999gd.  Add documentation of 
forceUtrValidation to section 7.5.5 above. 
60536: Change variations using multibyte Unicode characters so as to use only 2-byte Unicode 
characters.  Correct text to match final EFM text.  Correct variation 025ng description. 
61202: Remove dependence of 000gd on edgar-20081231.xsd file. 
62202: Correct missing imports. 
18-
120102 
62201: Add us-gaap and sec 2012 taxonomies to edgartaxonomies.xml 
62202: Change forbidden.xml list to include some 2012 entries 
62203: Add cases of incompatibilities using 2012 namespaces. 
18-
120228 
61006: Add variation 005ng for consecutive whitespace. 
60509: Correct namespace binding for empty prefix on <parameter> 
60510: Correct namespace binding for empty prefix on <parameter> 
60520: Correct namespace binding for empty prefix on <parameter> 
60521: Correct namespace binding for empty prefix on <parameter> 
60523: Correct namespace binding for empty prefix on <parameter> 
60524: Correct namespace binding for empty prefix on <parameter> 
60535: Correct namespace binding for empty prefix on <parameter> 
60904: remove unnecessary <parameter> element 
 
22-
130110 
lib/test.xsd: Allow an <image> input to a variation and allow uppercase characters and repetitions of 
underscore and dashes in file names, as EDGAR now allows. 


14
Interactive Data Public Test Suite, Version 77-260316, Page 14 of 32 
e60303: New test case covering valid file names 
e60306: Remove dependence on dei 2009 linkbases. 
e60403019ng: Change variation file names to 2012 
e60403020ng: New variation tests for missing preferred label. 
e60403: Update all dei-2011 to dei-2012. 
e60509, e60510: Simplify linkbase files used 
e60509, e60510: replace document type 'Other' with '497' 
e60509008gd: New variation making 24h duration valid. 
e60510001ng: change CIK 
e60510002ng: change CIK 
e60515000gd: Add a legal right bracket character. 
e60515004gd, e60515005gd, e60515006gd: Delete 
e60515007gd to e60515011gd: Update from dei 2009 to 2012 
e60515008ng: New variation tests for DOCTYPE in text block body. 
e60515: Update variations from dei 2011 to 2012 
e60516011gd: Provide the jpg image referenced in the text block. 
e60516015ng: Removed irrelevant nested table 
e60516016gd: Add a gif and jpg image to the text block. 
e60516018ng through 21ng: Update variations from dei 2009 to 2012. 
e60516028ng: New variation checks for undefined entity. 
e60516030ng: New variation with nested table 
e60516: Change .gif and .jpg file names to match instances. 
e60516: Clarify that nested tables are not detected by DTD 
e60516: Update variations from dei 2011 to dei 2012. 
e60519: Remove dependence on dei 2009. Edit to Remarks. 
e60520002ng: Change from dei 2008 to dei 2011 
e60520010ng-014ng: Remove variations and edgar-20081231 files. 
e60520: Many new variations covering additional submission types. 
e60520: Simplify linkbase files used 
e60520: Update the submission-to-document type table for dei 2012. 
e60521: Change document type ‘NCSR’ to correct value ‘N-CSR’ 
e60521: Simplify linkbase files used 
e60524: change variation names where case-insensitivity is important. 
e60525: Remove dependence on dei 2009. 
e60526: Change document type ‘NCSR’ to correct value ‘N-CSR’ 
e60526: Simplify linkbase files used 
e60534000gd: add a gif to the text block. 
e60534007ng: New variation testing absent image file 
e60534008ng: New variation testing invalid image file 
e60535998gd: New variation testing energy item type 
e60535999gd: Correct description so it refers to EEK currency. 
e60535: Edit remarks regarding UTR element triggering validation. 
e60704008ng: New variation tests for missing authority in namespace with only a date. 
e60707003ng: New variation tests for missing namespace prefix. 
e60727: Remove dependence on dei 2009 linkbases. 
e60728: Remove dependence on dei 2009 linkbases. 
e60903018ng: New variation tests for ineffectual calculations. 
e60903: Remove unused namespace prefix declarations. 
e60903: Variations 000gd, 004ng, 017gd change dei 2008 to 2009. 
e60909000gd: Remove dependence on dei 2009. 
e60909: Change use of rr-ent to rr-def 
e61001: change element labels to avoid spurious LC3 warnings. 
e61604000gd: Change dependence on rr 2008 to rr 2012. 
e61604: Change use of rr-ent to rr-def 
e61605000gd: Change dependence on rr 2008 to dei 2009 schema only 
e61605000gd: Variation removed, applied only to rr 2008. 
e61605001ng: Update from dei 2011 to dei 2012 
e61605031ng: New variation testing absent image file 
e61605032ng: New variation testing invalid image file 
e61607003ng: Change dependence on rr 2008 to dei 2009 schema only 
e61607003ng: Variation removed, applied only to dei 2009. 
e62201: Remove files from US GAAP 1.0, SOI 2008, RR 2008. 
e62202: Add files in US GAAP 1.0, SOI 2008, RR 2008. 
e62203: Remove variations involving US GAAP 1.0, SOI 2008, RR 2008 


15
Interactive Data Public Test Suite, Version 77-260316, Page 15 of 32 
22-
130206 
e60306304ng: Correct xpointer reference. 
e60311: Corrections to testcase file.  Remove variations that would be invalid because the XBRL 
linkbase schema does not allow xml:base attributes to appear. 
e604030004ng, e60504000gd, e60504002ng, e60507001ng, e60509001gd, e60509002gd, 
e60509003gd, e60509005ng, e60510007gd, e60519002gd, e60519003gd, e60527000ng, 
e60527001ng, e60527002ng, e60527003ng, e60527004ng, e60532000ng, e60701000ng, e60535*: 
align the document period end date with the required context end date. 
e60504,e60505: Add schemalocation attribute to linkbases. 
e60534000gd: Change gif image filename. 
e60903: Add remarks in testcase file concerning 018ng. 
e60903018ng: Correct typo in testcase file. 
e60903019ng: Add variation in which arc priorities are equal. 
e60903020ng: Add variation in which standard arc has lower priority. 
 
23-
130412 
Throughout: Update to the dei-2013 schema in any variation that does not depend on some earlier dei 
version, and remove dei elements EntityInformationCurrentLegalOrRegisteredName and 
DocumentReportType that were deprecated in 2012. 
lib/edgartaxonomies.xml: Remove us-gaap Family 2011 version, replace with us-gaap Family 2013 
version. 
e60403021gd: New variation in which a namespace has two schemas. 
e60403024ng: New variation in which the date 31 November appears. 
e60403025ng: New variation in which a schema import is missing. 
e60403026ng: New variation in which xsi:nil is absent from empty fact. 
e60535000gd: Add units MWh, etc.  Add a decimalItemType case. 
e60535001gd: Add units MWh, etc. Add a decimalItemType case. 
e60709000gd: Change URI because /role/ and LC3 are unimportant. 
e60710: Clarify remark to indicate which schema is being referred to. 
e62201, e62202, e62203, e62204: Retire Family us-gaap 2011. 
23-
130426 
e6040327ng: New variation testing a data type error. 
e6040328ng: New variation testing a unitRef attribute error. 
e6040329ng: New variation testing a missing namespace error. 
e6040330ng: New variation testing a bad footnote xlink:role value. 
e60528002gd: Correct bad footnote xlink:role value. 
e60907001ng: Correct reference to us-gaap 2011 element. 
e62202026ng: Remove conflict between dei-2011 and dei-2013 
e62202027ng: Remove conflict between dei-2011 and dei-2013 
 
24-130611 e603: Correct typo in assertion elements. 
e61801, e61802: Remove @xlink:role from reference locators. 
e62201007gd: New variation testing RXD family files. 
e623: New cases e62301 through e62309 and e62311 to e62344. 
24-130710 e62201003gd: Remove negated-2008-03-31.xsd import 
e62202: Add negated-2008-03-31.xsd to sample forbidden list 
e62202: Reduce the number of variations from 54 to 20. 
e62201007gd: Remove variation. 
e623: Remove all test cases. 
 
25-131024 errors.xml, errors.htm: Update the error code list for the web site. 
e60305001ng: Correct build problem resulting in an empty instance. 
e60905000gd: Update negated-2008 reference to negated-2009. 
e62202007ng: Remove unnecessary import. 
e62202011ng: Correct missing namespace attribute on import. 
e62202013ng: Correct missing namespace attribute on import. 
 
27-
140205 
Throughout: Update to the dei-2014 schema in any variation that does not depend on some earlier dei 
version, update to EFM v27. 
edgartaxonomies.xml, erxl.xsd: add required “version” attribute to indicate the EFM version, initially 
27. 
edgartaxonomies.xml, externals.txt: Remove 2012 US-GAAP Family version, replace with 2014 US-
GAAP Family version. 
errors.xml, errors.htm: Update with new error codes. 
e60403011ng: New variation testing context validity. 
e60504: Correct instances that would otherwise trigger 6.7.31. 


16
Interactive Data Public Test Suite, Version 77-260316, Page 16 of 32 
e60509: Edited all variations to relax the restrictions on contexts of one day and affirm that dimensions 
in contexts and document type have no impact on this rule. 
e60510: Removed rule and test cases. 
e60537: Test new error code for nonzero digit truncation. 
e60538: Test new error code for contexts using the forever period. 
e60731: Test new error code for custom fraction item types. 
e60905000gd: Correct minor typo in testcase file. 
e61009: Test new error code for numeric label roles. 
e609*,e610*,e612*,e614*,e616*: Correct usage of a nonnumeric abstract element with a numeric 
label role. 
e60507*,e60509*,e60516*,e60712*,e60725*,e60727*, e60905*, e61604*, e61609*: Correct 
EntityRegistrantName value.  
27-
140220 
doc/chapter6.htm: A subset of file conf/descriptions.htm that contains the draft text chapter 6 for the 
EFM version. 
e60520007ng: Correct missing contextRef attribute. 
e6052202*: Add remark regarding error cascades. 
e60516*,e60536*, e60703*, e60716*, e62201*, e62202*: remove relative anchor hrefs from the 
testcase files. 
e60511*: Remove obsolete remark from testcase. 
lib/utr.xml, lib/utr.xsd, lib/render.xsl: add UTR files. 
e60535*: Add new variations to cover units added to UTR 2013-05-17 since UTR 2012-11-30. 
27-
140327 
e60732*: New testcase. 
lib/errors.xml, lib/xbrlerrors.htm: Correct typos and add error du-0732. 
27-
140514 
e60718000gd: New variation covering the case of a non-xbrl element. 
e60732021gd: New variation covering the case of a non-xbrl element. 
 
29-
141217 
e60306609ng: Remove spurious xlink:role on reference locator. 
e60311, e60403, e60727, e60903: Remove unnecessary namespace prefix bindings. 
e60403032ng, e60403033ng, e6040334ng, 6040335gd: New variations to distinguish between floats 
(can have NaN, INF) and decimal types. 
e60503002ng: Remove unnecessary variation. 
e60509007gd: Correct the testcase text so as not to suggest that the result is in some way dependent 
on the document type. 
e60509012ng: New variation which seems similar to e60509004ng but receives a different result on 
some validators. 
e60526: update us-gaap version from 2013 to 2015. 
607-testcases.xml and others: Correct to list testcase 607-32. 
e60731002gd: New variation to confirm that type declaration equivalence is allowed; use of the 
specific type xbrli:fractionItemType is not. 
e62201: Update to include us-gaap and exch 2015 schemas. 
e62202: Update to exclude us-gaap and exch 2013 schemas. 
e62203: Remove unnecessary variations referencing dei-2012. 
errors.xml, warnings.xml: Update files to correspond to currently emitted errors and warnings. 
 
31-
150505 
e62203007gd: Add variation making explicit that dei-2014 can be used with rr-2012. 
e62201, externals.txt: Update to indicate that country-2012, currency-2012, invest-2012 will 
continue to be allowed. 
31-
150529 
e60537005ng: Add variation with positive values of the decimals attribute. 
e62201002gd: Remove erroneous references to 2013 and 2014 schemas. 
 
35-
151113 
e60306309ng, e60306609ng: remove, because invalid href to reference linkbases cause other EFM 
errors. 
e60308: add exhibitType attribute to allow multi-instance testing 
e60308001ng: New variation to distinguish multiple instance cases. 
e60310: New test case for EFM section 6.3.10. 
e60403021gd, e6043035gd: Remove unnecessary axes from presentation linkbase. 
e60512004ng, e60512006ng: remove, because these variations no longer violate section 6.5.12. 
e60512009gd, e60512010gd, e60512011gd: add variations illustrating cases where redundant facts 
are allowed (duplicates having the same values). 
e60513001ng: Change the C-equal facts so that they are not V-equal. 
e60516033ng: Add variation clarifying that images on the SEC web site cannot be referenced, only 
local images, as per EFM page 5-12. 
e60520: Remove unnecessary axes from presentation linkbases. 


17
Interactive Data Public Test Suite, Version 77-260316, Page 17 of 32 
e60523: Remove variations referencing ratings-2009 files. 
e607: Correct all element declarations to have capitalized names. 
e60706000gd: Remove unnecessary axes from presentation linkbases. 
e60729: Remove unnecessary axes from presentation linkbases. 
e60903017gd: Remove unnecessary axes from presentation linkbase. 
e61206: New test case for warning about multiple presentation roots. 
e61207: New test case for warning about mismatched preferred label roles. 
e61208: New test case for warning about axis without a domain child. 
e61209: New test case for warning about incomplete unit ordering. 
e61405012gd: Correct warning about multiple presentation roots. 
e62203: Remove unnecessary axes from presentation linkbases. 
e62601: New test case for warning about all facts being filtered. 
e62602: New test case for warning about incomplete instant - duration -instant fact patterns. 
e62603: New test case for warning about incomplete statements of changes in equity. 
e62604: New test case for errors in embedding command syntax. 
e62605: New test case for errors in missing rows or columns of embedding commands. 
e62606: New test case for warning about incomplete ordering of rows and column axes in an 
embedding command. 
e62607: New test case for warning about empty bar chart commands. 
e62608: New test case for warning about too many bar chart facts. 
e62609: New test case for warning about {Elements} token and primary axis on rows. 
e902: Test cases with variations specific to Form SDR in subfolders 60302, 60308, and 60524. 
 
35-
151218 
errors.xml: Update with error codes for multiple SDR attachments. 
e60305006ng: Add variation testing for XML BOM. 
e605...e626: Correct -testcase.xml files to match page and section numbers, and edit to match latest 
EFM v35.  
e60524: Correct file names in variations 004 and 005. 
e61207: Remove spurious edgar-* linkbases from testcase. 
624-rendering, 624-rr-rendering: Add new samples that exercise each rendering feature described in 
EFM sections 6.24 and 6.25.   
626-rendering-syntax: Add new test cases to exercise rendering syntax errors and warnings. 
902-sdr/60302: correct CIK and doc types on the first and second L SDR attachments so as not to 
raise errors unrelated to 6.3.2. 
902-sdr/60524: New test case and variations for detecting inconsistent CIK and registrant names in 
multiple L SDR attachments. 
902-sdr/62421: New test case specific to multiple SDR attachments. 
902-sdr: remove txt and xml files not needed for validation. 
35-
160213 
e62604007gd: New variation checking for tildes with nothing between. 
622: Update references to 2016 taxonomies. 
624: Update references to 2016 taxonomies. 
605-07: Update references to 2016 taxonomies. 
605-26: Update references to 2016 taxonomies. 
607-16: Update references to 2016 taxonomies.  
607-27: Update references to 2016 taxonomies.  
612-09: Update references to 2016 taxonomies.  
902-sdr/60302, 60308, 60524, 62421): Update references to 2016.  
625-rr/01: Update references to 2016 taxonomies. 
 
37-
160614 
525-ix-syntax: New section covering Inline XBRL. 
e60515: Correct typo in testcase description. 
e62201: Remove us-gaap 2014, exch 2014, currency 2012, country 2012 from standard taxonomies. 
e62202: Reduce the number of variations to focus on forbidden schemas and the -doc- and -ref- 
linkbases of recent schemas. 
e62205: New subsection of e622 using Inline XBRL instances. 
624: Add variation 10-heading/003gd to check column headings. 
625-rr/01 variations r01000gd, r01001gd, r02000gd: change DocumentPeriodEndDate to reflect that 
RR filings do not require the end date to match the required context end date. 
62602: Renamed from Duration-Without-Matching-Instant to Instant-Without-Matching-Duration. 
62603: Update us-gaap taxonomy references from 2014 to 2016. 
e62602004gd: New variation with non-abutting instants. 
902-sdr/60302/019ng and 020ng: two new variations testing attachment type consistency on EX-99.K 
SDR and EX-99.L SDR. 


18
Interactive Data Public Test Suite, Version 77-260316, Page 18 of 32 
37-
160623 
i00301ng: replace header with <!DOCTYPE html> 
i02200gd: Add example of mixed duration tagging. 
525-ix-syntax/efm/21-duplicates: new test case. 
603-08-sdr-instances-testcases: correct error code expected in 001ng. 
r09002gd: replace deprecated elements in us-gaap 2015. 
r13000gd: replace deprecated elements in us-gaap 2015. 
r15001gd: replace deprecated elements in us-gaap 2015. 
 
39-
161110 
<result>: document its optional children @expected and <instance> 
Throughout: use CIK=9876543210 and OID TEST CO #1 in variations 
525-syntax: throughout, remove unused namespace prefixes and unreferenced ix:hidden facts eligible 
for transformation according to EFM 5.2.5.14. 
i00203gd: new variation to check escaped character extraction. 
i00210gd,i00211gd: new variations to check xml:lang treatment. 
i00379ng-i00382ng: new variations to check namespace prefix usage. 
i02200gd: add edge case of 22.5 duration units. 
i02201gd-i02306ng: Add variations for new ixt-sec transforms for numbers and durations expressed in 
English words. 
i04202gd: Add variation with nonnumeric inside a text block. 
i09204gd-i09206gd: new variations to check footnote extraction. 
i09001gd,i09203gd: correct footnote role for EFM compliance. 
efm/11-hidden: new testcases for EFM 5.2.5.14 hidden facts and the style property -sec-ix-hidden. 
60505: Remove EFM rule forbidding all typed dimensions. 
60516: Update variations to allow <thead><tfoot><tbody><span>. 
60539: New rule covering use of standard typed dimensions.  
e62202015ng: correct namespace on schema import. 
errors.xml: Removed Segment-Child-Not-Dimension; added Segment-Child-Not-Dimension, Typed-
Dimension-Not-Standard, Hidden-Fact-Not-Found, Standard-Namespace-Prefix. 
warnings.xml: Added Hidden-Fact-Multiple-References. 
edbody.dtd: added span, tbody, thead, tfoot. 
edgartaxonomies-draft.xml, edgartaxonomies.xml: added us-gaap draft-2017-01-31.xsd locations and 
extensible-enumerations.xsd to facilitate testing. 
39-
161212 
Throughout: change p0 namespace prefix in _def.xml files to xbrldt 
i07001gd, i07111ng, i07112ng, i07113ng, i08001gd, i08002gd, i09101ng, i11001gd, i11100ng, 
i11101ng, i11102ng, i11103ng: correct schemas and linkbases to avoid warnings not relevant to the 
test. 
i09101ng: update manifest with <image>. 
e6060304ng: add a _def.xml linkbase with default members. 
e61405010gd, e61405012gd: clean up calculation inconsistency. 
r62409001gd, r62415000gd, r62422000gd, and r62502000gd: update manifest with _def.xml 
references. 
r62410000gd: update manifest with _cal.xml reference. 
lib/asserts.xml: update with new error and warning codes 
lib/errors.xml: update with error codes hidden-fact-not-found and standard-namespace-prefix. 
lib/warnings.xml: update with warning codes hidden-fact-multiple-references and hidden-fact-eligible-
for-transform. 
 


19
Interactive Data Public Test Suite, Version 77-260316, Page 19 of 32 
41-
170301 
lib/edgartaxonomies-17-1.xml, lib/edgartaxonomies.xml: Update with 2017 taxonomy schemas and 
us-gaap 2017 template linkbases. 
Throughout: Update uses of us-gaap, country, currency, exch, and naics schemas to their 2017 
versions. 
lib/asserts.xml, lib/errors.xml: New err Document-Type-Namespace-Inconsistency 
i02004gd: New variation referencing IFRS 2016 schema. 
i04001gd: Remove escaping from the registrant name content. 
i02200gd: Cosmetic change to inline instance table HTML. 
e60521: Update the testcase manifest to match EFM text. 
e60539100ng: Correct error code to 0539. 
e60703004ng: New variation for authority ifrs.org. 
e60727: Remove us-gaap 2009 variations 000gd and 004ng. 
e62201: Add IFRS taxonomy variation. 
e62203075ng: New variation testing 10-K using IFRS 2016. 
r07002gd, r07003gd, r07004gd: New variations 624/07 to test typed dimension rendering. 
902-sdr: remove dei:EntityFilerCategory from variation instances because it is no longer required on 
EX-99.K, L and M SDR exhibits. 
 
43-
170913 
edgartaxonomies-17-3-1.xml: new file 
forbidden.xml: added four example ifrs related files. 
asserts.xml, externals.txt: updated to current test suite version. 
701-sdr-inline: remove this testcase because Form SDR is not currently allowing Inline attachments.  
e60311212ng: correct missing label linkbase. 
e60520: remove variations for F-9 submission types because the F-9 was rescinded in 2011. 
e60707004ng: new variation signals error if different prefixes are bound to the same namespace. 
e60909, e61206, e61207, e61208, e626: in all variations that use the rr 2012 taxonomy, correct the 
form type from 8-K to 485BPOS. 
e61003006gd: new variation that references an IFRS taxonomy to ensure that IFRS references using 
xml:lang="en" do not error. 
e62201: remove us-gaap 2015 and add IFRS 2017, and change the document type of each instance to 
be consistent with the namespaces in the DTS. 
e62202020ng, e62202021ng: new variations with IFRS linkbases. 
e62203: correct variations to use 485BPOS as the document type for RR tests.   
e62203076ng: new variation checking IFRS/2016 vs IFRS/2017. 
e62415: new variations 002gd, 003gd, and 004g containing an IFRS statement of changes in equity, 
with IFRS 2016 and 2017 and with and without a restatements axis. 
e62602: Update the us-gaap reference from 2015 to 2017 and currency reference from 2016 to 2017. 
e62609: Correct filenames that had 008ng instead of 009ng. 
i00200gd: add to the variation instance a comprehensive list of all allowed HTML elements and 
element-attribute combinations, from EFM vol.2 v.41 section 5.2.2.5. 
i00200gd: correct the registrant name and central index key. 
i02200gd: remove the 0's from the duration transform outputs and correct minor HTML warning on a 
table having too few columns. 
o0220gd,i02210gd, i01211gd: add missing _htm.xml output files. 
i10301ng (ned/10-header): correct the error code from 8.1.3 to 8.1.2. 
i11104ng (ned/11-transform): new variation testing for disallowed text in ix:hidden. 
i15001gd, i16001gd: add missing _htm.xml output files. 
i21200gd (ned/02-transform): add duplicate facts in which one has xsi:nil='true'. 
i21200gd: remove the zero vs. null comparison test. 
i21201gd: new variation testing ways of expressing zero. 
i21301ng: add a zero vs. null comparison variation. 
Throughout: update references from IFRS 2016 to IFRS 2017 where it is not essential to the purpose 
of the test. 
Throughout: ensure all -testcases.xml files have a @name attribute. 
 
45-
180412 
lib/edgartaxonomies-18-1.xml, lib/edgartaxonomies.xml: Update with 2017 taxonomy schemas and 
us-gaap 2018 template linkbases. 
Throughout: Update uses of us-gaap, country, currency, exch, and naics schemas to their 2018 
versions. 
lib/asserts.xml, lib/errors.xml: New err Document-Type-Namespace-Inconsistency 
i02004gd: New variation referencing IFRS 2018 schema. 
e62202022ng: new variations with IFRS linkbases. 
edgartaxonomies-draft.xml, edgartaxonomies.xml: added us-gaap draft-2018-01-31.xsd locations and 
extensible-enumerations.xsd to facilitate testing. 


20
Interactive Data Public Test Suite, Version 77-260316, Page 20 of 32 
e62203: correct variations to use 485BPOS as the document type for RR tests.   
e62203076ng: new variation checking IFRS/2017 vs IFRS/2018. 
e62602: Update the us-gaap reference from 2017 to 2018 and currency reference from 2017 to 2018. 
e62201009gd, e62201010gd, e62201011gd, e62201012gd 
 
46-
180610 
lib/edgartaxonomies-18-2.xml, lib/edgartaxonomies.xml: Update with 2018 IFRS taxonomy schemas; 
remove dei 2009, dei 2013, rr 2010, us-gaap 2016, and exch 2016.  
lib/asserts.xml, lib/errors.xml: New error codes Incompatible-Taxonomy-Document-Type and 
Incompatible-Inline-Document-Type. 
Throughout: update uses of us-gaap, ifrs, rr, dei, and exch taxonomies to their 2018 versions. 
525/ned/i02002gd: correct typo in the _htm.xml result file. 
e60535: Removing e60535998 and e60535999. 
e60526: introduce the Share Classes Axis as an alternative to the us-gaap Axis for the common shares 
outstanding facts. 
e60703007ng: remove xbrl.us as a standard namespace authority. 
e60727007ng, e60727008ng: remove spurious import of 2009 us types 
e60728001ng, e60728004ng: remove variations using 2009 us types 
e62202: simplify by using only dei-2014 and dei-2018 base taxonomies. 
e6220306ng, e62203072ng, e62203074ng, e62203077ng: remove variations involving taxonomy 
versions being removed. 
e62203009ng, e62203075ng, e6220380ng: add consistency checks involving IFRS 2018, and correct 
expected validation error codes. 
i22201gd, i22301ng, i22302ng: New test cases for certain combinations of form type and inline format. 
902-sdr e60302 test case manifest: correct error codes and remove extraneous label linkbase 
reference. 
46-
180910 
Section 5: Expanded explanation of the content of the /lib folder 
lib/axiswarnings.json: new, for 6.5.43 
lib/signwarnings.json: new, for 6.5.44 
525-efm-testcases.xml: add missing case i00382ng. 
e60543010gw, e60543011gd: New variations 
<parameter>: explain ELOParams syntax. 
lib/edgartaxonomies-18-3.xml, lib/edgartaxonomies.xml: remove IFRS 2016 taxonomy reference.  
i00304ng: correct and replace with i00304gw indicating warning, not suspension. 
e60512: New variations 012 through 020 to exercise numeric comparisons and duplicate removal of 
"consistent" values. 
e60712: New variations to signal new warning. 
e60520: remove submission types N-1A, N-1A/A, POS462B, S-20, S-B, and S-BMEF variations since 
these are not allowed to have XBRL attachments.  Add case e60520475ng for disallowed POS462C. 
e60540, e60541, e60542, e60543, e60544: New test cases corresponding to new EFM sections 6.5.40 
through 6.5.44. 
e622: Update variations relating to ifrs/2016 usage. 
Throughout: Update schemas, linkbases, and instances so as to use dei-2018 elements and avoid 
warnings from rules 6.5.40 through 6.5.44.  Replace old US-GAAP and IFRS elements with us-
gaap/2018 and ifrs/2018 elements. 
 
48-
181001 
525-efm-testcases.xml: add missing entry for 04-nonnumeric tests. 
e60507002ng: New variation with typed dimension. 
e60520: Remove facts or set facts to nil so as to avoid producing 6.5.40 warnings. 
e60522: Correct problem with missing facts producing warnings. 
e60541: New variations testing for nil facts. Renumber gw variations to the conventional sequence. 
e60543010gw, e60543011gd: New variations for sign exceptions. 
e60543044: New variation for nil facts deprecated. 
All *-testcase.xml: Set "ELOparams" to better support offline testing. 
All instances: Set period end dates and effective dates to agree.  Change generic EntityRegistrantName 
to "OSD TEST CO".  Set elements such as EntitySmallBusiness to their default values. 
 
49-
181214 
902-sdr, 525-efm: create subfolder 'sto' for tests that are 'system test only', that is, not testable 
standalone outside of EDGAR. 
902-sdr/schemas: Update non-XBRL exhibit schemas, remove text referring to EX-100. 
902-sdr: new variation 60302/010ng signaling exhibit type error. 
e60302: Remove test case; EX-100 is no longer a valid exhibit type. 
e60308100ng: remove variation because EX-100 is no longer valid. 
e60310, e60721, e60723, e60724: edit test case remarks to remove the EX-100 references. 


21
Interactive Data Public Test Suite, Version 77-260316, Page 21 of 32 
e60516, e60534: add <primary>,<exhibit> to image variations 
e60520201gd through e60520206gd: remove N-CSR and N-Q submission type variations. 
e60521: remove all N-CSR and N-Q submission type variations. 
e60520470ng: remove variation, no longer needed. 
e60526: remove all N-CSR and N-Q submission type variations. 
e60540: new variations 255 through 260 to improve coverage. 
e62419003gd, e62419004gd, e62419005gd: add variations with QName-valued facts having labels on 
member values. 
625-rendering/01-embedding-commands: correct the testcase file 
efm/02-transform/202gd: add datequarterend transformations. 
efm/02-transform/307ng: add datequarterend transformation. 
efm/11-hidden: add variations for xs:lang and xs:token data types. 
efm/19-multiio: remove ng cases, add gd cases to reflect that EDGAR will accept Inline XBRL 
document sets. 
efm/22-forms : remove ng cases for Risk/Return RR filings. 
efm/23-rr : new folder of tests specific to Inline XBRL documents that are Risk/Return (RR) filings.  
Remove elements deprecated in 2018. 
lib/asserts.xml: new entries resulting from improved error coverage. 
lib/test.xsd: add new variation elements <primary> and <exhibit>. 
 
50-
190213 
lib/edgartaxonomies.xml: add us-gaap/2019, srt/2019, currency/2019 and exch/2019 to permitted 
taxonomy versions. 
lib/signwarnings.json: expand the set of exclusion axes and members. 
525-ix-syntax/efm/02-transform: in the numwordsen and durwordsen transformation examples, 
expand allowed whitespace to include no-break spaces and dash characters to the same as 
ixt:zerodash. 
525-ix-syntax/efm/23-rr: add variations appropriate for testing risk/return summary inline viewer 
features in addition to validation. 
525-ix-syntax/ned/00-filing: new test case for warning about self-closing tags. 
e60520: Change each variation in which the submission type equals the document type so that it is an 
Inline XBRL (.htm) file. 
e60520:  Expand the submission types covered to include 485APOS, 485BXT, N-1A and N-1A/A. 
e60521:  Correct variations using submission type S-11 to have the emerging growth company flag; 
add variations for N-CSR forms; correct assertion error names Current-Reporting-Status, Fiscal-
Period-Focus and Fiscal-Year-Focus. 
e60526:  Correct variations that were missing series IDs; add variations for N-CSR forms. 
e60542: Update variations to use elements appearing in 2019 taxonomy deprecations. 
e62201, e62202, e62203: All variations are now Inline XBRL instances. 
Throughout: Update references to currency/2017 and exch/2018 to currency/2019 and exch/2019 
respectively; remove occurrences of self-closing tags. 
50-
190311 
edgartaxonomies.xml: simplify by removing US GAAP IM family. 
525-ix-syntax/efm/23-rr: change sample instances to be more representative of Inline XBRL risk/return 
summary tagging. 
525-ix-syntax/efm/22-forms, 525-ix-syntax/efm/23-rr, e60903, e60519, e60520, e60521, e60522: 
add elements to instances so as to avoid spurious 6.5.41 warnings. 
e60520, e60521: Add variations for submission types 485APOS, 485BXT, N-1A, and N-1A/A. 
Several –testcase.xml files: correct typos in data parameter ELOparams key 
"emergingGrowthCompanyFlag". 
 
51-
190523 
Added new test variations corresponding to updated sections of EFM Vol2 Ch6, mainly sections 6.5.20, 
6.5.21, 6.5.24, 6.5.26, 6.5.40, 6.5.45 – 6.5.53. 
In some sections some of the variations are created manually which other generated by generator 
scripts. Suffixes man (manual) and gen (generated) are used to distinguish these.  
Added variations are combination of inline XBRL and traditional XBRL.  
New SEC inline transform (ref EFM v51 draft) examples are included in newly added manual test 
variations.   
51a-
190729 
The EFM Conformance Test Suite has been updated to reflect current implementation of EDGAR system 
going in production on July 29, 2019. As result of this, new variations have been added and existing 
ones have been cleaned up and/or corrected. Specifically: 
1. Updated description of sections 605-20, 21, 24, 40, and 46. 
2. Clean up of 605-21, 26, 40, 47-53.  
3. New test variations in 605-24, 605-40, 605-46  
4. Minor corrections as applicable.  


22
Interactive Data Public Test Suite, Version 77-260316, Page 22 of 32 
 
52d-
190830 
The EFM Conformance Test Suite has been updated corresponding to EFM V.52-draft. Mainly it 
includes: 
1) New test variations in 605-20, 605-21, 605-40 
2) Variation updates to reflect: 
• 
Deprecation of ifrs-2017 and dei-2014 taxonomies. 
• 
Deprecation of all elements of invest-2012 and invest-2013  
52-
190330 
1. 525-ix-syntax\efm\22-forms\22-forms-efm-testcase.xml: Added new inline XBRL form types. 
2. 605-instance-syntax\605-21-required-entity-elts\605-21-man\605-21-man-testcase.xml: Added 
test cases which 8-K with 5.03 item submission header 
3. 605-instance-syntax\605-20-required-document-elts\605-20-man\605-20-man-testcase.xml: 
Added dei:DocumentPeriodEndDate variations. 
4. 605-instance-syntax\605-40-submission-header\605-40-man1\605-40-man-testcase.xml: Added 
submission header tag test variations. 
 
53d-
191227 
The Interactive Data Conformance Test Suite is being updated as per EFM V.52-draft.  
1. 605-instance-syntax\605-20-required-document-elts\605-20-man\605-20-man-testcase.xml: 
Added test cases for dei:DocumentPeriodEndDate. 
2. 605-instance-syntax\605-21-required-entity-elts\605-21-man\605-21-man-testcase.xml: Added 
test cases for dei:EntityWellKnownSeasonedIssuer, dei: CurrentFiscalYearEndDate, 
dei:EntityVoluntaryFilers, and dei:EntityFilerCategory. 
3. 605-instance-syntax\605-40-submission-header\605-40-man1\605-40-man-testcase.xml: Added 
test cases for dei: EntitySmallBusiness. dei:EntityShellCompany, and dei: 
EntityEmergingGrowthCompany.  
53d-
200102 
Fixed some of the gd testcases which were producing unintended warnings.  
53-
200127 
Updated as per EFM Vol. II Version 53 final version. Specifically updated the tests for section 6.5.40 
where validation rules have been modified for EntityEmergingGrowthCompany and 
EntityExTransitionPeriod.  
53.1d-
200210 
lib/edgartaxonomies.xml: Add us-gaap/2020, srt/2020, currency/2020, country/2020, sic/2020 and 
exch/2020, and remove all versions of INVEST from permitted taxonomy versions. 
lib/signwarnings.json: Rebuilt signwarnings from fasb DQCRT 2020. 
e60542: Update variations to use elements appearing in 2020 taxonomy deprecations. 
e62201, e62202, e62203: Update references to us-gaap/2020, srt/2020, currency/2020, 
country/2020, sic/2020 and exch/2020, and remove all invest year respectively. 
53.1-
200309 
Finalize the draft version of conformance test suite and update 622-02 and 622-03. Specifically: 
1. Correct efm section reference in 622-03-consistent-locations-testcase.xml for e62203078ng and 
e62203085ng 
2. Fix html:syntaxError - srt xml namespace location e62203078ng 
3. Corrections to 622-03 testcase to remove cases that were referencing disallowed taxonomy files, 
and correct various imports and namespaces 
4. Remove variation 017ng from 622-02 testcase, it was incorrectly added 
53.2d-
200515 
1. lib/edgartaxonomies.xml – Add 2020 version of IFRS and DEI. Remove SRT 2018, US GAAP 2018, 
COUNTRY 2016, CURRENCY 2017 and EXCH 2018.  
2. Updated xbrlerrors.xml to correct the 6.22.03 error messages.  
3. Update section 622 test cases to add tests for all currently allowed taxonomies and negative tests 
for disallowed taxonomies.  
4. Update all tests where disallowed versions of taxonomies were used by updating imports to 
corresponding currently accepted versions.  
53.2-
200629 
1. Update the version from 53.2d to 53.2. No new test cases were added or updated.  
2. Correct the version of edgartaxonomies.xml from Version 54 -> version 53.2, to align with the 
published version of the conformance test suite.  
 
54d-
200824 
1. lib/edgartaxonomies.xml – remove disallowed versions of taxonomies: IFRS 2018, DEI 2018 and 
Risk Return 2018 linkbases (presentation, calculation and definition links) 
2. Update all the conformance tests that used the disallowed versions of taxonomies by using the 
corresponding 2019 versions.  
3. EDGAR now allows redlining in inline XBRL documents. (Refer to EFM Vol 2 draft for details.) Added 
new tests for redlining at - \525-ix-syntax\efm\16-redlining   
54-
200921 
1. Added ng (not good) test variations in 622-02 for DEI-2018 and RR Linkbases 
2. Version update from 54d (draft) to 54.  
 


23
Interactive Data Public Test Suite, Version 77-260316, Page 23 of 32 
56d-
201116 
Note: There are no changes in the conformance test suite corresponding to EFM version 55, therefore 
conformance test suite version 55 is being skipped.  
Version 56d-201116 changes: 
The main enhancement in the upcoming EDGAR Release 20.4 is that it add validations related to DEI 
2020 - dei:IcfrAuditorAttestationFlag for form types 10-K, 10-KT, 20-F and 40-F (Refer EFM Vol 2, 
Version 56-draft). Following is the summary of changes in this version of EFM conformance suite: 
1. Added tests for ICFR Auditor Attestation Flag (DEI 2020 - dei:IcfrAuditorAttestationFlag) in section 
6.05.21 (Id ranging from 500 to 521, total 10 variations).  
2. Updated the description for test case 6.5.21, as per current draft EDGAR Filer Manual Vol 2, to 
describe ICFR Auditor Attestation Flag validation.  
3. Added a new dir in 525-ix-syntax/ned/20-viewer-lang (xiispec="6.10.3", "Non-US English labels 
may appear for elements in the schema...") 
4. Added additional variations in 525-ix-syntax/efm/21-duplicates – 401gd, 402ng, 403gd, 404ng, 
405ng.  
5. Updated the testcases.htm and its copy index.htm in the conf dir to be able to navigate to all the 
test-case documentation.  
6. Updated descriptions in several testcase.xml files so now it is in sync with current filer manual. 
There are corresponding htm files for each testcase.xml. These files are navigable from 
testcases.htm (ref #5 above) 
7. Updated lib/xbrlwarnings.htm to include new warning related to ICFR Auditor Attestation Flag.  
56-
201214 
Finalized the v56-draft to v56, mainly with following changes: 
1. Corrected various minor typographical issues in the several testcase.xml description element. Now 
the description is in sync with current version of EFM Vol 2. This is useful as the generated 
conf/index.html now enables navigation to all of the test-case variations.  
2. Added test variations to clarify xml:lang on applies only to dei string and normalized string item 
types (e.g. for 6.5.12/6.5.13), is used to select applicable facts (e.g. for 6.5.24)  and that xml:lang 
is case-insensitive 
3. In section 605-21, refactored the dei: IcfrAuditorAttestationFlag related test variations to include 
additional types of tests. These tests are from id 500 to 526, total 18 variations. 
4. Addressed the feedback received on 605-21/_516gw for converting it to _515gd variation. 
Additionally related feedback in the test case description is addressed to correct it and in sync with 
EFM Vol 2 current version.   
 
57d-
210219 
1.  Updated lib/edgartaxonomies.xml to include newly accepted taxonomies –  
a)  US-GAAP 2021, SEC Reporting Taxonomy 2021 
b)  COUNTRY, CURRENCY, DEI, EXCH, RR, SIC, NAICS, and STPR 2021 
2.  Added test case variations in folder conf\622-only-supported-locations\622-01-all-supported-
locations: _008gd, _009gd, _011gd, _012gd and _013gd   to test references to various newly 
accepted taxonomies.  
3.  Added test case variations in folder conf\622-only-supported-locations\622-03-consistent-locations 
to test conflicting taxonomies rules: _300ng to _309ng 
4.  Removed test variations in directory 607-08, because EFM section 6.7.8 has been deleted. (Refer to 
Section 6.7.8 and Section 6.9 of EDGAR Filer Manual Version 57-draft for details.) 
5.  Added folder conf/dqcrt containing example scripts that have been used for 2021 US-GAAP DQCRT 
rules compliance testing. The testing is based on US-GAAP 2020 filings. (Please note that EDGAR will 
NOT apply DQCRT validation rules to filings using taxonomies prior to US-GAAP 2021. Refer to page i, 
Updates section of EDGAR Filer Manual Version 57-draft for details.) 
6.  Updated lib/xbrlwarnings.htm to add DQC validation warnings for rules – dqc-0001, dqc-004, dqc-
0008, dqc-009, dqc-0015 and dqc-0048. 
7.  Minor update to test case description in section 6.5.21 to be in sync with EDGAR Filer Manual 
Version 57-draft. (That is, removed “to be visible” from code E503 description.) 
57-
210322 
Following updates were made: 
1. For test variations conf\622-only-supported-locations\622-03-consistent-locations _300ng to 
_309ng, and _021gd folded the linkbases into the schema files. (This is now allowed, as EFM 
Section 6.7.8 validations have been removed.) 
2. Fixed erroneous test variation conf/622-only-supported-locations/622-01-all-supported-locations 
_13gd.  
3. Added new test variation in conf/605-instance-syntax/605-43-signs/ _13gw to test signwarnings 
with typed dimension. (This variation resulted in an exception in Arelle, which has been fixed now.) 
4. Added several new test variations to verify taxonomy conflict rules with newly added taxonomies 
dei-2021, rr-2021 - conf/622-only-supported-locations/622-03-consistent-locations. These are 
numbered _350 to _423. (All these variations have the linkbases folded into the schema files. Refer 
#1 above.) 
5. Updated dqcrt tests in conf/dqcrt 


24
Interactive Data Public Test Suite, Version 77-260316, Page 24 of 32 
6. Updated edgartaxonomies.xml to update version and fix a minor typo. 
7. Updated version from 57d, to 57 in all places (*.xml, *.htm) 
 
58d-
210524 
1) Updated lib/edgartaxonomies.xml to –  
a) Include newly accepted taxonomies IFRS 2021 
b) Remove disallowed versions - SRT-2019, US-GAAP-2019, COUNTRY-2017, CURRENCY-2019, 
DEI-2012, DEI-2019, EXCH-2019, RR-2012, SIC-2011, and NAICS-2011. Please see 
https://www.sec.gov/info/edgar/edgartaxonomies.shtml for further details. 
2) Updated the applicable test variations to the newer versions of accepted taxonomies.  
3) Added test variation – 607-32:_030ng to support updated Section 6.7.32 of the EDGAR Filer 
Manual, Volume II: “EDGAR Filing”.  
4) EDGAR intends to support recent transformation registry 
(xmlns:ixt=http://www.xbrl.org/inlineXBRL/transformation/2020-02-12) in the upcoming Q2 
release. Test variations: 525-2-transform: _010gd, _011gd, _012gd, _013gd, _020ng, _021ng are 
added related to this. (Transformation registry-3 will continue to be supported.) 
5) Test variations in sections 622-03-consistent-locations have been updated to test compatible 
versions of acceptable taxonomies.  
58-
210621 
Following updates were made: 
1) Updated edgartaxonomies.xml to:  
a) Remove duplicate entries of dei linkbases for the us-gaap-2021 
b) Added applicable dei linkbases to ifrs-2021 
2) Updated description of testcases corresponding to the EFM sections 6.10.1 and 6.12.3, to reflect 
current EFM version. (These changes were undone in the EFM draft version 58) 
3) In 622-only-supported-locations, updated descriptions of some variations to make it clearer. In 
addition, removed few redundant test variations.  
4) In section 525-2-transform, uncommented and fixed some broken test variations: _210ng to 
_216ng.  
5) Updated version from 58d -> 58 in all testcases.xml.  
 
59d-
210820 
In release 21.3, EDGAR will stop accepting the IFRS-2019 taxonomy. Additionally it will address 
some add additional ixt-sec:countrynameen and ixt-sec:edgarprovcountryen transformations for 
issues on certain country names listed in 
https://www.sec.gov/edgar/searchedgar/edgarstatecodes.htm and reflected in the DEI schema. 
Changes to the conformance suite tests: 
1) Removed IFRS-2019-specific test variations from 622.03: _114ng, _200gd, _210ng, _211ng, 
_212ng, _213ng, 
_214ng, _216ng, _219ng, _220ng, _221ng, _357ng, _409ng, _514ng, _600gd, _714ng, and 
_814ng. 
2) Added variation to 622-02-no-unsupported-locations to test for IFRS-2019 prohibition: 
_040ng. 
3) Added directory conf/ixt-sec to contain tests for ixt-sec transformations, with a 
README.md to explain how to execute these tests using file tests.xml. 
4) 
Updated lib/edgartaxonomies.xml to remove ifrs/2019 references. 
5) In all *testecase.xml, updated path to lib/test.xsl and lib/test.xst to relative paths. 
59-
210920 
The following minor updates were made: 
1. Updated the version from 59d, to 59 in all places (*.xml, *.htm) 
2. In testcase variations, updated names and descriptions for grammar and readability.  
 
60d-
211122 
In Release 21.4, EDGAR will be updated to support version 2021Q4 of the DEI Taxonomy and the new 
2021Q4 Closed-End Funds (CEF) Taxonomy.  
In the draft EFM section 6.5.21 is updated, and there are new Sections 6.5.54 and 6.5.55. Regarding 
linkbases the new sections are 6.9.10, 6.12.10, 6.14.6 and 6.16.10. 
The following updates were made to this draft of the test suite: 
1. A new section 6.5.54, Auditor Information.  
2. A new section 6.5.55, Cover Page – Form N-2.  
3. For the release version of this test suite, we anticipate adding more tests, including the linkbase 
new sections.  
4. Some prior existing test variations will be updated where new validation rules raise issues which 
were previously not tested for.  
60-
211220 
The following updates were made in this version: 
1. Tests have been updated in sections 6.5.54, Auditor Information,  
 and   6.5.55, Cover Page – Form N-2.   
2. New test variations have been added in 6.12.10, 6.14.6, 6.16.10, and 6.09.09 


25
Interactive Data Public Test Suite, Version 77-260316, Page 25 of 32 
3. New test variations are also added in 6.07.09 and 6.07.13 
4. Existing variations have been updated to comply with new validation rules. 
5. Version update in all testcase files.  
60.1-
220131 
The following updates were made in this version: 
1. Enhanced conformance suite tests of CEF linkbases to ensure compliance with EFM sections 
6.12.10, 6.14.6 and 6.16.10. 
2. In the lib directory, regenerated the xbrlerrors.xml/htm and xbrlwarnings.xml/htm files. (These 
will also be updated on https://www.sec.gov/page/osd_edgarvalandrender ) 
3. Updated lib/edgartaxonomies.xml, regarding cef-compatible taxonomies.  
4. Version update to 60.1 in all testcase files.  
 
61d-
220222 
Release 22.1 of EDGAR will include the 2022 versions of FASB and SEC taxonomies. The following 
updates were made in this version: 
1. Updated lib/edgartaxonomies.xml to include newly accepted taxonomies –  
a)  US-GAAP 2022, SEC Reporting Taxonomy 2022 
b)  COUNTRY, CURRENCY, DEI, EXCH, RR, SIC, NAICS, STPR, CEF and VIP 2022 
2.  Added test case variations in folder conf/622-only-supported-locations/622-01-all-supported-
locations: _015gd to _018gd   to test references to various newly accepted taxonomies.  
3.  Added test case variations in folder conf/622-only-supported-locations/622-03-consistent-locations 
to test conflicting taxonomies rules: _010ng, _012ng, _014ng, and  _016ng 
4.  Updated folder conf/dqcrt containing example scripts that have been used for 2022 US-GAAP 
DQCRT rules compliance testing. The testing is based on US-GAAP 2020 filings and won’t be applied 
to filings using taxonomies prior to US-GAAP 2021. (FRD 208.1.3: “DQCRT/2022 rules will be 
applied to both 2022 and 2021 taxonomy submissions (for those named elements existing in the 
submission’s taxonomy year), as the 2022 DQCRT rule set is developed from the us-gaap 2021 
taxonomy.  (The DQCRT/2021 version of rules will not be carried forth to release 22.1.)”) 
5.  Updated lib/xbrlerrorss.htm and lib/xbrlwarnings.htm to add new errors and warning including DQC 
validation warnings. 
61-
220331 
1. Added test case variations in conf/622-only-supported-locations to test vip-2022 taxonomy, 
removed unnecessary dependencies, and added tests to 622-03-consistent-locations to test 
conflicting taxonomies rules: 000gd to _020ng. 
2. Added new test variations for 605-56-prospectus-document-types 
3. Updated many tests to use dei-2022 and other 2022 taxonomy versions, removing unused 
references to deleted elements PrincipalAddressMember and EntityCountryOfIncorporationName.  
Removed many spurious errors and warnings where possible 
4. New test variations have been added in 612-11-vip-presentation-link-validations, 614-07-vip-
calculation-link-validations, and 616-11-vip-definition-link-validations. 
5. Some of the existing variations have been updated to comply with new validation rules. 
6. Version update in all testcase files and correction of bad relative references in the 605-testcases 
file. 
7. Updated manually generated variations from 2009 dtr to 2020.  
8. Cleanup of 603-filing-syntax, 604-filing-semantics, 612-07-preferred-label-mismatch, and 612-08-
axis-requires-domain-child removing spurious errors.  
9. Cleanup of 525-ix tests removing schema & XBRL 2.1 validation errors. 
10. Updated 626-03 to remove deprecation warning. 
11. Cleanup on 605-08-no-unused-contexts. 
12. Corrected spurious schema errors introduced by some dei changes – 605-07-no-duplicate-contexts. 
In addition, simplified by merging linkbases to schema.  
13. Corrected occurrences of Document, Submission, and Investment Company Type “N-1” to “N-1A”. 
14. Added testcases-not-525-not-605.xml to allow for rapid testing that skips over 605-instance-syntax 
and 525-ix-syntax cases. 
 
62d-
220520 
Release 22.2 of EDGAR will include the IFRS/2022 and VIP/2022q2 taxonomies. Additionally, for all 
XBRL taxonomies that have versions from three years outstanding, the version from the earliest 
year will be removed. This will result in only year 2021 and 2022 taxonomies being acceptable.  
Following changes have been made to accommodate this: 
1. Updated lib/edgartaxonomies.xml to:  
a) Include newly accepted taxonomies IFRS 2022, and VIP 2022Q2. 
b) Remove 2020 versions of SRT, US GAAP, IFRS, COUNTRY, CURRENCY, DEI and  EXCH 
taxonomies 
c) Remove 2018 versions of RR and STPR taxonomies 
d) Remove 2017 version NAICS taxonomy 


26
Interactive Data Public Test Suite, Version 77-260316, Page 26 of 32 
2.  Added test case variations in folder conf/622-only-supported-locations/622-01-all-supported-
locations: _020gd and _021gd   to test references to various newly accepted taxonomies.  
3. Added test case variations in folder conf/622-only-supported-locations/ 622-02-no-unsupported-
locations to test that prohibited taxonomies are not acceptable: _041ng to 043ng 
4. Added test case variations in folder conf/622-only-supported-locations/622-03-consistent-locations 
to test conflicting taxonomies rules: _018gd to _035ng 
5. Updated test case variations in other directories to only use “accepted” versions of taxonomies (i.e. 
year 2021 and year 2022 only). 
62-
220621 
1. VIP/2022q2 taxonomy was updated after the publication of 62d-220520 version, but this did not 
require any updates to the conformance test suite.  
2. No other additions or deletions were made in this iteration. 
 
64d-
221128 
Release 22.4 of EDGAR will include the ECD/2022q4 and DEI/2022q4 taxonomies.  
Following changes have been made to accommodate this (Refer to EFM V64d for any additional details): 
1. Updated lib/edgartaxonomies.xml to include newly accepted taxonomies DEI/2022q4 and 
ECD/2022q4. Also added an entry for XBRL Data Type Registry (version 2022-03-21) 
2. Added test variations (from id _310 to _344) for ecd taxonomy with applicable submission types at 
location: /efm/conf/605-instance-syntax/605-20-required-document-elts/605-20-man  
3. Added test variations (from id _601 to _602) for ecd taxonomy with applicable submission types at 
location: /efm/conf/605-instance-syntax/605-21-required-entity-elts/605-21-man 
4. Added test variations (from id _130 to _159) for ecd taxonomy with applicable submission types at 
location: /efm/conf/605-instance-syntax/605-49-cover-page-etls-and-sub-type/605-49-man  
5. Added test case variations in folder conf/622-only-supported-locations/622-01-all-supported-
locations: _023gd to test references to various newly accepted taxonomies.  
6. Added test case variations in folder conf/622-only-supported-locations/622-03-consistent-locations 
to test conflicting taxonomies rules: from id_040 to _058 
7. Enhanced conformance suite tests of ECD linkbases to ensure compliance with new EFM sections 
6.14.8 and 6.16.12. 
8. In the lib directory, regenerated the xbrlerrors.xml/htm and xbrlwarnings.xml/htm files.  
9. Version update to 64d in all testcase files. 
10. Corrected following variations in  /efm/conf/605-instance-syntax/605-21-required-entity-elts/605-
21-man/605-21-man-testcase.xml : 
10.1. 
 _138ng – corrected error-name 
10.2. 
_501gw, 503gw, _506gw, _508gw, _511gw, _521gw downgraded variation severity 
from err to wrn 
11. Corrected following variation in /efm/conf/605-instance-syntax/605-54-auditor-information/605-54-
auditor-information-testcase.xml 
11.1. 
_124gw – downgraded variation severity from err to wrn 
12. Updated description in following testcases (xml and corresponding htm files): 
conf/605-instance-syntax/605-20-required-document-elts/605-20-man/605-20-man-testcase.xml 
conf/605-instance-syntax/605-21-required-entity-elts/605-21-man/605-21-man-testcase.xml 
conf/605-instance-syntax/605-49-cover-page-etls-and-sub-type/605-49-man/605-49-man-
testcase.xml 
64-
221219 
Following updates were made: 
1. ECD/2022q4 taxonomy was updated since the publication of previous version 64d of conformance 
suite. This needed updates to most of the test variations that were added in last iteration. Affected 
sections are: 605-20, 605-21, 605-49, 614-08 and 616-12. All the variations, which were added in 
previous version have been updated.  
2. In section 622-03, previous test variations _041ng, and _047ng, are converted to good (gd) 
variations, as ecd/2022q4 is compatible with cef/2022 and dei/2022. 
3. Version update from 64d to 64 in all testcase files. 
4. In the lib directory, regenerated the xbrlerrors.xml/htm and xbrlwarnings.xml/htm files to reflect 
current EDGAR system.  
 
65d-
230221 
In the upcoming Release 23.1, EDGAR will be updated to support the 2023 versions of the following 
taxonomies: 
• 
US-GAAP, SRT (published by FASB) 
• 
CEF, COUNTRY, CURRENCY, DEI, ECD, EXCH, NAICS, RR, SIC, STPR, VIP (published by SEC).  
To support this, following updates are made to the conformance test suite: 
1. Version updated to v65d in all testcases.    
2. Updated lib/edgartaxonomies.xml to include newly accepted taxonomies. 
3. Updated lib/taxonomy-compatibility.json to include new additional taxonomy version compatibility 
rules.  


27
Interactive Data Public Test Suite, Version 77-260316, Page 27 of 32 
4. All the test variations are updated to use version 2023 of taxonomies. Exception to this are test 
variations which refer to ifrs/2022 (these still use version 2022 for compatibility), and others where 
the intent is to test prior version (mostly in 622).  
5. Added 622-01-all-supported-locations: variations _000gd to _004gd   and 622-03-consistent-
locations: variations _100gd to _120ng. 
6. At various places cleaned up the test variations, e.g. removed older versions of namespace 
declaration that were not in use, removed unintended warnings etc.  
7. All test variation are updated to use dtr/type/2022-03-31.  
8. Updated few test variations in 605-42 to test recent deprecations.  
9. Updated conf\dqcrt to incorporate DQCRT implementation of updated and new rules. 
10. In the lib directory, regenerated the xbrlerrors.xml/htm and xbrlwarnings.xml/htm files to add new 
DQCRT warnings. 
11. Some of the variation names contained specific taxonomy version. Since the taxonomies are 
updated, these names became incorrect. This has been fixed by removing the taxonomy version 
from the names.  
12. In some variations, there were minor discrepancies between the file list in the variation and files 
actually used in the variation. This has been corrected.   
65-
230320 
For the Release 23.1, the conformance test suite contains following updates: 
1. Version updated to v65 in all testcases, and corresponding htm files regenerated.  
2. Few test variations are added in conf/ixt-sec/tests.xml for transform ixt-sec: datequarterend, to 
address a related bug. 
3. Business needs related to ecd/2023 taxonomy requires that ifrs/2021 and ifrs/2022 should be 
compatible with year 2023 versions of taxonomies. To accommodate this: 
3.1. Updated lib/taxonomy-compatibility.json.  
3.2. 622-03-consistent-locations variation _120ng is converted to _120gd (ifrs/2022 is compatible 
with version 2023 of taxonomies.) 
3.3. Added _121gd to verify the compatibility of ifrs/2021 and version 2023 of taxonomies. 
 
66d-
230522 
Release 23.2 of EDGAR will include the IFRS/2023 and OEF/2023 taxonomies. Additionally, as part of 
regular annual update, only year 2022 and 2023 taxonomies will be allowed, and earlier version 
2021 will be prohibited. 
Following changes have been made to support this release: 
1) Updated lib/edgartaxonomies.xml to:  
a) Include newly accepted taxonomies.  
b) Remove 2021 versions of all taxonomies. 
2) Updated lib/taxonomy-compatibility.json 
3) Added test case variations in folder conf/622-only-supported-locations/622-01-all-supported-
locations: _005gd and _007gd to test references to various newly accepted taxonomies.  
4) Updated testcase in conf/622-only-supported-locations/622-02-no-unsupported-locations to test 
that prohibited taxonomies are not acceptable. 
5) Added test case variations in folder conf/622-only-supported-locations/622-03-consistent-locations 
to test conflicting taxonomies rules: _120ng and _122ng 
6) All other variations in the conformance test suite are upgraded to use version 2023 of taxonomies 
only.  
7) Additions: In directory conf/605-instance-syntax/605-20-required-document-elts/605-20-man, 
added test variations _350gd to 363gw (Refer to section 6.5.20 in EFM version 66-draft) 
8) Additions: In directory conf/605-instance-syntax/605-21-required-entity-elts/605-21-man/, added 
test variations _610gd to 615ng (Refer to section 6.5.21 in EFM version 66-draft) 
9) New section: In directory conf/605-instance-syntax/605-57-N-1A-Fund-Shareholder-Reports, 
added new testcase.  (Refer to new section 6.5.57 in EFM version 66-draft) 
10) New section: In directory conf/614-calculation-syntax/614-09-OEF-calculation-link-validations, 
added new testcase.  (Refer to new section 6.14.9 in EFM version 66-draft) 
11) New section: In directory conf/616-definition-syntax/616-13-OEF-definition-link-validations, added 
new testcase.  (Refer to new section 6.16.13 in EFM version 66-draft) 
12) In section conf/525-ix-syntax, the expected error/warning codes have been changed to use error 
codes from a new xml library.  
66-
230620 
Release 23.2 of EDGAR, in addition to including the IFRS/2023 and OEF/2023 taxonomies, also 
includes RXP/2023 taxonomy and the new ISO code taxonomy SNJ/2023. To support this and 
other enhancements, following updates were made since the previous version.  
1) Added test case variations in folder conf/622-only-supported-locations/622-01-all-supported-
locations: _006gd to test references to RXP/2023 and SNJ/2023 newly added taxonomies.  
2) Added test case variations in folder conf/622-only-supported-locations/622-03-consistent-locations 
to test conflicting taxonomies rules: _121ng to verify RXP taxonomy compatibility. 


28
Interactive Data Public Test Suite, Version 77-260316, Page 28 of 32 
3) Additions: In directory conf/605-instance-syntax/605-20-required-document-elts/605-20-man, 
added test variations _364gd to _370gw (Refer to section 6.5.20 in EFM version 66) 
4) Additions: In directory conf/605-instance-syntax/605-21-required-entity-elts/605-21-man/, added 
test variations _616gd to _618ng (Refer to section 6.5.21 in EFM version 66) 
5) New section: In directory conf/605-instance-syntax/ 605-58-Resource-Extraction-Payments-Form-
SD-Exhibit-201, added new testcase.  (Refer to new section 6.5.58 in EFM version 66) 
6) New section: In directory conf/614-calculation-syntax/ 614-10-RXP-calculation-link-validations, 
added new testcase.  (Refer to new section 6.14.10 in EFM version 66) 
7) New section: In directory conf/616-definition-syntax/ 616-14-RXP-definition-link-validations, 
added new testcase.  (Refer to new section 6.16.14 in EFM version 66) 
8) In all testcases, the testcase description is replaced with a hyperlink to the corresponding section 
in the EDGAR Filer Manual.  
9) Fixed some minor typos in few testcases.  
66.1d-
230727 
Release 23.2.3 of EDGAR, is a minor release. Following changes are made for this release: 
1) Fixed a minor typo in efm/conf/testcases.xml, where in line 173, a back slash \ is corrected to / 
2) Removed section 6.3.10 as in this release, the corresponding validation is being removed, and the 
efm section has been marked reserved.  
3) Fixed latent issues related to ixt transform of nil value, in various test variations.  
 
67d-
230821 
In the Release 23.3 the EDGAR system will allow a new taxonomy SHR/2023. Additionally, a new 
Submission type – F-SR, and a new Exhibit type- EX-26, are being added to the list of accepted 
Inline XBRL documents. (The EX-26 exhibit is a separate IXDS from the primary document, thus it 
does not share contexts, units or schemaRefs with the primary document.) 
Following updates are being made to support this release: 
1) In 605-20-required-document-elts/605-20-man added test variations - _371gd to _376gd (to test 
allowed optional dei:DocumentPeriodEndDate in :  DEF 14A, DEF 14C, PRE 14A, PRE 14C, 
PREM14A, PREM14C)  
2) In 605-20-required-document-elts/605-20-man added test variations - _001gd to _017gd (for the 
new Submission type: F-SR, and the new Exhibit type EX-26) 
3) In 605-21-required-entity-elts/605-21-man added test variations - _001gd to _008gd (for the new 
Submission type: F-SR, and the new Exhibit type EX-26) 
4) Removed test variations for 603-08, as this section is marked “reserved” in EFM. 
5) Fixed some test variations that were breaking due to recent changes. 
6) Updated version to v67d in all testcases (xml and htm) 
7) Fixed some minor typos at various places. 
8) Added new testcase - conf\612-presentation-syntax\612-12-shr-presentation-link-validations 
9)  Added new testcase – conf\614-calculation-syntax\614-11-shr-calculation-link-validations 
10) Added new testcase - conf\616-definition-syntax\616-15-shr-definition-link-validations 
67d-
230901 
A shell script for executing EX-26 related tests is provided in conf\525-ix-syntax\efm\24-multixds. 
67-
230918 
1) Version update to v67 and update links to the EFM final version in all testcase files.  
2) Added test variation conf/525-ix-syntax/ned: _306ng to test that a html instance must have xml 
declaration as first item in the file.  
3) Added test variation conf/622-only-supported-locations/622-01-all-supported-locations: _008ng to 
test references related to the newly added shr/2023 taxonomy. 
4) Added test variations conf/622-only-supported-locations/622-03-consistent-locations: _004gd, 
_005ng, _006ng, _007ng, _008ng, _009ng, to verify that only compatible taxonomy versions are 
permitted. 
 
68d-
231120 
In the Release 23.4 the EDGAR system will allow new taxonomy FND with versions 2022 and 2023. 
Additionally, new Submission types: S-6, S-6/A, N-8B-2, N-8B-2/A and 487 are being added to the 
list of accepted Inline XBRL documents.  
Following updates are being made to support this release: 
1) In 605-20-required-document-elts/605-20-man added test variations: _18gd to _35gw  
2) In 605-21-required-entity-elts/605-21-man added test variations: 009gd-020gd. 
3) In 605-56-prospectus-document-types added test variations: 001gd-010gd. 
4) In 622-01-all-supported-locations added test variation: _009gd-_013gd to test allow newly 
allowed schema locations. 
5) In 622-03-consistent-locations added test variations: 010ng-014ng, to test that only same year 
versions of taxonomies are compatible.  
6) Added - edgartaxonomies-23-4.xml. 
7) Updated edgartaxonomies-all-years.xml (added new FND related entries and removed some invalid 
href entries.) 


29
Interactive Data Public Test Suite, Version 77-260316, Page 29 of 32 
8) Updated taxonomy-compatibility.json to include FND entries.  
9) Updated all test variations for submission type EX-26 by removing EX-26/A, as amendment is not 
a valid submission type for this exhibit.  
10) Updated lib/xbrlerrors.xml and xbrlerrors.htm to add new errors.  
11) Updated version to v68d in all testcases (xml and htm) 
68-
231218 
Following are updated to create final version 68: 
1) In 622-03-consistent-locations added test variations: 015gd, to test that ECD and SHR are 
compatible taxonomies.  
2) Updated version to v68 and href links to final version of EFM in all testcases (xml and htm) 
68.1-
240129 
Release 24.0.1 of EDGAR system allows the ffd/2024 taxonomy and prohibits the ffd/2023 and 
shr/2023 taxonomies. Following updates are made to support this release: 
1) Added the Filing Fee Exhibits test cases under conf/filing-fee-exhibit. 
2) Updated lib/xbrlerrors.xml and xbrlerrors.htm to add new errors related to filing-fee-exhibit. A new 
column is added containing number identifier for the corresponding error/warning message.  
3) Removed all test variations related to shr/2023.  
 
69d-
240220 
Release 24.1 of EDGAR system allows the sro/2024 taxonomy, in addition to allowing year 2024 
versions of SEC and US-GAAP taxonomies. Additionally, new Submission types: 17AD-27, 17AD-
27/A, 11-K, 11-K/A, 11-KT, and 11-KT/A are being added to the list of accepted Inline XBRL 
documents. Refer to latest EFM for details.  
Following updates are being made to support this release: 
1) Added conf/525-ix-syntax/efm/17-redaction containing variations to test the redaction capability for 
document type 17AD-27.  
2) In 605-20-required-document-elts/605-20-man added test variations: _377gd to _394gw. 
3) In 605-21-required-entity-elts/605-21-man added test variations: _619ng to _626ng. 
4) In 605-40-submission-header/605-40-man1 added test variations: _427gw to _430gw. 
5) In 605-49-cover-page-etls-and-sub-type/605-49-man added test variations: _170gd to _176gw. 
6) In 622-01-all-supported-locations added test variations: _008gd, _014gd, _015gd, _024gd to 
_028gd. 
7) In 622-03-consistent-locations added test variations: _004ng, _005ng, _006ng, _007ng, _008ng, 
_009ng, _015ng, _017ng. 
8) In 605-instance-syntax/605-54-auditor-information updated test variation _111gd and added new 
test variations _176gd to _183ng, to test relaxed auditor tagging requirements for amendments.  
9) Corrected typos at various places 
10) Version updated to v69d in all testcases.    
11) Updated lib/edgartaxonomies.xml to include newly accepted taxonomies. 
12) Updated lib/taxonomy-compatibility.json to include new additional taxonomy version compatibility 
rules.  
69-
240318 
Following are updated to create final version 69: 
1) In 624-rendering/13-flow-through/gd added calculation linkbase for test variation 000gd. 
2) Updated file names and variation names under 605-instance-syntax/605-20-required-document-
elts/605-20-man and 605-instance-syntax/605-49-cover-page-elts-and-sub-type/605-49-man to 
ensure consistent usage of suffix: ng, gw and gd. 
3) Added new test case conf/605-instance-syntax/605-60-form-11-k. 
4) Added new test case 605-instance-syntax/605-59-form-17AD-27. 
5) Added new test case conf/616-definition-syntax/616-15-sro-definition-link-validations. 
6) Added new test case conf/525-ix-syntax/efm/24-numeric-units. 
 
70d-
240604 
 
 
EDGAR Release 24.2 updates: 
1) Incorporate sbs/2024 and ffd/2024q2 taxonomies. (Updated edgartaxonomies.xml and 
edgartaxonomies-all-years.xml) 
2) Updated descriptions for filing fee exhibit test cases 
3) Added new test case directories under filing-fee-exhibit: 000-debt, 000-filinglevel, 000-multiline, 
000-userstories. 
4) Updated taxonomy for filing fee exhibit test cases to ffd-2024q2 
5) Added test case variations in folder 622-only-supported-locations/622-01-all-supported-locations: 
_009gd to test references to sbs/2024 and _010gd to ifrs/2024.  
6) Added test case variations in folder conf/622-only-supported-locations/ 622-02-no-unsupported-
locations to test now prohibited taxonomies _001ng to _010ng. 
7) Added in 605-instance-syntax/605-20-required-document-elts/605-20-man, added test variations 
_001gd to _007gw. 
8) Added in 605-instance-syntax/605-21-required-entity-elts/605-21-man/, added test variations 
_001gd to _003ng 


30
Interactive Data Public Test Suite, Version 77-260316, Page 30 of 32 
 
Changes to the organization of the files having no intended impact on validation: 
9) In most test variations, embed linkbases into schemas to reduce file clutter. 
10) Updated most test case variations 2024 references. removing spurious namespace prefix bindings. 
11) Remove folders and files no longer referenced by testcase.xml files. 
12) Remove 525-ix-syntax/ned and 525-ix-syntax/sto. 
13) Add test for transformation of updated country name T&#xFC;rkiye. 
14) In 525-ix-syntax/elm, correct file names and update to 2024 taxonomy versions. 
15) In 525-ix-syntax/efm/22-forms, change samples using rr-2023 to use oef-rr-2024 entry point. 
16) Change 525-ix-syntax/efm/23-rr to more general scope 23-barcharts for oef. 
17) Remove obsolete 622-05 testcase 
70-
240701 
 
 
1) Add three variations to 6.4.3, to test for invalid NCNames. 
2) Remove spurious <linkbase> elements from 902-sdr/sto testcase 
3) Add new test variations in 622-only-supported-locations/622-01-all-supported-locations: 016gd to 
023gd 
4) Update 605-instance-syntax/605-58-Resource-Extraction-Payments-Form-SD-Exhibit-201 test 
cases to test all 9 validations. 
5) Minor cleanup at few other places.  
71d-
240816 
 
EDGAR Release 24.3 updates: 
1) Added test case variations in folder 622-only-supported-locations/622-01-all-supported-locations: 
_029gd to test references to cyd/2024 and _030gd to test references of rxp/2024q3, snj/2024 
2) Added test case variations in folder 605-instance-syntax\605-58-Resource-Extraction-Payments-
Form-SD-Exhibit-201: _017gd - _025gd to test filings using alternative reporting regime with 
rxp/2024q3 taxonomy 
3) Added test case variations under 605-instance-syntax/605-61-cybersecurity-incident-disclosure: 
_001gd - _003gd testing usage of cyd/2024 taxonomy 
4) Added test case variations in folder 605-instance-syntax/605-20-required-document-elts/605-20-
man: _008gd to _017gw and _036gd to _040gw. 
5) Added test case variations in folder 605-instance-syntax/605-21-required-entity-elts/605-21-man: 
_004gd to _008ng and _021ng to _024ng. 
6) SBSEF-exhibits do not require dei:DocumentPeriodEndDate as specified in EDGAR xbrl guide. Fixed 
various test variations to comply with this requirement.  
7) Added test case variation in 525-is-syntax/efm/00-filing : _025ng to verify that animated graphic is 
not allowed.  
 
71-
240916 
1) Updated linkbases for testcases under 605-instance-syntax, 614-calculation-syntax, 616-definition-
syntax, 622-only-supported-locations to account for new uncategorized facts warning. 
2) Renamed 624-rendering/17-uncategorized-facts/gd/17-uncategorized-facts-gd-testcase.xml to 624-
rendering/17-uncategorized-facts/gw/17-uncategorized-facts-gw-testcase.xml.  
3) Updated 605-61-cybersecurity-incident-disclosure: 001gd and 622-01-all-supported-locations: 
029gd to comply with latest CYD taxonomy.  
72d-
241118 
EDGAR Release 24.4 updates: 
1) Added test case variation in folder 622-only-supported-locations/622-01-all-supported-locations: 
_031gd to verify vip/2024q4 taxonomy is supported. 
2) Added test case variation in folder 622-only-supported-locations/622-03-consistent-locations: 
_119ng to test that vip/2024q4 is not compatible with dei/2023. 
3) Added test case variations in folder 605-instance-syntax/605-56-prospectus-document-types: 
_248ng to _250ng to test that the correct VIP taxonomy entry points are used on submission types 
N-4, N-3, and N-6. 
4) Removed 615-calculation-semantics, as no longer applicable. 
72-
241216 
1) Cleaned up schema files in folder 605-instance-syntax/605-57-N-1A-Fund-Shareholder-Reports: 
_001gd, _003ng to 017gw 
2) Cleaned up schema file in folder 605-instance-syntax/605-21-required-entity-elts/605-21-man: 
_610gd to _615ng 
3) Cleaned up schema file in folder 605-instance-syntax/605-41-seriesid: _203gw 
4) Cleaned up schema and instance files in folder 616-definition-syntax/616-13-oef-definition-link-
validations: _003ng to _004ng 
73d-
250218 
Release 25.1 of EDGAR system allows the spac/2025 taxonomy, in addition to allowing year 2025 
versions of SEC and US-GAAP taxonomies.   
Following updates are being made to support this release: 
1) In 622-01-all-supported-locations added test variations: _032gd to _048gd. 
2) In 622-3-622-03-consistent-locations added test variations: _000gd, 001ng to 003ng, _010ng to 
_014ng, _016ng, and _018ng. 


31
Interactive Data Public Test Suite, Version 77-260316, Page 31 of 32 
3) Updated lib/edgartaxonomies.xml to include newly accepted taxonomies. 
4) Updated lib/taxonomy-compatibility.json to include new additional taxonomy version compatibility 
rules. 
5) Lib/test.xsd is updated to  
a) Add blockedMeesageCodes in the variation results. This adds ability to ignore certain warning 
that are not important in context of the specific variation being tested.  
b) Update the error/warning num to contain string. This provides ability to add new error/warning 
num in compliance with the EDGAR XBRL Guide.  
6) Added new SPAC testcase under 605-62-special-purpose-acquisition-companies. 
7) Replaced EFM expected num 61210 with EXG.10.08.01 for test cases under 612-presentation-
syntax, 614-calculation-syntax, and 616-definition-syntax. 
8) Updated conf/dqcrt contents.  
73-
250317 
1) In 605-instance-syntax/605-20-required-document-elts/605-20-man renamed e60520394gw to 
e60520394gd. 
2) Corrected a typo in spac-lab namespace in edgartaxonomies-25-1.xml. 
3) Corrected some minor typos at various places. 
74-
250616 
1) Refactoring of testcase folders: All the test variations have been moved into testcase subfolders. 
2) Inline XBRL: The majority of testcase variations which were xBRL-XML instances have been 
converted into inline XBRL instances with 2025 taxonomies. 
3) Updated lib/test.xsd to allow testing schema file ending in _ins (used in 603-03-filename-pattern: 
_05ng) 
4) Removed 607-06-version-date-testcase because it is tested in 607-04-valid-ext-namespace-format 
5) In 622-01-all-supported-locations-testcase added test variation _11gd. 
6) In 622-02-no-unsupported-locations added variations _415ng to _434ng for 2023 taxonomies, 
which are no longer supported. 
7) Fixed empty documents under the filing-fee-exhibit directory. 
8) Removed 23-barcharts testcases under 525-ix-syntax. 
9) Removed 02-bar-charts testcases under 625-rr-rendering. 
10) Removed 604-filing-semantics testcases. 
11) In 607-32-nonnumeric-instant removed variations _000ng to _018ng and _020ng. 
12) Removed references to US-GAAP taxonomy across various testcases that did not require it. 
13) Reinstated variation _004gd under 626-02-instant-without-matching-duration-testcase.xml. 
14) Reinstated variations _000gd to _002gd under 624-rendering/09-start-end-labels/gd/09-start-end-
labels-gd-testcase.xml. 
75-
250804 
1) Recreated all test cases under filing-fee-exhibit folder to include OfferingTableNa, OffsetTableNa, 
CombinedProspectusTableNa elements. 
2) Added testcase 01-OtherSubmissions/13-OfferingTableNa/13-OfferingTableNa-testcase.xml. 
3) Added testcase 01-OtherSubmissions/14-OffsetTableNa/14-OffsetTableNa-testcase.xml. 
4) Added testcase 01-OtherSubmissions/15-CombinedProspectusTableNa/15-
CombinedProspectusTableNa-testcase.xml. 
5) Added testcase 02-424ISubmissions/14-OffsetTableNa/14-OffsetTableNa-testcase.xml. 
76-
251010 
1) In 616-12-ecd-definition-link-validations added variations _010gd and _011ng. 
2) Updated variations in 605-20-man, 605-21-man, 605-57-N-1A-Fund-Shareholder-Reports, 614-09-
oef-calculation-link-validations, 616-13-oef-definition-link-validations, 622-01-all-supported-
locations to ensure oef:ShareholderReportAnnualOrSemiAnnual is found in the required context. 
3) In 605-42-deprecated added variations _007gw to _013gw testing deprecated SPAC concepts. 
4) In 622-01-all-supported-locations added variation _049gd testing spac/2025q3. 
5) Various updates to testcases under dqcrt directory. 
6) In 13-OfferingTableNa added variation 0005gw. 
7) In 14-OffsetTableNa added variation 0005gw and 0006gw. 
8) In 15-CombinedProspectusTableNa added variation 0005gw and 0006gw. 
9) Added testcase 616-16-spac-definition-link-validations/616-16-spac-definition-link-validations-
testcase.xml. 
10) Updated instances in 605-12 to be iXBRL with minimal custom taxonomy files. 
11) Cleanup of cases in 605-08, 607, 614, 616, 618, 902 to align variation names with instance and 
taxonomy files, with removal of irrelevant warnings, errors, and portions of testcase files. 
12) Added references to EXG to complement EFM references in most -testcase.xml files. 
76d-
251201 
In Release 25.4, the allowed decimal precision for the following fee tagging tags is being set to a 
maximum of 8 decimal places: 
Affected tags: AmtSctiesRegd, AmtSctiesRcvd, Rule429NbOfUnsoldScties, OffsetPrrNbOfUnsoldScties, 
MaxOfferingPricPerScty, and ValSctiesRcvdPerShr 
To accommodate this requirement, these following tests are added/updated: 
1) Added in 300-offeringTable 


32
Interactive Data Public Test Suite, Version 77-260316, Page 32 of 32 
01-Rule457(a)/04-AmtSctiesRegd/0017ng 
01-Rule457(a)/05-MaxOfferingPricPerScty/0017ng 
02-Rule457(o)/04-AmtSctiesRegd/0009ng 
02-Rule457(o)/05-MaxOfferingPricPerScty/0017ng 
03-Rule457(r)/04-AmtSctiesRegd/0006ng 
03-Rule457(r)/05-MaxOfferingPricPerScty/0007ng 
04-Rule457(s)/04-AmtSctiesRegd/0006ng 
04-Rule457(s)/05-MaxOfferingPricPerScty/0006ng 
06-Ruleother/04-AmtSctiesRegd/0009ng 
06-Ruleother/05-MaxOfferingPricPerScty/0009ng 
07-Rule415(a)(6)/04-AmtSctiesRegd/0005ng 
09-Rule457(f)/04-AmtSctiesRegd/0015ng 
09-Rule457(f)/15-AmtSctiesRcvd/0015ng 
09-Rule457(f)/16-ValSctiesRcvdPerShr/0008ng 
2) Added 400-offsetTable/03-Rule457(p)/10-OffsetPrrNbOfUnsoldScties/0006ng 
3) Added 500-cmbndPrspctsTable/01-Rule429/06-Rule429NbOfUnsoldScties/0008ng 
4) Updated the existing test cases to comply with this new requirement.  
 
76d-
260217 
Release 26.1 of EDGAR allows the 2026 versions of SEC and US-GAAP taxonomies. In addition, many 
of the filing fee exhibit validations have been changed to errors from warnings  
(See the EDGAR XBRL Guide chapter 4 for details). 
1) In 622-01-all-supported-locations added variations _50gd to _067gd testing 2026 taxonomies. 
2) Replaced the taxonomy version across the test suite to use version 2026 of taxonomies. 
3) In the dqcrt directory added the 2026 dqcrt test cases. 
4) In filing-fee-exhibit directory updated the severity to error for test cases that were previously 
warning. Renamed the variation and directory from gw to ng. 
 
77-
260316 
1) Updated lib/xbrlerrors.htm and lib/xbrlwarnings to match changes to severity in filing-fee-exhibit 
directory. 
 

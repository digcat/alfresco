#!/usr/bin/env python

#
#      Licensed to the Apache Software Foundation (ASF) under one
#      or more contributor license agreements.  See the NOTICE file
#      distributed with this work for additional information
#      regarding copyright ownership.  The ASF licenses this file
#      to you under the Apache License, Version 2.0 (the
#      "License"); you may not use this file except in compliance
#      with the License.  You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#      Unless required by applicable law or agreed to in writing,
#      software distributed under the License is distributed on an
#      "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
#      KIND, either express or implied.  See the License for the
#      specific language governing permissions and limitations
#      under the License.
#
"""
Module containing the sample code for an Alfresco 4.0 EE installation
"""

import cmislib
from pprint import pprint
from contextlib import closing


def print_folder(folder):
    print '*****print childrens of the folder', folder.getName()
    for c in folder.getChildren():    
        print c.name
    print '*****print childrens of the folder', folder.getName()

    #acl=c.getACL()
    #pprint(acl.getEntries(),indent=4)
    #print '***ations:'
    #actions=c.getAllowableActions()
    #for k,v in actions.items():
    #    print k,':',v


''' print the document's properties (metadata)
'''
def print_doc(doc):
    print '*****print property of doc:',doc.getTitle()
    print 'isCheckedOut=',doc.isCheckedOut()
    for k,v in doc.properties.items():
        print "%s,%s\n" % (k,v)
    print '*****print property of doc:',doc.getTitle()



# log on to CMIS
cmisClient = cmislib.CmisClient('http://localhost:8080/alfresco/s/cmis', 'admin', 'admin')
#cmisClient = cmislib.CmisClient('http://localhost:8080/alfresco/s/cmis', 'mjackson', 'password')

# root repo
repo = cmisClient.defaultRepository
print('default repo=',repo)

print '*************repoinfo:'
for k,v in repo.getRepositoryInfo().items():
    print k,':',v
print '*************repoinfo:'

#print '************perm defs:'
#for permDef in repo.permissionDefinitions:
#    print permDef
#print '************perm defs:'

# get the CMIS object for sample site 's documentLibrary
dl_root= repo.getObjectByPath('/Sites/swsdp/documentLibrary')


# get the CMIS sample folder and sample doc
folder=repo.getObjectByPath('/Sites/swsdp/documentLibrary/Agency Files/Contracts/')
print_folder(folder)
doc=repo.getObjectByPath('/Sites/swsdp/documentLibrary/Agency Files/Contracts/Project Contract.pdf')
print_doc(doc)

# retrieve the content via getContentStream() and write a file locally
with closing(doc.getContentStream()) as s:
    content=s.read()
with open(doc.getTitle(),'w') as f:
    print >>f,content


# check it out
if not doc.isCheckedOut():
    pwc=doc.checkout()
# check it in
if doc.isCheckedOut():
    with open('sample1.pdf','r') as f:
        pwc.setContentStream(contentFile=f)
    pwc.checkin()
    
# create the content via folder.createDocument
#sample='sample1.pdf'
#props = {'cmis:someProp':'someVal'}
#with open(sample,'r') as f:
#    folder.createDocument(sample, properties=props,contentFile=f)
    


# Perform a CMIS query
print 'CMIS query........'
results = repo.query("select * from cmis:document where contains('Project')")
for r in results:
    print r.getTitle()
    


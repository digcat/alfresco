#!/usr/bin/env python
import cmislib
from pprint import pprint
from contextlib import closing


cmisClient = cmislib.CmisClient('http://localhost:8080/alfresco/s/cmis', 'admin', 'admin')
#cmisClient = cmislib.CmisClient('http://localhost:8080/alfresco/s/cmis', 'mjackson', 'password')


def print_chidren(parent):
    children = parent.getChildren()
    for c in children:    
        print c.name
    #acl=c.getACL()
    #pprint(acl.getEntries(),indent=4)
    #print '***ations:'
    #actions=c.getAllowableActions()
    #for k,v in actions.items():
    #    print k,':',v


def print_doc(doc):
    for k,v in doc.properties.items():
        print k,v,"\n"



repos=cmisClient.repositories
print('repos=',repos)

# root repo
repo = cmisClient.defaultRepository
print('default repo=',repo)

print '*************repoinfo:'
for k,v in repo.getRepositoryInfo().items():
    print k,':',v
print '*************repoinfo:'

print '************perm defs:'
for permDef in repo.permissionDefinitions:
    print permDef
print '************perm defs:'


# get root of incose
incose_root= repo.getObjectByPath('/incose')
print incose_root.getObjectId()

# create folder
folder=incose_root.createFolder('chapter1')
print folder.getName()
print folder.getObjectId()

# delete folder
#folder=repo.getObjectByPath('/incose/chapter1')
#print folder.getName()
#print folder.getObjectId()
#folder.deleteTree()

#print 'CMIS getObjectByPath........'
#doc=repo.getObjectByPath('/User Homes/u1/scalable-networking.pdf')
#print doc.getObjectId()
#doc2=repo.getObject('workspace://SpacesStore/7348b8e7-4651-4721-8ec5-36fcc15287ca')

#print 'title=',doc2.getTitle()
#print '\nproperties',doc2.getProperties()

#print_doc(doc2)

#with closing(doc.getContentStream()) as s:
#    content=s.read()

#with open('s.pdf','w') as f:
#    print >>f,content


#print 'CMIS query........'
#results = repo.query("select * from cmis:document where contains('2012')")
#for r in results:
#    print_doc(r)
    


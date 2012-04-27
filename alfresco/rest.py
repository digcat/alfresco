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


import json
from pprint import pprint
import requests
import urllib
import string


    

class AlfSession(object):

    # generic url templates
    URL_TEMPLATE=string.Template('http://$host:$port/alfresco/service/api/$func?alf_ticket=$alf_ticket')
   
    # login logout service
    URL_TEMPLATE_LOGIN=string.Template('http://$host:$port/alfresco/service/api/login')
    URL_TEMPLATE_LOGOUT=string.Template('http://$host:$port/alfresco/service/api/login/ticket/$alf_ticket?alf_ticket=$alf_ticket&format=json')

    # USER
    URL_TEMPLATE_USER=string.Template('http://$host:$port/alfresco/service/api/people/$user?alf_ticket=$alf_ticket')

    #Groups
    URL_TEMPLATE_ROOTGROUPS=string.Template('http://$host:$port/alfresco/service/api/rootgroups/$shortName?alf_ticket=$alf_ticket')

    #User's group membership
    URL_TEMPLATE_GROUP_MEMBERSHIP=string.Template('http://$host:$port/alfresco/service/api/groups/$shortName/children/$fullAuthorityName?alf_ticket=$alf_ticket')
    
    # SITE
    URL_TEMPLATE_SITES=string.Template('http://$host:$port/alfresco/service/api/sites/$site?alf_ticket=$alf_ticket')
    URL_TEMPLATE_LOGIN_SITE=string.Template('http://$host:$port/share/page/dologin')
    URL_TEMPLATE_CREATE_SITE=string.Template('http://$host:$port/share/service/modules/create-site')

    # SITE MEMBERSHIPS
    URL_TEMPLATE_MEMBERSHIPS_SITE=string.Template('http://$host:$port/alfresco/service/api/sites/$site/memberships?alf_ticket=$alf_ticket')
    URL_TEMPLATE_LEAVE_MEMBERSHIPS_SITE=string.Template('http://$host:$port/alfresco/service/api/sites/$site/memberships/$group?alf_ticket=$alf_ticket')

    # Tags
    URL_TEMPLATE_TAGS=string.Template('http://$host:$port/alfresco/service/api/node/$node_id/tags?alf_ticket=$alf_ticket&format=json')


    # Workflow definitions
    URL_TEMPLATE_WF_DEFS=string.Template('http://$host:$port/alfresco/service/api/workflow-definitions?alf_ticket=$alf_ticket')
    
    # Workflow instances
    URL_TEMPLATE_WF_INSTANCES=string.Template('http://$host:$port/alfresco/service/api/workflow-instances?alf_ticket=$alf_ticket')
    
    # Workflow tasks
    URL_TEMPLATE_TASK_INSTANCES=string.Template('http://$host:$port/alfresco/service/api/task-instances?authority=${authority}&state=IN_PROGRESS&alf_ticket=$alf_ticket')
    #URL_TEMPLATE_ALL_TASK_INSTANCES=string.Template('http://$host:$port/alfresco/service/api/task-instances?state=IN_PROGRESS&alf_ticket=$alf_ticket')
    
    
    # Audit
    URL_TEMPLATE_AUDIT_CLEAR=string.Template('http://$host:$port/alfresco/service/api/audit/clear/$application?alf_ticket=$alf_ticket')
    
    
    HEADERS={'content-type':'application/json','Accept':'application/json'}
    
    
    def __init__(self,host,port,uid,pwd):
        self.host=host
        self.port=port
        self.uid=uid
        self.pwd=pwd

    

        url_login=AlfSession.URL_TEMPLATE_LOGIN.substitute(self.__dict__)
        payload={'username':uid,'password':pwd}                
        r=requests.post(url_login,headers=AlfSession.HEADERS,data=json.dumps(payload))

        
        if r.status_code:
            self.alf_ticket=json.loads(r.content)['data']['ticket']
            
        else:
            print 'duh, alfresco problem?: ', r.status_code
        

    def logout(self):
        
        url=AlfSession.URL_TEMPLATE_LOGOUT.substitute(self.__dict__)    
        r=requests.delete(url,headers=AlfSession.HEADERS)
        response=json.loads(r.content)
        
        status_code=response['status']['code']
        
        return status_code==200
    
    
    
    def post(self,func,payload):    

        url=AlfSession.URL_TEMPLATE.substitute(self.__dict__,func=func)        
        r=requests.post(url,headers=AlfSession.HEADERS,data=json.dumps(payload))
        return json.loads(r.content)


    def put(self,func,payload=None):
        url=AlfSession.URL_TEMPLATE.substitute(self.__dict__,func=func)        

        r=requests.put(url,headers=AlfSession.HEADERS, data=json.dumps(payload))
        return json.loads(r.content)

    
    def get(self,func, data=None):
        
        url=AlfSession.URL_TEMPLATE.substitute(self.__dict__,func=func)                        
        if data:
            url=self.url+'/'+urllib.quote(data)
                
        r=requests.get(url,headers=AlfSession.HEADERS)
        return json.loads(r.content)
    
        
    def delete(self,url):
   
        r=requests.delete(url,headers=AlfSession.HEADERS)
        return r.content
    
    def sites(self):
        return self.get('sites')
        

    # list users 
    def users(self):
        return self.get('people')['people']

    def add_user(self,user):
        
        return self.post('people',user)

    def delete_user(self,user):

        url=AlfSession.URL_TEMPLATE_USER.substitute(self.__dict__,user=urllib.quote(user))
        return self.delete(url)
        
    # list groups       
    def groups(self):

        return self.get('rootgroups')['data']
        

    ''' add a group
    '''
    def add_group(self, group_name, display_name):

        url=AlfSession.URL_TEMPLATE_ROOTGROUPS.substitute(self.__dict__,shortName=urllib.quote(group_name))
                        
        payload={'displayName':display_name}                                
        r=requests.post(url,headers=AlfSession.HEADERS, data=json.dumps(payload))
        return json.loads(r.content)

   
    ''' remove a group
    '''
    def remove_group(self, group_name):

        url=AlfSession.URL_TEMPLATE_ROOTGROUPS.substitute(self.__dict__,shortName=urllib.quote(group_name))
                        
        r=requests.delete(url,headers=AlfSession.HEADERS)
        return json.loads(r.content)


   
    '''A user joining a group
    '''
    def join_group(self,user,group):
        
        url=AlfSession.URL_TEMPLATE_GROUP_MEMBERSHIP.substitute(self.__dict__,shortName=urllib.quote(group),fullAuthorityName=urllib.quote(user))
        r=requests.post(url,headers=AlfSession.HEADERS)
        return json.loads(r.content)
  
   
    '''A user leaves a group
    '''
    def leave_group(self,user,group):
        
        url=AlfSession.URL_TEMPLATE_GROUP_MEMBERSHIP.substitute(self.__dict__,shortName=urllib.quote(group),fullAuthorityName=urllib.quote(user))
        r=requests.delete(url,headers=AlfSession.HEADERS)
        return json.loads(r.content)
   
   
    ''' Add/remove group a permission from a folder
    '''
    

    
    ''' start and initate a workflow
    '''''
    def workflow_defs(self):
        
        url=AlfSession.URL_TEMPLATE_WF_DEFS.substitute(self.__dict__)
                        
        r=requests.get(url,headers=AlfSession.HEADERS)
        return json.loads(r.content)


    def wf_instances(self):
        
        url=AlfSession.URL_TEMPLATE_WF_INSTANCES.substitute(self.__dict__)
        
                        
        r=requests.get(url,headers=AlfSession.HEADERS)
            
        return json.loads(r.content)['data']

   
    
    def task_instances(self,authority):
        
        url=AlfSession.URL_TEMPLATE_TASK_INSTANCES.substitute(self.__dict__,authority=authority)
        
                        
        r=requests.get(url,headers=AlfSession.HEADERS)
            
        return json.loads(r.content)['data']

   
    def share_login(self):
        
        url=AlfSession.URL_TEMPLATE_LOGIN_SITE.substitute(self.__dict__)
        payload={'username':uid,'password':pwd}
        headers={'Content-Type':'application/x-www-form-urlencoded','User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0'}
        r=requests.post(url,headers=headers,data=payload)
        return r.cookies
        

    def create_site(self,site):

        #log in first
        cookies=self.share_login()
        print 'cookies=',cookies

        # create a session
        url=AlfSession.URL_TEMPLATE_CREATE_SITE.substitute(self.__dict__)
        r=requests.post(url,headers=AlfSession.HEADERS,data=json.dumps(site),cookies=cookies)
        return json.loads(r.content)

     
    def delete_site(self,site):
        url=AlfSession.URL_TEMPLATE_SITES.substitute(self.__dict__,site=urllib.quote(site))
        return self.delete(url)
        
    # site group memebership    
    def join_site(self,site,group):
        
        url=AlfSession.URL_TEMPLATE_MEMBERSHIPS_SITE.substitute(self.__dict__,site=urllib.quote(site))                
        r=requests.post(url,headers=AlfSession.HEADERS, data=json.dumps(group))
        return json.loads(r.content)

    def site_memberships(self,site):
        url=AlfSession.URL_TEMPLATE_MEMBERSHIPS_SITE.substitute(self.__dict__,site=urllib.quote(site))
        r=requests.get(url,headers=AlfSession.HEADERS)
        return json.loads(r.content)


    def leave_site(self,site,group):
        url=AlfSession.URL_TEMPLATE_LEAVE_MEMBERSHIPS_SITE.substitute(self.__dict__,site=urllib.quote(site),group=group)
        r=requests.delete(url,headers=AlfSession.HEADERS)
        return json.loads(r.content)

    ''' Free tags
    ''' 
    def node_tags(self,id):
        url=AlfSession.URL_TEMPLATE_TAGS.substitute(self.__dict__,node_id=id)
        r=requests.get(url,headers=AlfSession.HEADERS)        
        return r.content
    
    def add_tags(self,id,tags):
        url=AlfSession.URL_TEMPLATE_TAGS.substitute(self.__dict__,node_id=id)
        r=requests.post(url,headers=AlfSession.HEADERS,data=json.dumps(tags))
        return r.content


    ''' Audit Service
    '''
    def clear_audit_trial(self,app):
        
        url=AlfSession.URL_TEMPLATE_AUDIT_CLEAR.substitute(self.__dict__,application=urllib.quote(app))                
        return requests.post(url,headers=AlfSession.HEADERS).content

    
            
def test():    

    # configuration
    host='127.0.0.1'
    port='8080'
    uid='admin'
    pwd='admin'
    #uid='vyang'
    #pwd='password'
    
    #host='108.171.177.147'
    #port='80'
    #uid='admin'
    #pwd='NRG211EnergyPrince'

  
    alf_session=AlfSession(host,port,uid,pwd)
    
    # get tag for a node
    #node_id='workspace/SpacesStore/b399fcda-3c67-498e-afb0-f8bbcb763cec'
    
    # add a tag for a node
    #tag=['tag1','tag2']
    #print alf_session.add_tags(node_id,tag)    
    #print alf_session.node_tags(node_id)
    
    
    # create a user
    user={'userName':'u1','password':'password','firstName':'u1.first1','lastName':'u1.last1','email':'u1@example.com'}
    #alf_session.add_user(user)
    
    # delete a user
    #pprint(alf_session.delete_user('sglen'))
    
    #create a site
    #site={'shortName':'chapter1','sitePreset':'site-dashboard','title':'Chapter1','description':'This is site #1','visibility' : 'PUBLIC'}
    #pprint(alf_session.create_site(site))
    
    # delete a site
    #pprint(alf_session.delete_site('site1'))
    
    
    ##add a user to a site with an admin role
    #site_admin={"role":"SiteManager",'person':{'userName':'c1.admin'}}
    #pprint(alf_session.join_site('chapter1',site_admin))
    #
    ### add a group to a site with a role/faces/jsp/dialog/container.jsp
    #group={"role":"SiteCollaborator",'group':{'fullName':'GROUP_chapter1'}}
    #pprint(alf_session.join_site('chapter1',group))
    ##
    ### add a group to a site with a role
    #group={"role":"SiteConsumer",'group':{'fullName':'GROUP_IncoseMember'}}
    #pprint(alf_session.join_site('chapter1',group))
    #
    
    # remove a user group from a site
    #pprint(alf_session.leave_site('site1','GROUP_group1'))
    
    # clear audit log
    #pprint(alf_session.clear_audit_trial('alfresco-access'))
    
    
    # list site membership
    #print '******list site1 membership*****'
    #pprint(alf_session.site_memberships('site1'))
    #
    
    # list all sites
    #print '******list sites*****'
    #pprint(alf_session.sites())
    
    
    # root group management
    group='demogrp'
    #print alf_session.add_group(group, 'DemoGroup')
    #print alf_session.remove_group(group)
    
    # user group membership
    user_id='u1'
    #print alf_session.join_group(user_id,group)
    #print alf_session.leave_group(user_id,group)
    
    
    # list all users
    print '****users*****'
    for p in alf_session.users():
        print p['userName']
    print '****users*****\n'    
    
    # list all the groups
    print '****groups******'
    for g in alf_session.groups():
        print g['shortName']
    print '****groups******\n'
    
    
    # workflow instances
    #
    print '*************wf lists:'
    pprint(alf_session.wf_instances())
    
    # task list by user
    print '*************task lists:'
    tasks=alf_session.task_instances('vyang')
    for t in tasks:
        print t['id']
    
    # log out
    if alf_session.logout():
        print uid,' log out successfully'
    else:
        print uid,'log out error'
   
if __name__ == '__main__':
    test()
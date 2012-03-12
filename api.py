#!/usr/bin/env python
import json
from pprint import pprint
import requests
import urllib
import string


class AlfSession(object):

    # url templates
    URL_TEMPLATE=string.Template('http://$host:$port/alfresco/service/api/$func?alf_ticket=$alf_ticket')
   
    # login logout
    URL_TEMPLATE_LOGIN=string.Template('http://$host:$port/alfresco/service/api/login')
    URL_TEMPLATE_LOGOUT=string.Template('http://$host:$port/alfresco/service/api/login/ticket/$alf_ticket?alf_ticket=$alf_ticket&format=json')
    
    # SITE
    URL_TEMPLATE_SITES=string.Template('http://$host:$port/alfresco/service/api/sites/$site?alf_ticket=$alf_ticket')
    URL_TEMPLATE_LOGIN_SITE=string.Template('http://$host:$port/share/page/dologin')
    URL_TEMPLATE_CREATE_SITE=string.Template('http://$host:$port/share/service/modules/create-site?alf_ticket=$alf_ticket')

    # SITE MEMBER
    URL_TEMPLATE_MEMBERSHIPS_SITE=string.Template('http://$host:$port/alfresco/service/api/sites/$site/memberships?alf_ticket=$alf_ticket')
    URL_TEMPLATE_LEAVE_MEMBERSHIPS_SITE=string.Template('http://$host:$port/alfresco/service/api/sites/$site/memberships/$group?alf_ticket=$alf_ticket')
    
    HEADERS={'content-type':'application/json','Accept':'application/json'}
    
    
    def __init__(self,host,port,uid,pwd):
        self.host=host
        self.port=port
        self.uid=uid
        self.pwd=pwd
        url_login=AlfSession.URL_TEMPLATE_LOGIN.substitute(host=host,port=port)
        payload={'username':uid,'password':pwd}                
        r=requests.post(url_login,headers=AlfSession.HEADERS,data=json.dumps(payload))
        if r.status_code:
            self.ticket=json.loads(r.content)['data']['ticket']
        else:
            print 'duh, alfresco problem?: ', r.status_code
        

    def logout(self):
        
        url=AlfSession.URL_TEMPLATE_LOGOUT.substitute(host=host,port=port,alf_ticket=self.ticket)
            
        r=requests.delete(url,headers=AlfSession.HEADERS)
        response=json.loads(r.content)
        
        status_code=response['status']['code']
        
        return status_code==200
    
    
    
    def post(self,func,payload):    
    
        url=AlfSession.URL_TEMPLATE.substitute(func=func,host=self.host,port=self.port,alf_ticket=self.ticket)
            
        r=requests.post(url,headers=AlfSession.HEADERS,data=json.dumps(payload))
        return json.loads(r.content)

    def put(self,func,payload=None):
        
        url=AlfSession.URL_TEMPLATE.substitute(func=func,host=host,port=port,alf_ticket=self.ticket)
                
        r=requests.put(url,headers=AlfSession.HEADERS, data=json.dumps(payload))
        return json.loads(r.content)

    
    def get(self,func, data=None):
        
        url=AlfSession.URL_TEMPLATE.substitute(func=func,host=self.host,port=self.port,alf_ticket=self.ticket)
        
        if data:
            url=url+'/'+urllib.quote(data)
                
        r=requests.get(url,headers=AlfSession.HEADERS)
        return json.loads(r.content)
    
        
    def delete(self,url):
        
        r=requests.delete(url,headers=AlfSession.HEADERS)
        return r.content
    def sites(self):
        return self.get('sites')
        

    def users(self):
        return self.get('people')['people']
       
    def groups(self):
        return self.get('groups')['data']
   
    def share_login(self):
        
        url=AlfSession.URL_TEMPLATE_LOGIN_SITE.substitute(host=self.host,port=self.port)
        r=requests.post(url,auth=(self.uid,self.pwd))
        return r.cookies
        

    def create_site(self,site):

        #log in first
        cookies=self.share_login()
        print cookies

        # create a session
        url=AlfSession.URL_TEMPLATE_CREATE_SITE.substitute(host=self.host,port=self.port,alf_ticket=self.ticket)
        r=requests.post(url,headers=AlfSession.HEADERS,data=json.dumps(site),cookies=cookies)
        return json.loads(r.content)

     
    def delete_site(self,site):
        url=AlfSession.URL_TEMPLATE_SITES.substitute(host=self.host,port=self.port,alf_ticket=self.ticket,site=urllib.quote(site))
        return self.delete(url)
        
    # site group memebership    
    def group_join_site(self,site,group):
        
        url=AlfSession.URL_TEMPLATE_MEMBERSHIPS_SITE.substitute(host=host,port=port,alf_ticket=self.ticket,site=urllib.quote(site))                
        r=requests.post(url,headers=AlfSession.HEADERS, data=json.dumps(group))
        return json.loads(r.content)

    def group_leave_site(self,site,group):
        url=AlfSession.URL_TEMPLATE_LEAVE_MEMBERSHIPS_SITE.substitute(host=self.host,port=self.port,alf_ticket=self.ticket,site=urllib.quote(site),group=group)
        r=requests.delete(url,headers=AlfSession.HEADERS)
        return json.loads(r.content)

   
    def site_memberships(self,site):
        url=AlfSession.URL_TEMPLATE_MEMBERSHIPS_SITE.substitute(host=self.host,port=self.port,alf_ticket=self.ticket,site=urllib.quote(site))
        r=requests.get(url,headers=AlfSession.HEADERS)
        return json.loads(r.content)
        
        

# configuration
host='127.0.0.1'
port='8080'
uid='admin'
pwd='admin'

alf_session=AlfSession(host,port,uid,pwd)

#invite someone to the site

#create a site
#site={'shortName':'site2','sitePreset':'site-dashboard','title':'Chapter','description':'This is site','visibility' : 'PUBLIC'}
#pprint(alf_session.create_site(site))

# delete a site
#pprint(alf_session.delete_site('site1'))


# add a group to a site with a role
#group={"role":"SiteConsumer",'group':{'fullName':'GROUP_group1'}}
#pprint(alf_session.group_join_site('site1',group))

# remove a group from a site
#pprint(alf_session.group_leave_site('site1','GROUP_group1'))


# list site membership
print '******list site1 membership*****'
pprint(alf_session.site_memberships('site1'))


# list all sites
print '******list sites*****'
pprint(alf_session.sites())


# create a user
#user={'userName':'u2','password':'incose','firstName':'first1','lastName':'last1','email':'u2@incose.org'}
#user.update(data)
#pprint(json.loads(post('people',user)))

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




# log out
if alf_session.logout():
    print uid,' log out successfully'
else:
    print uid,'log out error'
    
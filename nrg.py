#!/usr/bin/env python
import rest

uids=['dennis.wang@nrgenergy.com','thomas.neri@nrgenergy.com', \
        
    'thomas.reagan@nrgenergy.com','crystal.clark@nrgenergy.com','randall.hickok@nrgenergy.com']

default_pwd='Passw0rd'

class User(object):
    def __init__(self,email_addr):
        self.userName=email_addr
        self.email=email_addr
        self.password=default_pwd
        self.firstName,self.lastName=self.userName.split('@')[0].split('.')
        self.firstName=self.firstName.title()
        self.lastName=self.lastName.title()

def create_users():

    
    return [User(e).__dict__ for e in emails]
    

def nrg():



    #configuration
    host='108.171.177.147'
    port='8080'

    for uid in uids:
        alf_session=rest.AlfSession(host,port,uid,default_pwd)
        print alf_session
        alf_session.logout()    


    uid='admin'
    pwd='NRG211EnergyPrince'

          
    alf_session=rest.AlfSession(host,port,uid,pwd)

    #for u in create_users():
    #    print alf_session.add_user(u)
    
    
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
        
if __name__ == '__main__':
    nrg()
    
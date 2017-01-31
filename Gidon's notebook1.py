
# coding: utf-8

# In[1]:

from model import *


# In[1]:




# In[2]:

## Add a New Member
member1 = Member(name="Lorenzo", email="lorenzo@gmail.com")
password="hello"
member1.hash_password(password)
session.add(member1)
session.commit()


# In[3]:

#Read the first member from the database
first_member=session.query(Member).first()


# In[4]:

first_member.name


# In[5]:

first_member.password_hash


# In[6]:

#Add an event
event1= Event(name="Skiing", location = "Chourchevel", date = "First of February")
session.add(event1)
session.commit()


# In[7]:

first_event=session.query(Event).filter_by(name="Skiing").first()


# In[8]:

first_event.name


# In[9]:

#MAKE GIDONS ACCOUNT
#GIDON MAKES AN EVENT
#GIDON INVITES LORENZO TO AN EVENT
member2 = Member(name="Gidon", email="gidon@gmail.com")
password="sup"
member2.hash_password(password)
session.add(member2)
session.commit()


# In[10]:

event1.owner_id=member2.id


# In[11]:

event1.owner.name


# In[12]:

def invite(event_id,member_id):
    member = session.query(Member).filter_by(id=member_id).one()
    event = session.query(Event).filter_by(id=event_id).one()
    invitation=InvitesAssociation(member_id = member_id, event_id = event_id, event = event, attending=False)
    event.invited.append(invitation)
    session.add_all([invitation,event,member])
    session.commit()
    


# In[13]:

invite(event1.id,member1.id)


# In[17]:

my_events = member1.events


# In[20]:

my_first_event = my_events[0]


# In[22]:

my_first_event.event.name


# In[ ]:




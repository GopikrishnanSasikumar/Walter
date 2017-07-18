from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import MetaData,delete
from sqlalchemy.sql import select,and_,exists
import os
from mlengine import fitandpredict
import random
import datetime
class queryrunner(object):
      def __init__(self,messege):
          self.response={}
          self.bookname=[]
          self.authors=[]
          self.desc=[]
          self.countavail=[]
          self.returndate=[]
          self.bookid=[]
          
          self.rating=[]
          self.rem=[]
          
          self.f=os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
          self.engine  = create_engine("sqlite:///"+os.path.join(self.f,"library_database","libraryoriginal.db"),echo=False)
          
          #self.engine = create_engine(r'sqlite:///C:\Users\HP\Desktop\projects\Walter\library database\libraryoriginal.db', echo=True)
          self.metadata = MetaData(bind=self.engine)
          self.connection = self.engine.connect()
          self.Books=Table('Books',self.metadata,autoload=True)
          self.BookDetail=Table('BookDetail',self.metadata,autoload=True)
          self.Bookreturn=Table('Bookreturn',self.metadata,autoload=True)
          self.Reminder=Table('Reminder',self.metadata,autoload=True)
          self.students=Table('students',self.metadata,autoload=True)
          self.greetings(messege)
          self.findbook(messege)
          self.login(messege)
          self.setandcancelreminder(messege)
          self.getreminder(messege)
          self.returndates(messege)
          self.fine(messege)
          self.greminder(messege)
          self.finereminder(messege)
          self.bookreminder(messege)
          self.getdesc(messege)
          self.libraryadmin(messege)
          self.renew(messege)
          self.ratingdef(messege)
          self.ratingcal(messege)
          self.connection.close()
      def login(self,messege):
          #res='pranav'
          if 'label' in messege:
             if messege['label']=='login':
                  bar=messege['barcode'].lower()
                  s=select([self.students.c.Name]).where(and_(self.students.c.Barcodeno==bar))
                  result=self.connection.execute(s)
                  for i in result:
                      res=i.Name
                  self.response={}
                  try:
                      res
                  except NameError:
                      self.response['status']='no'
                  else:
                      self.response['status']='yes'
                      self.response['name']=res
                  self.response['label']='login'

      def setandcancelreminder(self,messege):
          if 'label' in messege:
              if messege['label']=='cancelreminder':
                  self.bookname=[]
                  if 'barcode' in messege:
                      userid=messege['barcode'].lower()
                      k=messege['bookname'].lower()
                      s=select([self.BookDetail.c.Author,self.BookDetail.c.Bookname]).where(and_(self.BookDetail.c.Bookname==k))
                      result=self.connection.execute(s)
                  
                      for i in result:
                          k=select([self.Reminder.c.Bookname]).where(and_(self.Reminder.c.Bookname==k,self.Reminder.c.Author==i.Author,self.Reminder.c.Barcodeno==userid))
                          res=self.connection.execute(k)
                      for j in res:
                          self.bookname.append(j.Bookname)
                      if len(self.bookname)==0:
                         
                         
                         s=self.connection.execute(self.Reminder.insert().values(Barcodeno=userid,Bookname=i.Bookname,Author=i.Author))
                            
                        
                         k=select([self.Reminder.c.Bookname]).where(and_(self.Reminder.c.Bookname==k,self.Reminder.c.Author==i.Author,self.Reminder.c.Barcodeno==userid))
                         res=self.connection.execute(k)
                         for j in res:
                            self.bookname.append(j.Bookname)
                         
                         self.response={}
                         self.response['response']='Reminder set'
                         #self.response['response']=self.bookname
                      else:
                         
                         
                         
                         s=delete(self.Reminder,self.Reminder.c.Bookname==k,self.Reminder.c.Barcodeno==userid)
                         self.connection.execute(s)
                            
                         self.response={}
                         
                         self.response['response']='reminder removed'
                         #self.response['response']=self.bookname
     
      def getreminder(self,messege):
          bk=[]
          if 'label' in messege:
              if messege['label']=='bookarrived':
                  k=messege['barcode'].lower()
                  s=select([self.Reminder.c.Bookname]).where(and_(self.Reminder.c.Barcodeno==k))
                  result=self.connection.execute(s)
                  for i in result:
                      self.bookname.append(i.Bookname)
                      
                  for i in self.bookname:
                      s=select([self.BookDetail.c.Count_available,self.BookDetail.c.Bookname]).where(self.BookDetail.c.Bookname==i)
                      result=self.connection.execute(s)
                      for i in result:
                          if(i.Count_available>0):
                              bk.append(i.Bookname)
                  self.response={}
                  self.response['label']='bookarrived'
                  self.response['count']=len(bk)
                  for i in bk:
                      self.response['bookname'+str(bk.index(i))]=i
                  #trans=self.connection.begin()
                  for i in bk:       
                      
                      s=delete(self.Reminder,self.Reminder.c.Bookname==i)
                      self.connection.execute(s)
                      
                  
                  
                  
      def greminder(self,messege):
           if 'label' in messege:
               if messege['label']=='reminder':
                   k=messege['barcode'].lower()
                   s=select([self.Reminder.c.Bookname,self.Reminder.c.Author]).where(and_(self.Reminder.c.Barcodeno==k))
                   result=self.connection.execute(s)
                   for i in result:
                       self.bookname.append(i.Bookname)
                       self.authors.append(i.Author)
                   #self.bookname=['A','B','C','D']
                   #self.authors=['E','F','G','H']
                   self.response={}
                   self.response['label']='reminder'
                   for i in self.bookname:
                       self.response['bookname'+str(self.bookname.index(i))]=i
                   for i in self.authors:    
                       self.response['author'+str(self.authors.index(i))]=i
                   c=len(self.bookname)
                   self.response['ct']=c
                        
      def returndates(self,messege):
          if 'label' in messege:
              if messege['label']=='returndate':
                  k=messege['barcode'].lower()
                  s=select([self.Bookreturn.c.ReturnDate,self.BookDetail.c.Bookname,self.Bookreturn.c.Bookid]).where(and_(self.Bookreturn.c.Barcodeno==k,self.Bookreturn.c.Bookid==self.BookDetail.c.Bookid))
                  result=self.connection.execute(s)
                  for i in result:
                      self.returndate.append(i.ReturnDate)
                      #print(i.ReturnDate)
                      self.bookname.append(i.Bookname)
                      self.bookid.append(i.Bookid)
                  start=-1
                  self.response={}
                  self.response['label']='returndate'
                  for i in self.returndate:
                       self.response['returndate'+str(self.returndate.index(i,start+1))]=i
                       start=start+1
                  for i in self.bookname:    
                       self.response['bookname'+str(self.bookname.index(i))]=i
                  for i in self.bookid:
                      self.response['bookid'+str(self.bookid.index(i))]=i
                  c=len(self.bookname)
                  self.response['ct']=c
      def libraryadmin(self,messege):
          if 'label' in messege:
             if messege['label']=='return':
                k=messege['barcode'].lower()
                m=messege['bookname']
                if k=='1000':
                   o=select([self.BookDetail.c.Count_available]).where(self.BookDetail.c.Bookname==m)
                   res=self.connection.execute(o)
                   f=0
                   for r in res:
                       f=r.Count_available
                       
                       f=f+1
                   
                   a=self.BookDetail.update().where(and_(self.BookDetail.c.Bookname==m)).values(Count_available=f)
                   self.connection.execute(a)
                else:

                   s=select([self.Bookreturn.c.Bookname]).where(and_(self.Bookreturn.c.Barcodeno==k,self.Bookreturn.c.Bookname==m))
                   result=self.connection.execute(s)
                   for i in result:
                       o=select([self.BookDetail.c.Count_available]).where(self.BookDetail.c.Bookname==i.Bookname)
                       res=self.connection.execute(o)
                       f=0
                       s=select([self.Bookreturn.c.ReturnBit]).where(and_(self.Bookreturn.c.Bookname==i.Bookname,self.Bookreturn.c.Barcodeno==k))
                       resu=self.connection.execute(s)
                       for j in resu:
                           bit=j.ReturnBit
                       if bit==False:

                           for r in res:
                               f=r.Count_available
                               f=f+1
                           print(f)
                           a=self.BookDetail.update().where(and_(self.BookDetail.c.Bookname==i.Bookname)).values(Count_available=f)
                           self.connection.execute(a)

                           n=self.Bookreturn.update().where(and_(self.Bookreturn.c.Bookname==i.Bookname,self.Bookreturn.c.Barcodeno==k)).values(ReturnBit=True)  
                           self.connection.execute(n)
                           self.response={}
                           self.response['label']='return'
                           self.response['status']='success'
                       else:
                           self.response={}
                           self.response['status']='unsuccessful'
      def fine(self,messege):
          if 'label' in messege:
              if messege['label']=='fine':
                  k=messege['barcode'].lower()
                  s=select([self.students.c.Fine]).where(self.students.c.Barcodeno==k)
                  result=self.connection.execute(s)
                  for i in result:
                      res=i.Fine
                  try:
                      res
                  except NameError:
                      self.response={}
                      self.response['label']='fine'
                      self.response['fine']=0
                  else:
                      self.response={}
                      self.response['label']='fine'
                      self.response['fine']=res

      def renew(self,messege):
          if 'label' in messege:
              if messege['label']=='renew':
                  #self.response['status']='no'
                  if 'barcode' in messege:
                      k=messege['barcode'].lower()
                      if 'bookid' in messege:
                          i=messege['bookid']
                          #self.response['status']='no'
                          s=select([self.Bookreturn.c.ReturnDate,self.Bookreturn.c.RenewBit]).where(and_(self.Bookreturn.c.Barcodeno==k,self.Bookreturn.c.Bookid==i))
                          result=self.connection.execute(s)
                          for n in result:
                              res=n.ReturnDate
                              ren=n.RenewBit
                          if not res or ren==True:
                              self.response['status']='no'
                          else:
                              j=datetime.datetime.now()
                              j=j.strftime('%d-%m-%Y')
                              res=res.split(" ")[0]
                              d=datetime.datetime.strptime(res,'%d-%m-%Y')
                              
                              d=d.strftime('%d-%m-%Y')
                              
                              if j<d:
                                 d=datetime.datetime.strptime(d,'%d-%m-%Y').date() + datetime.timedelta(days=14)
                                 d=d.strftime('%d-%m-%Y')
                                 #print(d)
                                 s=self.Bookreturn.update().where(and_(self.Bookreturn.c.Barcodeno==k,self.Bookreturn.c.Bookid==i)).values(ReturnDate=d)
                                 self.connection.execute(s)
                                 self.response['status']='yes'
                                 s=self.Bookreturn.update().where(and_(self.Bookreturn.c.Barcodeno==k,self.Bookreturn.c.Bookid==i)).values(RenewBit=True)
                                 self.connection.execute(s)
                              elif j==d:
                                 d=datetime.datetime.strptime(res,'%d-%m-%Y').date() + datetime.timedelta(days=14)
                                 d=d.strftime('%d-%m-%Y')
                                 s=self.Bookreturn.update().where(and_(self.Bookreturn.c.Barcodeno==k,self.Bookreturn.c.Bookid==i)).values(ReturnDate=d)
                                 result=self.connection.execute(s)
                                 self.response['status']='yes'
                                 s=self.Bookreturn.update().where(and_(self.Bookreturn.c.Barcodeno==k,self.Bookreturn.c.Bookid==i)).values(RenewBit=True)
                                 self.connection.execute(s)
                              elif j>d:
                                 
                                 m=datetime.datetime.strptime(res,'%d-%m-%Y').date() + datetime.timedelta(days=14)
                                 m=m.strftime('%d-%m-%Y')
                                 if j>m:
                                    self.response['status']='no'
                                 else:
                                    d=datetime.datetime.strptime(res,'%d-%m-%Y').date() + datetime.timedelta(days=14)
                                    d=d.strftime('%d-%m-%Y')
                                    s=self.Bookreturn.update().where(and_(self.Bookreturn.c.Barcodeno==k,self.Bookreturn.c.Bookid==i)).values(ReturnDate=d) 
                                    result=self.connection.execute(s)
                                    self.response['status']='yes'
                                    s=self.Bookreturn.update().where(and_(self.Bookreturn.c.Barcodeno==k,self.Bookreturn.c.Bookid==i)).values(RenewBit=True)
                                    self.connection.execute(s)
                                    #renew bit should be added
                                 
                            
      def getdesc(self,messege):
          if 'label' in messege:
              if messege['label']=="description":
                 k=messege['bookname'].lower()
            
                 s=select([self.Books.c.Description]).where(and_(self.BookDetail.c.Bookname==k,self.BookDetail.c.Bookname==self.Books.c.Bookname)) 
                 result=self.connection.execute(s)
                 for i in result:
                     self.desc.append(i.Description)
                 self.response={}
                 for i in self.desc:
                       self.response['description']=i
                 
                   
      def findbook(self,messege):
          rems=[]
          if 'findbook' in messege:
             k=str(messege['findbook'])
             if 'barcode' in messege:
                userid=messege['barcode'].lower()
             if 'author' in messege:
                m=str(messege['author'])
                
                #s=select([self.BookDetail.c.Bookname,self.BookDetail.c.Author,self.Books.c.Description,self.BookDetail.c.Count_available]).where(and_(self.BookDetail.c.Bookname==k,self.BookDetail.c.Author==m,self.BookDetail.c.Bookid==self.Books.c.Bookid))
                s=select([self.BookDetail.c.Bookname,self.BookDetail.c.Author,self.BookDetail.c.Count_available]).where(and_(self.BookDetail.c.Bookname==k))                
                result=self.connection.execute(s)
                
                for i in result:
                    o=select([self.Reminder.c.Barcodeno]).where(and_(self.Reminder.c.Barcodeno==userid,self.Reminder.c.Bookname==i.Bookname))
                    res=self.connection.execute(o)
                    kl=list()
                    for r in res:
                        kl.append(r)
                    if len(kl)==0:
                       self.rem.append(False)
                    else:
                       self.rem.append(True) 
                    self.bookname.append(i.Bookname)
                    self.authors.append(i.Author)
                    self.countavail.append(i.Count_available)
                    self.rating.append(i.Rating)
                self.response={}
                for i in self.rating:
                    self.response['rating'+str(self.rating.index(i))]=str(i)
                for i in rems:
                    self.response['reminderset'+str(rem.index(i))]=i
                for i in self.countavail:
                    if(i>0):
                      self.response['available'+str(self.countavail.index(i))]=True
                    else:
                      self.response['available'+str(self.countavail.index(i))]=False
                for i in self.bookname:
                    self.response['findbook'+str(self.bookname.index(i))]=i.title()
                #messege['bookreminder']=k
                for i in self.authors:
                    self.response['author'+str(self.authors.index(i))]=i
                self.response['label']='text'
                
                
                if not self.response['findbook']:
                    self.response["response"]=random.choice(["Sorry i didn't get that","Sorry I don't understand","Nothing found"])
                else:
                    self.response["response"]=random.choice(["here is what i found","Check this out","look at this"])
             
             else:
                m=str(messege["findbook"])
                k=fitandpredict(m)
                for i in k:
                    #self.bookname.append(i)
                    s=select([self.BookDetail.c.Bookname,self.BookDetail.c.Author,self.BookDetail.c.Count_available,self.BookDetail.c.Rating]).where(and_(self.BookDetail.c.Bookname==i))
                    result=self.connection.execute(s)
                    for o in result:
                        
                        #if o.Count_available==0:
                         
                        q=select([self.Reminder.c.Slno]).where(and_(self.Reminder.c.Barcodeno==userid,self.Reminder.c.Bookname==o.Bookname))
                        res=self.connection.execute(q)
                        kl=list()
                        for r in res:
                            kl.append(r)
                        if len(kl)==0:
                           self.rem.append(False)
                        else:
                           self.rem.append(True) 
                        
                        if o.Bookname not in self.bookname:

                           self.bookname.append(o.Bookname)
                           self.authors.append(o.Author)
                           self.countavail.append(o.Count_available)
                           self.rating.append(o.Rating)
                print(self.authors)
                self.response={}
                self.response['check']=self.countavail
                for i in range(len(self.bookname)):
                    
                    self.response['rating'+str(i)]=self.rating[i]
                for i in range(len(self.rem)):
                    self.response['reminderset'+str(i)]=self.rem[i]
                for i in range(len(self.bookname)):
                    if self.countavail[i]>0:
                      self.response['available'+str(i)]=True
                    else:
                      self.response['available'+str(i)]=False  
                
                for i in self.bookname:
                    self.response['findbook'+str(self.bookname.index(i))]=i.title()
                    
                for i in self.authors:    
                    self.response['author'+str(self.authors.index(i))]=i
                c=len(self.bookname)
                self.response['ct']=c
                self.response['label']='text'
                if self.response['ct']==0:
                    self.response["response"]=random.choice(["I don't understand","Sorry I didn't get that","Nothing found"])
                else:
                    self.response["response"]=random.choice(["here is what i found","Check this out","look at this"])
                    
          else:
             pass
      def greetings(self,message):
          
          if 'greetings' in message:
             self.response={}
             self.response['response']=message['greetings']
             self.response['label']='greetings'
             
      def finereminder(self,messege):
          if 'barcode' in messege:
             userid=messege['barcode'].lower()
          if 'finereminder' in messege:
             s=select([self.BookDetail.c.Bookname,self.Bookreturn.c.ReturnDate]).where(and_(self.Bookreturn.c.Barcodeno==userid,self.BookDetail.c.Bookid==self.Bookreturn.c.Bookid))
             #s=select([self.BookDetail.c.Bookname,self.Bookreturn.c.ReturnDate]).where(and_(self.Bookreturn.c.Barcodeno==userid,self.BookDetail.c.Bookname==self.Bookreturn.c.Bookname))
             result=self.connection.execute(s)
             for i in result:
                 self.bookname.append(i.Bookname)
                 self.returndate.append(i.ReturnDate)
             
             self.response={}
             self.response['bookname']=self.bookname
             self.response['returndate']=self.returndate        
      
      def bookreminder(self,messege):
          if 'barcode' in messege:
             userid=messege['barcode'].lower()
          
          if 'bookreminder' in messege:
             k=str(messege['bookreminder'])
             s=select([self.BookDetail.c.Author]).where(and_(self.BookDetail.c.Bookname==k,self.BookDetail.c.Count_available==0))
             result=self.connection.execute(s)
             for i in result:
                self.authors.append(i.Author)
             if self.authors:
                s=self.Reminder.insert().values(Barcodeno=userid,Bookname=k,Author=self.authors[0])
                result=self.connection.execute(s)
                self.response={}
                self.response['response']="Reminder set"
      def ratingdef(self,messege):
          if 'label' in messege:
              if messege['label']=='rating':
                  if 'barcode' in messege:
                      m=list()
                      l=list()
                      k=messege['barcode'].lower()
                      
                      s=select([self.Bookreturn.c.Bookname,self.BookDetail.c.Author]).where(and_(self.Bookreturn.c.Barcodeno==k,self.Bookreturn.c.ReturnBit==True,self.Bookreturn.c.Bookname==self.BookDetail.c.Bookname))
                      res=self.connection.execute(s)
                      for i in res:
                          m.append(i.Bookname)
                          l.append(i.Author)
                      self.response={}
                      if len(m)>0:

                         self.response['label']='rating'
                         self.response['bookname']=m[0]
                         self.response['author']=l[0]
                         #s=delete(self.Bookreturn,self.Bookreturn.c.Bookname==m[0])
                         #self.connection.execute(s)
      def ratingcal(self,messege):
          if 'label' in messege:
              if messege['label']=='rate':
                  k=messege['bookname']
                  m=messege['author']
                  h=messege['ratevalue']
                  s=select([self.BookDetail.c.RateCount,self.BookDetail.c.Rating]).where(and_(self.BookDetail.c.Bookname==k,self.BookDetail.c.Author==m))
                  result=self.connection.execute(s)
                  for i in result:
                       rate=i.Rating
                       ratecount=i.RateCount
                  l=ratecount*rate
                  l=l+h
                  ratecount=ratecount+1
                  l=l/ratecount
                  ratecount=round(ratecount,2)
                  l=round(l,2)
                  s=self.BookDetail.update().where(and_(self.BookDetail.c.Bookname==k,self.BookDetail.c.Author==m)).values(RateCount=ratecount,Rating=l)
                  self.connection.execute(s)
      
      def getoutput(self):
          return self.response
          
      

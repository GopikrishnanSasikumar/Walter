#natural language engine implemented using regex and hardcoding
import random
import re
class nlengine(object):
      def __init__(self,message):
        self.response={}
        self.flag=False
        self.GREETING_KEYWORDS=("hello","hi","hey","what's up","who")
        self.GREETING_RESPONSE=["hello I am walter,how can I help you","Hey I am your library assistant,what can i do for you"]
        self.searchBook(message)
        self.isGreetings(message)
        self.isFineReminder(message)
        self.isThereReminder(message)
        self.remcommand(message)
        self.helpbro(message)
        self.credits(message)
        self.returncommand(message)
        self.logmeout(message)
        if not self.response:
           self.response["findbook"]=message
           self.flag=True
      def isGreetings(self,message):
          for word in message.split(): 
              if word in self.GREETING_KEYWORDS:
                 self.response={}
                 self.response["label"]="greetings"
                 self.response["response"]=random.choice(self.GREETING_RESPONSE)
      def getResult(self):
          if self.flag==True:
              self.response['bookread']="y"
          else:
              self.response['bookread']="n"
          return self.response
      def isFineReminder(self,message):
          for word in message.split():
              if word in ("remind","notify","reminder"):
                 for words in message.split():
                     if words in ("return","return date"):
                        self.response={}
                        self.response["finereminder"]=currentbook

      def credits(self,message):
          for word in message.split():
              if word in ("credit"):
                  self.response={}
                  self.response["label"]="credit"
      def returncommand(self,message):
          k=0
          for word in message.split():
              if word in ("show","open","read","return date","returndate","returndates","return dates"):
                 k=1
              if word in ("return date","returndate","returndates","return dates") and k==1:
                  self.response={}
                  self.response["label"]="returndate"
      def logmeout(self,message):
          for word in message.split():
              if word in ("logout","log out"):
                  self.response={}
                  self.response["label"]="logout"
    
      def remcommand(self,message):
          
          k=0
          for word in message.split():
              if word in ("show","open","read","reminder","reminders"):
                 k=1
              if word in ("reminder","reminders") and k==1:
                  self.response={}
                  self.response["label"]="reminder"
      def helpbro(self,message):
          for word in message.split():
              if word in ("help"):
                  self.response={}
                  self.response["label"]="help"
      def isThereReminder(self,message):
          for word in message.split():
              if word in ("remind","notify","tell","reminder"):
                 for words in message.split():
                     if words in ("available","arrive"):
                        self.response={}
                        self.response["bookreminder"]=currentbook
      def searchBook(self,message):
          
          global currentbook
          line=message
          actionobj1=re.search(r'find',line,re.M|re.I)
          actionobj2=re.search(r'get',line,re.M|re.I)
          actionobj3=re.search(r'want',line,re.M|re.I)
          entityobj=re.search(r'book',line,re.M|re.I)
          forobj=re.search(r'for',line,re.M|re.I)
          if actionobj1:
             if entityobj:
                if forobj:
                   k=message.split("for")[1]
                   byobj=re.search(r'by',k,re.M|re.I)
                   if byobj:
                      k=k.split("by")
                      self.response={}
                      k=k[0][1:]
                      self.response["findbook"]=k[:-1]

                      self.response["author"]=k[1][1:]
                      currentbook=self.response["findbook"]
                      self.response["booksearch"]=True
                   else:
                      self.response={}
                      self.response["findbook"]=k[1:]
                      self.flag=True
                      currentbook=k
                else:
                   k=message.split("book")[1]
                   byobj=re.search(r'by',k,re.M|re.I)
                   if byobj:
                      k=k.split("by")
                      self.response={}
                      self.response["findbook"]=k[0][1:]
                      self.response["author"]=k[1][1:]
                      self.flag=True
                      currentbook=k[0]
                   else:
                      self.response={}
                      self.response["findbook"]=k[1:]
                      self.flag=True
                      currentbook=k
             else:
                k=message.split("find")[1]
                byobj=re.search(r'by',k,re.M|re.I)
                if byobj:
                   k=k.split("by")
                   self.response={}
                   self.response["findbook"]=k[0][1:]
                   self.response["author"]=k[1][1:]
                   self.flag=True
                   currentbook=k[0]
                else:
                   self.response={}
                   self.response["findbook"]=k[1:]
                   self.flag=True
                   currentbook=k
          elif actionobj2:
               if entityobj:
                  if forobj:
                     k=message.split("for")[1]
                     byobj=re.search(r'by',k,re.M|re.I)
                     if byobj:
                        k=k.split("by")
                        self.response={}
                        self.response["findbook"]=k[0][1:]
                        self.response["author"]=k[1][1:]
                        self.flag=True
                        currentbook=k[0]
                     else:
                        self.response={}
                        self.response["findbook"]=k[1:]
                        self.flag=True
                        currentbook=k
                  else:
                     k=message.split("book")[1]
                     byobj=re.search(r'by',k,re.M|re.I)
                     if byobj:
                        k=k.split("by")
                        self.response={}
                        self.response["findbook"]=k[0][1:]
                        self.response["author"]=k[1][1:]
                        self.flag=True
                        currentbook=k[0]
                     else:
                        self.response={}
                        self.response["findbook"]=k[1:]
                        self.flag=True
                        currentbook=k
               else:
                  k=message.split("get")[1]
                  byobj=re.search(r'by',k,re.M|re.I)
                  if byobj:
                     k=k.split("by")
                     self.response={}
                     self.response["findbook"]=k[0][1:]
                     self.response["author"]=k[1][1:]
                     self.flag=True
                     currentbook=k[0]
                  else:
                     self.response={}
                     self.response["findbook"]=k[1:]
                     self.flag=True
                     currentbook=k
          elif actionobj3:
               if entityobj:
                  if forobj:
                     k=message.split("for")[1]
                     byobj=re.search(r'by',k,re.M|re.I)
                     if byobj:
                        k=k.split("by")
                        self.response={}
                        self.response["findbook"]=k[0][1:]
                        self.response["author"]=k[1][1:]
                        self.flag=True
                        currentbook=k[0]
                     else:
                        self.response={}
                        self.response["findbook"]=k[1:]
                        self.flag=True
                        currentbook=k
                  else:
                     k=message.split("book")[1]
                     byobj=re.search(r'by',k,re.M|re.I)
                     if byobj:
                        k=k.split("by")
                        self.response={}
                        self.response["findbook"]=k[0][1:]
                        self.response["author"]=k[1][1:]
                        self.flag=True                        
                        currentbook=k[0]
                     else:
                        self.response={}
                        self.response["findbook"]=k[1:]
                        self.flag=True
                        currentbook=k
               else:
                  k=message.split("want")[1]
                  byobj=re.search(r'by',k,re.M|re.I)
                  if byobj:
                     k=k.split("by")
                     self.response={}
                     self.response["findbook"]=k[0][1:]
                     self.response["author"]=k[1][1:]
                     self.flag=True
                     currentbook=k[0]
                  else:
                     self.response={}
                     self.response["findbook"]=k[1:]
                     self.flag=True
                     currentbook=k



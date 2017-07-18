from nlengine import nlengine #for natural language processing
from flask import Flask,request,jsonify
from query import queryrunner 
import json
import sys
app = Flask(__name__)

    
@app.route('/',methods=['GET','POST'])
def send_recieve():
   if request.method=='POST':
      #if there is incoming data from front end
      try:
         data = json.loads(request.data.decode('utf-8')) #loading json data recieved
         log(data)
      except (ValueError,TypeError,KeyError):
         print("Error caught")
         return json.dumps({'label': 'error'})
      
      if data['label']=="text":
         #for voice commands
         k=nlengine(data["request"])
         message=k.getResult()
         k=message["bookread"]
         
         if k=="y":
            #if need database access
            message['barcode']=data['barcode']
            k=queryrunner(message)
            message=k.getoutput()
            
            

         log(message)
         return json.dumps(message)
      else:
         #button clicks
         k=queryrunner(data)
         message=k.getoutput()
         message=json.dumps(message)
         log(message)
         return message
def log(message): 
    if message: 
       print(str(message))       
       sys.stdout.flush()
    else:
       print("NULL")
       sys.stdout.flush()
port_=int(sys.argv[1])

if __name__ == '__main__':
    app.debug = True
    app.run(host='192.168.43.29',port=port_)


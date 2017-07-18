import pandas as pd
import numpy as np
import pickle 
x=pd.ExcelFile("books.xlsx")
df=x.parse("Sheet1")
df1=df[[df.columns[1],df.columns[5]]]
df1=df1.iloc[[i for i in range(750)]]
df1=df1.dropna()
df=df1['Title of Book'].values.tolist()
df=[x.lower() for x in df]
print(df[:10])
#print(df1)
#df=df[df['Title of Book']!='Instrumentation']
out=open('first.pkl','wb')
pickle.dump(df,out)
out.close()

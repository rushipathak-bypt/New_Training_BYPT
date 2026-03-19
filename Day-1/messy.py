import pandas as pd,requests

def   myFunction( ):
 print("starting")
 x=1+2
 y=  3+4
 if(x<y):
  print( "x is smaller" )
 else:
     print("y is smaller")
 data ={"name":"Rushi","age":20}
 df=pd.DataFrame(data,index=[0])
 print( df )
 unused_var=10
 for  i in range( 5 ):
  print(i)

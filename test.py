import socket            
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
print ("Socket successfully created")
 
port = 40000             

s.bind(('', port))        
print ("socket binded to %s" %(port))
 
s.listen(5)    
print ("socket is listening")           

while True:
  c, addr = s.accept()    
  print ('Got connection from', addr )
  c.send('Thank you for connecting'.encode())
  c.close()
  break
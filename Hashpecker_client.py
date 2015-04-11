from socket import *
import sys


Alpha="0123456789AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
ToSend=''
default_stp=20000000

Hash=0
Type=0
Start=0
stp=0

PORT=4321 # the server's port

# .... Scanning ....

def GetSubnet():
	s=socket(AF_INET,SOCK_DGRAM)
	if s.connect_ex(("8.8.8.8",80)):
		del s
		return None
	res=str(s.getsockname()[0])
	s.close()
	del s
	if not res:
		return None
	if res[-2]==".":
		return res[:-2]+"."
	elif res[-3]==".":
		return res[:-3]+"."
	elif res[-4]==".":
		return res[:-4]+"."
	return None

while not Hash:
    Hash=str(raw_input('Your hash: '));
    if not Hash:
        print "You didn't enter anything"
while not Type:
    Type=str(raw_input('Type of the hash: '))
    if not Type:
        print "You didn't enter anything"
if str(raw_input('Set number to start from? (y/N)  '))=="y":
    while not Start:
        Start=int(raw_input('Start: '))
        if not Start:
            print "You didn't enter anything"
else:
    Start=1
    print "Start set to default"
if str(raw_input('Set step number? (y/N)  '))=="y":
    while not stp:
        stp=int(raw_input('Start: '))
        if not stp:
            print "You didn't enter anything"
else:
    stp=default_stp
    print "Step set to default"
	
try:
	sbn=GetSubnet()
except:
	add=''
	while not add:
		add=str(raw_input('Your IP address: '))
		if add[-2]==".":
			sbn=add[:-2]+"."
		elif add[-3]==".":
			sbn=add[:-3]+"."
		elif add[-4]==".":
			sbn=add[:-4]+"."
		else: 
			print 'Incorrect IP address'
			add=''
	
print '\nScanning subnet {} - {}...\n\n'.format(sbn+str(0),sbn+str(255))

servers=[]
	
for x in xrange(0,256):
	new_addr=sbn+str(x)
	so=socket(AF_INET,SOCK_STREAM)
	so.settimeout(0.2)
	if not so.connect_ex((new_addr,PORT)):
		
		so.send("HELLO"+'\0')
		res=so.recv(1024)

		if res=="SERVER_OK":
			servers.append(new_addr)
			print "Server found: {}".format(new_addr)
		elif res=="ERRFULL":
			print 'Server {} is full, skipping...'.format(new_addr)
	del so, new_addr
	
if not len(servers):
	print '\nScan finished, found no servers, exiting'
	sys.exit(-1)
		
print '\nScan finished, found {} servers\n'.format(len(servers))

# .... End of scan ....

MAX_STOP=0
MAX_START=0
STEP=stp
OK=True 


print 'Communicating with servers...\n'

for srv in servers:
    if srv==servers[0]:
        MAX_START=Start
        MAX_STOP=MAX_START+STEP
    else:
        MAX_START=MAX_STOP
        MAX_STOP+=STEP
    ToSend="{}:{}:{}:{}:{}".format(Hash,Type,MAX_START,MAX_STOP,Alpha)


    s=socket()
    if s.connect_ex((srv,PORT)):
        print 'Failed to send!'
        break 
    print 'Connected to ',srv
    s.sendall(ToSend+'\0')
    resp=s.recv(1024)
    if resp=="ALLOK":
        print "Data sent successfully to {}".format(srv)
    elif resp=="ERRFULL":
        print 'WARNING: server {} is full, range will be lost!'.format(srv)
    elif resp=="ERRHASH":
        print 'ERROR: wrong hash!'
        OK=False 
        s.close()
        break
    elif resp=="ERRMSG":
        print 'ERROR: malformed message!'
        OK=False
        s.close()
        break
    elif resp=="ERRTYPE":
        print 'ERROR: this hash type is not supported or incorrect!'
        OK=False 
        s.close()
        break
    elif resp=="ERRWRONGTYPE":
        print 'ERROR: the hash is not of the supplied type!'
        OK=False
        s.close()
        break
    elif resp=="ERRSTART":
        print 'ERROR: number to start from is incorrect!'
        OK=False
        s.close()
        break
    elif resp=="ERRSTOP":
        print 'ERROR: number to stop at is incorrect!'
        OK=False
        s.close()
        break
    elif resp=="ERRALPHA":
        print 'EOORO: alphabet must contain more than one character!'
        OK=False
        s.close()
        break
	s.close()
	
if not OK:
	sys.exit(-1)
print 'Starting server...\n'
sock=socket()
sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
sock.bind(('0.0.0.0',1234))
sock.listen(5)
found=False 

while not found and OK:
    conn,addr=sock.accept()
    data=str(conn.recv(1024)).split(':')
    if data[0]=="ERRNOTFOUND":
        print 'Tried {} - {}, continuing...'.format(data[1],data[2])
        MAX_START=MAX_STOP
        MAX_STOP+=STEP
        
        ToSend="{}:{}:{}:{}:{}".format(Hash,Type,MAX_START,MAX_STOP,Alpha)
            
        s=socket()
        s.connect((addr[0],PORT))
        s.sendall(ToSend+'\0')
        resp=s.recv(1024)
        
        if resp=="ERRHASH":
            print 'Error: wrong hash!'
            OK=False
        elif resp=="ERRTYPE":
            print 'This hash type is not supported or incorrect!'
            OK=False
        elif resp=="ERRMSG":
            print 'ERROR: malformed message!'
            OK=False
            s.close()
            break
        elif resp=="ERRWRONGTYPE":
            print 'The hash is not of the supplied type!'
            OK=False
        elif resp=="ERRSTART":
            print 'Number to start from is incorrect!'
            OK=False
        elif resp=="ERRSTOP":
            print 'Number to stop at is incorrect!'
            OK=False
        elif resp=="ERRALPHA":
            print 'Alphabet must contain more than one character!'
            OK=False
        s.close()
    elif data[0]=="FND":
        print '\n\n\tFound: {}\n\tBy {}\n'.format(data[1],addr[0])
        found=True
    else:
        print "Got unknown data: '{}'".format(data);

if not OK:
    sys.exit(-1)

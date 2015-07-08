import socket,struct
import array

s = socket.socket(socket.AF_PACKET,socket.SOCK_RAW,0x0800) 
s.bind(('eth1', 50007))


def ip_to_mac(ip):
    mac_old=ip.split('.')
    for i in range(len(mac_old)):
        mac_old[i]=hex(int(mac_old[i])).replace('0x','')
        if len(mac_old[i] ) == 1:
            mac_old[i]=str(0)+mac_old[i]
    mac_new="02:02:"+str(mac_old[0])+":"+str(mac_old[1])+":"+str(mac_old[2])+":"+str(mac_old[3])
    return mac_new

def int_to_byte(num,byte):
    s=hex(int(num)).replace('0x','')
    while len(s) <= byte*2:
         s=str(0)+str(s)

def mac_to_str(mac):
    mac_old=mac.split(':')
    mac_new=""
    for i in range(len(mac_old)):
        mac_new+=mac_old[i]
    return mac_new

def ip_to_str(ip):
    ip_old=ip.split('.')
    ip_new=""
    for i in range(len(ip_old)):
        ip_old[i]=hex(int(ip_old[i])).replace('0x','')
        if len(ip_old[i])==1 :
            ip_new=ip_new+str(0)+ip_old[i]
    return ip_new

def get_send_data(length):
    data=''
    for i in  range(int(length-42)) :
        data+="a"
    return data

sip="10.10.10.200"
dip="40.40.40.200"
pack_length=1000
dmac="00:e0:4c:05:d6:48"


s_mac=str(mac_to_str(ip_to_mac(sip)))
d_mac=str(mac_to_str(dmac))
type_ip="0800"
version="4"
header_length="5"
dcsp="00"
total_length=str(int_to_byte(1500,2))
ID="0000"
frag="4000"
ttl=str(int_to_byte(64,1))
protocal_udp=str(int_to_byte(17,1))
header_checknum="0000"
sourip=str(ip_to_str(sip))
destip=str(ip_to_str(dip))
sour_port=str(int_to_byte(1000,2))
dest_port=str(int_to_byte(1000,2))

udp_length=str(int(pack_length)-20-8) # ip length 20; udp length 8;
udp_checksum="0000"
data=str(get_send_data(int(pack_length)))

rawdata=s_mac+d_mac+type_ip+version+header_length+dcsp+total_length+ID+frag+ttl+protocal_udp+header_checknum+sourip+destip+sour_port+dest_port+udp_length+udp_checksum+data
print "rawdata=",rawdata

#data = ['00', '11', '22', '33', '44', 'cc'] #dest mac
#data += ['66', '77', '88', '99', 'AA', 'aa'] #sour mac 
#data += ['08', '00']  # ip
#data += ['45'] # ip_ver_hlen
#data += ['00'] #DCSP 
#data += ['00','6e'] # tolal_length
#data += ['0000'] #Identification
#data += ['40','00'] #fragment
#data += ['40'] # ttl
#data += ['11'] # udp
#data += ['00','00'] # header checknum
#data += ['c0','a8','02','69'] #source ip
#data += ['c0','a8','02','70'] # dest ip 

# data += ['45', '00', '00', '6E', '00', '00', '00', '00', '04', '06', '99', 'A7', '0A', '00', '04', '1B', '0A', '00', '04', 'C9'] 
#data += ['AA' for i in xrange(90)] 
#data += ['18', '2E', '93', 'CF'] 
#rawdata = array.array('B', [int(i, 16) for i in data[:-4]]) 
senddata=struct.pack('!1000s',rawdata)
print "senddata",senddata
s.send(senddata)
s.close() 

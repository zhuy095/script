# -*- coding:utf-8 -*-  

import encodings,exceptions,socket,re
global_encoding='gbk'
secket_time_out=30
socket.setdefaulttimeout(secket_time_out)

def _unicode_to_utf(unicode_str):
    return unicode(unicode_str).encode('utf-8')

def _searchchar(searchc,chars,expect,tpye='cmd'):
    if tpye=='cmd' :
        reobj=re.compile('%|Error')
        if expect == None or str(expect) == 'None' or expect == '':
            print("disinterest result!")
        #if expect != None and str(expect) != 'None' and reobj.search(chars)  :
        elif reobj.search(chars)  :
            if int(expect) != 0:
                raise ExpectError(message="expect run command success ,actually run failed")
            else :
                print("expect run command failed,actually run failed")
        else:
            if int(expect) == 0:
                raise ExpectError(message="expect run command failed ,actually run success")
            else:
                print("expect run command success,actually run success")
            #print("run command have failed")
            #raise ExpectError(message="run command have failed")

    if searchc != None and str(searchc) != str('None') and searchc != '':
        reobj=re.compile(searchc,re.M)
        if expect == None or str(expect) == 'None' :
            return reobj.search(chars)
        else:
            if reobj.search(chars) :
                if int(expect) == 1:
                    print("search %s : except success,actually success"%searchc)
                else:
                    raise ExpectError("search %s : except fail,actually success"%searchc)
            else:
                if int(expect) == 1:
                    raise ExpectError("search %s : except success,actually failed"%searchc)
                else:
                    print("search %s : except fail,actually fail"%searchc)
    
class ExpectError(Exception):
    """Custom expected error for automated test"""
    def __init__(self, message=None):
        self.message=message
    def __str__(self):
        return("%s"%self.message)
        
class lib_update(object):
    """Controll the server update."""
    def __init__(self):
        pass
    
    def updatelib(self,ip,port):
        """
        port 11211
        """
        ip=_unicode_to_utf(ip)
        port=_unicode_to_utf(port)
        addr=(ip,int(port))
        s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        data="update"
        s.sendto(data,addr)
        message,address=s.recvfrom(8192)
        print("message:%s"%message)
        s.close()
        _searchchar("success",message,1,"update")
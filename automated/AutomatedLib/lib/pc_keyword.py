# -*- coding:utf-8 -*-  

from AutomatedLib.lib.pub_lib import _unicode_to_utf,_searchchar,ExpectError,global_encoding
import subprocess,re,encodings,sys

class winpc_keyword(object):
    def __init__(self):
        pass
        
    def win_show_ip(self,inter='test',searchip=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='netsh interface ip show address "'+inter+'"'
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        reobj=re.compile("^[ ]$")
        if reobj.search(msgs[1])!= None:
            raise ExpectError("show interface %s is fail"%inter)
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        _searchchar(searchip,msg,expect=1,tpye='pc')

    def win_ip_add(self,inter='test',ip=None,netmask=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='netsh interface ip add address "'+inter+'" '+ip+' '+netmask
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=ip)
        
    def win_gw_add(self,inter='test',gw=None,metric=1):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='netsh interface ip add address "'+str(inter)+'" gateway='+str(gw)+' gwmetric='+str(metric)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=gw)
        
    def win_gw_del(self,inter='test',gw=None,metric=1):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='netsh interface ip del address "'+str(inter)+'" gateway='+str(gw)
        #cmd='netsh interface ip del address "'+str(inter)+'" gateway='+str(gw)+' gwmetric='+str(metric)
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=gw)
        
    def win_ip_del(self,inter='test',ip=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='netsh interface ip del address "'+inter+'" addr='+ip+' gateway=all'
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip()

    def win_set_dhcp_ip(self,inter='test'):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='netsh interface ip set address name="'+inter+'" source=dhcp'
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip()
    
    def win_dhcp_renew(self):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='ipconfig /renew'
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip()
    
    def win_dhcp_release(self):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='ipconfig /release'
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip()
        
    def win_set_static_ip(self,inter='test',ip=None,netmask='255.255.255.0'):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='netsh interface ip set address name="'+inter+'" static '+ip+' '+netmask
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=ip)
    
    def win_set_dhcp_dns(self,inter='test',search_dns=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='netsh interface ip set dns  name="'+inter+'" source=dhcp'
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        self.win_show_ip(inter='test',searchip=search_dns)
    
    def win_set_static_dns(self,inter='test',dns_ip=None):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='netsh interface ip set dns  name="'+inter+'" source=static '+dns_ip
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))
        
    def win_clean_arp(self):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='netsh interface ip delete arpcache'
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))

    def win_clean_dns_cache(self):
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        msgs=[]
        cmd='ipconfig /flushdns'
        p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)
        p.wait()
        msgs.append(p.stdout.read())
        msgs.append(p.stderr.read())
        p.terminate()
        msg='\n'.join(msgs)
        print("%s"%unicode(msg,global_encoding))

        
if __name__ == '__main__':
    test=winpc_keyword()
    test.win_show_ip('test')
    test.win_set_static_ip('test','40.40.40.1','255.255.255.0')
    test.win_ip_add('test','30.30.30.1','255.255.255.0')
    test.win_gw_add('test','30.30.30.30','10')
    test.win_ip_del('test','30.30.30.1')
    test.win_set_dhcp_ip('test')
    test.win_dhcp_release()
    test.win_dhcp_renew()
    test.win_set_dhcp_dns('test')
    test.win_set_static_ip('test','40.40.40.1','255.255.255.0')
    test.win_set_static_dns('test','50.50.50.50')
    test.win_clean_arp()
    
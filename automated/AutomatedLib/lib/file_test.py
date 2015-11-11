# -*- coding:utf-8 -*-  

''' ftp client 
author zhuyl
2015-09-02'''

import ftplib,os,re,sys
from pub_lib import _unicode_to_utf,ExpectError

class file_test(object):
    '''docstring for ClassName'''
    def __init__(self):
        pass

    def ftp_file(self,host='',ftp_file='test.file',port=21,user='anonymous',passwd='',act='get',pasv=1,expect=1):
        '''host : ftp server IP ; ftp_file : if act = get,then ftp_file is a file on the server,if act=put then ftp_file is a file on local; port : server port ,default is 21; act : if is get ,then download,if is put,then putload; pasv : if = 1 is pasv ,or is port '''
        print("run keyword:%s"%(sys._getframe().f_code.co_name))
        host=_unicode_to_utf(host)
        ftp_file=_unicode_to_utf(ftp_file)
        port=int(_unicode_to_utf(port))
        user=_unicode_to_utf(user)
        passwd=_unicode_to_utf(passwd)
        act=_unicode_to_utf(act)
        pasv=_unicode_to_utf(pasv)
        result_stat=0

        path='c:\\ftp\\'
        if os.path.isdir(path) is False:
            os.makedirs(path)

        f=ftplib.FTP()
        if pasv==1:
            f.set_pasv(1)
        try:
            f.connect(host,port,timeout=10)
        except Exception :
            if int(result_stat) != int(expect):
                f.quit()
                raise ExpectError("Connect error,Expect and result are not same!")
        f.login(user,passwd)
        if act=='get':
            print("get %s from ftp server %s"%(ftp_file,host))
            localfile=ftp_file
            local_file_tmp=path+ftp_file
            p=re.compile('/')
            localfile=p.sub(r'\\',local_file_tmp)
            path,lfile=os.path.split(localfile)
            if os.path.isdir(path) is False:
                os.makedirs(path)
            remotefile='RETR '+ftp_file
            f.retrbinary(remotefile,open(localfile,'wb').write)
        elif act=='put':
            print("put %s to ftp server %s"%(ftp_file,host))
            if os.path.isfile(path) is False:
                f.quit()
                raise ExpectError("put file is not exit!")
            else:
                remotefile='STOR '+ftp_file
                with open(path+ftp_file,'rb') as file_handler:
                    f.storbinary(remotefile,file_handler,4096)
#                file_handler=open(path+ftp_file,'rb')
#                ftp.storbinary(remotefile,file_handler,4096)
#                file_handler.close()
        result_stat=1
        if int(result_stat) != int(expect):
            f.quit()
            raise ExpectError("Expect and result are not same!")
        f.quit()

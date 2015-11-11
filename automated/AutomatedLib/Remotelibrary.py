# -*- coding:utf-8 -*-  
import sys
from lib.email_test import mail_test
from lib.file_test import file_test
from lib.http_test import http_keyword
from lib.remote_run_key import remote_run_key
from lib.telnet_test import telnet_test
from lib.pc_keyword import winpc_keyword
from lib.clear_all_conf import clear_all_conf
from lib.audit_mysql import audit_mysql

class import_remote_key(mail_test, \
                        file_test, \
                        http_keyword, \
                        remote_run_key, \
                        telnet_test, \
                        winpc_keyword, \
                        clear_all_conf, \
                        audit_mysql ):
    def __init__(slef):
        pass

if __name__ == '__main__': 
    from robotremoteserver import RobotRemoteServer 
    RobotRemoteServer(import_remote_key(), *sys.argv[1:])
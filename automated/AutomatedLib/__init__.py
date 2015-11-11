# -*- coding:utf-8 -*-  
from version import VERSION
_version_=VERSION
#import email_client
from lib.file_test import file_test
from lib.email_test import mail_test
from lib.http_test import http_keyword
from lib.remote_run_key import remote_run_key
from lib.pub_lib import lib_update
from lib.telnet_test import telnet_test
from lib.pc_keyword import winpc_keyword
from lib.clear_all_conf import clear_all_conf
from lib.audit_mysql import audit_mysql

class AutomatedLib(file_test, \
                   mail_test, \
                   http_keyword, \
                   remote_run_key, \
                   lib_update, \
                   telnet_test, \
                   winpc_keyword, \
                   clear_all_conf, \
                   audit_mysql):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
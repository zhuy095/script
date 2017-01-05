import unittest
from mul_sendpack import ip_change,sendPackSocket,vfwScoket,vfw_simulation
import socket

class Test_IP_Change(unittest.TestCase):
    def test_IP_change(self):
        self.assertEqual(ip_change("1.1.1.1",2),['1.1.1.1','1.1.1.2'])
        

class Test_sendPackSocket(unittest.TestCase):
    def setUp(self):
        self.s=sendPackSocket('172.17.23.100',10001)
    def test_sendPackSocket(self):
        self.assertTrue(isinstance(self.s, socket.socket))
        self.assertTrue(u'type=SocketKind.SOCK_DGRAM' in str(self.s))
        self.assertTrue(u"'172.17.23.100', 10001" in str(self.s) )
    def tearDown(self):
        self.s.close()
        
class Test_vfwScoket(unittest.TestCase):
    def setUp(self):
        self.vfws=vfwScoket(ip_change('172.17.23.2',2),4)
    def test_vfws_return(self):
        for sock in self.vfws.keys():
            self.assertIs(type(sock), socket.socket)
    def tearDown(self):
        for sock in self.vfws.keys():
            sock.close()
        
class Test_vfw_simulation(unittest.TestCase):
    def setUp(self):
        ip='172.17.23.100'
        self.vfw_simulation=vfw_simulation(ip,4)
    
    def test_vfw_simulation_core(self):
        self.assertEqual(self.vfw_simulation.core,4)

def suit_mul_sendpack():
    suite=unittest.TestSuite()
    suite.addTest(Test_IP_Change("test_IP_change"))
    #suite.addTest(NginxTest("suite_1"))
    suite.addTest(Test_sendPackSocket("test_sendPackSocket"))
    suite.addTest(Test_vfwScoket("test_vfws_return"))
    suite.addTest(Test_vfw_simulation("test_vfw_simulation_core"))
    unittest.TextTestRunner().run(suite)
    
if __name__ == '__main__':
    suit_mul_sendpack()
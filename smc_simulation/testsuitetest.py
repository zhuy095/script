#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import os,sys
import time
import datetime
import unittest
 
class NginxTest(unittest.TestCase):
    def setUp(self): #如果不需要每个case都预置和清理环境，而是每个class用一次，只需要用setUpClass、tearDownClass代替即可，如果是整个文件只需要用一次，则用要用 setUpModule() 和 tearDownModule() 这两个函数了，注意是函数，与 TestCase 类同级
        #预置环境
        print('--------------NginxTestSetUp--------------\n')
    def tearDown(self): 
        #清理环境
        print('--------------NginxTestClear--------------\n')
         
    def test_nginx(self):
        print('test_nginx')
    
    def test_nginxlog(self):              
        print('test_nginxlog')
         
    @unittest.skip("must skipping") #必须跳过下面用例，相当少用
    def test_mustskip(self):
        print('test_mustskip')
     
    # def test_1(self):
        # a=1
        # return 1
    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")#根据条件跳过下面这个用例
    def test_maybeskip(self):
        print('test_maybeskip')
     
    def suite_1(self):#非test开头的用例在NginxTest中不会被跑到
        print('suite_1')
         
    def suite_2(self):
        print('suite_2')       
     
 
class PhpTest(unittest.TestCase):#因为每个接口的预置环境可能不一样，所以每个接口的用例应该都用单独class来包含，不过每个class的用例都还是要用test开头
    def setUp(self):
        #预置环境
        print('--------------PhpTestSetUp--------------\n')
    def tearDown(self): 
        #清理环境
        print('--------------PhpTestClear--------------\n' )
         
    def test_php(self):
        print('test_php')
    
    def test_phplog(self):              
        print('test_phplog')
     
     
def suite():#这个表示测试集，不要放在class内，否则会提示"没有这样的测试方法在<class'myapp.tests.SessionTestCase'>：的runTest "，我觉得它唯一的好处就是调试的时候可以单独调试某个class而已，我一般不用它，调试时可以注释不需要的class啊 ;-)。不同接口用不同的class也是一种用法，不过那样用我下面说的import不同py的方法更好，因为所有用例写在一起的话文件太大了 ;-)。
    suite = unittest.TestSuite()
    suite.addTest(NginxTest("suite_1"))
    suite.addTest(NginxTest("suite_2"))
    suite.addTest(PhpTest("test_php"))
    suite.addTest(PhpTest("test_phplog"))
    unittest.TextTestRunner().run(suite)
     
if __name__ == '__main__':
    # unittest.main(exit = False,verbosity=2)#它是全局方法，把它屏蔽后，不在suite的用例就不会跑，exit = False表示中间有用例失败也继续执行；还有比较常用的verbosity=2，表示显示def名字
    suite()#执行suite
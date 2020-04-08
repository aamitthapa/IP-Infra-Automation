import paramiko
import time
import string
import os
import sys
import getpass
import xml.etree.ElementTree as ET
import socket
test_set_full=open('Test_Set/CGNAT_CONSUMER_TEST_SET_FULL.xml', "r")
test_set_select=open('test_set_select', "r")
#f=open("test_set.php", "w")
#f1=open("index_base.php", "r")
#f2=open("index_mid.php", "r")
#f3=open("index_end.php", "r")
for lines1 in test_set_full:
#    print lines1
    for lines2 in test_set_select:
#        print lines2
        if lines2 in lines1:
            print lines1
#f.close()
#f1.close()
#f2.close()
#f3.close()

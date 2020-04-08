import paramiko
import time
import string
import os
import sys
import getpass
import xml.etree.ElementTree as ET
import socket
test_set_full=open('Test_Set/CGNAT_CONSUMER_TEST_SET_FULL.xml', "r")
test_set_select=open('test_set_select')
root = tree.getroot()
f=open("test_set.php", "w")
f1=open("index_base.php", "r")
f2=open("index_mid.php", "r")
f3=open("index_end.php", "r")
for lines1 in test_set_full:
    for lines2 in test_set_select:
        if lines2 in lines1:
            print lines
f.close()
f1.close()
f2.close()
f3.close()

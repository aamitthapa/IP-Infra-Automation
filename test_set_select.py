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
test_set_xml=open('Test_Set/test_set.xml', "w")
#f=open("test_set.php", "w")
#f1=open("index_base.php", "r")
#f2=open("index_mid.php", "r")
#f3=open("index_end.php", "r")
#items=test_set_full.split("\n")
test_set_xml.write('''<?xml version="1.0"?>
<test_set> \n''')

for lines1 in test_set_full:
    test_set_select=open('test_set_select', "r")
    for lines2 in test_set_select:
	if  lines2.rstrip() in lines1:
	    test_set_xml.write(lines1)

    test_set_select.close()
test_set_xml.write('''</test_set>''')
#f.close()
#f1.close()
#f2.close()
#f3.close()

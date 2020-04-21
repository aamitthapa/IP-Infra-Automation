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
test_set_xml=open('test_set.xml', "w")
f=open('test_set_complete.php', "w")
f1=open("index_base1.php", "r")
f1_2=open("index_base3.php", "r")
f2=open("index_mid.php", "r")
f3=open("index_end.php", "r")
test_set_xml.write('''<?xml version="1.0"?>
<test_set> \n''')

for lines1 in test_set_full:
    test_set_select=open('test_set_select', "r")
    for lines2 in test_set_select:
	if  lines2.rstrip() in lines1:
	    test_set_xml.write(lines1)

    test_set_select.close()
test_set_xml.write('''</test_set>''')

test_set_xml.close()
tree = ET.parse('test_set.xml')
root = tree.getroot()

for lines in f1:
	f.write(lines)
for lines in f1_2:
	f.write(lines)

for lines in f2:
    f.write(lines)
f.write("<center><h3><label>Test Set Execution Completed</label></h3></center>")
f.write('<form action="load_test_set.php" method="post" class="container">\n')

for test_case in root.findall('test_case'):
        test_case=test_case.attrib.get('name')
        f.write('''<label>'''+ test_case+'''</label><br>\n''')
f.write('''
<input type="submit" name="Download Logs" value="Download Logs"/>
</form>
</div>
</div>
<div class="container">
<div class="jumbotron">
<center><h3><label>Test Logs</label></h3></center>''')
for lines in f3:
	f.write(lines)
f.close()
f1.close()
f2.close()
f3.close()

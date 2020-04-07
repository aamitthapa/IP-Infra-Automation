import paramiko
import time
import string
import os
import sys
import getpass
import xml.etree.ElementTree as ET
import socket
tree = ET.parse('Test_Set/CGNAT_CONSUMER_TEST_SET_FULL.xml')
root = tree.getroot()
f=open("test_set.php", "w")
f1=open("index_base.php", "r")
f2=open("index_mid.php", "r")
f3=open("index_end.php", "r")
for lines in f1:
	f.write(lines)
for lines in f2:
	f.write(lines)
f.write("<center><h3>Select Test Cases to Run</h3></center>")
f.write('<form action="#" method="post" class="container">\n')
f.write('''<input type="checkbox" name= "Select All" value="Select All"><label>Select All</label><br>\n''')
for test_case in root.findall('test_case'):
        test_case=test_case.attrib.get('name')
        f.write('''<input type="checkbox" name= "test_cases[]" value="'''+test_case+'"'+'''><label>'''+ test_case+'''</label><br>\n''')
f.write('''
<input type="submit" name="run" value="Run"/>
</form>''')

f.write('''
<?php
if(isset($_POST['run'])){//to run PHP script on submit
if(!empty($_POST['test_case'])){
// Loop to store and display values of individual checked checkbox.
foreach($_POST['test_case'] as $selected){
echo $selected."</br>";
}
}
}
?>''')

for lines in f3:
	f.write(lines)
f.close()
f1.close()
f2.close()
f3.close()

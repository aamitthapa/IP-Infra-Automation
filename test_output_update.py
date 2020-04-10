import time
import string
import os
import sys
import xml.etree.ElementTree as ET
test_set_full=open('Test_Set/CGNAT_CONSUMER_TEST_SET_FULL.xml', "r")
test_set_select=open('test_set_select', "r")
tree = ET.parse('test_set.xml')
root = tree.getroot()
f=open('test_set_select.php', "w")
f1=open("index_base.php", "r")
f2=open("index_mid.php", "r")
f3=open("index_end.php", "r")
time.sleep(2)

for lines in f1:
	f.write(lines)
for lines in f2:
	f.write(lines)
f.write("<center><h3><label>Below Test Cases are Running</label></h3></center>")
f.write('<form action="load_test_set.php" method="post" class="container">\n')
for test_case in root.findall('test_case'):
        test_case=test_case.attrib.get('name')
        f.write('''<label>'''+ test_case+'''</label><br>\n''')
f.write('''
<input type="submit" name="stop" value="Stop"/>
</form>
</div>
</div>
<div class="container">
<div class="jumbotron">
<center><h3><label>Test Logs</label></h3></center>''')
output=os.system('tail -1000 /Test_Result/test_log')
f.write(output)
for lines in f3:
	f.write(lines)
f.close()
f1.close()
f2.close()
f3.close()

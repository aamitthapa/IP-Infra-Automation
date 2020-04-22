import sys, os, string, threading
import client
import dut
import time
import paramiko
import xml.etree.ElementTree as ET
import interrupt
tree = ET.parse('input.xml')
root = tree.getroot()
timestr = time.strftime("%Y%m%d-%H%M%S")
checkattach=open("checkattach.txt","w")
checkattach.close()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
username="at171y"
password="!qaz2wsx"
for need_automated_traffic in root.findall('need_automated_traffic'):
	need_automated_traffic=need_automated_traffic.attrib.get('name')
for test_name in root.findall('test_name'):
	test_name=test_name.attrib.get('name')
os.mkdir(test_name+"_"+timestr)
os.system("echo "+ test_name+"_"+ timestr+" "+ ">> test_executed.txt")
def createthread(i):
#	try:

		if i==0 and need_automated_traffic=="yes":
#			print("Login in to Client")
			client.main(timestr)
		if i==1:
#			print("Login in to DUT")
			dut.main(timestr)
#	except:
#		print "Keyboard Interrupted, exiting"
#		os.system("bash exitscript.sh")
threads = []
for i in range(0,2):
	t = threading.Thread(target=createthread, args=(i,))
	t.start()
	threads.append(t)
	i=i+1
for t in threads:
	t.join()

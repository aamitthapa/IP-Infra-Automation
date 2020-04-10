import sys, os, string, threading
import client
import dut
import time
import paramiko
import xml.etree.ElementTree as ET
import interrupt
tree = ET.parse('input.xml')
root = tree.getroot()
tree_destination = ET.parse('input.xml')
destination = tree_destination.getroot()
tree_source = ET.parse('test_set.xml')
source = tree_source.getroot()
timestr = time.strftime("%Y%m%d-%H%M%S")
checkattach=open("checkattach.txt","w")
checkattach.close()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
username="at171y"
password="!qaz2wsx"
#os.system('rm Test_Result/test_log')
test_log=open("Test_Result/test_log", "w")
test_log.close()
for need_automated_traffic in root.findall('need_automated_traffic'):
	need_automated_traffic=need_automated_traffic.attrib.get('name')
for test_name in root.findall('test_name'):
	test_name=test_name.attrib.get('name')
#os.mkdir(test_name+"_"+timestr)
i=1
for test_case in source.findall('test_case'):
	name_1=test_case.attrib.get('name')
	apn_1=test_case.attrib.get('apn')
	duration_1=test_case.attrib.get('duration')
	need_automated_traffic_1=test_case.attrib.get('need_automated_traffic')
	bash_script_1=test_case.attrib.get('bash_script')
	need_pcap_1=test_case.attrib.get('need_pcap')
	merge_pcap_1=test_case.attrib.get('merge_pcap')
	debug_enable_1=test_case.attrib.get('debug_enable')
	print "\nExecuting Test case ", i, "\n", "APN ", apn_1, "\n", "Test Case ", name_1, "\n", "Test Duration ", duration_1
	test_log=open("Test_Result/test_log", "a")
	test_log.write("\nExecuting Test case "+ str(i)+"\n"+"APN "+apn_1+"\n"+"Test Case "+name_1+"\n"+"Test Duration "+duration_1+"\n")
	test_log.close()
#	print "APN ",apn_1
#	print "Test Case ", name_1
#	print "Test Duration ", duration_1
	time.sleep(2)
#	print name,apn,duration,need_automated_traffic,bash_script,need_pcap,merge_pcap,debug_enable
        for test_name in destination.findall('test_name'):
        	test_name.set('name', name_1)
        for apn in destination.findall('apn'):
                apn.set('name', apn_1)
        for duration in destination.findall('duration'):
               duration.set('name', duration_1)
        for need_automated_traffic in destination.findall('need_automated_traffic'):
             need_automated_traffic.set('name', need_automated_traffic_1)
        for bash_script in destination.findall('bash_script'):
                bash_script.set('name', bash_script_1)
        for need_pcap in destination.findall('need_pcap'):
                need_pcap.set('name', need_pcap_1)
        for merge_pcap in destination.findall('merge_pcap'):
                merge_pcap.set('name', merge_pcap_1)
        for debug_enable in destination.findall('debug_enable'):
                debug_enable.set('name', debug_enable_1)
	tree_destination.write('input.xml')
	os.system('python execute.py')
	i=i+1

check_run=os.popen('ls -l *"$(date +"%Y%m%d")"*').read()
if check_run == 0 and i==1:
	print "No Test Cases Selected \nExiting!!!!!!"
	test_log=open("Test_Result/test_log", "a")
	test_log.write("No Test Cases Selected \nExiting!!!!!!")
	test_log.close()
	time.sleep(2)
if check_run != 0 and i!= 1:
	os.system('mv *"$(date +"%Y%m%d")"* Test_Result/')
	print "Test Set Complete!!!!!!"
	test_log=open("Test_Result/test_log", "a")
        test_log.write("Test Set Complete!!!!!!")
        test_log.close()
	time.sleep(2)

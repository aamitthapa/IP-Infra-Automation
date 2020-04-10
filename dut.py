import paramiko
import time
import string
import os
import sys
import getpass
import xml.etree.ElementTree as ET
import socket
BASE_DIR=os.getcwd()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_2222 = paramiko.SSHClient()
ssh_2222.set_missing_host_key_policy(paramiko.AutoAddPolicy())
pdnsession=""
timestr =""
GTAC_username = "at171y"
GTAC_password = "Martha@98034"
nodeip=""
check_first=0
failed_node = ""
log_count=0
start = 'hostname' ###used to find the hostname of the node with split in string####
end="."
tree = ET.parse('input.xml')
root = tree.getroot()
for imsi in root.findall('imsi'):
	imsi=imsi.attrib.get('name')
for duration in root.findall('duration'):
	seconds_str=duration.attrib.get('name')
for dut_ip in root.findall('dut_ip'):
	nodeip=dut_ip.attrib.get('name')
for test_name in root.findall('test_name'):
	test_name=test_name.attrib.get('name')
for merge_pcap in root.findall('merge_pcap'):
	merge_pcap=merge_pcap.attrib.get('name')
for delete_pcap in root.findall('delete_pcap'):
	delete_pcap=delete_pcap.attrib.get('name')
for debug_enable in root.findall('debug_enable'):
	debug_enable=debug_enable.attrib.get('name')
for need_pcap in root.findall('need_pcap'):
	need_pcap=need_pcap.attrib.get('name')
for need_automated_traffic in root.findall('need_automated_traffic'):
        need_automated_traffic=need_automated_traffic.attrib.get('name')
#print "imsi: ",imsi
#print "Test Durations: ", seconds_str

def main(timest):
	global timestr
	timestr=timest
	f=open("checkattach.txt", 'r')
	chkattach=f.readline()
#	print chkattach
	time.sleep(1)
	if chkattach=="" and need_automated_traffic=="yes":
		main(timestr)
	else:
		main1(timestr)
#	except:
#		print "Keyboard interruption on dut.py"
#		time.sleep(5)
#		sys.exit()
def main1(timest):
        global timestr
	try:
		ssh.connect(nodeip.rstrip(), port=22, username=GTAC_username, password=GTAC_password, timeout=8)
		execute_command()
	except (paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.NoValidConnectionsError, paramiko.SSHException, socket.timeout):
		print "Authentication failure"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Authentication failure \n")
		test_log.close()
		file_logs = open(BASE_DIR+"/"+test_name+"_"+timestr+"/"+test_name+"_"+timestr+"."+"txt","a")
		file_logs.write("Could not run test, SSH to DUT failed")
		file_logs.close()
		time.sleep(5)
		sys.exit()
def take_logs():
	global log_count
	tree = ET.parse('input_1.xml')
	root = tree.getroot()
#	print(timestr)
	file_logs = open(BASE_DIR+"/"+test_name+"_"+timestr+"/"+test_name+"_DUT_"+timestr+"."+"txt","a")
	if log_count==0:
		print "Taking Pre Logs"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Taking Pre Logs \n")
		test_log.close()
		file_logs.write("########PRELOGS############################################################################################################################################\n")
	if log_count==1:
		print "Taking Logs in between traffic"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Taking Logs in between traffic \n")
		test_log.close()
		file_logs.write("########LOGS in Between Traffic############################################################################################################################\n")
	if log_count==2:
		print "Taking post Logs"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Taking port Logs \n")
		test_log.close()
		file_logs.write("########POSTLOGS###########################################################################################################################################\n")
	#########################################################
	for commands in root.findall('commands'):
		cli=commands.attrib.get('name')
		file_logs.write(cli+"\n")
		stdin, stdout, stderr = ssh.exec_command(cli)
		output = stdout.readlines()
		output_file="".join(output)
		file_logs.write(str(output_file))
		file_logs.write("****************************************************************")
		file_logs.write("\n\n\n")
		if "include nat" in cli:
#			print(output_file.rstrip())
			logs=output_file.split("\n")
			while("" in logs):
				logs.remove("")
#			print(logs)
			i=0
			for items in logs:
				if i!=0:
					file_logs.write("date; show subscriber pdn-service-data-flow " + items.rstrip() +"\n")
					stdin, stdout, stderr = ssh.exec_command("date; show subscriber pdn-service-data-flow " + items.rstrip())
					output = stdout.readlines()
					output_file="".join(output)
					file_logs.write(str(output_file))
					file_logs.write("****************************************************************")
					file_logs.write("\n\n\n")
				i=i+1
	log_count=log_count+1
	file_logs.close()

def execute_command():
	global file_node
	global GTAC_username
	global GTAC_password
	global failed_node
	global start
	global end
	global pdnsession
	global ssh
	print "Connected to DUT", nodeip.rstrip()
	test_log=open("Test_Result/test_log", "a")
	test_log.write("Connected to DUT " + nodeip.rstrip()+"\n")
	stdin, stdout, stderr = ssh.exec_command("show subscriber summary imsi " + imsi)
	output = stdout.readlines()
	output_file="".join(output)
	if output_file.rstrip()=="% No entries found.":
		print "UE not found....exiting"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("UE not found...exiting \n")
		test_log.close()
		file_logs = open(BASE_DIR+"/"+test_name+"_"+timestr+"/"+test_name+"_DUT_"+timestr+"."+"txt","a")
		file_logs.write("Could not run test as UE not found")
		file_logs.close()
		time.sleep(5)
		sys.exit()
	pdnsession_data=output_file.split(" ")
	pdnsession=pdnsession_data[2].rstrip()
	tempfile = open('input.xml', 'r+' )
	tempfiledata = tempfile.read()
	tempfile.close()
	newdata = tempfiledata.replace("$imsi",imsi)
	newdata = newdata.replace("$pdnsession", pdnsession)
	f = open('input_1.xml','w')
	f.write(newdata)
	f.close()
#	file_output.write(str(output_file))
	stdin, stdout, stderr = ssh.exec_command("show subscriber pdn-session "+ pdnsession)
	output = stdout.readlines()
	output_file="".join(output)
#	file_output.write(str(output_file))
	stdin, stdout, stderr = ssh.exec_command("show subscriber pdn-session "+ pdnsession+" " +"| include slot")
	output = stdout.readlines()
	output_file1="".join(output)
	slot=output_file1.split()
	slot_final=slot[1]
	print "UE landed on SLOT ",slot_final
	test_log=open("Test_Result/test_log", "a")
	test_log.write("UE landed on SLOT " + slot_final+"\n")
	##########Check capture status on SAEGW required slot###################
	stdin, stdout, stderr = ssh.exec_command("show network-context SAEGW ip interface-capture-status | include SAEGW_"+slot_final+"_1_5")
	output = stdout.readlines()
	output_file1="".join(output)
	saegw_capture_1=output_file1.split()
	saegw_capture_1_final=saegw_capture_1[4]

	stdin, stdout, stderr = ssh.exec_command("show network-context SAEGW ip interface-capture-status | include SAEGW_"+slot_final+"_2_5")
	output = stdout.readlines()
	output_file1="".join(output)
	saegw_capture_2=output_file1.split()
	saegw_capture_2_final=saegw_capture_2[4]


	##########Check capture status on SGI-CON required slot###################
	stdin, stdout, stderr = ssh.exec_command("show network-context SGI-CON ip interface-capture-status | include GI_"+slot_final+"_1_5")
	output = stdout.readlines()
	output_file1="".join(output)
	sgi_capture_1=output_file1.split()
	sgi_capture_1_final=sgi_capture_1[4]

	stdin, stdout, stderr = ssh.exec_command("show network-context SGI-CON ip interface-capture-status | include GI_"+slot_final+"_2_5")
	output = stdout.readlines()
	output_file1="".join(output)
	sgi_capture_2=output_file1.split()
	sgi_capture_2_final=sgi_capture_2[4]

	############If all the capture status on required slot are disabled.. start capture#######################
	if need_pcap!="yes":
		print "Ignoring Capture"
		print "Wait for ", round(int(seconds_str)/60)+1, " Minutes"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Wait for "+ str(round(int(seconds_str)/60)+1) + " Minutes"+"\n")
		test_log.close()
		for i in range(0,3):
			take_logs()
			time.sleep(int(seconds_str)/3)
		print "done!"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("done! \n")
		os.remove("input_1.xml")
		sys.exit()
	if saegw_capture_1_final=="disabled" and saegw_capture_2_final== "disabled" and sgi_capture_1_final=="disabled" and sgi_capture_2_final== "disabled":
		######Put caputure command here######
		print "Current capture status is disabled on slot ", slot_final, "\n", "Starting Capture"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Current capture status is disabled on slot "+slot_final+"\n"+"Starting Capture"+"\n")
		test_log.close()
		print("network-context SGI-CON ip-interface GI_"+slot_final+"_1_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_GI_"+slot_final+"_1_5")
		print("network-context SGI-CON ip-interface GI_"+slot_final+"_2_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_GI_"+slot_final+"_2_5")
		print("network-context SAEGW ip-interface SAEGW_"+slot_final+"_1_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_SAEGW_"+slot_final+"_1_5")
		print("network-context SAEGW ip-interface SAEGW_"+slot_final+"_2_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_SAEGW_"+slot_final+"_2_5")
		test_log=open("Test_Result/test_log", "a")
		test_log.write("network-context SGI-CON ip-interface GI_"+slot_final+"_1_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_GI_"+slot_final+"_1_5"+"\n"+"network-context SGI-CON ip-interface GI_"+slot_final+"_2_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_GI_"+slot_final+"_2_5"+"\n"+"network-context SAEGW ip-interface SAEGW_"+slot_final+"_1_5 "+"startcapture duration "+seconds_str+" count 100000000 filename "+"AMIT_"+timestr+"_SAEGW_"+slot_final+"_1_5"+"\n"+"network-context SAEGW ip-interface SAEGW_"+slot_final+"_2_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_SAEGW_"+slot_final+"_2_5"+"\n")
		test_log.close()
		ssh.exec_command("network-context SGI-CON ip-interface GI_"+slot_final+"_1_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_GI_"+slot_final+"_1_5")
		ssh.exec_command("network-context SGI-CON ip-interface GI_"+slot_final+"_2_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_GI_"+slot_final+"_2_5")
		ssh.exec_command("network-context SAEGW ip-interface SAEGW_"+slot_final+"_1_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_SAEGW_"+slot_final+"_1_5")
		ssh.exec_command("network-context SAEGW ip-interface SAEGW_"+slot_final+"_2_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_SAEGW_"+slot_final+"_2_5")
		print "Wait for ", round(int(seconds_str)/60)+1, " Minutes"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Wait for "+ str(round(int(seconds_str)/60)+1)+" Minutes"+"\n")
		test_log.close()
		for i in range(0,3):
			take_logs()
			time.sleep(int(seconds_str)/3)
		os.remove("input_1.xml")
		time.sleep(20)
		#############SCP files to local directory##########################
		print "Copying File"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Copying File \n")
		test_log.close()
		ssh_2222 = paramiko.SSHClient()
		ssh_2222.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_2222.connect(nodeip.rstrip(), port=2222, username=GTAC_username, password=GTAC_password)
		print "SFTP on 2222 connected \n Below are the PCAPS created \n"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("SFTP on 2222 connected \n Below are the PCAPS created \n")
		test_log.close()
		stdin, stdout, stderr = ssh_2222.exec_command("ls -l /boot/partitions/ext-storage/varlog/eventlog/AMIT_" + timestr+"*")
		output = stdout.readlines()
		output_file1="".join(output)
		output_file2=output_file1.split("\n")
		for items in output_file2:
			output_file3=items.split()
			if output_file3 !=[]:
				print(output_file3[8])
				test_log=open("Test_Result/test_log", "a")
				test_log.write(output_file3[8]+"\n")
				test_log.close()
		stdin, stdout, stderr = ssh_2222.exec_command("mv /boot/partitions/ext-storage/varlog/eventlog/AMIT_" + timestr+"*"+" "+"~")
		print "Moving and Merging PCAPS"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Moving and Merging PCAPS \n")
		test_log.close()
		time.sleep(2)
		if merge_pcap=="yes":
			stdin, stdout, stderr = ssh_2222.exec_command("mergecap -w GI_MERGED_"+timestr+".pcapng"+ " "+"AMIT_"+timestr+"_"+"GI"+"*")
			stdin, stdout, stderr = ssh_2222.exec_command("mergecap -w GN_MERGED_"+timestr+".pcapng"+ " "+"AMIT_"+timestr+"_"+"SAEGW"+"*")

##########SFTP to copy file###########
		transport=paramiko.Transport((nodeip.rstrip(), 2222))
		transport.connect(username=GTAC_username, password=GTAC_password)
		sftp=paramiko.SFTPClient.from_transport(transport)
		print "Files below are copied"
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Files below are copied \n")
		test_log.close()
		###########Copying merged pcap################
		if merge_pcap=="yes":
			sftp.get("GN_MERGED_"+timestr+".pcapng", BASE_DIR+"/"+test_name+"_"+timestr+"/"+"GN_MERGED_"+timestr+".pcapng")
			sftp.get("GI_MERGED_"+timestr+".pcapng", BASE_DIR+"/"+test_name+"_"+timestr+"/"+"GI_MERGED_"+timestr+".pcapng")
			print "GN_MERGED_"+timestr+".pcapng", "\n"+"GI_MERGED_"+timestr+".pcapng"
			test_log=open("Test_Result/test_log", "a")
			test_log.write("GN_MERGED_"+timestr+".pcapng", "\n"+"GI_MERGED_"+timestr+".pcapng"+"\n")
			test_log.close()
		############copying unmerged pcap##############
		for items in output_file2:
			output_file3=items.split()
			if output_file3 !=[]:
				print(output_file3[8].split("/")[6])
				test_log=open("Test_Result/test_log", "a")
				test_log.write(output_file3[8].split("/")[6]+"\n")
				test_log.close()
				sftp.get(output_file3[8], BASE_DIR+"/"+test_name+"_"+timestr+"/"+output_file3[8][45:])
		######Delete PCAPs from system###################
		if delete_pcap=="yes":
			stdin, stdout, stderr = ssh_2222.exec_command("rm AMIT_"+timestr+"*")
			stdin, stdout, stderr = ssh_2222.exec_command("rm GI_MERGED_"+timestr+"*")
			stdin, stdout, stderr = ssh_2222.exec_command("rm GN_MERGED_"+timestr+"*")

		print("done")
		test_log=open("Test_Result/test_log", "a")
		test_log.write("done! \n")
		test_log.close()
		time.sleep(5)
	else:
		print("Exiting as someone else is running capture")
		test_log=open("Test_Result/test_log", "a")
		test_log.write("Exiting as someone else is running capture \n")
		test_log.close()
		file_logs = open(BASE_DIR+"/"+test_name+"_"+timestr+"/"+test_name+"_"+timestr+"."+"txt","a")
		file_logs.write("Could not run test as someone else is running capture")
		file_logs.close()
		time.sleep(5)
		sys.exit()
if __name__ == "__main__":
	main()

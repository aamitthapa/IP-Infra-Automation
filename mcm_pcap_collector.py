import paramiko
import time
import string
import os
import sys
import getpass
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR2=os.getcwd()
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_2222 = paramiko.SSHClient()
ssh_2222.set_missing_host_key_policy(paramiko.AutoAddPolicy())
file_node = open('nodesip.txt', 'r')
num_nodes = sum(1 for line in open('nodesip.txt'))
timestr = time.strftime("%Y%m%d-%H%M%S")

nodeip=""
check_first=0
failed_node = ""
start = 'hostname' ###used to find the hostname of the node with split in string####
end="."
imsi=file_node.readline().rstrip()
nodeip=file_node.readline().rstrip()
seconds_str=file_node.readline().rstrip()
seconds=int(seconds_str)
GTAC_username =file_node.readline().rstrip()
GTAC_password =file_node.readline().rstrip()
#nodeip_2222=file_node.readline()
def patch_crypto_be_discovery():

    """
    Monkey patches cryptography's backend detection.
    Objective: support pyinstaller freezing.
    """

    from cryptography.hazmat import backends

    try:
        from cryptography.hazmat.backends.commoncrypto.backend import backend as be_cc
    except ImportError:
        be_cc = None

    try:
        from cryptography.hazmat.backends.openssl.backend import backend as be_ossl
    except ImportError:
        be_ossl = None

    backends._available_backends_list = [
        be for be in (be_cc, be_ossl) if be is not None
    ]
def main():
	file_node = open('nodesip.txt', 'r')
	global check_first
	global failed_node
	patch_crypto_be_discovery()
	global nodeip

	try:
		ssh.connect(nodeip.rstrip(), port=22, username=GTAC_username, password=GTAC_password)
		file_node.close()
		execute_command()
	except (paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.NoValidConnectionsError, paramiko.SSHException):
		print("Authentication failure")
		main()
def take_logs():
	file_logs = open("file_logs"+"_"+timestr+"."+"txt","w")
	file_logs.write("show subscriber summary imsi " + imsi+"\n")
	stdin, stdout, stderr = ssh.exec_command("show subscriber summary imsi " + imsi)
	output = stdout.readlines()
	output_file="".join(output)
	file_logs.write(str(output_file))
	file_logs.write("\n\n\n")


	file_logs.write("show subscriber pdn-session " + pdnsession + " "+ "| include slot" +"\n")
	stdin, stdout, stderr = ssh.exec_command("show subscriber pdn-session " + pdnsession + " "+ "| include slot")
	output = stdout.readlines()
	output_file="".join(output)
	file_logs.write(str(output_file))
	file_logs.write("\n\n\n")

	file_logs.write("show subscriber pdn-session " + pdnsession + " "+ "| include nat" +"\n")
	stdin, stdout, stderr = ssh.exec_command("show subscriber pdn-session " + pdnsession + " " + "| include nat "+ "| include "+pdnsession)
	output = stdout.readlines()
	output_file="".join(output)
	file_logs.write(str(output_file))
	file_logs.write("\n\n\n")
#	print(output_file.rstrip())
	logs=output_file.split("\n")
	while("" in logs):
		logs.remove("")
	print(logs)
	for items in logs:
		file_logs.write("show subscriber pdn-service-data-flow " + items.rstrip() +"\n")
		stdin, stdout, stderr = ssh.exec_command("show subscriber pdn-service-data-flow " + items.rstrip())
		output = stdout.readlines()
		output_file="".join(output)
		file_logs.write(str(output_file))
		file_logs.write("\n\n\n")

	file_logs.write("show subscriber pdn-session " + pdnsession + " "+"\n")
	stdin, stdout, stderr = ssh.exec_command("show subscriber pdn-session " + pdnsession)
	output = stdout.readlines()
	output_file="".join(output)
	file_logs.write(str(output_file))
	file_logs.write("\n\n\n")


	file_logs.write("show services subscriber-firewall alg-packet-statistics "+"\n")
	stdin, stdout, stderr = ssh.exec_command("show services subscriber-firewall alg-packet-statistics ")
	output = stdout.readlines()
	output_file="".join(output)
	file_logs.write(str(output_file))
	file_logs.write("\n\n\n")

	file_logs.write("show services subscriber-firewall nat session flow-group verbose "+ pdnsession+"\n")
	stdin, stdout, stderr = ssh.exec_command("show services subscriber-firewall nat session flow-group verbose "+ pdnsession)
	output = stdout.readlines()
	output_file="".join(output)
	file_logs.write(str(output_file))
	file_logs.write("\n\n\n")

	file_logs.write("show subscriber pdn-flow "+ pdnsession+"\n")
	stdin, stdout, stderr = ssh.exec_command("show subscriber pdn-flow "+ pdnsession)
	output = stdout.readlines()
	output_file="".join(output)
	file_logs.write(str(output_file))
	file_logs.write("\n\n\n")

def execute_command():
	global file_node
	global GTAC_username
	global GTAC_password
	global failed_node
	global start
	global end
	global pdnsession
	file_output = open("OUTPUT"+"_"+timestr+"."+"txt","w")
	print("Connected to ", nodeip.rstrip())
	ssh.connect(nodeip.rstrip(), port=22, username=GTAC_username, password=GTAC_password)

	stdin, stdout, stderr = ssh.exec_command("show subscriber summary imsi " + imsi)
	output = stdout.readlines()
	output_file="".join(output)
	if output_file.rstrip()=="% No entries found.":
		print("UE not found....exiting")
		time.sleep(5)
		sys.exit()
	pdnsession_data=output_file.split(" ")
	pdnsession=pdnsession_data[2].rstrip()
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
	print("UE landed on SLOT ",slot_final)
	print("Taking logs")
	take_logs()
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

#	stdin, stdout, stderr = ssh.exec_command("show subscriber pdn-session "+ pdnsession[2].rstrip()+" " +"| include connec")
#	output = stdout.readlines()
#	output_file1="".join(output)
#	print(output_file1)
#	file_output.write(str(output_file1))

#	print(sgi_capture_1_final, sgi_capture_2_final, saegw_capture_1_final, saegw_capture_2_final)
	############If all the capture status on required slot are disabled.. start capture#######################
	if saegw_capture_1_final=="disabled" and saegw_capture_2_final== "disabled" and sgi_capture_1_final=="disabled" and sgi_capture_2_final== "disabled":
		######Put caputure command here######
		print("Current capture status is disabled on slot ", slot_final)
		print("Starting Capture")
		print("network-context SGI-CON ip-interface GI_"+slot_final+"_1_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_GI_"+slot_final+"_1_5")
		print("network-context SGI-CON ip-interface GI_"+slot_final+"_2_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_GI_"+slot_final+"_2_5")
		print("network-context SAEGW ip-interface SAEGW_"+slot_final+"_1_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_SAEGW_"+slot_final+"_1_5")
		print("network-context SAEGW ip-interface SAEGW_"+slot_final+"_2_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_SAEGW_"+slot_final+"_2_5")

		ssh.exec_command("network-context SGI-CON ip-interface GI_"+slot_final+"_1_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_GI_"+slot_final+"_1_5")
		ssh.exec_command("network-context SGI-CON ip-interface GI_"+slot_final+"_2_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_GI_"+slot_final+"_2_5")
		ssh.exec_command("network-context SAEGW ip-interface SAEGW_"+slot_final+"_1_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_SAEGW_"+slot_final+"_1_5")
		ssh.exec_command("network-context SAEGW ip-interface SAEGW_"+slot_final+"_2_5 "+"startcapture duration "+seconds_str+" count 100000000 file-name "+"AMIT_"+timestr+"_SAEGW_"+slot_final+"_2_5")
		print("Wait for ", int(seconds/60)+1, " Minutes")
#		ssh.close()
		time.sleep(seconds+20)
		print("Taking logs")
		take_logs()
		#############SCP files to local directory##########################
		print("Copying File")
		ssh_2222 = paramiko.SSHClient()
		ssh_2222.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh_2222.connect(nodeip.rstrip(), port=2222, username=GTAC_username, password=GTAC_password)
		print("SFTP on 2222 connected")
		print("ls -l /boot/partitions/ext-storage/varlog/eventlog/AMIT_" + timestr+"*")
		stdin, stdout, stderr = ssh_2222.exec_command("ls -l /boot/partitions/ext-storage/varlog/eventlog/AMIT_" + timestr+"*")
		output = stdout.readlines()
		output_file1="".join(output)
		output_file2=output_file1.split("\n")
#		print(output_file2)
		transport=paramiko.Transport((nodeip.rstrip(), 2222))
		#transport.start_client()
#		print("I am here1")
		transport.connect(username=GTAC_username, password=GTAC_password)
#		print("I am here2")
		sftp=paramiko.SFTPClient.from_transport(transport)
		print("Files below are copied")
		for i in range(0,4):
#			print(i)
			output_file3=output_file2[i].split()
			print(output_file3)
			print(output_file3[8])
			sftp.get(output_file3[8], BASE_DIR2+"/"+output_file3[8][45:])
		print("done")
		time.sleep(5)
#		transport=paramiko.Transport((nodeip.rstrip(), 2222))
#		transport.connect(username=GTAC_username, password=GTAC_password)
#		sftp=paramiko.SFTPClient.from_transport(transport)
#		sftp.get("/var/log/eventlog/test.log", "BASE_DIR/")
	else:
		print("Exiting as someone else is running capture")
		time.sleep(5)
		sys.exit()
	#print(output_file1)
	#file_output.write(str(output_file))
	#print ("".join(output))
	file_output.close()
main()

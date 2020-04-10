import paramiko
import time
import string
import os
import sys
import getpass
import xml.etree.ElementTree as ET
import socket
#import getpass ###########for hidden password entry####
BASE_DIR=os.getcwd()
timestr=""
#print(BASE_DIR)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
CLIENT_username="root"
CLIENT_password="techm123"
tree = ET.parse('input.xml')
checkattach=open("checkattach.txt", "w")
file_logs=open("null", "w")
retry_attach=0
root = tree.getroot()
for apn in root.findall('apn'):
	apn=apn.attrib.get('name')
for imsi in root.findall('imsi'):
        imsi=imsi.attrib.get('name')
for bash_script in root.findall('bash_script'):
	bash_script=bash_script.attrib.get('name')
for client_ip in root.findall('client_ip'):
	client_ip=client_ip.attrib.get('name')
for test_name in root.findall('test_name'):
	test_name=test_name.attrib.get('name')
for apn in root.findall('apn'):
        apn=apn.attrib.get('name')
for duration in root.findall('duration'):
        duration=duration.attrib.get('name')
duration_n=int(duration)
#print apn
################################################
def main(timest):
	global ssh
	global timestr
	timestr=timest
	global file_logs
	file_logs=open(BASE_DIR+"/"+test_name+"_"+timestr+"/"+test_name+"_UE_"+timestr+"."+"txt","a")
	test_env="APN "+apn+"\n"+"IMSI "+imsi+"\n"+"Test Duration "+duration+"\n"+"Traffic "+bash_script.split("/")[3]+"\n"
	file_logs.write(test_env)
#	print "opened client"
	try:
#		print "connecting to ", client_ip
		ssh.connect(client_ip, port=22, username=CLIENT_username, password=CLIENT_password, timeout=8)
		print "Connected to CLIENT ", client_ip
        test_log_1=open("Test_Result/test_log", "a")
		test_log_1.write("Connected to CLIENT "+ client_ip)
        test_log_1.close()
		execute_command()
	except (paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.NoValidConnectionsError, paramiko.SSHException, socket.timeout):
		print "Authentication failure on Client"
        test_log=open("Test_Result/test_log", "a")
		test_log.write("Authentication failure on Client \n")
        test_log.close()
#		file_logs = open(test_name+"_UE_"+timestr+"."+"txt","a")
#		file_logs = open(BASE_DIR+"/"+test_name+"_"+timestr+"/"+test_name+"_UE_"+timestr+"."+"txt","a")
		file_logs.write("SSH to Client Failed")
#		file_logs.close()
		time.sleep(5)
		sys.exit()
def execute_command():
	global ssh
	global retry_attach
	global file_logs
#	print "Connected to CLIENT ", client_ip
#	file_logs = open(BASE_DIR+"/"+test_name+"_"+timestr+"/"+test_name+"_UE_"+timestr+"."+"txt","a")
	stdin, stdout, stderr = ssh.exec_command("nmcli connection show --active | grep gsm > activeconnection; IFS=' ' read -ra my_array <<< $(tail -1 activeconnection); nmcli con down id ${my_array[0]}")
	time.sleep(5)
	connectionup="nmcli connection up "+apn
	stdin, stdout, stderr = ssh.exec_command(connectionup)
	if retry_attach==0:
		print "Attaching UE"
        test_log=open("Test_Result/test_log", "a")
        test_log.write("Attaching UE \n")
        test_log.close()
	time.sleep(30)
	checkipversion=apn.split('-')
	stdin, stdout, stderr = ssh.exec_command("nmcli d show ttyUSB3 | grep IP4.GATEWAY")
        output = stdout.readlines()
        IPV4_GW="".join(output)
	stdin, stdout, stderr = ssh.exec_command("nmcli d show ttyUSB3 | grep IP6.GATEWAY")
        output = stdout.readlines()
        IPV6_GW="".join(output)
	if (len(IPV4_GW.split())>0 and checkipversion[2]=="V4"):
		checkattach.write("IPV4 attach is good")
		checkattach.close()
		print "IPV4 attach is good"
        test_log=open("Test_Result/test_log", "a")
		test_log.write("IPV4 attach is good \n")
        test_log.close()
		file_logs.write("IPV4 attach is good \n")
		route1="ip route add 172.21.26.0/24 via " + IPV4_GW.split()[1]
                route2="ip route add 50.227.195.3 via " + IPV4_GW.split()[1]
		route3="ip route add 17.0.0.0/8 via " + IPV4_GW.split()[1]
		stdin, stdout, stderr = ssh.exec_command(route1)
		stdin, stdout, stderr = ssh.exec_command(route2)
		stdin, stdout, stderr = ssh.exec_command(route3)
		time.sleep(5)
		traffic="bash "+bash_script
		print "Running ", bash_script
        test_log=open("Test_Result/test_log", "a")
		test_log.write("Running " + bash_script+"\n")
        test_log.close()
		for i in range(0, duration_n-3, 5):
			if i==0:
                        	stdin, stdout, stderr = ssh.exec_command(traffic)
                        	output = stdout.readlines()
                        	traffic_result="".join(output)
				file_logs.write("Test Output below \n")
#				file_logs = open(BASE_DIR+"/"+test_name+"_"+timestr+"/"+test_name+"_UE_"+timestr+"."+"txt","a")
                		file_logs.write(traffic_result)
#                		file_logs.close()
				time.sleep(5)

			else:
                                stdin, stdout, stderr = ssh.exec_command(traffic)
				time.sleep(5)
	if (len(IPV6_GW.split())>0 and checkipversion[2]=="V6"):
		checkattach.write("IPV6 attach is good")
		checkattach.close()
		print "IPV6 attach is good"
        test_log=open("Test_Result/test_log", "a")
        test_log.write("IPV6 attach is good")
        test_log.close()
		file_logs.write("IPV6 attach is good \n")
		route4="ip -6 route add 2606:ae00:2001:2311::/64 via "+ IPV6_GW.split()[1] + " wwp0s20u6i7"
                stdin, stdout, stderr = ssh.exec_command(route4)
		time.sleep(5)
		traffic="bash "+bash_script
		print "Running ", bash_script
        test_log=open("Test_Result/test_log", "a")
        test_log.write("Running " + bash_script+"\n")
        test_log.close()

                for i in range(0, duration_n-3, 5):
                        if i==0:
                                stdin, stdout, stderr = ssh.exec_command(traffic)
                                output = stdout.readlines()
                                traffic_result="".join(output)
				file_logs.write("Test Output below \n")
#                               file_logs = open(BASE_DIR+"/"+test_name+"_"+timestr+"/"+test_name+"_UE_"+timestr+"."+"txt","a")
                                file_logs.write(traffic_result)
#                               file_logs.close()
                                time.sleep(5)

                        else:
                                stdin, stdout, stderr = ssh.exec_command(traffic)
                                time.sleep(5)
	if (len(IPV6_GW.split())>0 and len(IPV4_GW.split())>0 and checkipversion[2]=="V4V6"):
                checkattach.write("IPV4V6 attach is good")
		checkattach.close()
		print "IPV4V6 attach is good"
        test_log=open("Test_Result/test_log", "a")
        test_log.write("IPV4V6 attach is good \n")
        test_log.close()
		file_logs.write("IPV4V6 attach is good \n")
		route1="ip route add 172.21.26.0/24 via " + IPV4_GW.split()[1]
                route2="ip route add 50.227.195.3 via " + IPV4_GW.split()[1]
		route3="ip route add 17.0.0.0/8 via " + IPV4_GW.split()[1]
                route4="ip -6 route add 2606:ae00:2001:2311::/64 via "+ IPV6_GW.split()[1] + " wwp0s20u6i7"
		stdin, stdout, stderr = ssh.exec_command(route1)
                stdin, stdout, stderr = ssh.exec_command(route2)
                stdin, stdout, stderr = ssh.exec_command(route3)
		stdin, stdout, stderr = ssh.exec_command(route4)
		time.sleep(5)
                traffic="bash "+bash_script
		print "Running ", bash_script
        test_log=open("Test_Result/test_log", "a")
        test_log.write("Running " + bash_script + "\n")
        test_log.close()

                for i in range(0, duration_n-3, 5):
                        if i==0:
                                stdin, stdout, stderr = ssh.exec_command(traffic)
                                output = stdout.readlines()
                                traffic_result="".join(output)
				file_logs.write("Test Output below \n")
 #                               file_logs = open(BASE_DIR+"/"+test_name+"_"+timestr+"/"+test_name+"_UE_"+timestr+"."+"txt","a")
                                file_logs.write(traffic_result)
 #                               file_logs.close()
                                time.sleep(5)

                        else:
                                stdin, stdout, stderr = ssh.exec_command(traffic)
                                time.sleep(5)

	if len(IPV4_GW.split())==0 and len(IPV6_GW.split())==0:
		checkattach.write("UE ATTACH FAILED")
		checkattach.close()
		print "UE ATTACH FAILED"
        test_log=open("Test_Result/test_log", "a")
        test_log.write("UE ATTACH FAILED")
        test_log.close()

		if retry_attach<2:
			print "Retrying UE ATTACH"
            test_log=open("Test_Result/test_log", "a")
            test_log.write("Retrying UE ATTACH")
            test_log.close()
			if retry_attach==1:
				file_logs.write("UE ATTACH FAILED \n")
			retry_attach=retry_attach+1
			execute_command()
	time.sleep(5)
	sys.exit()
if __name__ == "__main__":
	main()

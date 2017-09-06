#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import paramiko

sshConnection = {}

def readConfig():
    host_file = open("ots_hosts")
    lines = file.readlines(host_file)
    result = []
    for line in lines:
        #print line
        if(len(line.strip()) > 0 and line[0] != "#"):
            result.append(line)
    return result

def connectServer(server_ip, port=22, name="root", pwd="SztyxM!2007@"):
    if(sshConnection.get(server_ip) != None):
        return sshConnection.get(server_ip)
    # 创建SSH对象
    ssh = paramiko.SSHClient()
    # 把要连接的机器添加到known_hosts文件中
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接服务器
    ssh.connect(hostname=server_ip, port=port, username=name, password=pwd)
    sshConnection[server_ip] = ssh
    return sshConnection[server_ip]

def executeCmd(ssh, cmd):
    stdin, stdout, stderr = ssh.exec_command(cmd)
    result = stdout.read()
    if not result:
        result = stderr.read()
    return result

def runOtsCmd(ots_cmd, silence="Y"):
    config = readConfig()
    for ots in config:
        param = ots.split(" ")
        ssh = connectServer(param[0].strip(), 22, "root", "SztyxM!2007@")
        cmd = ots_cmd + " -n " + param[1].strip()
        if(silence != "Y"):
            input_str = raw_input("execute " + cmd + " on " + param[0].strip() + ". (Y/N)\n")
            if(input_str != "Y"):
                continue
        result = executeCmd(ssh, cmd)
        print(param[0].strip() + " -- " +cmd + "\n" + result)

def otsInit():
    config = readConfig()
    for ots in config:
        param = ots.split(" ")
        ssh = connectServer(param[0].strip(), 22, "root", "SztyxM!2007@")
        cmd = "oinit -n " + param[1].strip()
        result = executeCmd(ssh, cmd)
        print(param[0].strip() + " -- " +cmd + "\n" + result)
        cmd = "cp -r /ots/config/%s/* /ots/runtime/%s/config/" % (param[1].strip(), param[1].strip())
        result = executeCmd(ssh, cmd)
        print(param[0].strip() + " -- " + cmd + "\n" + result)

def otsLoad(priority=1):
    config = readConfig()
    for ots in config:
        param = ots.split(" ")
        if(priority > 0 and param[2].strip() != priority):
            continue
        ssh = connectServer(param[0].strip(), 22, "root", "SztyxM!2007@")
        cmd = "oload -n " + param[1].strip()
        result = executeCmd(ssh, cmd)
        print(param[0].strip() + " oload -n " + param[1].strip() + "\n" + result)

def otsRun(priority=1):
    config = readConfig()
    for ots in config:
        param = ots.split(" ")
        if(param[2].strip() != priority):
            continue
        ssh = connectServer(param[0].strip(), 22, "root", "SztyxM!2007@")
        cmd = "orun -n " + param[1].strip()
        result = executeCmd(ssh, cmd)
        print(param[0].strip() + " orun -n " + param[1].strip() + "\n" + result)

def otsStatus():
    config = readConfig()
    for ots in config:
        param = ots.split(" ")
        ssh = connectServer(param[0].strip(), 22, "root", "SztyxM!2007@")
        cmd = "ostatus -n " + param[1].strip() + "|grep -v Custom|grep Status"
        result = executeCmd(ssh, cmd)
        print(param[0].strip() + " ostatus -n " + param[1].strip() + "\n" + result)

def otsStatusTrans():
    config = readConfig()
    for ots in config:
        param = ots.split(" ")
        ssh = connectServer(param[0].strip(), 22, "root", "SztyxM!2007@")
        cmd = "ostatus -n " + param[1].strip() + "|grep 'Custom Status' -A 1"
        result = executeCmd(ssh, cmd)
        print(param[0].strip() + " ostatus -n " + param[1].strip() + "\n" + result)
        print("*"*100)

def stopAll():
    runOtsCmd("ostop")

def cleanAll():
    config = readConfig()
    for ots in config:
        param = ots.split(" ")
        ssh = connectServer(param[0].strip(), 22, "root", "SztyxM!2007@")
        cmd = "rm -rf /ots/runtime/*"
        result = executeCmd(ssh, cmd)
        print(param[0].strip() + " rm -rf /ots/runtime/*\n" + result)
        result = executeCmd(ssh, "ps -ef|grep Node|awk '{print $2}'|xargs kill -9")
        print(result)

def df():
    config = readConfig()
    for ots in config:
        param = ots.split(" ")
        ssh = connectServer(param[0].strip(), 22, "root", "SztyxM!2007@")
        cmd = "df -h | grep sda2 -B 1"
        result = executeCmd(ssh, cmd)
        print(param[0].strip() + "  --  " + cmd + "\n" + result)

def run():
    '''
    ##1 挡板
    ##2 登录
    ##3 消息类接收
    ##4 消息类发送
    ##5 toCS类音频
    ##6 app发起音视频接收
    ##7 app发起音视频发送
    ##8 pc发起音视频接收
    ##9 pc发起音视频发送
    :return:
    '''
    stopAll()
    cleanAll()
    otsInit()
    otsLoad(-1)
    otsRun(1)
    time.sleep(10)
    otsRun(2)
    time.sleep(60)
    otsRun(3)
    time.sleep(2)
    otsRun(5)
    time.sleep(2)
    otsRun(6)
    time.sleep(2)
    otsRun(8)
    time.sleep(180)
    otsRun(4)
    time.sleep(2)
    otsRun(7)
    time.sleep(2)
    otsRun(9)


if __name__ == "__main__":
    while 1:
        input_str = raw_input("input cmd\n")
        if (input_str == "init"):
            otsInit()
        if (input_str == "loadall"):
            otsLoad(-1)
        elif (input_str[0:4] == "load"):
            otsLoad(input_str[4:5])
        if (input_str[0:3] == "run"):
            otsRun(input_str[3:4])
        if (input_str == "status"):
            otsStatus()
        if (input_str == "trans"):
            otsStatusTrans()
        if(input_str == "stopall"):
            stopAll()
        if (input_str == "cleanall"):
            cleanAll()
        if (input_str == "df"):
            df()


'''
##1 挡板
##2 登录
##3 消息类接收
##4 消息类发送
##5 toCS类音频
##6 app发起音视频接收
##7 app发起音视频发送
##8 pc发起音视频接收
##9 pc发起音视频发送
def main():
    ssh = connectServer("172.21.8.36", 22, "root", "SztyxM!2007@")
    result = executeCmd(ssh, "ostatus | grep -v Custom | grep Status")
    print(result)
    ssh.close()
    
salt -L '172.21.8.31' cmd.run 'ostop -n login'
salt -L '172.21.8.31' cmd.run 'ostatus | grep "Status("' 
salt -L '172.21.8.31' cmd.run 'oload -n login' 
salt -L '172.21.8.31' cmd.run 'orun -n login' 
salt -L '172.21.8.31' cmd.run 'oinit -n login'
'''
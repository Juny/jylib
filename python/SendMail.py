# -*- coding: UTF-8 -*-
'''
发送txt文本邮件
小五义：http://www.cnblogs.com/xiaowuyi
'''
import string
import sys
import socket
import smtplib  
from email.mime.text import MIMEText  
mailto_list=["13581701046@139.com","abc@a.com"] 
mail_host="smtp.feinno.com"  #设置服务器
mail_port="587"
mail_user="guojunying"    #用户名
mail_pass="******"   #口令 
mail_postfix="feinno.com"  #发件箱的后缀
  
def send_mail(to_list,sub,content):  
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='gb2312')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host,mail_port)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception, e:  
        print str(e)  
        return False  
    
def start(port):
    '''
    Constructor
    '''
    myHost = ''
    myPort = port
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    serverSocket.bind((myHost, myPort)) 
    serverSocket.listen(5) 
    
    print 'start complete.'

    try:
        while True:
            #connection == socket
            connection, address = serverSocket.accept() 
            print('Server connected by', address) 
            while True:
                data = connection.recv(512)
                if not data:
                    print('no data.')
                    break 
                print('recv=>' + data)
                msg = data.split('##')
                if send_mail(mailto_list,msg[0],msg[1]):
                    connection.send("发送成功")
                else:
                    connection.send("发送失败") 
                connection.send('ok.')
            connection.close()
    except Exception:
        print 'Server Stop.'
        connection.close()
        import traceback
        traceback.print_exc(file=sys.stdout)
        
if __name__ == '__main__': 
    start(10086)
    pass

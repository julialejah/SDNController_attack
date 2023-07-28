from scapy.layers.http import HTTPRequest
from faker import Faker
from scapy.all import *

import requests
import time
import random
import paramiko

def generate_ssh_traffic(tiempo_deseadofuncion, dirIP):
    tiempo_iniciofuncion = time.time()

    while time.time() - tiempo_iniciofuncion < tiempo_deseadofuncion:
        # Crear una solicitud SSH
        # Crea una sesión SSH utilizando la biblioteca Paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #coneccion al servidor 
        #-------------------------------------------------cambiar estos valores----------------------------------------------------------
        sshcx = RandIP()._fix()
        ssh.connect(sshIP, username='root', password='password123')
        #-------------------------------------------------------------------------------------------------------------------------------
        # tiempo de espera
        espera = random.randint(10, 30)
        time.sleep(espera) 
        # enviar comando a través de la conexión SSH
        comado= random.randint(1, 5)
        if comado == 1:
            stdin, stdout, stderr = ssh.exec_command('pwd')
        elif comado == 2:
            stdin, stdout, stderr = ssh.exec_command('cd')
        elif comado == 3:
            stdin, stdout, stderr = ssh.exec_command('mkdir')
        elif comado == 4:
            stdin, stdout, stderr = ssh.exec_command('cp')
        else:
            stdin, stdout, stderr = ssh.exec_command('ls')
        # cerrar la conexión SSH
        ssh.close()
        #filtro ssh

def getHttp(dst_ip):

    # Construir el paquete HTTP GET
    http_request1 = scapy.all.Ether()/scapy.all.IP(dst=dst_ip)/scapy.all.TCP(dport=80)/HTTPRequest(Method='GET', Path='/')

    # Enviar el paquete
    print("Get http")
    sendp(http_request1)

def postHttp(dst_ip):
    # Construir el paquete HTTP POSt
    http_request2 = scapy.all.Ether()/scapy.all.IP(dst=dst_ip)/scapy.all.TCP(dport=80)/HTTPRequest(Method='POST', Path='/', Host=dst_ip)
    print("Post http")
    # Enviar el paquete
    sendp(http_request2)

def putHttp(dst_ip):  
    # Construir el paquete HTTP POSt
    http_request3 = scapy.all.Ether()/scapy.all.IP(dst=dst_ip)/scapy.all.TCP(dport=80)/HTTPRequest(Method='PUT', Path='/', Host=dst_ip)
    print("Put http")
    # Enviar el paquete
    sendp(http_request3)

def deleteHttp(dst_ip):   
    # Construir el paquete HTTP POSt
    http_request4 = scapy.all.Ether()/scapy.all.IP(dst=dst_ip)/scapy.all.TCP(dport=80)/HTTPRequest(Method='DELETE', Path='/', Host=dst_ip)
    print("Delete http")
    # Enviar el paquete
    sendp(http_request4)

def postHttps(url):
    myobj = {'somekey': 'somevalue'}
    try:
        _ = requests.post(url, json = myobj)
    except requests.exceptions.RequestException as e:
        print("Error al realizar la solicitud HTTPS:", e)
    print("Post https")

def getHttps(url):
    try:
        _ = requests.get(url)
    except requests.exceptions.RequestException as e:
        print("Error al realizar la solicitud HTTPS:", e)
    print("Get https")


def generate_http_traffic(tiempo_deseadofuncion):
    # Tiempo de inicio
    tiempo_iniciofuncion = time.time()

    while time.time() - tiempo_iniciofuncion < tiempo_deseadofuncion: 
        # Crear una lista con las funciones y sus respectivas probabilidades
        funciones = [getHttp, postHttp, putHttp, deleteHttp]
        probabilidades = [0.6, 0.2, 0.1, 0.1]

        # Elegir una función con las probabilidades específicas
        funcion_elegida = random.choices(funciones, probabilidades)[0]
        #ip
        dst_ip = fake.ipv4_private()
        # Llamar a la función elegida
        funcion_elegida(dst_ip)
        # time.sleep(10)
        espera = random.randint(10, 30)
        time.sleep(espera) 
        #filtro http


def generate_https_traffic(tiempo_deseadofuncion):

    url = fake.url()
    tiempo_iniciofuncion = time.time()

    while time.time() - tiempo_iniciofuncion < tiempo_deseadofuncion: 
        # Crear una lista con las funciones y sus respectivas probabilidades
        funciones = [getHttps, postHttps]
        probabilidades = [0.8, 0.2]

        # Elegir una función con las probabilidades específicas
        funcion_elegida = random.choices(funciones, probabilidades)[0]

        # Llamar a la función elegida
        funcion_elegida(url)
        # time.sleep(10)
        espera = random.randint(10, 30)
        time.sleep(espera) 
        #filtro http
        #filtro tls.handshake.type == 1 and tcp.port == 443 and ssl.handshake.extensions_server_name == "www.example.com"
    

def generate_mail_traffic(tiempo_deseadofuncion):
    tiempo_iniciofuncion = time.time()

    while time.time() - tiempo_iniciofuncion < tiempo_deseadofuncion:
        # Crear una solicitud de correo electrónico
        dst_ip = fake.ipv4_private()
        mail_request = scapy.all.Ether()/scapy.all.IP(dst=dst_ip)/scapy.all.TCP(dport=25)/scapy.all.Raw(load="HELO example.com\r\nMAIL FROM: user@example.com\r\nRCPT TO: user2@example.com\r\nDATA\r\nSubject: prueba de correo electrónico\r\nEste es un mensaje de prueba.\r\n.\r\nQUIT\r\n")
        # tiempo de espera
        espera = random.randint(10, 30)
        time.sleep(espera) 
        #envia paquete
        scapy.all.sendp(mail_request)
        #filtro smtp

def generate_ftp_traffic(tiempo_deseadofuncion):
    tiempo_iniciofuncion = time.time()

    while time.time() - tiempo_iniciofuncion < tiempo_deseadofuncion:
        # Crear una solicitud FTP
        dst_ip = fake.ipv4_private()
        ftp_request = scapy.all.Ether()/scapy.all.IP(dst=dst_ip)/scapy.all.TCP(dport=21)/scapy.all.Raw(load="USER anonymous\r\nPASS anonymous\r\nLIST\r\nQUIT\r\n")
        scapy.all.sendp(ftp_request)
        # tiempo de espera
        espera = random.randint(10, 30)
        time.sleep(espera)
        #filtro ftp

def generate_traffic(sshIP):
    # Generar tráfico aleatorio
    traffic_type = random.randint(1, 5)
    # Tiempo que dura el trafico
    traffic_time = random.randint(10, 200) #entre 10 segundos y 3,333 minutos
    print("Tiempo de trafico:", traffic_time)
    if traffic_type == 1:
        print("HTTP")
        generate_http_traffic(traffic_time)            
    elif traffic_type == 2:
        print("HTTPS")
        generate_https_traffic(traffic_time)
            
    elif traffic_type == 3:
        print("SSH")
        generate_ssh_traffic(traffic_time,sshIP)
            
    elif traffic_type == 4:
        print("SMTP")
        generate_mail_traffic(traffic_time)
    elif traffic_type == 5:
        print("FTP")
        generate_ftp_traffic(traffic_time)

        
fake = Faker()

# Tiempo de ejecución deseado en segundos
tiempo_deseado = 5000
# Tiempo de inicio
tiempo_inicio = time.time()
sshIP = sys.argv[1]
if __name__ == "__main__":
    traffic_interval = random.randint(0, 5)  # tiempo entre cada generación de tráfico, en segundos
    while time.time() - tiempo_inicio < tiempo_deseado:       
        
        generate_traffic(sshIP)
        print("Termino un trafico")
        time.sleep(traffic_interval) 
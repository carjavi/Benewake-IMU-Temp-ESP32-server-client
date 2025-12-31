# python3
# sudo apt-get install python3-opencv -y // capture imagen
# pip3 install imutils //  comunication socket
# pip3 install sockets // comunication socket
# pip3 install serial-tool // serail comunication 
# pip3 install psutil // chequeo temperatura
# el host_ip = '192.168.1.100' cambia dependiendo del dispositivo, tanto en el servidor como cliente


# This is server code to send video frames over UDP
import cv2, imutils, socket
import numpy as np
import base64

# Sensor TF03********************************************************
import serial.tools.list_ports
import time
import numpy as np
ser = serial.Serial()
ser.port = '/dev/ttyUSB1'
ser.baudrate = 115200

# CPU Temperature
import psutil

# IMU
from rsl_comm_py import UM7Serial
um7_serial = UM7Serial(port_name='/dev/ttyUSB2')

# Salida del bucle, cierre del socket puerto Serial ******************
try:
    if ser.is_open == False:
        try:
            ser.open()
        except:
            print('Open COM failed')
except KeyboardInterrupt:
    if ser != None:
        ser.close()
        server_socket.close()
    print('\nInterrupted, pressed ctrl-c button')
    
# measure_temp
def obtener_temperatura_procesador():
    # Obtener la temperatura del procesador en grados Celsius
    temperatura = psutil.sensors_temperatures().get('cpu_thermal')
    if temperatura:
        return temperatura[0].current
    else:
        return None

def calcular_promedio(datos):
    if not datos:
        return None
    return sum(datos) / len(datos)


# Se crea un socket UDP (socket.SOCK_DGRAM) y se configura su tamaño de búfer para manejar grandes cantidades de datos.
BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

# Asignación del host y el puerto
host_name = socket.gethostname()
host_ip = '192.168.2.2' # wifi: 192.168.1.100 / socket.gethostbyname(host_name)
print('CMS Server')#print(host_ip)
port = 5000 # 
socket_address = (host_ip,port)
server_socket.bind(socket_address)
print('Listening at:',socket_address)

# Inicialización de la captura de video
vid = cv2.VideoCapture(0) #  replace 'rocket.mp4' with 0 for webcam

fps,st,frames_to_count,cnt = (0,0,20,0)

# Bucle principal para recibir el mensaje de conexión y transmitir fotogramas de vídeo
datos_temp = [] # temperature
while True:
	
	# El servidor espera recibir un mensaje de conexión.
	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
	print('GOT connection from ',client_addr)
	WIDTH=400	

	# Bucle interno para transmitir fotogramas de video
	while(vid.isOpened()):
		_,frame = vid.read()
		frame = imutils.resize(frame,width=WIDTH)
		encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])
		
		# Codificar fotograma
		message = base64.b64encode(buffer)
		
		# Obtener datos del Sensor de distancia TFmini ***********************************
		count = ser.in_waiting
		if count > 8:
			recv = ser.read(9)
			ser.reset_input_buffer()
			if recv[0] == 0x59 and recv[1] == 0x59:
				distance = np.int16(recv[2] + np.int16(recv[3]<<8))
				tfmini = distance
				#print('distance = %5d' % (distance))
				ser.reset_input_buffer()

		else:
			time.sleep(0.050) # 50ms
   
		# Temperature 
		temperatura = obtener_temperatura_procesador()

		# Recibe el primer paquete de ángulos de Euler del sensor UM7
		packet = next(um7_serial.recv_euler_broadcast())
		# Accede a los atributos del paquete para obtener los valores de pitch, roll y yaw
		pitch = packet.pitch
		roll = packet.roll
		yaw = packet.yaw
  
  
		# Imprime los valores de pitch, roll y yaw
		print(f"Tfmini: {distance}, Pitch: {pitch:.2f}, Roll: {roll:.2f}, Yaw: {yaw:.2f}, CPU Temp: {temperatura:.2f}°C     ", end = "\r")
		
			
		# Enviar fotograma y Dato *********************************************************
		server_socket.sendto(message + b'|' + str(tfmini).encode(),client_addr)
		
		# ***** Anotar FPS y el Dato en el fotograma **************
		# frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)
		# frame = cv2.putText(frame, 'Elapsed Time: ' + str(elapsed_time), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		# hace que se visualice el video en el server
		# cv2.imshow('TRANSMITTING VIDEO',frame)  #si no hay GUI debe estar desabilitada
		key = cv2.waitKey(1) & 0xFF
        
		
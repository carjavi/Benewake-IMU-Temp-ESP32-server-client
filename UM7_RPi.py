from rsl_comm_py import UM7Serial
um7_serial = UM7Serial(port_name='/dev/ttyUSB2')
for packet in um7_serial.recv_euler_broadcast():
    # Accede a los atributos del paquete para obtener los valores de pitch, roll y yaw
    pitch = packet.pitch
    roll = packet.roll
    yaw = packet.yaw
    
     # Imprime los valores de pitch, roll y yaw por separado
    print(f"Pitch: {pitch}, Roll: {roll}, Yaw: {yaw}")

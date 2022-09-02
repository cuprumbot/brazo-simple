import numpy as np
import math
import time
import serial

# Conectar con Arduino
# Cambiar COMx segun puerto de la maquina
arduino = serial.Serial('COM7', 9600, timeout=.1)
print("connected to arduino")
# Sleep mientras el brazo llega a posiciones iniciales
time.sleep(1)

########## CINEMATICA INVERSA ##########
########### HECHA POR FALFO ############
########### NO CAMBIAR NADA ############
def horizontal(t, r, z, a5):
	return np.array([t, r-a5, z])

def vertical(t, r, z, a5):
	return np.array([t, r, z+a5])

def cartesianToCylindrical(x, y, z, a2):
	r = np.sqrt(x**2+y**2)
	t = math.atan(y/x)
	return np.array([t, r-a2, z])

def horizontalEEf(t1, t2):
	return  -t1 + t2

def verticalEEF(t1, t2):
	return -t1+t2-np.pi/2

def max_range(z,a3,a4):
	return math.sqrt(2*a3*a4-z**2+a3**2 + a4**2)

def twoLinkPlannarArm(r, z, a3, a4, ver):
	if (z >= 0):
		t2 = math.acos((r**2 + z**2 - a3**2 - a4**2)/(2*a3*a4))
		t1 = math.atan(z/r) + math.atan((a4*math.sin(t2))/(a3+a4*math.cos(t2)))
	else:
		t2 = math.acos((r**2 + z**2 - a3**2 - a4**2)/(2*a3*a4))
		t1 = math.atan(z/r) + math.atan((a4*math.sin(t2))/(a3+a4*math.cos(t2)))

	t1 = t1
	return np.array([t1,t2])
####### FIN DECINEMATICA INVERSA #######
########### HECHA POR FALFO ############
########### NO CAMBIAR NADA ############

# Mover un solo servo
# Normalmente no se llama de forma individual
# servo y angulo se reciben como strings para facilitar transmision
def moveOne (servo, angulo, wait):
	try:
		arduino.write('0'.encode())
		time.sleep(0.2)
		arduino.write(servo.encode())
		time.sleep(0.2)
		arduino.write('1'.encode())
		time.sleep(0.2)
		arduino.write(angulo.encode())

		if servo == '4' and wait < 4:
			wait = 4

		time.sleep(wait)
	except Exception as e:
		print("fallo movimiento, servo ", servo, " a posicion ", angulo)
		print(e)

# Abre la garra
def open (wait):
	moveOne('6', '70', wait)
	print("open finalizado!")

# Cierra la garra
def close (wait):
	moveOne('6', '10', wait)
	print("close finalizado!")

# Regresa el brazo a posicion inicial
def resetArm (wait):
	print("iniciando reset...")
	moveOne('1', '90', wait)
	moveOne('3', '0', wait)
	moveOne('2', '0', wait)
	moveOne('4', '0', wait)
	print("reset finalizado!")

# Hace "medio" reset
# Levanta el brazo y regresa rotacion al inicio
# No estira los codos
def halfReset (wait):
	print("iniciando half reset")
	moveOne('1', '90', wait)
	moveOne('3', '0', wait)
	print("half reset finalizado!")

# Reset y un poco extra en el codo
# ACTUALMENTE NO SE DEBE USAR
def moveBack (wait):
	print("iniciando back...")
	moveOne('1', '115', wait)
	moveOne('3', '0', wait)
	moveOne('2', '0', wait)
	moveOne('4', '0', wait)
	print("back finalizado!")

# Abre y cierra garra
def claw (wait):
	print("iniciando claw...")
	open(wait)
	close(wait)
	print("claw finalizado!")


########## CINEMATICA INVERSA ##########
########### HECHA POR FALFO ############
########### NO CAMBIAR NADA ############
#### excepto por los arduino.write() ###
# ver: indica posicion del codo cercano a la garra
# 	true: vertical, cerca
# 	false: horizontal, lejos
#	SE DEBE ENVIAR VALOR CORRECTO, O CINEMATICA FALLARA
# pinza: indica que parte de la pinza usar
# 	true: punta de la pinza
# 	false: parte gruesa de la pinza
#	ACTUALMENTE SIEMPRE SE USA TRUE
def move (coordx, coordy, coordz, ver, wait, pinza):
	coordenadas = np.array([coordx, coordy, coordz])
	print(f'Goal: {coordenadas}')
	a1 = 150	#altura del primer eje
	a2 = 21.11	#distancia horizontal del centro al primer eje
	a3 = 145	#largo del primer link
	a4 = 133.86	#largo del segundo link
	a5 = 130	#largo del 3er joint al end effector
	if (pinza):
		a5 = 175

	if(coordenadas[0] <0):
		a2 = -a2

	coordenadas[2] = coordenadas[2] - a1
	print(f'Coordenadas a partir del joint 1: {coordenadas}')
	cylindrical = cartesianToCylindrical(coordenadas[0], coordenadas[1], coordenadas[2], a2)
	cylindricalMod = None
	if (ver):
		cylindricalMod = vertical(cylindrical[0], cylindrical[1], cylindrical[2], a5)
	else:
		cylindricalMod = horizontal(cylindrical[0], cylindrical[1], cylindrical[2], a5)
	print(f'Coordenadas cilindricas {cylindrical}')
	print(f'Coordenadas cilindricas modificadas {cylindricalMod}')
	if ver:
		print("Agarre vertical")
	else:
		print("Agarre horizontal")
	result1 = twoLinkPlannarArm(cylindricalMod[1], cylindricalMod[2], a3, a4, ver)

	t3 = 0
	if (ver):
		t3 = verticalEEF(result1[0], result1[1])
	else:
		t3 = horizontalEEf(result1[0], result1[1])
	print("Resultado:" )
	angles = np.array([cylindrical[0], result1[0], -result1[1], t3])
	print(np.degrees(angles))
	if(coordenadas[0]<0):
		angles[1] = math.pi - angles[1]
		angles[2] = -angles[2]
		angles[3] = -angles[3]

	x = [0, a2, a2+ a3*math.cos(result1[0]), a2+ a3*math.cos(result1[0]) + a4*math.cos(-result1[1]+result1[0]), a2+ a3*math.cos(result1[0]) + a4*math.cos(-result1[1]+result1[0]) + a5*math.cos(-result1[1]+result1[0]+t3)]
	y = [a1,a1, a1+ a3*math.sin(result1[0]), a1+ a3*math.sin(result1[0]) + a4*math.sin(-result1[1]+result1[0]), a1+ a3*math.sin(result1[0]) + a4*math.sin(-result1[1]+result1[0]) + a5*math.sin(-result1[1]+result1[0]+t3)]

	### Escrito por Luis ###
	# Modificar solo si se realizan cambios a placa
	try:
		arduino.write('0'.encode())
		time.sleep(0.2)
		arduino.write('4'.encode())
		time.sleep(0.2)
		arduino.write('1'.encode())
		time.sleep(0.2)
		arduino.write(str(int(np.degrees(angles[3]))).encode())
		print("codo (azul) - moviendose...")
		time.sleep(wait)

		arduino.write('0'.encode())
		time.sleep(0.2)
		arduino.write('2'.encode())
		time.sleep(0.2)
		arduino.write('1'.encode())
		time.sleep(0.2)
		arduino.write(str(int(np.degrees(angles[2]))).encode())
		print("codo (gris) - moviendose...")
		time.sleep(wait)

		arduino.write('0'.encode())
		time.sleep(0.2)
		arduino.write('3'.encode())
		time.sleep(0.2)
		arduino.write('1'.encode())
		time.sleep(0.2)
		arduino.write(str(int(np.degrees(angles[0]))).encode())
		print("rotacion (base) - moviendose...")
		time.sleep(5)

		arduino.write('0'.encode())
		time.sleep(0.2)
		arduino.write('1'.encode())
		time.sleep(0.2)
		arduino.write('1'.encode())
		time.sleep(0.2)
		arduino.write(str(int(np.degrees(angles[1]))).encode())
		print("elevacion (negro) - moviendose...")
		time.sleep(wait)

	except:
		print("Error escribiendo a Arduino")
####### FIN DE CINEMATICA INVERSA ######
########### HECHA POR FALFO ############
########### NO CAMBIAR NADA ############
#### excepto por los arduino.write() ###
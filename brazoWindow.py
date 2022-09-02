import sys
import glob 				# no se usa?
import cinematica as ci
import time
import cv2
import numpy as np

from math import sqrt

# Tiempos de espera
normalTime = 2		# 20 * 90 = 1800
bigTime = 4			# 20 * 180 = 3600

# Globales
# Se llenan tras recibir un click en ventana
front = 0
sides = 0
comando = []



# MOVIMIENTO DEL BRAZO
# MODIFICAR CON EXTREMO CUIDADO

'''
PROTOCOLO
Debe implementarse en cualquier otro programa que se use para manejar el brazo

Comandos especiales:
open / close / reset / half
Ejecutan la funcion correspondiente (ver cinematica.py)

Coordenadas:
x y z
	x - Distancia hacia el frente del brazo, positiva
	y - Distancia hacia los lados del brazo, negativa = izquierda, positiva = derecha
	z - Altura a donde llegara la garra, normalmente siempre se usa 50
'''
def moveArm():
	print(comando)

	comm = comando[0]

	# Si se recibio un comando especial, no se tendran coordenadas
	if (comm == 'open' or comm == 'close' or comm == 'reset' or comm == 'half'):
		x = 0
		y = 0
		z = 0
		print(">>> comando especial")
	# Obtener coordenadas
	else:
		x = int(comando[0])
		y = int(comando[1])
		z = int(comando[2])
		print(">>> coordenadas [x:", x, "y:", y, "z:", z, "]\n")

	# Calcular radio
	radius = sqrt(x*x + y*y)

	# Si es un comando especial, ejecutarlo
	if (comm == 'open'):
		ci.open(normalTime)
		return
	elif (comm == 'close'):
		ci.close(normalTime)
		return
	elif (comm == 'reset'):
		ci.resetArm(normalTime)
		return
	elif (comm == 'half'):
		ci.halfReset(normalTime)
		return
	else:
		print('>>> revisando coordenadas')

	# Si son coordenadas, revisar en que area se encuentra
	print('>>> revisando radio')
	if (radius < 210):
		# Esta demasiado cerca del brazo
		# TO DO: Modificar x, y, z para que se alejen un poco, siempre en la misma direccion
		print("-----\n-----\n-----\nDistancia demasiado cercana\n-----\n-----\n-----")
		return
	elif (radius > 440):
		# Esta demasiado lejos del brazo
		# TO DO: Modificar x, y, z para que se acerquen un poco, siempre en la misma direccion
		print("-----\n-----\n-----\nDistancia demasiado lejana\n-----\n-----\n-----")
		return
	elif (radius > 280 and radius < 360):
		# Esta en la zona muerta (ver ventana, la zona entre las dos azules)
		# TO DO: Modificar x, y, z para que se aleje o acerque un poco, siempre en la misma direccion
		# la modificacion tiene que llevarlos al lugar mas cercano posible
		print("-----\n-----\n-----\nNo hay angulos validos en esta zona\n-----\n-----\n-----")
		return

	# Tiempo por movimiento individual: 2 segundos
	# Tiempo por movimiento de todo el brazo: 8 segundos
	t = normalTime

	# Solo se usaba cuando el brazo iba hacia atras
	#if (x < 0):
	#	t = bigTime

	print('>>> moviendo')
	if (radius >= 210 and radius <= 280):
		print("---------- Calculando angulos y moviendo ----------")
		# Se envia True como cuarto argumento para posicion de la garra
		ci.move(x, y, z, True, t, True)
	elif (radius >= 360 and radius <= 440):
		print("---------- Calculando angulos y moviendo ----------")
		# Se envia False como cuarto argumento para posicion de la garra
		ci.move(x, y, z, False, t, True)
# FIN MOVIMIENTO DEL BRAZO



# WINDOW
# Para mas detalles y/o modificar ver window.py
img = np.zeros(shape=(450, 1100, 3), dtype=np.uint8)

cv2.circle(img, (450,450), 450, (255,0,0), -1)
cv2.circle(img, (450,450), 360, (0,0,0), -1)
cv2.circle(img, (450,450), 280, (255,0,0), -1)
cv2.circle(img, (450,450), 210, (0,0,0), -1)

cv2.rectangle(img, (900,0), (1100, 112), (0,0,200), -1)
cv2.rectangle(img, (900,113), (1100, 225), (0,50,150), -1)
cv2.rectangle(img, (900,226), (1100, 338), (0,150,100), -1)
cv2.rectangle(img, (900,339), (1100, 450), (0,200,0), -1)

cv2.putText(img, 'RESET', (900, 74), cv2.FONT_HERSHEY_SIMPLEX, 2, (250,250,250), 5, cv2.LINE_AA)
cv2.putText(img, 'HALF', (924, 186), cv2.FONT_HERSHEY_SIMPLEX, 2, (250,250,250), 5, cv2.LINE_AA)
cv2.putText(img, 'OPEN', (916, 298), cv2.FONT_HERSHEY_SIMPLEX, 2, (250,250,250), 5, cv2.LINE_AA)
cv2.putText(img, 'CLOSE', (900, 410), cv2.FONT_HERSHEY_SIMPLEX, 2, (250,250,250), 5, cv2.LINE_AA)

def clicky(event, x, y, flags, param):
	global front, sides, comando

	if event == cv2.EVENT_LBUTTONDOWN:
		if (x < 900):
			front = 450 - y
			sides = x - 450
			print("front: ", front)
			print("sides: ", sides)
			print()

			comando = [front, sides, 50]			
		else:
			if (y < 112):
				print("reset")
				comando = ["reset"]
			elif (y < 225):
				print("half")
				comando = ["half"]
			elif (y < 338):
				print("open")
				comando = ["open"]
			else:
				print("close")
				comando = ["close"]

		moveArm()
# FIN WINDOW


# Crear ventana
cv2.namedWindow("brazo")
cv2.setMouseCallback("brazo", clicky)
cv2.imshow("brazo", img)

# Iniciar garra
ci.close(normalTime)
ci.open(normalTime)

# Los servos de la garra a veces se traban al inicio
# Es posible que se necesite algun movimiento extra para destrabarlos
#ci.close(normalTime)
#ci.open(normalTime)

# La ventana espera por siempre, recibiendo clicks
# Cualquier tecla que se presione cierra la ventana y termina el programa
cv2.waitKey(0)

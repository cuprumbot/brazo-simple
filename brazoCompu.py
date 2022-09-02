import sys
import glob					# no se usa?
import cinematica as ci
import time

from math import sqrt

# Tiempos de espera
normalTime = 2		# 20 * 90 = 1800
bigTime = 4			# 20 * 180 = 3600

# MOVIMIENTO DEL BRAZO
# MODIFICAR CON EXTREMO CUIDADO
# COMPARAR CON moveArm() EN brazoWindow.py

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
while True:
	data = input("Esperando comando: ")

	# Valores iniciales colocados por seguridad
	# en caso que el usario escriba algo incorrecto
	# en la terminal
	x = -1
	y = -1
	z = -1

	sp = data.split()

	comm = sp[0]

	# Si se recibio un comando especial, no se tendran coordenadas
	if (comm == 'open' or comm == 'close' or comm == 'reset' or comm == 'half'):
		x = 0
		y = 0
		z = 0
		print(">>> comando especial")
	# Obtener coordenadas
	else:
		x = int(sp[0])
		y = int(sp[1])
		z = int(sp[2])
		print(">>> coordenadas [x:", x, "y:", y, "z:", z, "]\n")

	# Calcular radio
	radius = sqrt(x*x + y*y)

	# Si es un comando especial, ejecutarlo
	if (comm == 'open'):
		ci.open(normalTime)
		continue
	elif (comm == 'close'):
		ci.close(normalTime)
		continue
	elif (comm == 'reset'):
		ci.resetArm(normalTime)
		continue
	elif (comm == 'half'):
		ci.halfReset(normalTime)
		continue
	else:
		print('>>> revisando coordenadas')

	# Si son coordenadas, revisar en que area se encuentra
	print('>>> revisando radio')
	
	# Para mas detalle, ver comentarios en brazoWindow.py
	# Se usa continue en lugar de return
	if (radius < 210):
		print("-----\n-----\n-----\nDistancia demasiado cercana\n-----\n-----\n-----")
		continue
	elif (radius > 440):
		print("-----\n-----\n-----\nDistancia demasiado lejana\n-----\n-----\n-----")
		continue
	elif (radius > 280 and radius < 360):
		print("-----\n-----\n-----\nNo hay angulos validos en esta zona\n-----\n-----\n-----")
		continue

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
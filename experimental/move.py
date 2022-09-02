import cinematica as ci

from math import sqrt

# Tiempos de espera
normalTime = 2		# 20 * 90 = 1800
bigTime = 4			# 20 * 180 = 3600

def moveArm(comando):
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
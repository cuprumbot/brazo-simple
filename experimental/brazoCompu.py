import sys
import glob					# no se usa?
import cinematica as ci
import time

from math import sqrt

# Tiempos de espera
normalTime = 2		# 20 * 90 = 1800
bigTime = 4			# 20 * 180 = 3600

# Iniciar garra
ci.close(normalTime)
ci.open(normalTime)

# Los servos de la garra a veces se traban al inicio
# Es posible que se necesite algun movimiento extra para destrabarlos
#ci.close(normalTime)
#ci.open(normalTime)

while True:
	data = input("Esperando comando: ")

	comando = data.split()

	moveArm(comando)
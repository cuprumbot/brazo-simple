import sys
import glob 				# no se usa?
import cinematica as ci
import time
import cv2
import numpy as np
import move as mv

from math import sqrt

# Tiempos de espera
normalTime = 2		# 20 * 90 = 1800
bigTime = 4			# 20 * 180 = 3600

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

		mv.moveArm(comando)
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

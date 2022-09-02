# Demo de ventana
# Probar cambios a interfaz grafica aqui

import cv2
import numpy as np

# Matriz vacia
# El brazo puede llegar 45 cm hacia adelante (450 mm)
# y 45 cm hacia cada lado (450 + 450 = 900 mm en total)
# 200 pixeles hasta la derecha para colocar botones
img = np.zeros(shape=(450, 1100, 3), dtype=np.uint8)

# Dibujar zonas vivas en azul
# El brazo no es capaz de moverse hacia zonas muertas
cv2.circle(img, (450,450), 450, (255,0,0), -1)
cv2.circle(img, (450,450), 360, (0,0,0), -1)
cv2.circle(img, (450,450), 280, (255,0,0), -1)
cv2.circle(img, (450,450), 210, (0,0,0), -1)

# Dibujar botones
cv2.rectangle(img, (900,0), (1100, 112), (0,0,200), -1)
cv2.rectangle(img, (900,113), (1100, 225), (0,50,150), -1)
cv2.rectangle(img, (900,226), (1100, 338), (0,150,100), -1)
cv2.rectangle(img, (900,339), (1100, 450), (0,200,0), -1)

# Colocar texto a botones
cv2.putText(img, 'RESET', (900, 74), cv2.FONT_HERSHEY_SIMPLEX, 2, (250,250,250), 5, cv2.LINE_AA)
cv2.putText(img, 'HALF', (924, 186), cv2.FONT_HERSHEY_SIMPLEX, 2, (250,250,250), 5, cv2.LINE_AA)
cv2.putText(img, 'OPEN', (916, 298), cv2.FONT_HERSHEY_SIMPLEX, 2, (250,250,250), 5, cv2.LINE_AA)
cv2.putText(img, 'CLOSE', (900, 410), cv2.FONT_HERSHEY_SIMPLEX, 2, (250,250,250), 5, cv2.LINE_AA)

# Capturar clicks
def clicky(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		if (x < 900):
			# Transformar posicion del click en posicion usable por cinematic.py
			print("front: ", 450-y)
			print("sides: ", x-450)
			print()
		else:
			# Click en botones
			if (y < 112):
				print("reset")
			elif (y < 225):
				print("half")
			elif (y < 338):
				print("open")
			else:
				print("close")

cv2.namedWindow("brazo")
cv2.setMouseCallback("brazo", clicky)
cv2.imshow("brazo", img)

cv2.waitKey(0)
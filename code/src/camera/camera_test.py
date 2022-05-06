import picamera

# Fem el setup de la camera, es tancara quan ja no la necessitem
print("A punt de prendre una foto.")
with picamera.PiCamera() as camera:
	camera.resolution = (1280, 720)
	camera.capture("/home/pi/Luci/camera_output/novaImatge.jpg")
print("Foto realitzada.")

import serial
import pygame
import time

### 1: Identificar el comandament

pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
print ('Detected controller : %s' % j.get_name() )


### 2: Obrim canal serial amb l'arduino

serial_is_on = True                            # Deixar en False si l'arduino no està connectada
serial_port = '/dev/ttyACM0'			        # nom del port on està connectada l'arduino. Es veu mitjançant la comanda ls /dev/tty*
baud_rate = 9600					              # ni idea què és, però ha de ser el mateix número que el que hi ha al setup de l'arduino

if serial_is_on == True:                          # objecte que representa la connexió serial
    ser = serial.Serial(serial_port, baud_rate, timeout=1)	


### 3: seleccionar els Axes a tenir en compte. Es pot veure el seu número executant el script i moure botos. La consola fa print de l'identificador del botó en qüestió


# 1 -> L vertical
# 2 -> L2
# 3 -> R horitzontal
# 4 -> R vertical
# 0 -> L horitzontal
# 5 -> R2   
axes_to_check = [0,5,2]                         # botons a llegir del comandament
check_frequency = 2                             # vegades que llegim per segon
breakout_button = 3                             # Botó que apaga el programa. Actualment és el Quadrat

#############################
### 4: Llegim input del comandament

while True:

    pygame.event.pump()			                  # És un trigger per cada cop que hi ha un nou event
    recent_values = []		                      # Es guarden els valors per després enviar-los per serial
    throttle = 0                                  # valor per l'accelerador, entre 0 i 255
    turn = 0                                      # valor per girar, -1 a l'esquerra, 0 recte, 1 a l'esquerra
    endavant = 1                                  # multiplica el valor final dels motors
    
    for current_axis in axes_to_check:	          # Anem fent loop pels Axes per comprovar-los
        latest_value = j.get_axis(current_axis)	  # Guardem l'últim valor
                                                  # evitem fer print quan el Axis està en posició de repós
        #if latest_value != 0.00: print ('Axis %i reads %.3f' % (current_axis, latest_value))

                                                  # Sincerament ni idea dels càlculs, però els passem a un valor entre 0 i 200
        multiplicador = 100
        #value_mod = 0
        if current_axis == 2:
            endavant = -1                         # si s'apreta L2, el resultat final serà negatiu i anirà cap endarrere
        if current_axis == 5 or current_axis == 2:# L2 o R2
            multiplicador = 127;
            throttle = int(round(latest_value*multiplicador,2)+multiplicador) * endavant
            if throttle != 0:                     # si ja ha passat per un accelerador activat, o cal veure l'altre durant aquesta iteració.
                break; 
        else:                                     # L horitzontal
            turn = latest_value
        #value_mod = int(round(latest_value*multiplicador,2))
        #value_mod = str(value_mod)                # Convertim a string
        #recent_values.append(value_mod)           # l'afegim a la llista de valors a enviar
    
    left = throttle
    right = throttle
    if turn > 0:                                  # càlcul de les veolictats de cada motor.
        right = int(right * (1-turn))
    if turn < 0:
        left = int(left * (1-abs(turn)))
    #print(turn, left, right)
        
        
    recent_values.append(str(left))                 # afegirm les velocitats a la llista
    recent_values.append(str(right))
    
    
    serial_output =','.join(recent_values) + ';'  # convertim llista a string
    print(serial_output)                       # mostra el string que s'envia per serial

    if serial_is_on == True:
        ser.write(serial_output.encode())                  # S'envia per serial

    time.sleep(1/check_frequency)                 # posem un delay

    if j.get_button(breakout_button) == 1:        # comprovem si s'ha clicat el botó d'aturada
        break


import pyfirmata as py

#check from device manager
port= 'COM20'
out=""

board=py.Arduino(port)

SpeedR = board.get_pin('d:5:o')
Rpin1 = board.get_pin('d:12:o')# pintype,pinnum, pinmode//purple 
Rpin2 = board.get_pin('d:11:o')
Lpin3 = board.get_pin('d:13:o')
Lpin4 = board.get_pin('d:9:o')
SpeedL = board.get_pin('d:4:o')


def RCCAR(total):
    if total==0:
        SpeedR.write(0)
        SpeedL.write(0)
        Rpin1.write(0)
        Rpin2.write(0)
        Lpin3.write(0)
        Lpin4.write(0)
        print("BRAKE")
        return "Brake"
        
        

    if total==2:
        SpeedR.write(0)
        SpeedL.write(1)
        Rpin1.write(0)
        Rpin2.write(0)
        Lpin3.write(1)
        Lpin4.write(0)
        print("RIGHT")
        return "Right"

    if total==3:
        SpeedR.write(1)
        SpeedL.write(0)
        Rpin1.write(1)
        Rpin2.write(0)
        Lpin3.write(0)
        Lpin4.write(0)
        print("LEFT")
        return "Left"

    if total==5:
        SpeedR.write(1)
        SpeedL.write(1)
        Rpin1.write(1)
        Rpin2.write(0)
        Lpin3.write(1)
        Lpin4.write(0)
        print("FORWARD")
        return "Up"
        
    if total==4:
        SpeedR.write(1)
        SpeedL.write(1)
        Rpin1.write(0)
        Rpin2.write(1)
        Lpin3.write(0)
        Lpin4.write(1)
        print("BACKWARD")
        return "Down"
print('Successfuly Uploaded')






# from pyfirmata import *
# import time

# board = Arduino("/dev/tty.usbserial-110")

# print(board.get_firmata_version())

# loopTimes = input('How many times would you like the LED to blink: ')
# print("Blinking " + loopTimes + " times.")

# for x in range(int(loopTimes)):
#     board.digital[13].write(1)
#     time.sleep(0.2)
#     board.digital[13].write(0)
#     time.sleep(0.2)
     
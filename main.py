def right():
    pins.analog_write_pin(AnalogPin.P14, turnspeed)
    pins.analog_write_pin(AnalogPin.P13, 0)
    pins.analog_write_pin(AnalogPin.P16, 0)
    pins.analog_write_pin(AnalogPin.P15, turnspeed)
def left():
    pins.analog_write_pin(AnalogPin.P14, 0)
    pins.analog_write_pin(AnalogPin.P13, turnspeed)
    pins.analog_write_pin(AnalogPin.P16, turnspeed)
    pins.analog_write_pin(AnalogPin.P15, 0)
def stopdrive():
    pins.analog_write_pin(AnalogPin.P14, 0)
    pins.analog_write_pin(AnalogPin.P13, 0)
    pins.analog_write_pin(AnalogPin.P16, 0)
    pins.analog_write_pin(AnalogPin.P15, 0)

def on_button_pressed_a():
    global whiteP1, whiteP2
    whiteP1 = rechtsP1
    whiteP2 = linksP2
input.on_button_pressed(Button.A, on_button_pressed_a)

def backward():
    pins.analog_write_pin(AnalogPin.P14, 0)
    pins.analog_write_pin(AnalogPin.P13, speed)
    pins.analog_write_pin(AnalogPin.P16, 0)
    pins.analog_write_pin(AnalogPin.P15, speed)

def on_button_pressed_b():
    global stopDisp, blackP1, blackP2, wp1cal, wp2cal, bp1cal, bp2cal
    stopDisp = True
    blackP1 = rechtsP1
    blackP2 = linksP2
    wp1cal = (1 * blackP1 + 8 * whiteP1) / 9
    wp2cal = (1 * blackP2 + 8 * whiteP2) / 9
    bp1cal = (3 * whiteP1 + 1 * blackP1) / 4
    bp2cal = (3 * whiteP2 + 1 * blackP2) / 4
    OLED12864_I2C.show_string(0, 0, "CAL", 1)
    basic.pause(2000)
    OLED12864_I2C.show_number(0, 0, bp2cal, 1)
    OLED12864_I2C.show_number(0, 1, bp1cal, 1)
    OLED12864_I2C.show_number(0, 2, wp2cal, 1)
    OLED12864_I2C.show_number(0, 3, wp1cal, 1)
    basic.pause(5000)
    OLED12864_I2C.clear()
    stopDisp = False
input.on_button_pressed(Button.B, on_button_pressed_b)

def forward():
    pins.analog_write_pin(AnalogPin.P14, speed)
    pins.analog_write_pin(AnalogPin.P13, 0)
    pins.analog_write_pin(AnalogPin.P16, speed)
    pins.analog_write_pin(AnalogPin.P15, 0)

def on_logo_touched():
    global stop
    stop = not (stop)
input.on_logo_event(TouchButtonEvent.TOUCHED, on_logo_touched)

def getShowLine():
    global linksP2, rechtsP1
    linksP2 = pins.analog_read_pin(AnalogPin.P2)
    rechtsP1 = pins.analog_read_pin(AnalogPin.P1)
    if not (stopDisp):
        OLED12864_I2C.show_string(0, 2, "    ", 1)
        OLED12864_I2C.show_string(0, 3, "    ", 1)
        OLED12864_I2C.show_number(0, 2, linksP2, 1)
        OLED12864_I2C.show_number(0, 3, rechtsP1, 1)
blackP2 = 0
blackP1 = 0
linksP2 = 0
whiteP2 = 0
rechtsP1 = 0
whiteP1 = 0
stopDisp = False
wp2cal = 0
wp1cal = 0
bp2cal = 0
bp1cal = 0
turnspeed = 0
speed = 0
stop = False
led.enable(False)
OLED12864_I2C.init(60)
OLED12864_I2C.clear()
OLED12864_I2C.zoom(True)
stop = True
speed = 500
turnspeed = 350
bp1cal = 400
bp2cal = 400
wp1cal = 280
wp2cal = 280
lastDir = -1
stopDisp = False

def on_forever():
    global lastDir
    getShowLine()
    basic.pause(200)
    if stop:
        stopdrive()
    elif linksP2 < wp2cal and rechtsP1 < wp1cal:
        if lastDir == 1:
            right()
        elif lastDir == 2:
            left()
        elif lastDir == 0:
            backward()
        else:
            stopdrive()
    elif linksP2 > bp2cal and rechtsP1 > bp1cal:
        lastDir = 0
        forward()
    elif linksP2 > bp2cal and rechtsP1 < wp1cal:
        lastDir = 1
        left()
    elif linksP2 < wp2cal and rechtsP1 > bp1cal:
        lastDir = 2
        right()
basic.forever(on_forever)

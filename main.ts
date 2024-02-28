function right () {
    pins.analogWritePin(AnalogPin.P14, turnspeed)
    pins.analogWritePin(AnalogPin.P13, 0)
    pins.analogWritePin(AnalogPin.P16, 0)
    pins.analogWritePin(AnalogPin.P15, turnspeed)
}
function left () {
    pins.analogWritePin(AnalogPin.P14, 0)
    pins.analogWritePin(AnalogPin.P13, turnspeed)
    pins.analogWritePin(AnalogPin.P16, turnspeed)
    pins.analogWritePin(AnalogPin.P15, 0)
}
function stopdrive () {
    pins.analogWritePin(AnalogPin.P14, 0)
    pins.analogWritePin(AnalogPin.P13, 0)
    pins.analogWritePin(AnalogPin.P16, 0)
    pins.analogWritePin(AnalogPin.P15, 0)
}
input.onButtonPressed(Button.A, function () {
    whiteP1 = rechtsP1
    whiteP2 = linksP2
})
function backward () {
    pins.analogWritePin(AnalogPin.P14, 0)
    pins.analogWritePin(AnalogPin.P13, speed)
    pins.analogWritePin(AnalogPin.P16, 0)
    pins.analogWritePin(AnalogPin.P15, speed)
}
input.onButtonPressed(Button.B, function () {
    stopDisp = true
    blackP1 = rechtsP1
    blackP2 = linksP2
    wp1cal = (1 * blackP1 + 8 * whiteP1) / 9
    wp2cal = (1 * blackP2 + 8 * whiteP2) / 9
    bp1cal = (3 * whiteP1 + 1 * blackP1) / 4
    bp2cal = (3 * whiteP2 + 1 * blackP2) / 4
    OLED12864_I2C.showString(
    0,
    0,
    "CAL",
    1
    )
    basic.pause(2000)
    OLED12864_I2C.showNumber(
    0,
    0,
    bp2cal,
    1
    )
    OLED12864_I2C.showNumber(
    0,
    1,
    bp1cal,
    1
    )
    OLED12864_I2C.showNumber(
    0,
    2,
    wp2cal,
    1
    )
    OLED12864_I2C.showNumber(
    0,
    3,
    wp1cal,
    1
    )
    basic.pause(5000)
    OLED12864_I2C.clear()
    stopDisp = false
})
function forward () {
    pins.analogWritePin(AnalogPin.P14, speed)
    pins.analogWritePin(AnalogPin.P13, 0)
    pins.analogWritePin(AnalogPin.P16, speed)
    pins.analogWritePin(AnalogPin.P15, 0)
}
input.onLogoEvent(TouchButtonEvent.Touched, function () {
    stop = !(stop)
})
function getShowLine () {
    linksP2 = pins.analogReadPin(AnalogPin.P2)
    rechtsP1 = pins.analogReadPin(AnalogPin.P1)
    if (!(stopDisp)) {
        OLED12864_I2C.showString(
        0,
        2,
        "    ",
        1
        )
        OLED12864_I2C.showString(
        0,
        3,
        "    ",
        1
        )
        OLED12864_I2C.showNumber(
        0,
        2,
        linksP2,
        1
        )
        OLED12864_I2C.showNumber(
        0,
        3,
        rechtsP1,
        1
        )
    }
}
let blackP2 = 0
let blackP1 = 0
let linksP2 = 0
let whiteP2 = 0
let rechtsP1 = 0
let whiteP1 = 0
let stopDisp = false
let wp2cal = 0
let wp1cal = 0
let bp2cal = 0
let bp1cal = 0
let turnspeed = 0
let speed = 0
let stop = false
led.enable(false)
OLED12864_I2C.init(60)
OLED12864_I2C.clear()
OLED12864_I2C.zoom(true)
stop = true
speed = 500
turnspeed = 350
bp1cal = 400
bp2cal = 400
wp1cal = 280
wp2cal = 280
let lastDir = -1
stopDisp = false
basic.forever(function () {
    getShowLine()
    basic.pause(200)
    if (stop) {
        stopdrive()
    } else if (linksP2 < wp2cal && rechtsP1 < wp1cal) {
        if (lastDir == 1) {
            right()
        } else if (lastDir == 2) {
            left()
        } else if (lastDir == 0) {
            backward()
        } else {
            stopdrive()
        }
    } else if (linksP2 > bp2cal && rechtsP1 > bp1cal) {
        lastDir = 0
        forward()
    } else if (linksP2 > bp2cal && rechtsP1 < wp1cal) {
        lastDir = 1
        left()
    } else if (linksP2 < wp2cal && rechtsP1 > bp1cal) {
        lastDir = 2
        right()
    }
})

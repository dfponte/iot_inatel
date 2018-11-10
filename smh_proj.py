import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO
from dweet import Dweet

GPIO_CS = GPIO.gpio_id('GPIO_B')
BUTTON = GPIO.gpio_id('GPIO_A')
RELE = GPIO.gpio_id('GPIO_C')
LED = GPIO.gpio_id('GPIO_E')

pins = ((GPIO_CS, 'out'), (BUTTON, 'in'), (RELE, 'out'), (LED, 'out'),)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

system_status = 1

dweet = Dweet()


def readTemp(gpio):

	gpio.digital_write(GPIO_CS, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(GPIO_CS, GPIO.LOW)
	r = spi.xfer2([0x01, 0xA0, 0x00])
	gpio.digital_write(GPIO_CS, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)
	adc_temp = (adcout *5.0/1023-0.5)*100
	return adc_temp



#def readDweet():


if __name__=='__main__':
	with GPIO(pins) as gpio:
		while True:
		                temp = readTemp(gpio)
				print "Temp: %2.1f\n"%(temp)
				dweet.dweet_by_name(name="inatel_ead", data={"Temperatura":temp})
			        time.sleep(5)

from picamera2 import Picamera2, Preview
from time import sleep

def picture(x):
    picam2 = Picamera2()
    preview_config = picam2.preview_configuration(main={"size": (640, 480)})
    picam2.configure(preview_config)

    picam2.start_preview(Preview.QTGL)
    picam2.start()
    sleep(2)
    
    for picture in range(10):
        metadata = picam2.capture_file("/home/rasberrypi/Desktop/" + x + "{0:04d}.jpg".format(picture))
        sleep(0.10)
        
    picam2.close() 
    print("Donee")

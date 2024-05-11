import socket
import picamera2
import time
from picamera2 import Picamera2

# Create a socket object
s = socket.socket()
print('Socket created successfully ...')
host = '192.168.1.11'
port = 4000
print('Server will start on host:', host)
s.bind((host, port))
print('Server is bound successfully ...')                           
s.listen(5)
print('Server is listening ...')

while True:
    conn, addr = s.accept()
    print('Got connection from:', addr)
    conn.send(b'Thank you for connecting')
    picam2 = Picamera2()
    camera_config = picam2.create_preview_configuration()
    picam2.configure(camera_config)
    picam2.start_preview()
    picam2.start()
    time.sleep(2)
    picam2.capture_file("image.jpg")



    conn.send(b'image.jpg')
    

    # send image data
    with open('image.jpg', 'rb') as f:
        data = f.read(1024)
        while data:
            conn.send(data)
            data = f.read(1024)
        print('Image data sent')

    print('Image sent')
    conn.send()



    time.sleep(3)
    conn.close()

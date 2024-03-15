import socket

def receive_image(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))

        # Receive the welcome message
        welcome_message = client_socket.recv(1024)
        print(welcome_message.decode())

        # Request the image and receive the filename from the server
        filename = client_socket.recv(1024).decode()
        print(f"Received filename: {filename}")

        # Check if the filename is empty
        if not filename:
            raise ValueError("Received an empty filename")

        # Receive the image data
        print("Receiving image data ...")
        image_data = b''
        while True:
            data = client_socket.recv(1024)
            # print(data)

            image_data += data
            print(f"Received {len(image_data)} bytes")
            if  data == b'': # No more data to receive
                break
            
        # Save the received image to a file with the received filename
        with open(filename, 'wb') as image_file:
            image_file.write(image_data)

        print(f'Image received and saved as {filename}')

        # Send OK to server
        client_socket.sendall(b'OK')

    except Exception as e:
        print(f"Error: {e}")
        with open(filename, 'wb') as image_file:
            image_file.write(image_data)
    finally:
        client_socket.close()

if __name__ == '__main__':
    server_host = '192.168.1.11'  # Replace with the server's IP address
    server_port = 4000

    receive_image(server_host, server_port)

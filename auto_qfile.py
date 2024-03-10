import serial
import time
# Set the port and baud rate
port = 'COM16'  # Replace 'COM1' with your port
baudrate = 115200  # Replace 9600 with your baud rate

# Connect to Tera Term
try:
    ser = serial.Serial(port, baudrate, timeout=1)
    print("Connected to Tera Term.")
except serial.SerialException as e:
    print("Failed to connect to Tera Term:", e)
    exit()

# Wait for a moment before sending command
time.sleep(2)

# Send command
command = b'dtach\r\n'  # Command to send, adjust as needed
ser.write(command)

# Read the response
response = ser.readline()
print("Response from Tera Term:", response.decode())

# Close the connection
ser.close()

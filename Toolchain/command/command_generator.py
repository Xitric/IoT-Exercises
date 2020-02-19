from serial import Serial, EIGHTBITS, PARITY_NONE, STOPBITS_ONE

# Must match ESP32 connection
conn = Serial("COM4", baudrate=115200, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE, timeout=1)

while True:
    msg = input("> ") + '\n'
    print(conn.is_open)
    conn.write(msg.encode("utf-8"))  # Expects data to be bytes or a byte array

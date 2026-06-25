import serial
import time

def send_to_arduino(
    braille_text,
    port="/dev/ttyACM0",
    baudrate=9600
):

    """
    점자 문자열을 Arduino로 전송
    """

    try:
        # Arduino 연결
        ser = serial.Serial(
            port,
            baudrate,
            timeout=1
        )
        time.sleep(2)

        # 데이터 전송
        ser.write(
            braille_text.encode("utf-8")
        )
        print("Braille data sent")

        ser.close()

    except Exception as e:

        print("Arduino connection failed")
        print(e)

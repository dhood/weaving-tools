import time

import arduino_comm
import lift_pattern_io

USING_ARDUINO = False
wait_time = 5  # seconds

if __name__ == '__main__':
    if USING_ARDUINO:
        arduinoComm = arduino_comm.ArduinoComm()

    lift_pattern_filename = 'lift_pattern.txt'
    liftPattern = lift_pattern_io.read_lift_pattern(lift_pattern_filename)

    numShafts = max(max(liftPattern))

    for liftStep in liftPattern:
        settings = [1 if shaft in liftStep else 0 for shaft in range(1, numShafts+1)]
        print('Lifting shafts: ' + str(liftStep))
        print('Setting shafts to settings: ' + str(settings))

        # Send settings to arduino
        for shaft in range(1, numShafts+1):
            if USING_ARDUINO:
                arduinoComm.sendShaftSetting(shaft, setting)

        # Wait for the pick to be complete
        time.sleep(wait_time)


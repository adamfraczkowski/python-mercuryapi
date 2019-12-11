#!/usr/bin/env python3
import mercury
import time
from datetime import datetime
import mercury
reader = mercury.Reader("tmr:///dev/ttyUSB0", baudrate=115200)

#param_list_val = reader.get_param_list_values()
#print(param_list_val)
#for i in range(len(param_list_val)):
#    print(param_list_val[i])

reader.set_region("EU3")
reader.set_read_plan([1], "GEN2", read_power=1900)
print(reader.read())

reader.start_reading(lambda tag: print(tag.epc, tag.antenna, tag.read_count, tag.rssi, datetime.fromtimestamp(tag.timestamp)))
time.sleep(1)
reader.stop_reading()

#!/usr/bin/env python3
import mercury
reader = mercury.Reader("tmr:///dev/ttyS0")
reader.set_region("open")
reader.set_read_plan([3], "GEN2", ["epc"], 3150)
print("model:              " + reader.get_model())
print("antennas:           " + str(reader.get_antennas()))
print("connected antennas: " + str(reader.get_connected_port_list()))
print("power range:        " + str(reader.get_power_range()))

""" print("GET PARAM LIST")
print(reader.get_param_list())
param_list = reader.get_param_list()
for i in range(len(param_list)):
    print(param_list_val[0] + " : " + param_list_val[1])
 """
param_list_val = reader.get_param_list_values()
print(param_list_val)
#for i in range(len(param_list_val)):
#    print(param_list_val[i])

#print(reader.set_read_powers([1, 2, 3, 4], [3150, 500, 500, 500]))
#print(reader.set_read_powers([1, 2, 3, 4], [500, 500, 500, 500]))
""" read = reader.read(5000)
print("read:               " + str(len(read)))
for i in range(len(read)):
    print("----------------------------------")
    print("epc:        " + str(read[i].epc))
    print("antenna:    " + str(read[i].antenna))
    print("read count: " + str(read[i].read_count))
    print("rssi:       " + str(read[i].rssi))
print("----------------------------------") """
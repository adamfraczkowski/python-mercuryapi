#!/usr/bin/env python3
import mercury
import time
reader = mercury.Reader("tmr:///dev/ttyS0")
reader.set_region("open")
reader.set_read_plan([1], "GEN2", ["epc"], 2000)
print("model:              " + reader.get_model())
print("antennas:           " + str(reader.get_antennas()))
print("connected antennas: " + str(reader.get_connected_port_list()))
print("power range:        " + str(reader.get_power_range()))

#param_list_val = reader.get_param_list_values()
#print(param_list_val)
#for i in range(len(param_list_val)):
#    print(param_list_val[i])

#print(reader.set_read_powers([1, 2, 3, 4], [3150, 500, 500, 500]))
#print(reader.set_read_powers([1, 2, 3, 4], [500, 500, 500, 500]))
read = reader.read(1000)
print("read:               " + str(len(read)))
start = time.time()
for i in range(len(read)):
    print(str(read[i].epc)[2:-1])
    #reader.write_reserved_bank(str(read[i].epc)[2:-1],'87654321')
    #reader.kill_tag(str(read[i].epc)[2:-1],'87654321')
end = time.time()
print("KILL TIME--------------------: ")
print(end-start)
'''
start = time.time()
reader.write_reserved_bank('E20032E2EBB7D5F124756F57','87654321')
reader.kill_tag('E20032E2EBB7D5F124756F57','87654321')
end = time.time()
read = reader.read(1000)
print("read:               " + str(len(read)))
for i in range(len(read)):
    print("----------------------------------")
    print("epc:        " + str(read[i].epc))
    print("antenna:    " + str(read[i].antenna))
    print("read count: " + str(read[i].read_count))
    print("rssi:       " + str(read[i].rssi))
print("----------------------------------")
print("KILL TIME--------------------: ")
print(end-start)
'''
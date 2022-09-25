from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from datetime import datetime
from enum import Enum
import time
import numpy as np
import sys
import json
import os

# Load configuration JSON file

# Opening JSON file
cw = os.getcwd()
# print(cw)
config = cw + '/config.json'
f = open(config)
  
# returns JSON object as 
# a dictionary
data = json.load(f)

# print (data)
  
# Set device parameters
plc_address = data['device']['ipv4_address']
modbus_port = data['device']['port']
modbus_unit_id = data['device']['unit_id']
polling_time = data['device']['polling_time'] # seconds

# Load list of variables

  
# Closing file
f.close()

# Connection state init
connection_state = 0

# Modbus TCP-IP communication parameters
# plc_address = str(sys.argv[0])
# modbus_port = sys.argv[1]
# modbus_unit_id = sys.argv[2]

# Polling time
# polling_time = int(sys.argv[3]) # seconds

print('IPv4 address: ' + plc_address)
print('Port: ' + modbus_port)
print('Unit ID: ' + str(modbus_unit_id))
print('Polling time: ' + str(polling_time))
                                                                                                
# Values array - Matrix 100 INT   
values = np.zeros(100)

#DValues array
dvalues = np.zeros(5)

# Modbus client
client = ModbusClient(plc_address, modbus_port)

# Try first socket connection
connection_state = client.connect()

# Error code 
error_code = 0
error_code_desc = ""

try:
 if(connection_state == True):
    connection_state = 1
    print("PLC connection: ONLINE")
 elif(connection_state == False):
    connection_state = 0
    print("PLC connection: OFFLINE")
except:
    connection_state = 0
    print("PLC connection: OFFLINE")
   
# print("PLC Connection = CONNECT")
# request = client.read_holding_registers(3025, 2, modbus_unit)
# decoder = BinaryPayloadDecoder.fromRegisters(request.registers, Endian.Little, wordorder=Endian.Little)
# value = decoder.decode_32bit_float()

#Read register each 5s

while True:
  
   # Start reading time
   startime = time.time()

   print("------------------------------------")
   timestamp = datetime.now()   
   print("Timestamp: ", timestamp)
   if(connection_state == 1):
        print("Connection state: ONLINE")
   elif(connection_state == 0):
        print("Connection state: OFFLINE")
  

   # If connection is open run modbus reading registers
   if(connection_state == 1):
    
      
      
      try: 
              # Read 50 registers - 16 int
              register = 1000 # start address
              request = client.read_holding_registers(register, 100, unit = 1)
              
              # print(request.registers)
              
              # decode_16_bit
              index_register = 0
              index_register_modbus = 0
              
              for index_register in range (50):
              
                  
                  temp_register_value_1 = request.registers[index_register_modbus]
                  temp_register_value_2 = request.registers[index_register_modbus + 1]
                  temp_registers = []
                  temp_registers.append(temp_register_value_1)
                  temp_registers.append(temp_register_value_2)
                  
                  decoder = BinaryPayloadDecoder.fromRegisters(temp_registers, Endian.Big, wordorder=Endian.Big)
                  values[index_register] = decoder.decode_16bit_int()
                  
                  # index_register_modbus += 2
                  index_register_modbus += 1
                  
                  
                  
                  
              # print(index_register_modbus)    
              # Read 50 registers - DINT and SET
              register = 1050 # start address
              request = client.read_holding_registers(register, 100, unit = 1)
              
              # print(request.registers)
              
               # decode_16_bit
              index_register = 0
              index_register_modbus = 0
              
              for index_register in range (50):
              
                  
                  temp_register_value_1 = request.registers[index_register_modbus]
                  temp_register_value_2 = request.registers[index_register_modbus + 1]
                  temp_registers = []
                  temp_registers.append(temp_register_value_1)
                  temp_registers.append(temp_register_value_2)
                  
                  decoder = BinaryPayloadDecoder.fromRegisters(temp_registers, Endian.Big, wordorder=Endian.Big)
                  values[index_register + 50] = decoder.decode_16bit_int()
                  
                  # index_register_modbus += 2
                  index_register_modbus += 1
                  
              
      except  Exception as e:
              values = np.zeros(100)
              error_code = 1
              error_code_desc = e.args[0]
              # client.close()
              connection_state = 0
              # break
        

      # Send dato to externa source
      # TO DO


      # End time
      endtime = time.time()
      print("Execution time: %s seconds " % (endtime - startime))
      print("Error code: ", error_code, " description: ", error_code_desc)
      time.sleep(polling_time)
     
     
   # Else if connection is close store zeros in to dabatabase
   elif(connection_state == 0):
      
        values = np.zeros(100)
        dvalues = np.zeros(5)
        
        
        # End time
        endtime = time.time()
        print("Execution time: %s seconds " % (endtime - startime))
        #  print("Error: ", error_code)
        print("Error code: ", error_code, " description: ", error_code_desc)
        connection_state = client.connect()
     
        if(connection_state == True):
           connection_state = 1
           # print("Re-Connection: ", connection_state)
           error_code = 0
           error_code_desc = ""
        elif(connection_state == False):
           connection_state = 0
           # print("Re-Connection: ", connection_state)
           error_code = 0
           error_code_desc = ""

        time.sleep(polling_time)



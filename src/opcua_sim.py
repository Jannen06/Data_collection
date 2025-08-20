'''This script simulates an OPC-UA server that provides a temperature sensor value.
It can be used for testing OPC-UA clients and data collection scripts.
'''


from opcua import Server
import random
import time

# Create an instance of the OPC-UA server
server = Server()

# Set endpoint for clients to connect
server.set_endpoint("opc.tcp://0.0.0.0:4840")

# Setup server namespace
namespace = server.register_namespace("SimulatedPLC")

# Get the Objects node, which is the root for custom objects
objects_node = server.get_objects_node()

# Create a new object to simulate a PLC
plc_object = objects_node.add_object(namespace, "PLC")

# Add a variable to simulate a temperature sensor
temperature_var = plc_object.add_variable(namespace, "TemperatureSensor1", 25.0)
temperature_var.set_writable()  # Allow clients to write to this variable

# Start the server
server.start()
print("Simulated OPC-UA Server started at opc.tcp://0.0.0.0:4840")

try:
    # Continuously update the temperature value
    while True:
        new_temp = round(random.uniform(20.0, 30.0), 2)
        temperature_var.set_value(new_temp)
        print(f"Updated TemperatureSensor1 to {new_temp}")
        time.sleep(2)

finally:
    # Stop the server on exit
    server.stop()
    print("Simulated OPC-UA Server stopped.")

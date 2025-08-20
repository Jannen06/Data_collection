from opcua import Client

# URL of the OPC-UA server
url = "opc.tcp://localhost:4840"  
client = Client(url)

try:
    client.connect()
    print("Connected to OPC-UA Server")

    # Browse the root node
    root = client.get_root_node()
    print("Root node is:", root)

    # Example: Read a variable node
    # Replace with your actual node ID
    var_node = client.get_node("ns=2;s=TemperatureSensor1")
    value = var_node.get_value()
    print("Value of TemperatureSensor1:", value)

finally:
    client.disconnect()
    print("Disconnected from OPC-UA Server")

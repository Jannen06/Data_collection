from opcua import Client
from influxdb import InfluxDBClient
import time
# OPC-UA server URL
opcua_url = "opc.tcp://192.168.1.100:4840" 

# InfluxDB configuration
influx_host = "localhost"
influx_port = 8086
influx_user = "admin"
influx_password = "password"
influx_dbname = "plc_data"

# Node ID to read from the PLC
node_id = "ns=2;s=TemperatureSensor1"

# Connect to OPC-UA server
opc_client = Client(opcua_url)
opc_client.connect()
print("Connected to OPC-UA Server")

# Connect to InfluxDB
influx_client = InfluxDBClient(
    host=influx_host,
    port=influx_port,
    username=influx_user,
    password=influx_password,
    database=influx_dbname
)
print("Connected to InfluxDB")

try:
    while True:
        # Read value from PLC
        var_node = opc_client.get_node(node_id)
        value = var_node.get_value()
        print(f"Read value: {value}")

        # Prepare data for InfluxDB
        json_body = [
            {
                "measurement": "plc_temperature",
                "fields": {
                    "value": float(value)
                }
            }
        ]

        # Write to InfluxDB
        influx_client.write_points(json_body)
        print("Data written to InfluxDB")

        # Wait before next read
        time.sleep(5)

finally:
    opc_client.disconnect()
    influx_client.close()
    print("Disconnected from OPC-UA Server and InfluxDB")

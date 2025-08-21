'''
This script connects to an OPC-UA server, reads data from a specified node,
and writes that data to an InfluxDB database.
'''

import time
from opcua import Client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import requests

class DataCollection:
    def __init__(self):
        # OPC-UA server URL
        self.opcua_url = "opc.tcp://jannen-ThinkPad:53530/OPCUA/SimulationServer"
        # opcua_url = "opc.tcp://192.168.0.5:4840" 

        # NodeIDs to read from the OPC-UA server
        self.node_ids = [
            "ns=3;i=5",
            "ns=3;i=6",
            "ns=3;i=7",
            "ns=3;i=8",
            "ns=3;i=9"
        ]
        # InfluxDB configuration
        self.influx_host = "http://localhost:8086"
        # influx_host = "10.80.10.1"  # Company InfluxDB server
        self.token = "UDb3euK28xX5A027jQStLnv4yJ9Hmsbx43TpCUUftiHsfV6EY4Q2RNJu1u600Ldi-R1jWcVOsluzoU8yVVGBoQ=="
        self.org = "jannen" # We should replace this with real organization name
        # bucket = "plc_data" 
        self.bucket = "machine_status"


    def run(self):     
        # Connect to OPC-UA server
        opc_client = Client(self.opcua_url)
        try:
            opc_client.connect()
            if opc_client.is_connected():
                print("Connected to OPC-UA Server")
            else:
                print("OPC-UA Server connection failed.")

        # Exit the run method gracefully
        except Exception as e:
            print(f"Error connecting to OPC-UA Server: {e}")


        # Connect to InfluxDB
        try:
            influx_client = InfluxDBClient(url=self.influx_host, token=self.token, org=self.org)
            # health check
            health = requests.get(f"{self.influx_host}/health")
            if health.ok and health.json().get("status") == "pass":
                write_api = influx_client.write_api(write_options=SYNCHRONOUS)
                print("Connected to InfluxDB and health check passed.")
            else:
                print("InfluxDB health check failed.")
        except Exception as e:
            print(f"Failed to connect to InfluxDB: {e}")
            return


        try:
            while True:
                json_body = []
                # Read values from the specified nodes
                for node_id in self.node_ids:
                    node = opc_client.get_node(node_id)
                    value = node.get_value()
                    print(f"Read {node_id}: {value}")

                    if value is None:
                        print(f"Warning: Node {node_id} returned None")
                        continue

                    json_body.append({
                        "measurement": "machine_status",
                        "tags": {
                            "node_id": node_id
                        },
                        "fields": {
                            "value": int(value) if isinstance(value, bool) else float(value)
                        }
                    })

                    # Write to InfluxDB            
                    point = Point("machine_status").tag("node_id", node_id) \
                        .field("value", int(value) if isinstance(value, bool) else float(value)) \
                        .time(time.time_ns(), WritePrecision.NS)
                    write_api.write(bucket=self.bucket, org=self.org, record=point)

                print("Data written to InfluxDB")

                # Wait before next read
                print("Waiting for 1 second before next read...")
                time.sleep(1)

        finally:
            opc_client.disconnect()
            influx_client.close()
            print("Disconnected from OPC-UA Server and InfluxDB")
            print("Data collection completed.")
            print("Exiting...")

def main(args=None):
    data_collector = DataCollection()
    data_collector.run()

if __name__ == "__main__":
    main()
    

# This script connects to an OPC-UA server, reads data from specified nodes,
# and writes that data to an InfluxDB database.
# It is designed to run continuously, reading data every second and writing it to the database.
# Make sure to replace the OPC-UA server URL and InfluxDB configuration with your actual settings.
# The script handles connection and disconnection gracefully, ensuring resources are cleaned up on exit.
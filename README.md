
# OPC-UA to InfluxDB Data Collection

This project connects to a Prosys OPC-UA simulation server, reads machine status data from specified nodes, and writes it to an InfluxDB database using Docker.

---

## Requirements

- Docker
- Python 3.10+
- Prosys OPC-UA Simulation Server
- Python packages:
  - `opcua`
  - `influxdb-client`
  - `requests`

Install dependencies:
```bash
pip install opcua influxdb-client requests
```

---

## Setup Instructions

### 1. Run InfluxDB with Docker

```bash
docker volume create influxdb-storage

docker run -d   --name=influxdb   -p 8086:8086   -v influxdb-storage:/var/lib/influxdb2   -e INFLUXDB_ADMIN_USER=admin   -e INFLUXDB_ADMIN_PASSWORD=password   -e INFLUXDB_DB=machine_status   influxdb:2.7
```

Access InfluxDB UI at: [http://localhost:8086](http://localhost:8086)

Create:
- **Organization**: `xxxx`
- **Bucket**: `machine_status` // change according to the need
- **Token**: with read/write access to the bucket

---

### 2. Run Prosys OPC-UA Simulation Server

- Download and install from: [https://www.prosysopc.com/products/opc-ua-simulation-server/](https://www.prosysopc.com/products/opc-ua-simulation-server/)
- Start the server
- Add custom nodes under `MachineStatus` object with NodeIDs:
  - `ns=3;i=5` to `ns=3;i=9`

---

## Running the Script

Update `opcua_to_influx.py` with your token and server details.

Run the script:
```bash
python src/opcua_to_influx.py
```

This will:
- Connect to the OPC-UA server
- Read values from nodes `ns=3;i=5` to `ns=3;i=9`
- Write data to InfluxDB bucket `machine_status`

---

## Viewing Data in InfluxDB

1. Go to **Explore** in the InfluxDB UI
2. Select bucket `machine_status`
3. Use the Script Editor with this query:

```flux
from(bucket: "machine_status")
  |> range(start: -1h)
  |> filter(fn: (r) => r._measurement == "machine_status")
  |> filter(fn: (r) => r._field == "value")
```

---

## Stopping InfluxDB

To stop the container:
```bash
docker stop influxdb
```

To remove it:
```bash
docker rm -f influxdb
```

To remove the volume:
```bash
docker volume rm influxdb-storage
```

---
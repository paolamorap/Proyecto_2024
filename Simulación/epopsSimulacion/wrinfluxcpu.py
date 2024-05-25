from influxdb import InfluxDBClient
import time
# Conexión al servidor InfluxDB
client = InfluxDBClient(host='localhost', port=8086, username='admin', password='admin', database='influx')
data = []
def wr_influx(datos):
    direc = list(datos.keys())
    for ip in direc:
        try:    
            d1 = {
                    "measurement": "cpupython",
                    "tags": {
                        "dispositivo": str(ip)
                    },
                    "fields": {
                        "uso5min": float(datos[ip])
                    }
                }
        except TypeError:
            pass
        data.append(d1)
    client.write_points(data)
    time.sleep(1)
    client.close()

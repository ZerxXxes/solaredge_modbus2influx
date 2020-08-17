#!/usr/bin/env python3
try:
    from influxdb import InfluxDBClient
    import solaredge_modbus
    import json
    import time
    from datetime import datetime
except:
    print("You need to install the packages 'influxdb' and 'solaredge_modbus' with pip")

def create_db():
    client.create_database('solaredge_data')
    client.switch_database('solaredge_data')
    #Create the default retention policy that deletes to old data
    client.create_retention_policy('standard_policy', config["INFLUXDB_RETENTION_TIME"], 1, default=True)

#This function takes all output from the inverter, finds all scale-values and applies them to their metrics so all values gets correct scale
def scale_fields(input):
    result = dict()
    for key, val in input.items():
        #Ignore everything that is not a metric value here
        if key.endswith('_scale') or key.startswith('c_') or isinstance(val, bool):
            continue
        if "status" in key:
            result[key] = val
        try:
            #Apply the _scale-value to the corresponding metric and save the value correctly scaled
            result[key] = float(round((10**input['%s_scale' % key]) * val, 2))
        except KeyError:
            try:
                #when scale name is not an exact match as the metric(p1_voltage for example) split away everything before the _
                result[key] = float(round((10**input['%s_scale' % key.split("_",2)[1]]) * val, 2))
            except:
                continue
        except:
            continue
    return result

#Load all config from file
with open('/etc/se_modbus2influx.conf') as config_file:
    config = json.load(config_file)

#Connect to Inverter and InfluxDB
inverter = solaredge_modbus.Inverter(host=config["INVERTER_ADDRESS"], port=config["INVERTER_TCP_PORT"])
client = InfluxDBClient(host=config["INFLUXDB_ADDRESS"], port=config["INFLUXDB_PORT"], username=config["INFLUXDB_USER"], password=config["INFLUXDB_PASSWORD"])

# Create InfluxDB data template
data = {
    'measurement': 'SolarEdge_data',
    'tags': '',
    'fields': ''
}
tags = {}
fields = {}
json_body = []
loop_count = 0

#Check if the database already exsists, if not create it
databases = client.get_list_database()
if 'solaredge_data' not in databases:
    create_db()

print("Starting Solaredge Modbus2Influx")
print("Solaredge Inverter address: {}, port: {}".format(config["INVERTER_ADDRESS"], config["INVERTER_TCP_PORT"]))
print("InfluxDB Server address: {}, port: {}".format(config["INFLUXDB_ADDRESS"], config["INFLUXDB_PORT"]))
print("Collected data from the inverter will be printed to stdout every 5s the first minute, then once every 15min")

#Start main lopp
while True:
    if inverter.connected():
        try:
            inverter_data = inverter.read_all()
        except:
            time.sleep(5)
            continue
        #data starting with c_ is static names like model name and serial number, save these as tags in influx
        for k,v in inverter_data.items():
            if k.startswith('c_'):
                tags[k] = v

        data['tags'] = tags
        data['fields'] = scale_fields(inverter_data)
        json_body.append(data)
        
        #Print datablock to stdout the first minute and then every 15min to make the log less bloaty
        if loop_count < 12 or loop_count % 180 == 0:
            print("{} - Inserting data to influx".format(datetime.now()))
            print(data)
        try:
            client.write_points(json_body)
        except:
            print("{} - ERROR! Can not write to influxDB".format(datetime.now()))
        time.sleep(5)
    else:
        print("{} - ERROR! Not connected to Inverter".format(datetime.now()))
        time.sleep(5)
    loop_count += 1



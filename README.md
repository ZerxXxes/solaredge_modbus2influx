# Solaredge Modbus To InfluxDB
This is a small script to collect data from Solaredge inverters via their Modbus TCP-interface and store the data in influxDB so that it can be picked up by Grafana to make nice dashboards.   
Data is collected every 5s giving much higher resolution than Solaredge's own app that saves datapoints every 15min.  

![Example Grafana dashborad](/docs/solar_dash.png "A Grafana dashboard with this data")

#### Data collected over modbus
- Current (Total and per phase)
- Frequency
- DC Power from solar panels
- AC Power out from inverter
- Voltage per phase
- Inverter temperature
- Lifetime production
- Inverter status

#### Models tested
- SE15K-RW0T0BNN4
- SE3500H-RW000BNN4

## Installation
This install guide is tested on Ubuntu Linux.  
Make sure you have installed **InfluxDB** and **Grafana** first.  
Then make sure your Solaredge inverter has Modbus over TCP enabled (This is disabled by default on newer firmware) otherwise scroll down for a guide on how to enable this. 
  
Start by cloneing this repo:  
``git clone https://github.com/ZerxXxes/solaredge_modbus2influx.git``  
Then edit **se_modbus2influx.conf** with your own settings:  

    {
        "INVERTER_ADDRESS":"192.168.1.99", <-- The IP-address of your Solaredge Inverter on your network, can be found in the DHCP-table of your router
        "INVERTER_TCP_PORT":"1502",        <-- The Modbus TCP-port your inverter uses, 1502 seems to be standard
        "INFLUXDB_ADDRESS":"localhost",    <-- Address of your influxdb-server, localhost if influx runs on the same server
        "INFLUXDB_PORT":"8086",            <-- InfluxDB Port, 8086 is default
        "INFLUXDB_USER":"",                <-- InfluxDB User, not needed if you run influx on the same server
        "INFLUXDB_PASSWORD":"",            <-- InfluxDB Password, not needed if you run influx on the same server
        "INFLUXDB_RETENTION_TIME":"12w"    <-- How long influxDB should save data in the database, set to INF to save data forever. (Might use a LOT of diskspace)
    }  

Then run ``sudo ./install.sh``  
This will install the script as a systemd service.  
You can check the status of the service with  
``systemctl status se_modbus2influx.service``  
and you can read the logs with  
``sudo journalctl -u se_modbus2influx.service``  

## Setting up Grafana

## Enable Modbus TCP on Solaredge Inverter

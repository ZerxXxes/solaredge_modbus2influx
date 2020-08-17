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
Make sure you have installed [InfluxDB](https://docs.influxdata.com/influxdb/v1.8/introduction/install/) and [Grafana](https://grafana.com/docs/grafana/latest/installation/debian/) first.  
Then make sure your Solaredge inverter has Modbus over TCP enabled (This is disabled by default on newer firmware) otherwise scroll down for a guide on how to enable this. 
  
**1.**  
Start by cloneing this repo:  
``git clone https://github.com/ZerxXxes/solaredge_modbus2influx.git``  
  
**2.**  
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
  
**3.**  
Then run ``sudo ./install.sh``  
This will install the script as a systemd service.  
  
You can check the status of the service with  
``systemctl status se_modbus2influx.service``  
and you can read the logs with  
``sudo journalctl -u se_modbus2influx.service``  

## Setting up Grafana  
Go to the Grafana interface and login. First you need to add a new datasource.  
Choose the influxDB-datasource and if you run influxDB on the same machine just use address localhost and port 8086.  
Enter the database name **solaredge_data** and save and test the connection.  
If grafana can connect to the database then you are ready to go.  
You can now create a new dashboard and add your own graphs as you like.  
If you want the example dashboard in the top of this README you can just go to Dashboards>Manage in grafana and click Import.  
Then you can select the **grafana_dashboard.json** from this repo to import that finished dashboard.  

## Enable Modbus TCP on Solaredge Inverter
1. Make sure you have the most recent Solaredge app called **mySolarEdge**
2. Open the menu in the app and choose Inverter Status and follow the instructions in the app to connect to the inverter.
3. As soon as you are connected to the inverter, exit the app and open your webbrowser. Go to: http://172.16.0.1
4. This is the web version of the inverter settings page. Here you go to Communication->Modbus TCP port and Enable Modbus TCP.

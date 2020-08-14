#!/usr/bin/env bash
if [[ $EUID -ne 0 ]]; then
  echo -e "ERROR: You must be a root user" 2>&1
  exit 1
fi
cp main.py /usr/local/bin/se_modbus2influx
cp se_modbus2influx.conf /etc/se_modbus2influx.conf
cp se_modbus2influx.service /etc/systemd/system/se_modbus2influx.service
systemctl start se_modbus2influx
systemctl enable se_modbus2influx


from sungrow_websocket import SungrowWebsocket
import time
import influxdb_client
import logging
import os

logging.basicConfig(level=logging.WARNING)

def pull_inverter_data():
    host = os.environ['SUNGROW_IP_ADDR']
    sg = SungrowWebsocket(host)
    data = sg.get_data()
    return data
        
def conenct_influx(influx_data):
    token = os.environ['INFLUX_TOKEN']
    url = f'http://{os.environ["INFLUX_HOST"]}:8086'
    client = influxdb_client.InfluxDBClient(url=url, token=token, org=os.environ['INFLUX_ORG'])
    points = []
    for key, value in influx_data.items():
        points.append(influxdb_client.Point(os.environ['INFLUX_MEASUREMENT_PV']).tag(os.environ['INFLUX_MEASUREMENT_PV'], 100).field(key, value).time(time.time_ns(), influxdb_client.WritePrecision.NS))
    with client.write_api(write_options=influxdb_client.client.write_api.SYNCHRONOUS) as write_api:
        for point in points:
            write_api.write(bucket=os.environ['INFLUX_BUCKET'], org=os.environ['INFLUX_ORG'], record=point)


def influx_mapping(sungrow_data):
    INFLUX_SCHEMA = {
        'inverter_power': 0,
        'house_power': 0,
        'mpp1_power': 0,
        'mpp2_power': 0,
        'mpp3_power': 0,
        'house_power': 0,
        'bat_power_plus': 0,
        'bat_power_minus': 0,
        'bat_fuel_charge': 0,
        'wallbox_charge_power': 0,
        'wallbox_charge_power0': 0,
        'wallbox_charge_power1': 0,
        'wallbox_charge_power2': 0,
        'wallbox_charge_power3': 0,
        'grid_power_plus': 0,
        'grid_power_minus': 0,
        'power_ratio': 0,
        'case_temp': 0,
        'current_state': 0,
        'current_state_code': 0,
        'current_state_ok': 0
    }
    for key, value in sungrow_data.items():
        if key == 'total_active_power':
            if float(value[2]) < 0:
                INFLUX_SCHEMA['inverter_power'] = 0
            else: 
                INFLUX_SCHEMA['inverter_power'] = int(float(value[2])*1000)
        if key == 'load_total_active_power':
            INFLUX_SCHEMA['house_power'] = int(float(value[2])*1000)
        if key == 'mppt1_current':
            INFLUX_SCHEMA['mpp1_power'] = int(float(value[2])*1000)
        if key == 'mppt2_current':
            INFLUX_SCHEMA['mpp2_power'] = int(float(value[2])*1000)
        if key == 'mppt3_current':
            INFLUX_SCHEMA['mpp3_power'] = int(float(value[2])*1000)
        if key == 'house_power':
            INFLUX_SCHEMA['house_power'] = int(float(value[2])*1000)
        if key == 'config_key_3907':
            INFLUX_SCHEMA['bat_power_plus'] = int(float(value[2])*1000)
        if key == 'config_key_3921':
            INFLUX_SCHEMA['bat_power_minus'] = int(float(value[2])*1000)
        if key == 'battery_soc':
            INFLUX_SCHEMA['bat_fuel_charge'] = float(value[2])
        if key == 'wallbox_charge_power':
            INFLUX_SCHEMA['wallbox_charge_power'] = int(float(value[2])*1000)
        if key == 'wallbox_charge_power0':
            INFLUX_SCHEMA['wallbox_charge_power0'] = int(float(value[2])*1000)
        if key == 'wallbox_charge_power1':
            INFLUX_SCHEMA['wallbox_charge_power1'] = int(float(value[2])*1000)
        if key == 'wallbox_charge_power2':
            INFLUX_SCHEMA['wallbox_charge_power2'] = int(float(value[2])*1000)
        if key == 'wallbox_charge_power3':
            INFLUX_SCHEMA['wallbox_charge_power3'] = int(float(value[2])*1000)
        if key == 'config_key_4060':
            INFLUX_SCHEMA['grid_power_plus'] = int(float(value[2])*1000)
        if key == 'feed_network_total_active_power':
            INFLUX_SCHEMA['grid_power_minus'] = int(float(value[2])*1000)
        if key == 'power_ratio':
            INFLUX_SCHEMA['power_ratio'] = value[2]
        if key == 'air_tem_inside_machine':
            INFLUX_SCHEMA['case_temp'] = float(value[2])
        if key == 'device_status':
            INFLUX_SCHEMA['current_state'] = value[2]
        if key == 'current_state_code':
            INFLUX_SCHEMA['current_state_code'] = value[2]
        if key == 'current_state_ok':
            INFLUX_SCHEMA['current_state_ok'] = value[2]
    return INFLUX_SCHEMA

if __name__ == "__main__":
    data = pull_inverter_data()
    influx_data = influx_mapping(data)
    conenct_influx(influx_data)
    

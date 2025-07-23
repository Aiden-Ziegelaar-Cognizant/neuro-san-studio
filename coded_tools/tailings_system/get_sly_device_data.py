from neuro_san.interfaces.coded_tool import CodedTool
import duckdb
from typing import Any, Dict, Union
from datetime import date, timedelta

# con_t.execute("CREATE TABLE sites (site_id INTEGER PRIMARY KEY, site_name TEXT)")
# con_t.execute("CREATE TABLE dataloggers (datalogger_id INTEGER PRIMARY KEY, site_id INTEGER, serial_number TEXT)")
# con_t.execute("CREATE TABLE vwp_devices (vwp_device_id INTEGER PRIMARY KEY, datalogger_id INTEGER, device_name TEXT, channel INTEGER)")
# con_t.execute("CREATE TABLE readings (vwp_device_id INTEGER, reading_date DATE, reading_value INTEGER, is_exceedence BOOL, PRIMARY KEY (vwp_device_id, reading_date))")

class GetSlyDeviceData(CodedTool):
    def __init__(self):
        self.tailings_db = duckdb.connect("/Users/2279890/Documents/GitHub/neuro-san-studio/coded_tools/tailings_system/tailings.db")
        super().__init__()
    
    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        device_list = args.get("device_list", [])

        # select all readings
        query = """
        SELECT v.device_name, r.reading_date, r.reading_value
        FROM vwp_devices v
        JOIN readings r ON v.vwp_device_id = r.vwp_device_id
        WHERE 
        """

        # add device list if provided
        if device_list:
            query += f" v.device_name IN ({','.join(['?']*len(device_list))})"
            self.tailings_db.execute(query, device_list)
        

        readings = self.tailings_db.fetchall()

        #sort readings into device keys
        devices = {}
        for reading in readings:
            device_name = reading[0]
            if device_name not in devices:
                devices[device_name] = []
            devices[device_name].append([reading[1].isoformat(), reading[2]])
        
        sly_data["graphing_data"] = devices

        return {
            "message": "data stored in sly data variable graphing_data" 
        }

from neuro_san.interfaces.coded_tool import CodedTool
import duckdb
from typing import Any
from typing import Dict
from typing import Union

# con_t.execute("CREATE TABLE sites (site_id INTEGER PRIMARY KEY, site_name TEXT)")
# con_t.execute("CREATE TABLE dataloggers (datalogger_id INTEGER PRIMARY KEY, site_id INTEGER, serial_number TEXT)")
# con_t.execute("CREATE TABLE vwp_devices (vwp_device_id INTEGER PRIMARY KEY, datalogger_id INTEGER, device_name TEXT, channel INTEGER)")
# con_t.execute("CREATE TABLE readings (vwp_device_id INTEGER, reading_date DATE, reading_value INTEGER, is_exceedence BOOL, PRIMARY KEY (vwp_device_id, reading_date))")

class GetDevices(CodedTool):
    def __init__(self):
        self.tailings_db = duckdb.connect("/Users/2279890/Documents/GitHub/neuro-san-studio/coded_tools/tailings_system/tailings.db")
        super().__init__()
    
    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        # get site_name from args
        datalogger_serial = args["datalogger_serial"]
        # get a list of devices for the datalogger from the db
        self.tailings_db.execute(f"SELECT device_name FROM vwp_devices WHERE datalogger_id = (SELECT datalogger_id FROM dataloggers WHERE serial_number = ?)", [datalogger_serial])
    
        # return sites
        return {
            "devices": self.tailings_db.fetchall()
        }

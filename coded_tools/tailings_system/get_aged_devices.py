from neuro_san.interfaces.coded_tool import CodedTool
import duckdb
from typing import Any, Dict, Union
from datetime import date, timedelta

# con_t.execute("CREATE TABLE sites (site_id INTEGER PRIMARY KEY, site_name TEXT)")
# con_t.execute("CREATE TABLE dataloggers (datalogger_id INTEGER PRIMARY KEY, site_id INTEGER, serial_number TEXT)")
# con_t.execute("CREATE TABLE vwp_devices (vwp_device_id INTEGER PRIMARY KEY, datalogger_id INTEGER, device_name TEXT, channel INTEGER)")
# con_t.execute("CREATE TABLE readings (vwp_device_id INTEGER, reading_date DATE, reading_value INTEGER, is_exceedence BOOL, PRIMARY KEY (vwp_device_id, reading_date))")

class GetAgedDevices(CodedTool):
    def __init__(self):
        self.tailings_db = duckdb.connect("/Users/2279890/Documents/GitHub/neuro-san-studio/coded_tools/tailings_system/tailings.db")
        super().__init__()
    
    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        device_list = args.get("device_list", [])  # Optional list of devices to filter
        age = args.get("age", "30")

        age_number = int(age)

        # get date minus age in days
        age_date = date.today() - timedelta(days=age_number)

        query = """
        WITH latest_readings AS (
            SELECT vwp_device_id, MAX(reading_date) as last_reading_date
            FROM readings
            GROUP BY vwp_device_id
        )
        SELECT v.device_name, lr.last_reading_date
        FROM vwp_devices v
        JOIN latest_readings lr ON v.vwp_device_id = lr.vwp_device_id
        """
        
        # Add device filter if provided
        if device_list:
            placeholders = ", ".join(["?" for _ in device_list])
            query += f" AND v.device_name IN ({placeholders})"
            query += f" AND lr.last_reading_date < '{age_date}'"
            self.tailings_db.execute(query, device_list)
        else:
            query += f" AND lr.last_reading_date < '{age_date}'"
            self.tailings_db.execute(query, [])

        return {
            "aged_devices": self.tailings_db.fetchall()
        }

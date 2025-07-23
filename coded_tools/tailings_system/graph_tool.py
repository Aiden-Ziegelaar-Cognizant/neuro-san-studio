from neuro_san.interfaces.coded_tool import CodedTool
from typing import Any, Dict, Union
from datetime import date

from itertools import chain

import numpy as np

import matplotlib.dates as mdates
import matplotlib.units as munits

import matplotlib.pyplot as plt
import matplotlib

import uuid

# con_t.execute("CREATE TABLE sites (site_id INTEGER PRIMARY KEY, site_name TEXT)")
# con_t.execute("CREATE TABLE dataloggers (datalogger_id INTEGER PRIMARY KEY, site_id INTEGER, serial_number TEXT)")
# con_t.execute("CREATE TABLE vwp_devices (vwp_device_id INTEGER PRIMARY KEY, datalogger_id INTEGER, device_name TEXT, channel INTEGER)")
# con_t.execute("CREATE TABLE readings (vwp_device_id INTEGER, reading_date DATE, reading_value INTEGER, is_exceedence BOOL, PRIMARY KEY (vwp_device_id, reading_date))")

class PlotGraphData(CodedTool):
    def __init__(self):
        super().__init__()
    
    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        data = sly_data["graphing_data"]
        matplotlib.use('Agg')
        print(data)
        fig, ax = plt.subplots(figsize=(5.4, 2), layout='constrained')
        for key in data:
            data_np = np.array(data[key])
            time , y = data_np.transpose()
            # convert times to datetime
            time = [date.fromisoformat(t) for t in time]
            y = [int(t) for t in y]
            ax.plot(time, y, label=key)
        ax.legend()

        fig.set_size_inches(18.5, 10.5)        

        fig_name = str(uuid.uuid4()) + ".png"
        
        path = f"/Users/2279890/Documents/GitHub/neuro-san-studio/coded_tools/tailings_system/{fig_name}"

        fig.savefig(path, dpi=100)

        return {
            "message": f"figure stored at path {path}"
        }
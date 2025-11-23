from neuro_san.interfaces.coded_tool import CodedTool
import duckdb
from typing import Any
from typing import Dict
from typing import Union

# con_wo.execute("CREATE TABLE inventory (item_id INTEGER PRIMARY KEY, item_type TEXT, quantity INTEGER, location TEXT)")

class GetInventory(CodedTool):
    def __init__(self):
        self.work_order_db = duckdb.connect("/Users/2279890/Documents/GitHub/neuro-san-studio/coded_tools/tailings_system/work_orders.db")
        super().__init__()
    
    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        # get site_name from args
        site = args["site"]
        device_type = args["device_type"]

        # Select stock level for site and device type
        self.work_order_db.execute(f"SELECT quantity FROM inventory WHERE location = ? AND item_type = ?", [site, device_type])

        result = self.work_order_db.fetchone()[0]

        print(result)

        # return sites
        return {
            "stock_level": result,
            "minimum_quantity": 2,
            "spare": result - 2
        }
from neuro_san.interfaces.coded_tool import CodedTool
import duckdb
from typing import Any
from typing import Dict
from typing import Union

# con_wo.execute("CREATE TABLE inventory (item_id INTEGER PRIMARY KEY, item_type TEXT, quantity INTEGER, location TEXT)")
# con_wo.execute("CREATE TABLE work_orders (work_order_id INTEGER PRIMARY KEY, date DATE, status TEXT, instructions TEXT)")
# con_wo.execute("CREATE TABLE transfer_requests (transfer_request_id INTEGER PRIMARY KEY, date DATE, item_type TEXT, quantity TEXT, from TEXT, to TEXT)")

class CreateWorkOrder(CodedTool):
    def __init__(self):
        self.work_order_db = duckdb.connect("/Users/2279890/Documents/GitHub/neuro-san-studio/coded_tools/tailings_system/work_orders.db")
        super().__init__()
    
    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        # get details from args
        status = "NEW"
        instructions = args["instructions"]

        # Insert new work order
        self.work_order_db.execute("INSERT INTO work_orders (work_order_id, status, instructions) VALUES (nextval('work_order_sequence'), ?, ?) RETURNING work_order_id", [status, instructions])

        # return workorder id
        return {
            "work_order_id": self.work_order_db.fetchall()
        }
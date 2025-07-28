from neuro_san.interfaces.coded_tool import CodedTool
import duckdb
from typing import Any
from typing import Dict
from typing import Union

#con_wo.execute("CREATE TABLE work_orders (work_order_id INTEGER PRIMARY KEY, date DATE, status TEXT, instructions TEXT)")
# # create work_order_sequence
# con_wo.execute("CREATE SEQUENCE work_order_sequence START 1")
# con_wo.execute("CREATE TABLE transfer_requests (transfer_request_id INTEGER PRIMARY KEY, date DATE, item_type TEXT, quantity TEXT, from_site TEXT, to_site TEXT)")
# # create transfer_request_sequence
# con_wo.execute("CREATE SEQUENCE transfer_request_sequence START 1")

class CreateTransferRequest(CodedTool):
    def __init__(self):
        self.work_order_db = duckdb.connect("/Users/2279890/Documents/GitHub/neuro-san-studio/coded_tools/tailings_system/work_orders.db")
        super().__init__()
    
    def invoke(self, args: Dict[str, Any], sly_data: Dict[str, Any]) -> Union[Dict[str, Any], str]:
        # get details from args
        item_type = args["item_type"]
        quantity = args["quantity"]
        from_site = args["from_site"]
        to_site = args["to_site"]

        # Insert new transfer request
        self.work_order_db.execute("INSERT INTO transfer_requests (transfer_request_id, item_type, quantity, from_site, to_site) VALUES (nextval('transfer_request_sequence'), ?, ?, ?, ?) RETURNING transfer_request_id", [item_type, quantity, from_site, to_site])

        # return transfer request id
        return {
            "transfer_request_id": self.work_order_db.fetchall()
        }
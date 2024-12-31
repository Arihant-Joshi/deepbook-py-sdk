import json
import time
import os
import sys

from pysui.sui.sui_pgql.pgql_sync_txn import SuiTransaction
import pysui.sui.sui_pgql.pgql_query as qn

libs_dir = os.path.join(os.getcwd(),"src", "deepbook_sdk_hun43r")
sys.path.insert(0,libs_dir)
import deepbook_client

#digest = "4ucqDZuWieEcFYoBMKX6EeCKm12wR9h6pazA2yRjdouN"
digest = None
#owner = "0x44d3015d3c8252692af5fd3215d9bf2e07e862c8c70b49557b8fa69837820923"
balance_manager_address = "0x41d5ec0637b7d821ee67359cd2b80a7c9231b9221ebd7b37886aa321ae3fdfad"

deepbook_client = deepbook_client.DeepbookClient(env="testnet")

if balance_manager_address is None and digest is None:
    tx: SuiTransaction = SuiTransaction(client=deepbook_client.pysui_client)
    deepbook_client.balance_manager_contract.createAndShareBalanceManager(tx)
    tx_dict = tx.build_and_sign()
    result = tx.client.execute_query_node(
        with_node=qn.ExecuteTransaction(**tx_dict))

    if result.is_ok():
        print("Transaction Successful")
        digest = json.loads(result.result_data.to_json())["digest"]
    else:
        print("Transaction failed")
        print(result.result_string)
    print(f"Balance Manager Creation Digest: {digest}")
    time.sleep(2)

if balance_manager_address is None:
    if not os.path.exists(f"../../output-dumps/{digest}.json"):
        tx: SuiTransaction = SuiTransaction(client=deepbook_client.pysui_client)
        result = tx.client.execute_query_node(
            #with_node=qn.GetObjectsOwnedByAddress(owner=owner))
            with_node=qn.GetTx(digest=digest))
    
        with open(f"../../output-dumps/{digest}.json", "w") as f:
            f.writelines(result.result_data.to_json(indent=2))

    with open(f"../../output-dumps/{digest}.json", "r") as f:
        tx_details = json.load(f)
        created_objects_manifest = tx_details["effects"]["objectChanges"]["nodes"]
        
    for created_object in created_objects_manifest:
        if created_object["created"] == "true":
            continue
        try:
            if created_object["output_state"] is None:
                continue
            object_type = created_object["output_state"]["as_move_content"]["as_object"]["object_type_repr"]["object_type"]
        except KeyError:
            continue

        if "balance_manager::BalanceManager" in object_type:
            balance_manager_address = created_object["address"]
            break

print(f"Using Balance Manager at: {balance_manager_address}")

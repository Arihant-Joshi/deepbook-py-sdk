import json

from pysui.sui.sui_pgql.pgql_sync_txn import SuiTransaction
import pysui.sui.sui_pgql.pgql_query as qn

from deepbook_client import DeepbookClient

def balanceManager_add(client: DeepbookClient, balance_manager_address, balance_manager_key, balance_manager_trading_cap=None, force_update=False):
    if balance_manager_key in client.deepbook_config.balance_managers and not force_update:
        raise ValueError(f"Balance Manager with key {balance_manager_key} already exists")
    client.deepbook_config.balance_managers.update({
        balance_manager_key: {
            "address": balance_manager_address,
            "tradingCap": balance_manager_trading_cap}})

def balanceManager_createAndShare(client: DeepbookClient, balance_manager_key, balance_manager_trading_cap=None, force_update=False):
    if balance_manager_key in client.deepbook_config.balance_managers and not force_update:
        raise ValueError(f"Balance Manager with key {balance_manager_key} already exists")
    
    ## First Create and Share a Balance Manager
    tx: SuiTransaction = SuiTransaction(client=client.pysui_client)
    client.balance_manager_contract.createAndShareBalanceManager(tx)
    tx_dict = tx.build_and_sign()
    result = tx.client.execute_query_node(
        with_node=qn.ExecuteTransaction(**tx_dict))

    if result.is_ok():
        print("Balance Manager Created Successfully")
        digest = json.loads(result.result_data.to_json())["digest"]
        print(f"Transaction Digest: {digest}")
    else:
        print("Transaction failed")
        print(result.result_string)

    ## Now get the address of the created Balance Manager
    result = client.getResultFromDigest(digest, wait=5)
    
    created_objects_manifest = json.loads(result.result_data.to_json())["effects"]["objectChanges"]["nodes"]
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

    balanceManager_add(client, balance_manager_address, balance_manager_key, balance_manager_trading_cap, force_update)

## TRY WITH FFULL DRY RUN
def balanceManager_getBalance(client: DeepbookClient, balance_manager_key, coin):
    tx: SuiTransaction = SuiTransaction(client=client.pysui_client)
    client.balance_manager_contract.checkManagerBalance(tx, balance_manager_key, coin)
    tx_bytestr = tx.build()
    result = tx.client.execute_query_node(
        with_node=qn.ExecuteTransaction(tx_bytestr=tx_bytestr))
    
    if result.is_ok():
        print("Balance Manager Balance Checked Successfully")
        print(result.result_data.to_json(indent=2))
        digest = json.loads(result.result_data.to_json())["digest"]
        print(f"Transaction Digest: {digest}")
    else:
        print("Could not get Balance Manager Balance")
        print(result.result_string)
    
    result = client.getResultFromDigest(digest, wait=5)
    print(result.result_data.to_json(indent=2))
    #created_objects_manifest = json.loads(result.result_data.to_json())["effects"]["objectChanges"]["nodes"]

def balanceManager_deposit(client: DeepbookClient, balance_manager_key: str, coin: str, amount:int):
    tx: SuiTransaction = SuiTransaction(client=client.pysui_client)
    client.balance_manager_contract.depositIntoManager(tx, balance_manager_key, coin, amount)
    tx_dict = tx.build_and_sign()
    result = tx.client.execute_query_node(
        with_node=qn.ExecuteTransaction(**tx_dict))

    if result.is_ok():
        print(f"Deposited {amount} {coin} into Balance Manager {balance_manager_key}")
        digest = json.loads(result.result_data.to_json())["digest"]
        print(f"Transaction Digest: {digest}")
        return True
    else:
        print("Transaction failed")
        print(result.result_string)
        return False

def balanceManager_withdraw(client: DeepbookClient, balance_manager_key: str, coin: str, amount:str):
    pass

## TODO - This should get all balanceManager Objects owned by current address and update the balance_managers dict
def balanceManager_refresh(client):
    pass

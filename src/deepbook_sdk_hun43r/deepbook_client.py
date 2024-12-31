from typing import Dict
import time
import json

from pysui import PysuiConfiguration, SyncGqlClient
from pysui.sui.sui_pgql.pgql_sync_txn import SuiTransaction
import pysui.sui.sui_pgql.pgql_query as qn

from utils import config
from transactions import balanceManager


class DeepbookClient:
    def __init__(self, pysui_client=None, env=None, deepbook_address=None):
        if pysui_client is None:
            cfg = PysuiConfiguration(group_name=PysuiConfiguration.SUI_GQL_RPC_GROUP )
            pysui_client = SyncGqlClient(pysui_config=cfg,write_schema=False)
        self.pysui_client = pysui_client
        self.set_deepbook_config(env)
        self.balance_manager_contract = balanceManager.BalanceManagerContract(self.deepbook_config)


    def set_deepbook_config(self, env=None):
        self.deepbook_config = config.DeepbookConfig(self.pysui_client, env=env)
        

    def getActiveAddress(self):
        return self.pysui_client.config.active_address
    
    def getResultFromDigest(self, digest, wait=5):
        time.sleep(wait)

        tx: SuiTransaction = SuiTransaction(client=self.pysui_client)
        result = tx.client.execute_query_node(
            with_node=qn.GetTx(digest=digest))
        return result

    def bm_add(self, balance_manager_address, balance_manager_key, balance_manager_trading_cap=None, force_update=False):
        if balance_manager_key in self.deepbook_config.balance_managers and not force_update:
            raise ValueError(f"Balance Manager with key {balance_manager_key} already exists")
        self.deepbook_config.balance_managers.update({
            balance_manager_key: {
                "address": balance_manager_address,
                "tradingCap": balance_manager_trading_cap}})
    
    def bm_createAndShare(self, balance_manager_key, balance_manager_trading_cap=None, force_update=False):
        if balance_manager_key in self.deepbook_config.balance_managers and not force_update:
            raise ValueError(f"Balance Manager with key {balance_manager_key} already exists")
        
        ## First Create and Share a Balance Manager
        tx: SuiTransaction = SuiTransaction(client=self.pysui_client)
        self.balance_manager_contract.createAndShareBalanceManager(tx)
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
        result = self.getResultFromDigest(digest, wait=5)
        
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
    
        self.bm_add(balance_manager_address, balance_manager_key, balance_manager_trading_cap, force_update)

    ## TRY WITH FFULL DRY RUN
    def bm_getBalance(self, balance_manager_key, coin):
        tx: SuiTransaction = SuiTransaction(client=self.pysui_client)
        self.balance_manager_contract.checkManagerBalance(tx, balance_manager_key, coin)
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
        
        result = self.getResultFromDigest(digest, wait=5)
        print(result.result_data.to_json(indent=2))
        #created_objects_manifest = json.loads(result.result_data.to_json())["effects"]["objectChanges"]["nodes"]

    def bm_deposit(self, balance_manager_key: str, coin: str, amount:int):
        tx: SuiTransaction = SuiTransaction(client=self.pysui_client)
        self.balance_manager_contract.depositIntoManager(tx, balance_manager_key, coin, amount)
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

    def bm_withdraw(self, balance_manager_key: str, coin: str, amount:str):
        pass

    ## TODO - This should get all balanceManager Objects owned by current address and update the balance_managers dict
    def bm_refresh(self):
        pass


    ##TODO???
    def deepbookContractCall(self):
        txn = SuiTransaction(client=self.pysui_client)
        txn.move_call(self.deepbook_address("DEEP_SUI"), "getPool", [])      

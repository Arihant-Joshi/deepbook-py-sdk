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
        self.deepbook_config: config.DeepbookConfig = config.DeepbookConfig(self.pysui_client, env=env)
        

    def getActiveAddress(self):
        return self.pysui_client.config.active_address
    
    def getResultFromDigest(self, digest, wait=5):
        time.sleep(wait)

        tx: SuiTransaction = SuiTransaction(client=self.pysui_client)
        result = tx.client.execute_query_node(
            with_node=qn.GetTx(digest=digest))
        return result

    ##TODO???
    def deepbookContractCall(self):
        txn = SuiTransaction(client=self.pysui_client)
        txn.move_call(self.deepbook_address("DEEP_SUI"), "getPool", [])      

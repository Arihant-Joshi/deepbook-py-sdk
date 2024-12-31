import json
import time
import os
import sys

from pysui.sui.sui_pgql.pgql_sync_txn import SuiTransaction
import pysui.sui.sui_pgql.pgql_query as qn

libs_dir = os.path.join(os.getcwd(),"src", "deepbook_sdk_hun43r")
sys.path.insert(0,libs_dir)
import deepbook_client
from examples.balance_manager import *

owner = "0x44d3015d3c8252692af5fd3215d9bf2e07e862c8c70b49557b8fa69837820923"
deepbook_client = deepbook_client.DeepbookClient(env="testnet")

#deepbook_client.createAndShareBalanceManager("test-1")
#deepbook_client.createAndShareBalanceManager("test-2")

def initialize_balance_managers():
    balance_managers = {
        'test-1': 
        {
            'address': '0xa6d57d35d2af04bcdf96abdc6b08bf8720fff0627a5772fc81871891cbad78f5', 
            'tradingCap': None
        }, 
        'test-2': 
        {
            'address': '0x6f5b5cff5ba6848b3053525053ae326238947cb4e4d2a6541c7be62c0186f1a1', 
            'tradingCap': None
        }
    }
    for bm in balance_managers:

        balanceManager_add(deepbook_client, balance_managers[bm]['address'], bm, balance_managers[bm]['tradingCap'])

initialize_balance_managers()
balanceManager_createAndShare(deepbook_client, "test-3")

print(f"Using Balance Managers Dict: {deepbook_client.deepbook_config.balance_managers}")

#print("Getting Balance for test-1")
#deepbook_client.bm_getBalance("test-1", "DEEP")
#print("Getting Balance for test-2")
#deepbook_client.bm_getBalance("test-2", "DEEP")

#deepbook_client.bm_deposit("test-1", "SUI", 500000000)

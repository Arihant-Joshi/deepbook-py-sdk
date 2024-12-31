from pysui.sui.sui_pgql.pgql_sync_txn import SuiTransaction
from utils.config import DeepbookConfig
from pysui.sui.sui_txresults.single_tx import SuiCoinBalance

class BalanceManagerContract:
    def __init__(self, config: DeepbookConfig):
        self.config = config

    def createAndShareBalanceManager(self, tx: SuiTransaction):
        manager = tx.move_call(target=f"{self.config.DEEPBOOK_PACKAGE_ID}::balance_manager::new", 
                               arguments=[], 
                               type_arguments=[])

        tx.move_call(target='0x2::transfer::public_share_object', 
                     arguments=[manager], 
                     type_arguments=[f"{self.config.DEEPBOOK_PACKAGE_ID}::balance_manager::BalanceManager"])
    
    def checkManagerBalance(self, tx: SuiTransaction, managerKey: str, coin: str):
        if managerKey not in self.config.balance_managers:
            raise ValueError(f"Balance Manager with key {managerKey} does not exist")
        if coin not in self.config.COINS:
            raise ValueError(f"Coin with key {coin} does not exist")
        balance_manager_address = self.config.balance_managers[managerKey]["address"]
        coin_type = self.config.COINS[coin]["type"]
        tx.move_call(target=f"{self.config.DEEPBOOK_PACKAGE_ID}::balance_manager::balance", 
                     arguments=[balance_manager_address], 
                     type_arguments=[coin_type])
    
    #Get All Coins, Merge All, Split whats needed
    def depositIntoManager(self, tx: SuiTransaction, managerKey: str, coin: str, amount: int):
        if managerKey not in self.config.balance_managers:
            raise ValueError(f"Balance Manager with key {managerKey} does not exist")
        if coin not in self.config.COINS:
            raise ValueError(f"Coin with key {coin} does not exist")
        balance_manager_address = self.config.balance_managers[managerKey]["address"]
        coin_type = self.config.COINS[coin]["type"]
        deposit = SuiCoinBalance(coin_type, amount, str(amount))

        print(type(balance_manager_address))
        print(balance_manager_address.object_owner)

        tx.move_call(target=f"{self.config.DEEPBOOK_PACKAGE_ID}::balance_manager::deposit", 
                     arguments=[balance_manager_address,deposit], 
                     type_arguments=[coin_type])


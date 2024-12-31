import re
from typing import Dict

from pysui import SyncGqlClient

from utils import constants

class DeepbookConfig:
    def __init__(self, client: SyncGqlClient, env=None, balance_managers: Dict[str, dict]={}):
        self.client = client
        
        if env is None:
            if re.match(constants.suiURL_regex["testnet"], self.client.config.url):
                env = "testnet"
            elif re.match(constants.suiURL_regex["mainnet"], self.client.config.url):
                env = "mainnet"
            else:
                errorString = f"""No DeepbookV3 Address Passed to constructor, and PySUI Client's URL did not match any known URLs.
                Recognized URLs should match regex: ^(http[s]{0,1}://){0,1}(testnet|mainnet).suiblockchain.com/*$
                Given URL: {self.client.config.url}
                """
                raise ValueError(errorString)
        
        self.DEEPBOOK_PACKAGE_ID = constants.deepbookPackageIds[env]["DEEPBOOK_PACKAGE_ID"]
        self.REGISTRY_ID = constants.deepbookPackageIds[env]["REGISTRY_ID"]
        self.DEEP_TREASURY_ID = constants.deepbookPackageIds[env]["DEEP_TREASURY_ID"]
        self.COINS = constants.coins[env]

        self.balance_managers: Dict[str, dict] = balance_managers

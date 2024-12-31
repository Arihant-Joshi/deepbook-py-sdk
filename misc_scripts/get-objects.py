from pysui.sui.sui_client import SuiClient
from pysui.sui.sui_types import SuiTransactionBuilder, SuiModuleType

def create_balance_manager():
    try:
        # Initialize the Sui client with the default configuration
        client = SuiClient.default()

        # Define the Balance Manager module type
        module_type = SuiModuleType("0xcbf4748a965d469ea3a36cf0ccc5743b96c2d0ae6dee0762ed3eca65fac07f7e::balance_manager::BalanceManager")  # Replace with the actual module address

        # Create a transaction to initialize the Balance Manager
        tx_builder = SuiTransactionBuilder(client)
        tx_builder.create(module_type)

        # Sign and execute the transaction
        response = client.sign_and_submit_transaction(tx_builder.build())
        
        # Check response
        if response.is_ok():
            print(f"Balance Manager created successfully. Tx Digest: {response.result}")
        else:
            print(f"Failed to create Balance Manager: {response.error_message}")
    except Exception as ex:
        print(f"An error occurred: {ex}")

# Run the function
create_balance_manager()

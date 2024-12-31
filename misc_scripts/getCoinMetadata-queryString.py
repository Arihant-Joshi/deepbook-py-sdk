
from pysui import PysuiConfiguration, SyncGqlClient


def main(client: SyncGqlClient):
    query_string = """
    {
        owner(address: "0x44d3015d3c8252692af5fd3215d9bf2e07e862c8c70b49557b8fa69837820923") {
            address
            balance {
                totalBalance
                failthis
            }
        }
    }
    """
    """
    objects {
                address
                owner
            }
    """
    qres = client.execute_query_string(
        string=query_string
    )

    # 1. QueryNode results are mapped to dataclasses/dataclasses-json
    print(qres.result_data)


    # 2. Or get the data through handle_result
    # print(handle_result(qres).to_json(indent=2))


if __name__ == "__main__":
    # Initialize synchronous client
    cfg = PysuiConfiguration(group_name=PysuiConfiguration.SUI_GQL_RPC_GROUP )
    client_init = SyncGqlClient(pysui_config=cfg,write_schema=False)

    main(client_init)

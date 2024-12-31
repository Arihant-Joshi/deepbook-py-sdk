from pysui import PysuiConfiguration, handle_result, SyncGqlClient

import pysui.sui.sui_pgql.pgql_query as qn



def main(client: SyncGqlClient):

    """Fetch 0x2::sui::SUI (default) for owner."""

    # GetCoins defaults to '0x2::sui::SUI' coin type so great for owners gas listing

    q_docnode = qn.GetCoins(
            owner="0x44d3015d3c8252692af5fd3215d9bf2e07e862c8c70b49557b8fa69837820923"
        ).as_document_node()
    
    qres = client.execute_document_node(q_docnode)

    # 1. QueryNode results are mapped to dataclasses/dataclasses-json

    print(qres.result_data.to_json(indent=2))


    # 2. Or get the data through handle_result

    # print(handle_result(qres).to_json(indent=2))


if __name__ == "__main__":

    # Initialize synchronous client

    cfg = PysuiConfiguration(group_name=PysuiConfiguration.SUI_GQL_RPC_GROUP )

    client_init = SyncGqlClient(pysui_config=cfg,write_schema=False)

    main(client_init)

from pysui import PysuiConfiguration, SyncGqlClient


def main():

    """Dump Sui GraphQL Schema."""

    # Initialize synchronous client
    cfg = PysuiConfiguration(group_name=PysuiConfiguration.SUI_GQL_RPC_GROUP )
    
    client_init = SyncGqlClient(pysui_config=cfg,write_schema=True)
    print(f"Schema dumped to: {client_init.base_schema_version}.graqhql`")


if __name__ == "__main__":
    main()

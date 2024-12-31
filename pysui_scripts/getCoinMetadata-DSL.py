from typing import Optional, Callable, Union, Any
from gql.dsl import DSLQuery, dsl_gql, DSLSchema
from graphql import DocumentNode

from pysui.sui.sui_pgql.pgql_clients import PGQL_QueryNode
import pysui.sui.sui_pgql.pgql_types as pgql_type

from pysui import PysuiConfiguration, handle_result, SyncGqlClient
import pysui.sui.sui_pgql.pgql_query as qn

class GetCoinMetaData(PGQL_QueryNode):
    """GetCoinMetaData returns meta data for a specific `coin_type`."""

    def __init__(self, *, coin_type: Optional[str] = "0x2::sui::SUI") -> None:
        """QueryNode initializer.

        :param coin_type: The specific coin type string, defaults to "0x2::sui::SUI"
        :type coin_type: str, optional
        """
        self.coin_type = coin_type

    def as_document_node(self, schema: DSLSchema) -> DocumentNode:
        """Build the DocumentNode."""
        qres = schema.Query.coinMetadata(coinType=self.coin_type).select(
            schema.CoinMetadata.decimals,
            schema.CoinMetadata.name,
            schema.CoinMetadata.symbol,
            schema.CoinMetadata.description,
            schema.CoinMetadata.iconUrl,
            schema.CoinMetadata.supply,
            object_data=schema.CoinMetadata.asMoveObject.select(
                schema.MoveObject.asObject.select(meta_object_id=schema.Object.location)
            ),
        )
        return dsl_gql(DSLQuery(qres))

    @staticmethod
    def encode_fn() -> Callable[[dict], pgql_type.SuiCoinMetadataGQL]:
        """Return the encoding function to create a SuiCoinMetadataGQL dataclass."""
        return pgql_type.SuiCoinMetadataGQL.from_query

cfg = PysuiConfiguration(group_name=PysuiConfiguration.SUI_GQL_RPC_GROUP )
client_init = SyncGqlClient(pysui_config=cfg,write_schema=False)

obj_getCoinMetaData = GetCoinMetaData()
obj_getCoinMetaData.as_document_node()

#qres = client_init.execute_document_node(obj_getCoinMetaData.as_document_node())

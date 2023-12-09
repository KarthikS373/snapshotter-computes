import time
from typing import Dict
from typing import Optional
from typing import Union

from redis import asyncio as aioredis

from .utils.core import get_pair_reserves
from .utils.models.message_models import EpochBaseSnapshot
from .utils.models.message_models import UniswapPairTotalReservesSnapshot
from snapshotter.utils.callback_helpers import GenericProcessorSnapshot
from snapshotter.utils.default_logger import logger
from snapshotter.utils.models.message_models import PowerloomSnapshotProcessMessage
from snapshotter.utils.rpc import RpcHelper


class FanatixRoyalities(GenericProcessorSnapshot):
    transformation_lambdas = None

    def __init__(self) -> None:
        self.transformation_lambdas = []
        self._logger = logger.bind(module='FanatixRoyalities')

    async def compute(
        self,
        epoch: PowerloomSnapshotProcessMessage,
        redis_conn: aioredis.Redis,
        rpc_helper: RpcHelper,

    ) -> Optional[Dict[str, Union[int, float]]]:

        min_chain_height = epoch.begin
        max_chain_height = epoch.end

        data_source_contract_address = epoch.data_source
        contract = self.web3.eth.contract(
            address=data_source_contract_address, abi=self.contract_abi)

        tier_max_supply = {}
        current_supply = {}
        balance_of_tokens = {}
        owned_tokens = {}
        token_uri = contract.functions.tokenURI().call()
        token_owner = contract.functions.tokenOwner().call()
        mintable_tier = {}

        for tier_id in range(1, N):  # Replace N with the actual number of tiers
            tier_max_supply[str(tier_id)] = contract.functions.tierMaxSupply(
                tier_id).call()
            current_supply[str(tier_id)] = contract.functions.currentSupply(
                tier_id).call()
            mintable_tier[str(tier_id)] = contract.functions.mintableTier(
                tier_id).call()
            # Add logic to extract balanceOfTokens and ownedTokens

        # Construct the snapshot
        fanatix_contract_snapshot = FanatixContractSnapshot(
            contract=data_source_contract_address,
            chainHeightRange=EpochBaseSnapshot(
                begin=min_chain_height, end=max_chain_height,
            ),
            timestamp=int(time.time()),
            tierMaxSupply=tier_max_supply,
            currentSupply=current_supply,
            balanceOfTokens=balance_of_tokens,
            ownedTokens=owned_tokens,
            tokenURI=token_uri,
            tokenOwner=token_owner,
            mintableTier=mintable_tier
        )

        self._logger.debug(
            f'Contract data for {data_source_contract_address} processed at {time.time()}')

        return fanatix_contract_snapshot

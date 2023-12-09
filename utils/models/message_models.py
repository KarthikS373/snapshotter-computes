from typing import Dict
from typing import List

from pydantic import BaseModel

from snapshotter.utils.models.message_models import AggregateBase


class EpochBaseSnapshot(BaseModel):
    begin: int
    end: int


class SnapshotBase(BaseModel):
    contract: str
    chainHeightRange: EpochBaseSnapshot
    timestamp: int


class FanatixContractSnapshot(SnapshotBase):
    tierMaxSupply: Dict[str, int]  # tierId to max supply
    currentSupply: Dict[str, int]  # tierId to current supply
    balanceOfTokens: Dict[str, Dict[str, int]]  # tierId to owner to balance
    # tierId to owner to list of tokens
    ownedTokens: Dict[str, Dict[str, List[int]]]
    tokenURI: str
    tokenOwner: str
    mintableTier: Dict[str, bool]  # tierId to mintability


class FanatixTierSnapshot(BaseModel):
    tierMaxSupply: Dict[str, int]  # tierId to max supply
    currentSupply: Dict[str, int]  # tierId to current supply


class FanatixOwnershipSnapshot(SnapshotBase):
    balanceOfTokens: Dict[str, Dict[str, int]]  # tierId to owner to balance
    # tierId to owner to list of tokens
    ownedTokens: Dict[str, Dict[str, List[int]]]


class FanatixRoyaltiesSnapshot(SnapshotBase):
    royalties: Dict[str, float]  # tokenId or ownerId to royalty amount


class logsTradeModel(BaseModel):
    logs: List
    trades: Dict[str, float]


class UniswapTradeEvents(BaseModel):
    Swap: logsTradeModel
    Mint: logsTradeModel
    Burn: logsTradeModel
    Trades: Dict[str, float]


class UniswapTradesSnapshot(SnapshotBase):
    totalTrade: float  # in USD
    totalFee: float  # in USD
    token0TradeVolume: float  # in token native decimals supply
    token1TradeVolume: float  # in token native decimals supply
    token0TradeVolumeUSD: float
    token1TradeVolumeUSD: float
    events: UniswapTradeEvents


class UniswapTradesAggregateSnapshot(AggregateBase):
    totalTrade: float = 0  # in USD
    totalFee: float = 0  # in USD
    token0TradeVolume: float = 0  # in token native decimals supply
    token1TradeVolume: float = 0  # in token native decimals supply
    token0TradeVolumeUSD: float = 0
    token1TradeVolumeUSD: float = 0
    complete: bool = True


class UniswapTopTokenSnapshot(BaseModel):
    name: str
    symbol: str
    decimals: int
    address: str
    price: float
    priceChange24h: float
    volume24h: float
    liquidity: float


class UniswapTopTokensSnapshot(AggregateBase):
    tokens: List[UniswapTopTokenSnapshot] = []
    complete: bool = True


class UniswapTopPair24hSnapshot(BaseModel):
    name: str
    address: str
    liquidity: float
    volume24h: float
    fee24h: float


class UniswapTopPairs24hSnapshot(AggregateBase):
    pairs: List[UniswapTopPair24hSnapshot] = []
    complete: bool = True


class UniswapTopPair7dSnapshot(BaseModel):
    name: str
    address: str
    volume7d: float
    fee7d: float


class UniswapTopPairs7dSnapshot(AggregateBase):
    pairs: List[UniswapTopPair7dSnapshot] = []
    complete: bool = True


class UniswapStatsSnapshot(AggregateBase):
    volume24h: float = 0
    tvl: float = 0
    fee24h: float = 0
    volumeChange24h: float = 0
    tvlChange24h: float = 0
    feeChange24h: float = 0
    complete: bool = True

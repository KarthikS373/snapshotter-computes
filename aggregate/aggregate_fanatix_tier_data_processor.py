class AggregateFanatixTierDataProcessor:
    def __init__(self, web3: Web3, contract_address: str, contract_abi: list):
        self.contract = web3.eth.contract(
            address=contract_address, abi=contract_abi)

    def aggregate_tier_data(self):
        tier_data = {}
        for tier_id in range(1, 4):
            max_supply = self.contract.functions.tierMaxSupply(tier_id).call()
            current_supply = self.contract.functions.currentSupply(
                tier_id).call()
            tier_data[f"tier_{tier_id}"] = {
                "max_supply": max_supply,
                "current_supply": current_supply
            }

        return tier_data

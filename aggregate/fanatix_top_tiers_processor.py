class FanatixTopTiersProcessor:
    def __init__(self, web3: Web3, contract_address: str, contract_abi: list):
        self.contract = web3.eth.contract(
            address=contract_address, abi=contract_abi)

    def identify_top_tiers(self):
        top_tiers = {}

        for tier_id in range(1, 4):
            current_supply = self.contract.functions.currentSupply(
                tier_id).call()
            top_tiers[f"tier_{tier_id}"] = {"current_supply": current_supply}

        # Sorting tiers based on current supply
        sorted_tiers = dict(sorted(
            top_tiers.items(), key=lambda item: item[1]['current_supply'], reverse=True))

        return sorted_tiers

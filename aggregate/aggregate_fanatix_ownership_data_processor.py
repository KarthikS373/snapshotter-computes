class AggregateFanatixOwnershipDataProcessor:
    def __init__(self, web3: Web3, contract_address: str, contract_abi: list):
        self.contract = web3.eth.contract(
            address=contract_address, abi=contract_abi)

    def aggregate_ownership_data(self):
        ownership_data = {}

        # Loop through each tier
        for tier_id in range(1, 4):
            ownership_data[f"tier_{tier_id}"] = {}

            # Fetch all owner IDs for the tier
            owner_ids = self.contract.functions._OWNID_().call()
            for owner_id in owner_ids:
                balance = self.contract.functions.tierBalanceOf(
                    tier_id, owner_id).call()
                ownership_data[f"tier_{tier_id}"][owner_id] = balance

        return ownership_data

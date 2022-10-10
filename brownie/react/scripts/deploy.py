from brownie import SolidityStorage, VyperStorage, accounts, network,config
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy

gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)
gas_price(gas_strategy)

def main():
    # requires brownie account to have been created
    if network.show_active()=='development':
        # add these accounts to metamask by importing private key
        owner = accounts[0]
        simple_storage = SolidityStorage.deploy({'from':accounts[0],
                                'gas_price':gas_strategy})
        print(simple_storage.get())
        transaction = simple_storage.set(15,{'from':accounts[0]})
        # VyperStorage.deploy({'from':accounts[0],
        #                     'gas_price':gas_strategy})
        transaction.wait(1)
        print(simple_storage.get())
        
    elif network.show_active() == 'kovan':
        # add these accounts to metamask by importing private key
        owner = accounts.load("main")
        SolidityStorage.deploy({'from':owner})
        # VyperStorage.deploy({'from':owner})
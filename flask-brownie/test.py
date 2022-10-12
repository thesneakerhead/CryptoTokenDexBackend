from brownie import *
p = project.load('./brownie/react',name='ReactProject')
p.load_config()
network.connect('development')
from brownie.network import accounts
from brownie.network import gas_price
from brownie.network.gas.strategies import LinearScalingStrategy
gas_strategy = LinearScalingStrategy("60 gwei", "70 gwei", 1.1)
gas_price(gas_strategy)
p.SolidityStorage.deploy( {'from':accounts[0], 'gas_price':gas_price('60 gwei')})


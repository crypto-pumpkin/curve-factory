from brownie import (
    DepositZapBTC,
    DepositZapUSD,
    Factory,
    MetaImplementationBTC,
    MetaImplementationUSD,
    OwnerProxy,
    accounts
)
from brownie.network.gas.strategies import GasNowScalingStrategy

# modify me prior to deployment on mainnet!
DEPLOYER = accounts.at("0xDd79dc5B781B14FF091686961ADc5d47e434f4B0", force=True)

gas_price = GasNowScalingStrategy("slow", "fast")


OWNER_ADMIN = "0x49B8a0893B83A171D7d461198b69A0b1bb4dd0Ed"
PARAM_ADMIN = "0x49B8a0893B83A171D7d461198b69A0b1bb4dd0Ed"
EMERGENCY_ADMIN = "0x16AB959f2225bcD892069193d2120Ac6E0940e3c"

BASE_3POOL = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
BASE_SBTC = "0x7fC77b5c7614E1533320Ea6DDc2Eb61fa00A9714"

FEE_RECEIVER_USD = "0x6BeF09F99Bf6d92d6486889Bdd8A374af151461D"
FEE_RECEIVER_BTC = "0x6BeF09F99Bf6d92d6486889Bdd8A374af151461D"


def main(deployer=DEPLOYER):
    factory = Factory.deploy({'from': deployer})

    implementation_usd = MetaImplementationUSD.deploy({'from': deployer, 'gas_price': gas_price})
    factory.add_base_pool(
        BASE_3POOL,
        implementation_usd,
        FEE_RECEIVER_USD,
        {'from': deployer, 'gas_price': gas_price}
    )

    implementation_btc = MetaImplementationBTC.deploy({'from': deployer, 'gas_price': gas_price})
    factory.add_base_pool(
        BASE_SBTC,
        implementation_btc,
        FEE_RECEIVER_BTC,
        {'from': deployer, 'gas_price': gas_price}
    )

    proxy = OwnerProxy.deploy(
        OWNER_ADMIN,
        PARAM_ADMIN,
        EMERGENCY_ADMIN,
        {'from': deployer, 'gas_price': gas_price}
    )

    factory.commit_transfer_ownership(proxy, {'from': deployer, 'gas_price': gas_price})
    proxy.accept_transfer_ownership(factory, {'from': deployer, 'gas_price': gas_price})

    DepositZapUSD.deploy({'from': deployer, 'gas_price': gas_price})
    DepositZapBTC.deploy({'from': deployer, 'gas_price': gas_price})

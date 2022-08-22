from solana.publickey import PublicKey
from .program_id import PROGRAM_ID

class Seeds:
    MARKET_VARS_SEED = b'market-vars'
    ORDER_VAULT_SEED = b'order-vault-account'
    ORDER_VAULT_AUTH_SEED = b'order-vault-auth'
    REGISTERED_CURRENCY_SEED = b'registered-currency'
    OPEN_ORDERS_COUNTER = b'open-orders-counter'

def getMarketVarsAccount():
    """
    Returns the public key and bump seed for the market variables account

    :return:
    """
    return PublicKey.find_program_address(
        [
            Seeds.MARKET_VARS_SEED
         ],
        PROGRAM_ID
    )

def getOrderVaultAccount(
        orderInitializer: PublicKey,
        tokenMint: PublicKey):
    """
    Returns the public key and bump seed for an order escrow account

    :param orderInitializer:
    :param tokenMint:
    :return:
    """
    return PublicKey.find_program_address(
        [
            Seeds.ORDER_VAULT_SEED,
            bytes(orderInitializer),
            bytes(tokenMint)
         ],
        PROGRAM_ID
    )

def getOrderVaultAuthAccount(
        playerPubkey: PublicKey):
    """
    Returns the public key and bump seed for an order escrow authority.

    :param playerPubkey: Pubkey of order initializer
    :return:
    """
    return PublicKey.find_program_address(
        [
            Seeds.ORDER_VAULT_AUTH_SEED,
            bytes(playerPubkey)
        ],
        PROGRAM_ID
    )

def getRegisteredCurrencyAccount(
        currencyMint: PublicKey):
    """
    Returns the public key and bump seed for a registered currency account

    :param currencyMint: Mint address for registered currency
    :return:
    """
    return PublicKey.find_program_address(
        [
            Seeds.REGISTERED_CURRENCY_SEED,
            bytes(currencyMint)
        ],
        PROGRAM_ID
    )

def getOpenOrdersCounterAccount(
        playerPubkey: PublicKey,
        depositMint: PublicKey):
    """
    Orders counter

    :param playerPubkey:
    :param depositMint:
    :return:
    """
    return PublicKey.find_program_address(
        [
            Seeds.OPEN_ORDERS_COUNTER,
            bytes(playerPubkey),
            bytes(depositMint)
        ],
        PROGRAM_ID
    )


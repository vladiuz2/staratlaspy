from solana.publickey import PublicKey
from .program_id import PROGRAM_ID

class Seeds:
    FACTION_PREFIX = b'FACTION_ENLISTMENT'

def getPlayerFactionAccount(
    playerPublicKey: PublicKey):
    """
    Returns player's faction account and bump

    :param playerPublicKey: the player's pubkey (wallet)
    :return:
    """
    return PublicKey.find_program_address(
        [
            Seeds.FACTION_PREFIX,
            bytes(playerPublicKey)
         ],
        PROGRAM_ID
    )

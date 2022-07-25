import typing
from anchorpy.error import ProgramError


class InvalidDestinationAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6000, "Invalid Destination Token Account")

    code = 6000
    name = "InvalidDestinationAccount"
    msg = "Invalid Destination Token Account"


class InvalidInstruction(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "Invalid instruction.")

    code = 6001
    name = "InvalidInstruction"
    msg = "Invalid instruction."


class InvalidMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "Invalid SPL Token mint")

    code = 6002
    name = "InvalidMint"
    msg = "Invalid SPL Token mint"


class InvalidOfferAccountOwner(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, "Invalid Offer Account Owner")

    code = 6003
    name = "InvalidOfferAccountOwner"
    msg = "Invalid Offer Account Owner"


class InvalidTokenAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "Invalid SPL Token account")

    code = 6004
    name = "InvalidTokenAccount"
    msg = "Invalid SPL Token account"


class NumericalOverflowError(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, "Numerical overflow error")

    code = 6005
    name = "NumericalOverflowError"
    msg = "Numerical overflow error"


class InvalidUpdateAuthorityAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, "Invalid Update Authority account")

    code = 6006
    name = "InvalidUpdateAuthorityAccount"
    msg = "Invalid Update Authority account"


class InvalidOrderVaultAuthorityAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, "Invalid Order Vault Authority account")

    code = 6007
    name = "InvalidOrderVaultAuthorityAccount"
    msg = "Invalid Order Vault Authority account"


class UninitializedTokenAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, "Uninitialized Token Account")

    code = 6008
    name = "UninitializedTokenAccount"
    msg = "Uninitialized Token Account"


class InsufficientBalance(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, "Insufficient Balance")

    code = 6009
    name = "InsufficientBalance"
    msg = "Insufficient Balance"


class InvalidOrderDuration(ProgramError):
    def __init__(self) -> None:
        super().__init__(6010, "Invalid Order Duration")

    code = 6010
    name = "InvalidOrderDuration"
    msg = "Invalid Order Duration"


class InvalidOriginationQty(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, "Origination quantity must be greater than 0")

    code = 6011
    name = "InvalidOriginationQty"
    msg = "Origination quantity must be greater than 0"


class InsufficientOrderQty(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, "Insufficient Order Quantity Remaining")

    code = 6012
    name = "InsufficientOrderQty"
    msg = "Insufficient Order Quantity Remaining"


class InvalidRoyalty(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, "Invalid Royalty Value")

    code = 6013
    name = "InvalidRoyalty"
    msg = "Invalid Royalty Value"


class InvalidCounter(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, "Invalid Open Order Counter")

    code = 6014
    name = "InvalidCounter"
    msg = "Invalid Open Order Counter"


class MintDecimalError(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, "Mint must be zero decimal")

    code = 6015
    name = "MintDecimalError"
    msg = "Mint must be zero decimal"


class InvalidOrderAccountError(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, "Order Account does not match provided account")

    code = 6016
    name = "InvalidOrderAccountError"
    msg = "Order Account does not match provided account"


class InvalidRoyaltyTier(ProgramError):
    def __init__(self) -> None:
        super().__init__(6017, "No royalty tier exists with provided stake amount")

    code = 6017
    name = "InvalidRoyaltyTier"
    msg = "No royalty tier exists with provided stake amount"


class RoyaltyTierLength(ProgramError):
    def __init__(self) -> None:
        super().__init__(6018, "Royalty Tier vector cannot hold any additional tiers")

    code = 6018
    name = "RoyaltyTierLength"
    msg = "Royalty Tier vector cannot hold any additional tiers"


CustomError = typing.Union[
    InvalidDestinationAccount,
    InvalidInstruction,
    InvalidMint,
    InvalidOfferAccountOwner,
    InvalidTokenAccount,
    NumericalOverflowError,
    InvalidUpdateAuthorityAccount,
    InvalidOrderVaultAuthorityAccount,
    UninitializedTokenAccount,
    InsufficientBalance,
    InvalidOrderDuration,
    InvalidOriginationQty,
    InsufficientOrderQty,
    InvalidRoyalty,
    InvalidCounter,
    MintDecimalError,
    InvalidOrderAccountError,
    InvalidRoyaltyTier,
    RoyaltyTierLength,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: InvalidDestinationAccount(),
    6001: InvalidInstruction(),
    6002: InvalidMint(),
    6003: InvalidOfferAccountOwner(),
    6004: InvalidTokenAccount(),
    6005: NumericalOverflowError(),
    6006: InvalidUpdateAuthorityAccount(),
    6007: InvalidOrderVaultAuthorityAccount(),
    6008: UninitializedTokenAccount(),
    6009: InsufficientBalance(),
    6010: InvalidOrderDuration(),
    6011: InvalidOriginationQty(),
    6012: InsufficientOrderQty(),
    6013: InvalidRoyalty(),
    6014: InvalidCounter(),
    6015: MintDecimalError(),
    6016: InvalidOrderAccountError(),
    6017: InvalidRoyaltyTier(),
    6018: RoyaltyTierLength(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err

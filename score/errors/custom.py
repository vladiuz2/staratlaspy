import typing
from anchorpy.error import ProgramError


class ScorevarsNotInitialized(ProgramError):
    def __init__(self) -> None:
        super().__init__(300, "Scorevars auth is not initialized")

    code = 300
    name = "ScorevarsNotInitialized"
    msg = "Scorevars auth is not initialized"


class ScorevarsAuthInvalid(ProgramError):
    def __init__(self) -> None:
        super().__init__(301, "Scorevars auth invalid")

    code = 301
    name = "ScorevarsAuthInvalid"
    msg = "Scorevars auth invalid"


class FactionTypeError(ProgramError):
    def __init__(self) -> None:
        super().__init__(302, "Faction ID must be 0, 1, or 2.")

    code = 302
    name = "FactionTypeError"
    msg = "Faction ID must be 0, 1, or 2."


class InvalidShipError(ProgramError):
    def __init__(self) -> None:
        super().__init__(303, "Invalid Ship Mint")

    code = 303
    name = "InvalidShipError"
    msg = "Invalid Ship Mint"


class InvalidResourceError(ProgramError):
    def __init__(self) -> None:
        super().__init__(304, "Invalid Resource Mint")

    code = 304
    name = "InvalidResourceError"
    msg = "Invalid Resource Mint"


class ZeroResourceError(ProgramError):
    def __init__(self) -> None:
        super().__init__(305, "Resource Quantity must be >0.")

    code = 305
    name = "ZeroResourceError"
    msg = "Resource Quantity must be >0."


class ZeroShipError(ProgramError):
    def __init__(self) -> None:
        super().__init__(306, "Ship Quantity must be >0.")

    code = 306
    name = "ZeroShipError"
    msg = "Ship Quantity must be >0."


class NumericalOverflowError(ProgramError):
    def __init__(self) -> None:
        super().__init__(307, "Numerical overflow error")

    code = 307
    name = "NumericalOverflowError"
    msg = "Numerical overflow error"


class ResourceAmountTooSmall(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            308, "Resource Amount Too Small, would add 0 seconds to capacity"
        )

    code = 308
    name = "ResourceAmountTooSmall"
    msg = "Resource Amount Too Small, would add 0 seconds to capacity"


class InvalidScoreVarsAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            309, "Invalid ScoreVars account for ship Staking Account given"
        )

    code = 309
    name = "InvalidScoreVarsAccount"
    msg = "Invalid ScoreVars account for ship Staking Account given"


class InvalidResourceWithdraw(ProgramError):
    def __init__(self) -> None:
        super().__init__(310, "Invalid Resource Withdraw, nothing to withdraw")

    code = 310
    name = "InvalidResourceWithdraw"
    msg = "Invalid Resource Withdraw, nothing to withdraw"


class InvalidShipStakingOwner(ProgramError):
    def __init__(self) -> None:
        super().__init__(311, "Invalid Ship Staking Owner")

    code = 311
    name = "InvalidShipStakingOwner"
    msg = "Invalid Ship Staking Owner"


class InvalidShipWithdraw(ProgramError):
    def __init__(self) -> None:
        super().__init__(312, "Invalid Ship Withdraw")

    code = 312
    name = "InvalidShipWithdraw"
    msg = "Invalid Ship Withdraw"


class NotEnoughToolkits(ProgramError):
    def __init__(self) -> None:
        super().__init__(313, "Not enough toolkits for Ship Withdraw")

    code = 313
    name = "NotEnoughToolkits"
    msg = "Not enough toolkits for Ship Withdraw"


class EscrowAccountNotZero(ProgramError):
    def __init__(self) -> None:
        super().__init__(314, "Escrow account must be 0 to close accounts")

    code = 314
    name = "EscrowAccountNotZero"
    msg = "Escrow account must be 0 to close accounts"


class IncorrectTokenAccountOwner(ProgramError):
    def __init__(self) -> None:
        super().__init__(315, "Token account does not have correct owner!")

    code = 315
    name = "IncorrectTokenAccountOwner"
    msg = "Token account does not have correct owner!"


class UninitializedTokenAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(316, "Token or Mint Account is not initialized!")

    code = 316
    name = "UninitializedTokenAccount"
    msg = "Token or Mint Account is not initialized!"


class IncorrectTokenAccountMint(ProgramError):
    def __init__(self) -> None:
        super().__init__(317, "Token or Mint Account mint is not correct!")

    code = 317
    name = "IncorrectTokenAccountMint"
    msg = "Token or Mint Account mint is not correct!"


CustomError = typing.Union[
    ScorevarsNotInitialized,
    ScorevarsAuthInvalid,
    FactionTypeError,
    InvalidShipError,
    InvalidResourceError,
    ZeroResourceError,
    ZeroShipError,
    NumericalOverflowError,
    ResourceAmountTooSmall,
    InvalidScoreVarsAccount,
    InvalidResourceWithdraw,
    InvalidShipStakingOwner,
    InvalidShipWithdraw,
    NotEnoughToolkits,
    EscrowAccountNotZero,
    IncorrectTokenAccountOwner,
    UninitializedTokenAccount,
    IncorrectTokenAccountMint,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    300: ScorevarsNotInitialized(),
    301: ScorevarsAuthInvalid(),
    302: FactionTypeError(),
    303: InvalidShipError(),
    304: InvalidResourceError(),
    305: ZeroResourceError(),
    306: ZeroShipError(),
    307: NumericalOverflowError(),
    308: ResourceAmountTooSmall(),
    309: InvalidScoreVarsAccount(),
    310: InvalidResourceWithdraw(),
    311: InvalidShipStakingOwner(),
    312: InvalidShipWithdraw(),
    313: NotEnoughToolkits(),
    314: EscrowAccountNotZero(),
    315: IncorrectTokenAccountOwner(),
    316: UninitializedTokenAccount(),
    317: IncorrectTokenAccountMint(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err

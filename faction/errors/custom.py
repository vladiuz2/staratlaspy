import typing
from anchorpy.error import ProgramError


class FactionTypeError(ProgramError):
    def __init__(self) -> None:
        super().__init__(300, "Faction ID must be 0, 1, or 2.")

    code = 300
    name = "FactionTypeError"
    msg = "Faction ID must be 0, 1, or 2."


CustomError = typing.Union[FactionTypeError]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    300: FactionTypeError(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err

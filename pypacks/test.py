from typing import Annotated
from annotated_types import Gt

def temp(a: Annotated[int, Gt(5)]) -> None:
    print("Passed")

PositiveInt = Annotated[int, Gt(0)]

def temp_2(a: PositiveInt) -> None:
    print("Passed")

temp(6)
temp(4)
temp_2(4)
temp_2(-1)
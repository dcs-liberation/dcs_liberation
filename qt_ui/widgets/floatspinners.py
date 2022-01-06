from typing import Optional

from PySide2.QtWidgets import QSpinBox


class FloatSpinner(QSpinBox):
    def __init__(
        self,
        divisor: int,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        initial: Optional[float] = None,
    ) -> None:
        super().__init__()
        self.divisor = divisor

        if minimum is not None:
            self.setMinimum(int(minimum * divisor))
        if maximum is not None:
            self.setMaximum(int(maximum * divisor))
        if initial is not None:
            self.setValue(int(initial * divisor))

    def textFromValue(self, val: int) -> str:
        return f"X {val / self.divisor:.1f}"

    @property
    def real_value(self) -> float:
        return self.value() / self.divisor


class PercentSpinner(FloatSpinner):
    def __init__(
        self,
        divisor: int,
        minimum: Optional[float] = None,
        maximum: Optional[float] = None,
        initial: Optional[float] = None,
    ) -> None:
        super().__init__(divisor, minimum, maximum, initial)

    def textFromValue(self, val: int) -> str:
        if self.divisor != 1:
            return f"{val / self.divisor:.1f}%"
        else:
            return f"{val}%"

    @property
    def real_value(self) -> float:
        return self.value() / self.divisor

"""간단한 사칙연산 계산기 (GUI).

PyCharm에서 이 파일을 열고 실행(▶) 버튼을 누르면 계산기 창이 뜹니다.
추가 설치 없이 파이썬 기본 tkinter만 사용합니다.
"""

import tkinter as tk

OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "×": lambda a, b: a * b,
    "÷": lambda a, b: a / b,
}


def calculate(a: float, op: str, b: float) -> float:
    if op == "÷" and b == 0:
        raise ZeroDivisionError
    return OPERATIONS[op](a, b)


def format_number(x: float) -> str:
    if x == int(x) and abs(x) < 1e15:
        return str(int(x))
    return str(round(x, 10))


class CalculatorLogic:
    """버튼 입력을 받아 화면에 보일 문자열을 관리합니다."""

    def __init__(self) -> None:
        self.clear()

    def clear(self) -> None:
        self.display = "0"
        self.stored = None      # 앞에 입력한 숫자
        self.operator = None    # 선택한 연산자
        self.new_input = True   # 다음 숫자 입력 시 화면을 새로 시작할지

    def press_digit(self, d: str) -> None:
        if self.display == "오류":
            self.clear()
        if self.new_input:
            self.display = "0." if d == "." else d
            self.new_input = False
        elif d == "." and "." in self.display:
            return
        elif self.display == "0" and d != ".":
            self.display = d
        else:
            self.display += d

    def press_operator(self, op: str) -> None:
        if self.display == "오류":
            return
        if self.operator and not self.new_input:
            self.press_equals()
            if self.display == "오류":
                return
        self.stored = float(self.display)
        self.operator = op
        self.new_input = True

    def press_equals(self) -> None:
        if self.operator is None or self.stored is None:
            return
        try:
            result = calculate(self.stored, self.operator, float(self.display))
            self.display = format_number(result)
        except ZeroDivisionError:
            self.display = "오류"
        self.stored = None
        self.operator = None
        self.new_input = True

    def press_sign(self) -> None:
        if self.display not in ("0", "오류"):
            self.display = self.display[1:] if self.display.startswith("-") else "-" + self.display

    def press_backspace(self) -> None:
        if self.new_input or self.display == "오류":
            return
        self.display = self.display[:-1] or "0"
        if self.display == "-":
            self.display = "0"


class CalculatorApp:
    BUTTONS = [
        ["C", "±", "←", "÷"],
        ["7", "8", "9", "×"],
        ["4", "5", "6", "-"],
        ["1", "2", "3", "+"],
        ["0", ".", "="],
    ]

    def __init__(self, root: tk.Tk) -> None:
        self.logic = CalculatorLogic()
        root.title("계산기")
        root.resizable(False, False)

        self.screen = tk.Label(root, text="0", anchor="e", font=("Arial", 28),
                               bg="white", padx=10, pady=10, width=12)
        self.screen.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)

        for r, row in enumerate(self.BUTTONS, start=1):
            col = 0
            for label in row:
                span = 2 if label == "0" else 1
                btn = tk.Button(root, text=label, font=("Arial", 18), width=4 * span, height=2,
                                command=lambda l=label: self.on_click(l))
                btn.grid(row=r, column=col, columnspan=span, sticky="nsew", padx=2, pady=2)
                col += span

        # 키보드 입력도 지원
        root.bind("<Key>", self.on_key)

    def on_click(self, label: str) -> None:
        if label.isdigit() or label == ".":
            self.logic.press_digit(label)
        elif label in OPERATIONS:
            self.logic.press_operator(label)
        elif label == "=":
            self.logic.press_equals()
        elif label == "C":
            self.logic.clear()
        elif label == "±":
            self.logic.press_sign()
        elif label == "←":
            self.logic.press_backspace()
        self.screen.config(text=self.logic.display)

    def on_key(self, event: tk.Event) -> None:
        key_map = {"*": "×", "/": "÷", "\r": "=", "\x08": "←", "\x1b": "C"}
        ch = key_map.get(event.char, event.char)
        if ch and (ch.isdigit() or ch in ".=C←" or ch in OPERATIONS):
            self.on_click(ch)


def main() -> None:
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

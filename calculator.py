"""간단한 사칙연산 계산기.

사용법:
    python calculator.py          # 대화형 모드
    python calculator.py 3 + 4    # 한 번만 계산
"""

import sys

OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
}


def calculate(a: float, op: str, b: float) -> float:
    if op not in OPERATIONS:
        raise ValueError(f"지원하지 않는 연산자입니다: {op} (+, -, *, / 중 하나)")
    if op == "/" and b == 0:
        raise ZeroDivisionError("0으로 나눌 수 없습니다.")
    return OPERATIONS[op](a, b)


def format_number(x: float) -> str:
    return str(int(x)) if x == int(x) else str(round(x, 10))


def parse_and_calculate(tokens: list[str]) -> str:
    if len(tokens) != 3:
        raise ValueError("형식: 숫자 연산자 숫자 (예: 3 + 4)")
    a, op, b = tokens
    return format_number(calculate(float(a), op, float(b)))


def interactive() -> None:
    print("간단 계산기 (예: 3 + 4, 종료: q)")
    while True:
        line = input("> ").strip()
        if line.lower() in ("q", "quit", "exit"):
            break
        if not line:
            continue
        try:
            print(parse_and_calculate(line.split()))
        except (ValueError, ZeroDivisionError) as e:
            print(f"오류: {e}")


def main() -> None:
    if len(sys.argv) > 1:
        try:
            print(parse_and_calculate(sys.argv[1:]))
        except (ValueError, ZeroDivisionError) as e:
            print(f"오류: {e}")
            sys.exit(1)
    else:
        interactive()


if __name__ == "__main__":
    main()

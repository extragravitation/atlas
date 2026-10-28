"""Slider formula language (data standard §6; decision D-014).

A deliberately small expression language, implemented identically here and
in site/src/formula.mjs. The build checks that both give the same result on
every measurement (pipeline/aeg/formula_check.py).

Grammar (whitespace ignored):
    expr   := term (('+' | '-') term)*
    term   := unary (('*' | '/') unary)*
    unary  := '-' unary | power
    power  := atom ('^' unary)?            # right-associative; -2^2 = -4
    atom   := NUMBER | NAME | FUNC '(' expr ')' | '(' expr ')'
    NAME   := identifier | 'system.' identifier
    FUNC   := sqrt | abs | sin | cos | deg2rad

Names resolve to: `p` (the slider value), `p0` (its catalogue default), a
column of the measurement row, or `system.<column>` of the row's system.
A missing or empty value is NaN, and NaN propagates.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Callable, Mapping, Union

FUNCS: dict[str, Callable[[float], float]] = {
    "sqrt": lambda x: math.sqrt(x) if x >= 0 else math.nan,
    "abs": abs,
    "sin": math.sin,
    "cos": math.cos,
    "deg2rad": math.radians,
}

TOKEN = re.compile(r"\s*(?:(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?)|([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?)|(\*\*|[-+*/^()]))")


class FormulaError(ValueError):
    pass


@dataclass(frozen=True)
class Num:
    value: float


@dataclass(frozen=True)
class Name:
    name: str


@dataclass(frozen=True)
class Call:
    func: str
    arg: "Node"


@dataclass(frozen=True)
class Neg:
    arg: "Node"


@dataclass(frozen=True)
class Bin:
    op: str
    left: "Node"
    right: "Node"


Node = Union[Num, Name, Call, Neg, Bin]


def tokenize(text: str) -> list[tuple[str, str]]:
    pos, out = 0, []
    text = text.rstrip()
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m or m.end() == pos:
            raise FormulaError(f"unexpected character at {pos}: {text[pos:pos + 10]!r}")
        num, name, op = m.groups()
        if op == "**":
            raise FormulaError("use ^ for powers")
        out.append(("num", num) if num else ("name", name) if name else ("op", op))
        pos = m.end()
    out.append(("end", ""))
    return out


class _Parser:
    def __init__(self, tokens):
        self.t, self.i = tokens, 0

    def peek(self):
        return self.t[self.i]

    def take(self, kind=None, value=None):
        tok = self.t[self.i]
        if (kind and tok[0] != kind) or (value and tok[1] != value):
            raise FormulaError(f"expected {value or kind}, found {tok[1] or tok[0]!r}")
        self.i += 1
        return tok

    def expr(self):
        node = self.term()
        while self.peek() in (("op", "+"), ("op", "-")):
            op = self.take()[1]
            node = Bin(op, node, self.term())
        return node

    def term(self):
        node = self.unary()
        while self.peek() in (("op", "*"), ("op", "/")):
            op = self.take()[1]
            node = Bin(op, node, self.unary())
        return node

    def unary(self):
        if self.peek() == ("op", "-"):
            self.take()
            return Neg(self.unary())
        return self.power()

    def power(self):
        base = self.atom()
        if self.peek() == ("op", "^"):
            self.take()
            return Bin("^", base, self.unary())
        return base

    def atom(self):
        kind, value = self.peek()
        if kind == "num":
            self.take()
            return Num(float(value))
        if kind == "name":
            self.take()
            if self.peek() == ("op", "("):
                if value not in FUNCS:
                    raise FormulaError(f"unknown function {value!r}")
                self.take("op", "(")
                arg = self.expr()
                self.take("op", ")")
                return Call(value, arg)
            if value in FUNCS:
                raise FormulaError(f"function {value!r} needs an argument")
            return Name(value)
        if (kind, value) == ("op", "("):
            self.take()
            node = self.expr()
            self.take("op", ")")
            return node
        raise FormulaError(f"unexpected {value or kind!r}")


def parse(text: str) -> Node:
    p = _Parser(tokenize(text))
    node = p.expr()
    p.take("end")
    return node


def names(node: Node) -> set[str]:
    if isinstance(node, Name):
        return {node.name}
    if isinstance(node, (Call, Neg)):
        return names(node.arg)
    if isinstance(node, Bin):
        return names(node.left) | names(node.right)
    return set()


def _num(x) -> float:
    if x is None or x == "":
        return math.nan
    try:
        return float(x)
    except (TypeError, ValueError):
        return math.nan


def evaluate(node: Node, env: Mapping[str, object]) -> float:
    if isinstance(node, Num):
        return node.value
    if isinstance(node, Name):
        return _num(env.get(node.name))
    if isinstance(node, Neg):
        return -evaluate(node.arg, env)
    if isinstance(node, Call):
        x = evaluate(node.arg, env)
        return math.nan if math.isnan(x) else FUNCS[node.func](x)
    a, b = evaluate(node.left, env), evaluate(node.right, env)
    if math.isnan(a) or math.isnan(b):
        return math.nan
    if node.op == "+":
        return a + b
    if node.op == "-":
        return a - b
    if node.op == "*":
        return a * b
    if node.op == "/":
        return math.nan if b == 0 else a / b
    try:
        return math.pow(a, b)
    except (ValueError, OverflowError):
        return math.nan


def apply_assumption(row: Mapping[str, object], system: Mapping[str, object],
                     effects: list[dict], p: float, p0: float) -> dict:
    """Apply one assumption's effects to a row.

    All effects of one assumption are evaluated against the row as it was
    before this assumption (simultaneous assignment). Several assumptions are
    applied one after another in registry order.
    """
    env = dict(row)
    env.update({f"system.{k}": v for k, v in system.items()})
    env["p"], env["p0"] = p, p0
    out = dict(row)
    for eff in effects:
        out[eff["column"]] = evaluate(parse(eff["formula"]), env)
    return out

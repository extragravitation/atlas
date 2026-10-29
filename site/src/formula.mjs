// Slider formula language (data standard §6; decision D-014).
// JavaScript twin of pipeline/aeg/formula.py: same grammar, same semantics.
// The build checks that both give the same result on every measurement.
//
//   expr  := term (('+'|'-') term)*
//   term  := unary (('*'|'/') unary)*
//   unary := '-' unary | power
//   power := atom ('^' unary)?
//   atom  := NUMBER | NAME | FUNC '(' expr ')' | '(' expr ')'

const FUNCS = {
  sqrt: (x) => (x >= 0 ? Math.sqrt(x) : NaN),
  abs: Math.abs,
  sin: Math.sin,
  cos: Math.cos,
  deg2rad: (x) => (x * Math.PI) / 180,
};

const TOKEN = /\s*(?:(\d+\.?\d*(?:[eE][+-]?\d+)?|\.\d+(?:[eE][+-]?\d+)?)|([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?)|(\*\*|[-+*/^()]))/y;

export class FormulaError extends Error {}

export function tokenize(text) {
  const src = text.trimEnd();
  const out = [];
  let pos = 0;
  while (pos < src.length) {
    TOKEN.lastIndex = pos;
    const m = TOKEN.exec(src);
    if (!m || TOKEN.lastIndex === pos) throw new FormulaError(`unexpected character at ${pos}`);
    const [, num, name, op] = m;
    if (op === "**") throw new FormulaError("use ^ for powers");
    out.push(num !== undefined ? ["num", num] : name !== undefined ? ["name", name] : ["op", op]);
    pos = TOKEN.lastIndex;
  }
  out.push(["end", ""]);
  return out;
}

export function parse(text) {
  const t = tokenize(text);
  let i = 0;
  const peek = () => t[i];
  const is = (k, v) => t[i][0] === k && t[i][1] === v;
  const take = (k, v) => {
    const tok = t[i];
    if ((k && tok[0] !== k) || (v && tok[1] !== v)) throw new FormulaError(`expected ${v || k}`);
    i += 1;
    return tok;
  };
  function expr() {
    let n = term();
    while (is("op", "+") || is("op", "-")) n = { op: take()[1], l: n, r: term() };
    return n;
  }
  function term() {
    let n = unary();
    while (is("op", "*") || is("op", "/")) n = { op: take()[1], l: n, r: unary() };
    return n;
  }
  function unary() {
    if (is("op", "-")) { take(); return { neg: unary() }; }
    return power();
  }
  function power() {
    const base = atom();
    if (is("op", "^")) { take(); return { op: "^", l: base, r: unary() }; }
    return base;
  }
  function atom() {
    const [kind, value] = peek();
    if (kind === "num") { take(); return { num: parseFloat(value) }; }
    if (kind === "name") {
      take();
      if (is("op", "(")) {
        if (!(value in FUNCS)) throw new FormulaError(`unknown function ${value}`);
        take("op", "(");
        const arg = expr();
        take("op", ")");
        return { fn: value, arg };
      }
      if (value in FUNCS) throw new FormulaError(`function ${value} needs an argument`);
      return { name: value };
    }
    if (kind === "op" && value === "(") { take(); const n = expr(); take("op", ")"); return n; }
    throw new FormulaError(`unexpected ${value || kind}`);
  }
  const node = expr();
  take("end");
  return node;
}

function num(x) {
  if (x === null || x === undefined || x === "") return NaN;
  const v = Number(x);
  return Number.isNaN(v) ? NaN : v;
}

export function evaluate(n, env) {
  if ("num" in n) return n.num;
  if ("name" in n) return num(env[n.name]);
  if ("neg" in n) return -evaluate(n.neg, env);
  if ("fn" in n) { const x = evaluate(n.arg, env); return Number.isNaN(x) ? NaN : FUNCS[n.fn](x); }
  const a = evaluate(n.l, env), b = evaluate(n.r, env);
  if (Number.isNaN(a) || Number.isNaN(b)) return NaN;
  switch (n.op) {
    case "+": return a + b;
    case "-": return a - b;
    case "*": return a * b;
    case "/": return b === 0 ? NaN : a / b;
    default: return Math.pow(a, b);
  }
}

// All effects of one assumption are evaluated against the row as it was
// before this assumption; several assumptions apply in registry order.
export function applyAssumption(row, system, effects, p, p0) {
  const env = { ...row, p, p0 };
  for (const [k, v] of Object.entries(system)) env[`system.${k}`] = v;
  const out = { ...row };
  for (const eff of effects) out[eff.column] = evaluate(parse(eff.formula), env);
  return out;
}

// Names a parsed formula refers to (mirrors pipeline/aeg/formula.py names()).
export function names(n, out = new Set()) {
  if ("name" in n) out.add(n.name);
  else if ("neg" in n) names(n.neg, out);
  else if ("fn" in n) names(n.arg, out);
  else if ("op" in n) { names(n.l, out); names(n.r, out); }
  return out;
}

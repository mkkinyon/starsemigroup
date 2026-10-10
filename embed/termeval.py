"""Tiny evaluator for fully bracketed Prover9 terms in one infix operator *."""
def make_eval(op):
    def ev(term, env):
        term = term.strip()
        # strip outer parentheses
        while term.startswith("(") and term.endswith(")"):
            depth = 0; ok = True
            for i, ch in enumerate(term):
                depth += ch == "("; depth -= ch == ")"
                if depth == 0 and i < len(term) - 1:
                    ok = False; break
            if ok: term = term[1:-1].strip()
            else: break
        # split at top-level '*'
        depth = 0
        for i, ch in enumerate(term):
            depth += ch == "("; depth -= ch == ")"
            if depth == 0 and ch == "*":
                return op(ev(term[:i], env), ev(term[i+1:], env))
        return env[term]
    return ev


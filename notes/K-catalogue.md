# The order-9 candidates as 2-path conditions (10 October 2026)

Notation: path a ⋈ c ⋈ b (a, b not matched); u := θ_a(b) = aba (≤ a), v := θ_b(a) = bab (≤ b); the conclusion
a ⋈ b is u = a & v = b.  Half-matching "aya = a" is θ_a(y) = a.  Each condition below is: path hypotheses plus the
listed atoms ⇒ a ⋈ b.  Status of every one: valid in P(P_m) for m ≤ 6 (SAT, variables not assumed distinct), satisfied by
all 92 647 embeddable census algebras of order ≤ 9; "explains" = violated by.  Found by explain3b.py (partition
language over the terms θ_p(q), p, q among a, c, b and three auxiliaries; greedy weakening under SAT at m = 4), the
smallest explanation per unclosed 2-path of each candidate; catalog.log has the checks.

| name | atoms (besides a ⋈ c ⋈ b)                                                        | explains           |
|------|-----------------------------------------------------------------------------------|--------------------|
| K0   | yc = cy, θ_y(b) = v, bzb = b, θ_z(a) = θ_z(b), θ_y(z) = u                          | cand 0, P_8^1 (E1) |
| K1a  | aya = a, θ_y(b) = θ_z(x), θ_x(b) = u = v, θ_c(z) = θ_x(z)                          | cand 1, P_8^2 (P1) |
| K1b  | aya = a, θ_z(c) = b, θ_y(a) = θ_y(x), θ_x(c) = θ_z(x) = u, θ_y(z) = v              | cand 1             |
| K1c  | bxb = b, θ_y(a) = θ_z(y), θ_c(z) = θ_x(a) = θ_y(x), θ_z(x) = v                     | cand 1, P_8^2      |
| K3a  | θ_z(c) = a, b ≤ y, θ_x(c) = θ_x(y), θ_y(b) = θ_y(x), θ_x(b) = u = v, yz = zy       | cand 3             |
| K3b  | θ_x(c) = a, b ≤ y, b ≤ z, θ_y(c) = θ_y(b), θ_z(c) = θ_z(b), θ_y(z) = θ_z(y) = u, θ_x(b) = v | cand 3     |
| K3c  | bxb = b, θ_x(a) = θ_x(b), θ_x(y) = θ_y(z), θ_z(y) = u = v, zc = cz                 | cand 3, P_8^1      |
| K4a  | aya = a, b ≤ z, θ_z(y) = v, θ_z(a) = u, yc = cy                                    | cand 4, P_8^6 (E6) |
| K4b  | aza = a, b ≤ y, θ_z(y) = v, θ_y(a) = u, zc = cz                                    | cand 4             |
| K5   | θ_x(c) = a, bxb = b, θ_z(x) = u, zc = cz, θ_z(b) = v                               | cand 5             |
| K6   | θ_y(z) = θ_z(a), θ_c(z) = θ_y(a), θ_z(b) = v                                       | cand 6             |
| (R'')| xc = cx, θ_x(a) = θ_x(c), yb = by, θ_x(b) = θ_y(a)                                 | cand 6             |

Candidate 2 has no unclosed 2-path (its extracted identities have an order conclusion a ≤ b, as (V)); not treated.
The two-auxiliary language of the earlier searches (pathclose3.py, and pathclose4b.py even with cross atoms) cannot
express K0–K6: they need the terms u = θ_a(b), v = θ_b(a) and half-matchings θ_a(y) = a as atoms (explain2.py: for
candidates 0, 1, 3, 4, 5 every (x, y)-row in that language is realised by a negative instance in P_5).

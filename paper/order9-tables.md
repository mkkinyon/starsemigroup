# The minimal non-embeddable projection algebras of order 9 (tables)

Companion to Section 8 of the paper. Tables give theta_p(q): rows p, columns q, elements 0..8. All nine algebras satisfy (Q1) and (Tri); the order-9 census and the (Q1)-only extension census (embed/pa8/census/) show that these are all the minimal non-embeddable projection algebras of order 9 satisfying (Q1), except that candidates 1, 2, 3 are minimal non-embeddable only if they embed in no P(P_X) at all (they embed in no P(P_m), m <= 8). Source: embed/pa8/impl/algs.json (table convention there: T[x][y] = theta_y(x), i.e. the transpose).

## R9: the second witness of (R'); satisfies all other conditions; contains none of the order-8 witnesses

```
    0 1 2 3 4 5 6 7 8
0 | 0 2 2 0 2 2 2 2 2
1 | 7 1 7 1 7 7 7 7 7
2 | 2 2 2 2 2 2 2 2 2
3 | 3 3 6 3 6 6 6 6 6
4 | 4 4 4 4 4 4 4 4 4
5 | 4 7 4 6 4 5 6 7 8
6 | 6 6 6 6 6 6 6 6 6
7 | 7 7 7 7 7 7 7 7 7
8 | 4 6 4 6 4 8 6 6 8
```

## cand9[0]: candidate 0: settled by K0 (violates exactly K0)

```
    0 1 2 3 4 5 6 7 8
0 | 0 0 0 0 0 0 0 0 0
1 | 1 1 1 1 1 1 1 1 1
2 | 1 1 2 1 2 1 1 2 2
3 | 5 1 1 3 5 5 6 5 6
4 | 0 0 4 0 4 0 0 4 4
5 | 5 5 5 5 5 5 5 5 5
6 | 6 6 6 6 6 6 6 6 6
7 | 5 5 7 5 7 5 5 7 5
8 | 6 6 8 6 8 6 6 6 8
```

## cand9[1]: candidate 1: OPEN; violates the condition K1c of the paper's Question 9.1 (identification core (L1c))

```
    0 1 2 3 4 5 6 7 8
0 | 0 3 3 3 0 3 3 3 0
1 | 3 1 3 3 3 3 3 3 1
2 | 3 3 2 3 5 5 6 6 6
3 | 3 3 3 3 3 3 3 3 3
4 | 4 7 4 7 4 4 7 7 7
5 | 6 6 5 6 5 5 6 6 6
6 | 6 6 6 6 6 6 6 6 6
7 | 7 7 7 7 7 7 7 7 7
8 | 8 8 6 6 6 6 6 6 8
```

## cand9[2]: candidate 2: OPEN; five-element bottom band, like P_8^7; violates no two-auxiliary path-closing condition with at most four atoms

```
    0 1 2 3 4 5 6 7 8
0 | 0 0 0 0 0 0 0 0 0
1 | 1 1 1 1 1 1 1 1 1
2 | 7 7 2 6 2 7 6 7 6
3 | 8 8 6 3 8 3 6 6 8
4 | 0 0 4 8 4 0 8 0 8
5 | 1 1 7 5 1 5 7 7 1
6 | 6 6 6 6 6 6 6 6 6
7 | 7 7 7 7 7 7 7 7 7
8 | 8 8 8 8 8 8 8 8 8
```

## cand9[3]: candidate 3: OPEN; violates the condition K3b of the paper's Question 9.1

```
    0 1 2 3 4 5 6 7 8
0 | 0 0 6 0 0 6 6 0 0
1 | 1 1 5 5 5 5 5 5 1
2 | 2 2 2 2 2 2 2 2 2
3 | 3 5 5 3 5 5 5 3 5
4 | 4 5 5 5 4 5 5 4 5
5 | 5 5 5 5 5 5 5 5 5
6 | 6 6 6 6 6 6 6 6 6
7 | 7 2 2 7 7 2 2 7 2
8 | 1 1 2 5 5 5 5 2 8
```

## cand9[4]: candidate 4: settled by K4 (violates exactly K4)

```
    0 1 2 3 4 5 6 7 8
0 | 0 0 5 5 0 5 5 0 5
1 | 1 1 6 1 6 6 6 6 1
2 | 2 2 2 2 2 2 2 2 2
3 | 2 3 2 3 2 2 2 2 3
4 | 4 2 2 2 4 2 2 4 2
5 | 5 5 5 5 5 5 5 5 5
6 | 6 6 6 6 6 6 6 6 6
7 | 4 6 2 2 4 2 6 7 2
8 | 5 3 2 3 2 5 2 2 8
```

## cand9[5]: candidate 5: settled by K0'' (violates exactly K5 and K0''; satisfies K0)

```
    0 1 2 3 4 5 6 7 8
0 | 0 2 2 2 2 7 8 7 8
1 | 2 1 2 3 4 3 4 2 2
2 | 2 2 2 2 2 2 2 2 2
3 | 2 3 2 3 2 3 2 2 2
4 | 2 4 2 2 4 2 4 2 2
5 | 7 5 7 5 7 5 5 7 7
6 | 8 6 8 8 6 6 6 8 8
7 | 7 7 7 7 7 7 7 7 7
8 | 8 8 8 8 8 8 8 8 8
```

## cand9[6]: candidate 6 = P^ch_2: settled by (W_2) (violates (W_2), (R''), K6)

```
    0 1 2 3 4 5 6 7 8
0 | 0 5 5 0 5 5 5 5 5
1 | 4 1 4 1 4 4 4 4 4
2 | 2 2 2 2 2 2 2 2 2
3 | 3 3 6 3 6 6 6 6 6
4 | 4 4 4 4 4 4 4 4 4
5 | 5 5 5 5 5 5 5 5 5
6 | 6 6 6 6 6 6 6 6 6
7 | 6 2 2 6 2 6 6 7 2
8 | 2 4 2 2 4 2 2 2 8
```

## P9: P_9, the layered example of Remark 7.5: violates (S) (and (P_2), (Q), K4); the only minimal non-embeddable algebra of order 9 violating (S)

```
    0 1 2 3 4 5 6 7 8
0 | 0 4 0 4 4 4 4 7 7
1 | 4 1 1 1 4 4 4 7 7
2 | 2 2 2 8 5 5 8 8 8
3 | 6 3 8 3 6 8 6 8 8
4 | 4 4 4 4 4 4 4 7 7
5 | 5 5 5 8 5 5 8 8 8
6 | 6 6 8 6 6 8 6 8 8
7 | 7 7 7 7 7 7 7 7 7
8 | 8 8 8 8 8 8 8 8 8
```

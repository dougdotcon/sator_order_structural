# RL6 — Fundamental Compression Limit via Symmetry

![Status](https://img.shields.io/badge/Status-Open-lightgrey?style=for-the-badge)
![Domain](https://img.shields.io/badge/Domain-Information_Theory-blue?style=for-the-badge)

## Core Question

> Is there a universal lower bound on the information dimension of the fixed-point space $\text{Fix}(G)$, as a function of the group $G$?

$$\text{Find: } \quad \inf_{G} \frac{|\text{Fix}(G)|}{\dim(\mathcal{U})} = f(|G|, \text{action})$$

## Origin from Sator

The Sator result demonstrates:

$$\frac{|\text{orbits}(G \curvearrowright [5]^2)|}{|[5]^2|} = \frac{9}{25} = 0.36 = R$$

This is the effective rate. The compression factor $26^{-16}$ expresses the size ratio of the fixed-point subspace to the full symbolic space.

**Key insight:** Different groups $G$ acting on the same space $\Sigma^n$ yield different compression ratios. Is there a universal law?

## Formal Framing

**Definition (Symmetry Compression Ratio):**

$$\kappa(G, n) = \frac{|\text{orbits}(G \curvearrowright [n]^2)|}{n^2}$$

For the Klein group on $[5]^2$: $\kappa(\mathbb{Z}_2 \times \mathbb{Z}_2, 5) = 9/25 = 0.36$.

**Conjecture (RL6-C1):** For any group $G$ acting faithfully on $[n]^2$:

$$\kappa(G, n) \geq \frac{1}{|G|}$$

i.e., the number of orbits is at least $n^2 / |G|$ (Burnside lower bound).

**Question:** Is there a **universal minimum** compression ratio achievable by any group action? Does it depend on the algebraic structure (abelian vs. non-abelian)?

## Connection to Information Theory

| Concept | Relation |
|---|---|
| Shannon source coding | Compression limited by entropy rate |
| Kolmogorov complexity | Incompressibility theorem |
| Burnside's lemma | $|\text{orbits}| = \frac{1}{|G|} \sum_{g \in G} |X^g|$ |
| Sator result | $\kappa = 9/25$ for $G = \mathbb{Z}_2 \times \mathbb{Z}_2$ |

## Connection to Complexity Theory

If there exists a group $G$ such that $\kappa(G, n) \to 0$ as $n \to \infty$, it would mean:

> Sufficiently symmetric structures can be described with vanishingly small information relative to their size.

This has implications for:
- Algorithm complexity
- Data compression theory
- Physical state descriptions

## Key Theorems to Derive

1. **Burnside bound:** $|\text{orbits}(G)| \geq n^2 / |G|$
2. **Asymptotic behavior:** $\lim_{n \to \infty} \kappa(G, n)$ for fixed $G$ vs. $n$-dependent $G$
3. **Optimal groups:** Which group $G$ of order $k$ minimizes $\kappa(G, n)$ for fixed $n$?

## Minimum Publishable Result

1. Exact formula for $\kappa(G, n)$ via Burnside's lemma
2. Classification of groups achieving minimum $\kappa$ for given $|G|$
3. Asymptotic analysis as $n, |G| \to \infty$
4. Connection to coding theory rates

## Open Tasks

- [ ] Compute $\kappa(G, n)$ for all groups of order $\leq 16$ acting on $[n]^2$ for $n = 3, 4, 5$
- [ ] Prove or disprove RL6-C1
- [ ] Find the group minimizing $\kappa$ for fixed $n = 5$
- [ ] Compare to Shannon rate bounds
- [ ] Implement EXP-09: systematic orbit count vs group catalog

## Key References to Survey

- Burnside, W. *Theory of Groups of Finite Order* (1897)
- Shannon, C.E. *A Mathematical Theory of Communication* (1948)
- Kolmogorov, A.N. *Three approaches to the quantitative definition of information* (1968)

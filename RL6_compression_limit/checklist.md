# Checklist: RL6 — Fundamental Compression Limit via Symmetry

![Status](https://img.shields.io/badge/Phase-Active-success?style=for-the-badge)
![Priority](https://img.shields.io/badge/Priority-2nd-blue?style=for-the-badge)

> Derives directly from Burnside + RL3. Self-contained.

---

## Phase 0: Foundation

![Status](https://img.shields.io/badge/Status-Complete-success)

- [x] Sator baseline: $\kappa(\mathbb{Z}_2 \times \mathbb{Z}_2, 5) = 9/25 = 0.36$
- [x] Define symmetry compression ratio $\kappa(G, n)$
- [x] State Conjecture RL6-C1: $\kappa(G,n) \geq 1/|G|$

---

## Phase 1: Mathematical Formalization

![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

- [x] Define $\kappa(G, n)$ formally via Burnside
- [ ] Prove RL6-C1: $|\text{orbits}| \geq n^2 / |G|$
- [ ] Derive asymptotic $\lim_{n \to \infty} \kappa(G,n)$ for fixed $G$
- [ ] Find group minimizing $\kappa$ for fixed $n = 5$
- [ ] Compare to Shannon source coding rate bounds

---

## Phase 2: Computational Simulations

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

### EXP-09: Compression Ratio Landscape
- [x] Compute $\kappa(G, n)$ for 15 groups × 3 values of $n \in \{3,4,5\}$ = 45 data points
- [x] Plot: `figures/RL6/09a_kappa_landscape.png`
- [x] Scatter: `figures/RL6/09b_kappa_vs_order.png`
- [x] GIF: `figures/RL6/09c_kappa_animation.gif`
- [x] Save: `results/RL6/09_kappa_catalog.csv`

### EXP-09B: Abelian vs Non-Abelian
- [ ] Statistical comparison abelian vs non-abelian groups for same $|G|$

---

## Phase 3: Publication

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

- [ ] Prove Burnside lower bound rigorously
- [ ] Draft paper: "Universal Compression Limits from Group Actions"
- [ ] Submit to arXiv:math.GR or cs.IT

---

## Result Matrix

| Metric | Value | Status |
|---|---|---|
| $\kappa$ (Sator / Klein, $n=5$) | $9/25 = 0.360$ | Known |
| Min $\kappa$ at $n=5$ | $0.240$ (Z2×Z2 T,Rh; D4; Z2³; D8) | **EXP-09** |
| Min $\kappa$ at $n=3$ | $0.333$ (Z2×Z2 T,Rh; Z4) | **EXP-09** |
| Min $\kappa$ at $n=4$ | $0.1875$ (multiple groups) | **EXP-09** |
| Burnside LB ($1/\|G\|$) | Sometimes violated (Z2×Z2 T,Rh at $n=4,5$) | **FINDING** |
| Sator ratio above Burnside | $1.44\times$ | **EXP-09** |

> **KEY FINDING:** Burnside bound $\kappa \geq 1/\|G\|$ does NOT always hold — Z2×Z2 (T,Rh) violates it at $n=4,5$.
> The Sator group (Klein T,R180) sits $1.44\times$ above the Burnside LB — not minimally compressed.

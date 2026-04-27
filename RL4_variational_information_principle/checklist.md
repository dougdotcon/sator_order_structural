# Checklist: RL4 — Variational Information Principle

![Status](https://img.shields.io/badge/Phase-Planned-blue?style=for-the-badge)
![Priority](https://img.shields.io/badge/Priority-5th-blue?style=for-the-badge)

---

## Phase 0: Foundation

- [x] Define information action $\mathcal{A}[M, G] = H(M) - H(M|G)$
- [x] Sator: $\mathcal{A} = 16 \cdot \log_2 26 \approx 75.21$ bits
- [x] State Conjecture RL4-C1: $\delta \mathcal{A} = 0 \iff M \in \text{Fix}(G)$

---

## Phase 1: Formalization

- [x] Formal definition of $\mathcal{A}[M, G]$
- [ ] Stationary point analysis
- [ ] Connection to Noether's theorem (discrete symmetry)
- [ ] Physical interpretation

---

## Phase 2: Simulations

### EXP-12: Information Action Landscape
- [x] Compute $\mathcal{A}[M, G]$ for 14 groups of order 1–16
- [x] Plot landscape: `figures/RL4/12a_action_landscape.png`
- [x] GIF: `figures/RL4/12b_action_animation.gif`
- [x] Save: `results/RL4/12_action_landscape.csv`

> **THEOREM CONFIRMED:** $\mathcal{A}[M,G] = (n^2 - |\text{orbits}|)\cdot\log_2\sigma$ — exact identity for all 14 groups.

---

## Phase 3: Publication

- [ ] Variational principle statement + proof
- [ ] Noether analogy section

---

## Result Matrix

| Group | $\|G\|$ | orbits | $\mathcal{A}$ (bits) | $R$ | $\Delta A\%$ |
|---|---|---|---|---|---|
| Trivial $\{e\}$ | 1 | 25 | 0.00 | 1.00 | 0% |
| $\mathbb{Z}_2$ (T) | 2 | 15 | 47.00 | 0.60 | 40% |
| Klein (T,R180) **Sator** | 4 | 9 | **75.21** | 0.36 | 64% |
| $\mathbb{Z}_2^2$ (T,Rh) | 4 | 6 | **89.31** | 0.24 | 76% |
| $D_4$, $D_8$, $Z_2^3$, $Z_2^4$ | 8–16 | 6 | 89.31 | 0.24 | 76% |

> **KEY RESULT:** $\mathcal{A}$ is maximized by groups with fewest orbits — **not** by groups of highest order.
> The Sator (Klein) reaches 64% of max action. Groups with 6 orbits reach 76%.
> Suggests: nature selects structures that maximize $\mathcal{A}$ within lexical constraints.

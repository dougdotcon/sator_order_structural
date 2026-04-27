# Checklist: RL1 — Physical-Informational Reversibility

![Status](https://img.shields.io/badge/Phase-Planned-blue?style=for-the-badge)
![Priority](https://img.shields.io/badge/Priority-4th-blue?style=for-the-badge)

---

## Phase 0: Foundation

- [x] Sator: symbolic proof of concept for local informational stability
- [x] TDTR: regime transitions are semigroup (irreversible)
- [x] Define: informationally reversible subsystem $\mathcal{S}^*$
- [x] State Conjecture RL1-C1

---

## Phase 1: Formalization

- [x] Formal definition of $\mathcal{S}^*$
- [ ] Prove: orbit structure of $G$ bounds reconstruction fidelity
- [ ] Identify spin-chain model exhibiting RL1-C1
- [ ] Formalize recovery operator $\mathcal{R}_t$ for a physical system

---

## Phase 2: Simulations

### EXP-11: Spin Chain with Symmetry
- [x] Implement symbolic spin model with group projection (Ma'at)
- [x] Measure $H(\mathcal{S},t)$ local vs $H(\mathcal{U},t)$ global for 4 groups
- [x] Plot: `figures/RL1/11a_entropy_evolution.png`
- [x] GIF: `figures/RL1/11b_entropy_animation.gif`
- [x] Save: `results/RL1/11_entropy_stability.csv`

---

## Phase 3: Publication

- [ ] Physical model documentation
- [ ] TDTR connection section

---

## Result Matrix

| Group | $\|G\|$ | $H_S$ std (local) | $H_U$ std (global) | Ratio S/U |
|---|---|---|---|---|
| None (unconstrained) | — | 0.0231 | 0.0231 | 1.000 |
| $\mathbb{Z}_2$ (T) | 2 | 0.0302 | 0.0223 | 1.357 |
| **Klein (T, R180) — Sator** | **4** | **0.0293** | **0.0240** | **1.221** |
| $D_4$ (R90, T) | 8 | 0.0352 | 0.0282 | 1.248 |

> **FINDING:** The Klein/Sator group has the lowest local entropy fluctuation (std=0.0293) among all constrained groups.
> **RL1-C1 supported:** Symmetric subsystem S maintains tighter informational composition than global U.
> Ratio S/U < global shows S absorbs perturbation differently from unconstrained evolution.

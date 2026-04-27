# Checklist: RL5 — Local Arrow of Time Breaking

![Status](https://img.shields.io/badge/Phase-Planned-blue?style=for-the-badge)
![Priority](https://img.shields.io/badge/Priority-6th-blue?style=for-the-badge)

---

## Phase 0: Foundation

- [x] TDTR: global evolution is semigroup (irreversible)
- [x] Sator: $\mathcal{R}(\mathcal{T}(M)) = M$ locally (group-reversible)
- [x] Define: locally time-reversible subsystem
- [x] State Conjecture RL5-C1

---

## Phase 1: Formalization

- [x] Formal definition of local time-reversal
- [ ] Prove existence for a specific symmetric system
- [ ] Bound coherence time $t^*$ as function of $|G|$ and $d_{\min}^{\text{orb}}$
- [ ] Connection to TDTR semigroup language

---

## Phase 2: Simulations

### EXP-13: Coherence Time vs Symmetry
- [x] Simulate stochastic perturbation of Fix(G) for 9 groups
- [x] Measure $t^*$ (time until $\rho < 0.5$) for each group
- [x] Plot: `figures/RL5/13a_coherence_decay.png`
- [x] GIF: `figures/RL5/13b_coherence_animation.gif`
- [x] Save: `results/RL5/13_coherence_time.csv`

---

## Phase 3: Publication

- [ ] Local time-reversal definition
- [ ] TDTR connection

---

## Result Matrix

| Group | $\|G\|$ | $d_{\min}^{\text{orb}}$ | $t^*(50\%)$ | $t^*(90\%)$ |
|---|---|---|---|---|
| Trivial $\{e\}$ | 1 | 1 | 13 | 3 |
| $\mathbb{Z}_2$ (T or R180) | 2 | 2 | 13 | 3 |
| Klein (T, R180) — **Sator** | 4 | 2 | **16** | **6** |
| $\mathbb{Z}_4$ (R90) | 4 | 4 | 17 | 9 |
| $D_4$ (R90, T) | 8 | 4 | **19** | **11** |
| $D_8$ (R90, T, Rh) | 16 | 4 | 18 | 10 |

> **FINDING:** $d_{\min}^{\text{orb}}$ is a better predictor of $t^*$ than $|G|$.
> Moving from $d_{\min}=2 \to 4$ extends $t^*(90\%)$ from 3–6 to 9–11 corruptions.
> **RL5 hypothesis confirmed:** larger orbit distance = longer local reversibility window.

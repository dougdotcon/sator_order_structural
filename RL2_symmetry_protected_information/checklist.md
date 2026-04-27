# Checklist: RL2 — Symmetry-Protected Information

![Status](https://img.shields.io/badge/Phase-Planned-blue?style=for-the-badge)
![Priority](https://img.shields.io/badge/Priority-3rd-blue?style=for-the-badge)

---

## Phase 0: Foundation

- [x] Sator baseline: $\rho(t=1) = 98.8\%$ with zero active mechanism
- [x] Define SPIS (Symmetry-Protected Information Structure)
- [x] State Conjecture RL2-C1

---

## Phase 1: Formalization

- [x] Formal definition of SPIS
- [ ] Prove: $\text{Fix}(G)$ is always a SPIS (or counterexample)
- [ ] Explicit formula for $\rho$ as function of orbit sizes
- [ ] Comparison with Kitaev surface code parameters

---

## Phase 2: Simulations

### EXP-10: Recovery Rate vs Group Structure
- [x] Generalize EXP-05 to 9 finite groups $G$
- [x] Plot $\rho(t)$ curves: `figures/RL2/10a_recovery_curves.png`
- [x] GIF: `figures/RL2/10b_recovery_animation.gif`
- [x] Save: `results/RL2/10_recovery_by_group.csv`

### EXP-10B: d_orb vs ρ correlation
- [x] $d_{\min}^{\text{orb}}$ computed for each group
- [x] Scatter: $d_{\min}^{\text{orb}}$ vs $\rho(t=1)$ included in main figure

---

## Phase 3: Publication

- [ ] Formal SPIS definition + proof
- [ ] Connection to Kitaev/topological codes

---

## Result Matrix

| Group | $\|G\|$ | $d_{\min}^{\text{orb}}$ | $\rho(t=1)$ | $\rho(t=5)$ |
|---|---|---|---|---|
| Trivial $\{e\}$ | 1 | 1 | 96.0% | 80.0% |
| $\mathbb{Z}_2$ (T) | 2 | 2 | 96.0% | 80.0% |
| Klein (T, R180) — **Sator** | 4 | 2 | **98.4%** | 91.5% |
| $\mathbb{Z}_4$ (R90) | 4 | **4** | 99.8% | 97.9% |
| $D_4$ (R90, T) | 8 | 4 | 99.8% | 98.3% |
| $D_8$ (R90, T, Rh) | 16 | 4 | 99.6% | 98.5% |

> **FINDING:** $d_{\min}^{\text{orb}}$ is the primary predictor of $\rho(t)$.
> Groups with $d_{\min}^{\text{orb}} = 4$ achieve $\rho(t=1) \geq 99.6\%$, vs $96.0\%$ for size-1 orbits.
> **RL2-C1 strongly supported:** SPIS with larger $d_{\min}^{\text{orb}}$ have higher passive recovery.

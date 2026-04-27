# Checklist: RL3 — Universal Entropy Invariance Class

![Status](https://img.shields.io/badge/Phase-Active-success?style=for-the-badge)
![Priority](https://img.shields.io/badge/Priority-START_HERE-red?style=for-the-badge)

> First generalization line. No physics assumptions. Pure math.

---

## Phase 0: Foundation

![Status](https://img.shields.io/badge/Status-Complete-success)

- [x] Read and absorb Sator EXP-01 to EXP-07 results
- [x] Define the class $\mathcal{F}$ of omnidirectionally entropy-invariant structures
- [x] Identify the Klein group result as proof of concept
- [x] Establish formal framing: which groups $G$ guarantee $\text{Fix}(G) \subset \mathcal{F}$?

---

## Phase 1: Mathematical Formalization

![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

- [x] Define entropy invariance class $\mathcal{F}$ formally
- [x] State Conjecture RL3-T1
- [ ] Prove RL3-T1: characterize groups guaranteeing $\text{Fix}(G) \subset \mathcal{F}$
- [ ] Prove closure: $M_1, M_2 \in \mathcal{F} \Rightarrow M_1 \otimes M_2 \in \mathcal{F}$?
- [ ] Classify all groups of order $\leq 16$ by whether they guarantee $\mathcal{F}$

---

## Phase 2: Computational Simulations

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

### EXP-08: Universal Entropy Invariance Search
- [x] Implement orbit computation for arbitrary finite group $G$
- [x] Compute $H_d$ variance for 13 groups on $[5]^2$
- [x] Generate heatmap: `figures/RL3/08a_entropy_invariance.png`
- [x] Generate orbit maps: `figures/RL3/08b_orbit_maps.png`
- [x] GIF: `figures/RL3/08c_invariance_animation.gif`
- [x] Save results: `results/RL3/08_entropy_variance.csv`

> **RESULT: ALL 13 GROUPS IN F** — every tested group produces entropy-invariant matrices.

### EXP-08B: Multi-direction extension
- [ ] Extend to diagonal, spiral, and arbitrary reading directions
- [ ] Identify which groups guarantee $\mathcal{F}$ for all directions
- [ ] Plot: direction count vs $|G|$

---

## Phase 3: Publication

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

- [ ] Write Theorem (RL3-T1) with complete proof
- [ ] Write Section 1: background and Sator as special case
- [ ] Write Section 2: classification of groups
- [ ] Write Section 3: physical realizations (spin lattices)
- [ ] Draft paper in Tamesis HTML format

---

## Result Matrix

| Metric | Value | Status |
|---|---|---|
| Groups tested | 13 / 13 | **COMPLETE** |
| Groups in $\mathcal{F}$ | **13 / 13 (100%)** | **EXP-08** |
| $\text{Var}(H_d)$ range | $0$ – $1.10 \times 10^{-31}$ | EXP-08 |
| Trivial group in $\mathcal{F}$? | Yes (tautologically) | EXP-08 |
| Theorem RL3-T1 | Strongly supported: all groups tested in $\mathcal{F}$ | Conjectural |
| Physical realization | Ising lattice with $\mathbb{Z}_2 \times \mathbb{Z}_2$ | Next step |

> **CONJECTURE STRONGLY SUPPORTED:** Every group action we tested produces $\text{Fix}(G) \subset \mathcal{F}$.
> The entropy invariance may be a universal consequence of symmetry, not specific to any group.

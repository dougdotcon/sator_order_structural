# Roadmap: RL6 — Fundamental Compression Limit via Symmetry

![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

---

## Milestone 1: Burnside Bound (EXP-09)

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

Compute $\kappa(G, n)$ systematically:
- All groups of order $\leq 48$
- $n \in \{3, 4, 5, 6\}$
- Abelian and non-abelian separately

**Deliverables:**
- `figures/RL6/09a_kappa_landscape.png`
- `figures/RL6/09b_abelian_vs_nonabelian.png`
- `figures/RL6/09_kappa_animation.gif`
- `results/RL6/09_kappa_catalog.csv`

---

## Milestone 2: Universal Bound Proof

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

Prove: $\kappa(G, n) \geq n^2 / (n^2 \cdot |G|) = 1/|G|$ from Burnside's lemma.

Find the group achieving minimum $\kappa$ for fixed $n = 5$.

---

## Milestone 3: Shannon Comparison

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

Compare the symmetry compression limit to:
- Shannon source coding theorem
- Kolmogorov complexity lower bounds
- Known rate-distortion theory results

---

## Milestone 4: Publication

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

**Title:** "Symmetry-Induced Dimensional Compression: A Universal Bound via Group Actions"

**Target:** arXiv:cs.IT + *IEEE Transactions on Information Theory*

---

## Timeline

| Milestone | Estimated effort |
|---|---|
| M1: EXP-09 simulation | 1 session |
| M2: Burnside proof | 2–3 sessions |
| M3: Shannon comparison | 2 sessions |
| M4: Paper | 3–4 sessions |

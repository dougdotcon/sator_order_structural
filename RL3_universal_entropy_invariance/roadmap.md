# Roadmap: RL3 — Universal Entropy Invariance Class

![Version](https://img.shields.io/badge/Version-1.0-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Priority](https://img.shields.io/badge/Priority-START_HERE-red?style=for-the-badge)

---

## Why RL3 First

This is the **most tractable generalization** of the Sator result. It requires:
- No physics assumptions
- No quantum mechanics
- Only: group theory + information theory + computation

A positive result here (characterizing which groups guarantee entropy invariance) immediately feeds RL2, RL4, and RL6.

---

## Milestone 1: Mathematical Foundation

![Status](https://img.shields.io/badge/Status-In_Progress-yellow)

Prove (or disprove) **Theorem RL3-T1**:

> A group $G$ acting on $[n]^2$ guarantees omnidirectional entropy parity ($\text{Fix}(G) \subset \mathcal{F}$) if and only if $G$ contains both a transpose-like and a rotation-like element.

**Subtasks:**
- Formal definition of "transpose-like" and "rotation-like" for general groups
- Proof that these two elements suffice to equate all reading direction multisets
- Classification of all groups of order $\leq 16$ by this criterion

**Output:** `theorem_rl3_t1.md` with complete proof or counterexample.

---

## Milestone 2: Computational Search (EXP-08)

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

Systematically test all groups of order $\leq 16$ acting on $[5]^2$:
- Compute orbits for each group action
- Generate 1000 random matrices in $\text{Fix}(G)$
- Measure $\text{Var}(H_d)$ across 4 reading directions
- Flag groups where $\text{Var}(H_d) < \varepsilon$

**Deliverables:**
- `figures/RL3/08a_entropy_variance_heatmap.png`
- `figures/RL3/08b_invariant_groups.png`
- `figures/RL3/08_animation.gif`
- `results/RL3/08_entropy_variance.csv`

---

## Milestone 3: Physical Realization

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

Identify one physical system (spin lattice, optical lattice, quantum circuit) where the entropy invariance class $\mathcal{F}$ appears naturally.

Candidate: **Ising model on $\mathbb{Z}_2 \times \mathbb{Z}_2$-symmetric lattice** at criticality.

---

## Milestone 4: Publication

![Status](https://img.shields.io/badge/Status-Pending-lightgrey)

**Target:** arXiv:math.CO + arXiv:cs.IT simultaneous submission.

**Title candidates:**
- "Omnidirectional Entropy Invariance Under Group Actions on Symbolic Spaces"
- "A Universal Class of Information-Symmetric Matrix Structures"

**Journal target:** *Information and Computation* or *Journal of Combinatorial Theory*

---

## Timeline (estimated)

| Milestone | Estimated effort |
|---|---|
| M1: Theorem RL3-T1 | 2–3 sessions |
| M2: EXP-08 simulation | 1 session |
| M3: Physical realization | 3–5 sessions |
| M4: Paper draft | 3–4 sessions |

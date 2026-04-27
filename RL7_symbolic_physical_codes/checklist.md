# Checklist: RL7 — Symbolic Codes and Physical Information

![Status](https://img.shields.io/badge/Phase-Speculative-orange?style=for-the-badge)
![Priority](https://img.shields.io/badge/Priority-Last-lightgrey?style=for-the-badge)
![Risk](https://img.shields.io/badge/Risk-High-red?style=for-the-badge)

> All claims at this stage must be labeled as formal analogies, not physical assertions.

---

## Phase 0: Foundation

- [x] Holographic principle: bulk encoded on boundary
- [x] Sator analogy: 9 free vars encode 25 positions
- [x] State Conjecture RL7-C1 (speculative)
- [x] Define the analogy chain explicitly

---

## Phase 1: Mathematical Correspondence

- [x] Formal analogy table: Fix(G) ↔ boundary state
- [ ] Compute $\kappa(G, n)$ for known holographic models
- [ ] Ryu-Takayanagi comparison
- [ ] One falsifiable prediction formulated

---

## Phase 2: Simulations

### EXP-14: Holographic Ratio Comparison
- [x] Compute $\kappa_{\text{sym}}$ for all 9 symbolic groups
- [x] Compare to $\kappa_{\text{holo}}(N)=1/N$ for $N \in \{2,\ldots,25\}$
- [x] Plot: `figures/RL7/14a_holographic_comparison.png`
- [x] Save: `results/RL7/14_symbolic_vs_holographic.csv`
- [x] Save: `results/RL7/14_holographic_catalog.csv`

---

## Phase 3: Publication

- [ ] All text labeled: "formal analogy"
- [ ] Falsification condition stated explicitly
- [ ] Submit to arXiv:hep-th with speculative notation

---

## Result Matrix

| Group | $\kappa_{\text{sym}}$ | Best match $N$ | $\kappa_{\text{holo}}(N)$ | $|\Delta\kappa|$ |
|---|---|---|---|---|
| Trivial $\{e\}$ | 1.00 | 2 | 0.50 | 0.50 |
| $\mathbb{Z}_2$ (R180) | 0.52 | 2 | 0.50 | 0.02 |
| **Klein (T,R180) Sator** | **0.36** | **3** | **0.333** | **0.027** |
| $\mathbb{Z}_4$ (R90) | 0.28 | 4 | 0.25 | 0.03 |
| $D_4$, $D_8$, $Z_2^3$ | 0.24 | 4 | 0.25 | 0.01 |

> **FINDING (formal analogy):** Sator $\kappa = 0.36 \approx 1/3 = \kappa_{\text{AdS/CFT}}(N=3)$.
> $D_4$ and $D_8$ map to $N=4$ in AdS/CFT with $|\Delta\kappa| = 0.01$ (closest match).
> **Interpretation:** If a quantum system had $G \cong D_4$ symmetry, its boundary in AdS$_3$ would require $\approx N=4$ holographic units.
> All claims remain speculative formal analogies until a falsifiable prediction is formulated.

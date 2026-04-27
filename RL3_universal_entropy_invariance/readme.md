# RL3 — Universal Entropy Invariance Class

![Status](https://img.shields.io/badge/Status-Open-lightgrey?style=for-the-badge)
![Domain](https://img.shields.io/badge/Domain-Statistical_Physics-blue?style=for-the-badge)
![Priority](https://img.shields.io/badge/Priority-Start_Here-success?style=for-the-badge)

## Core Question

> Is the Sator Square a member of a universal class of objects characterized by omnidirectional entropy parity?

$$\mathcal{F} = \{ M \in \Sigma^{n \times n} : H_d(M) = H_{d'}(M) \;\; \forall\, d, d' \in \mathcal{D} \}$$

## Why Start Here

This is the most tractable generalization. It requires no physics assumptions — only extending the mathematical result. If $\mathcal{F}$ is non-trivial and characterizable, it becomes the foundation for all other lines.

## Origin from Sator

We proved (Theorem 2 + EXP-02) that for the Sator Square:

$$|H_{\text{LR}} - H_{\text{RL}}| < \varepsilon_{\text{machine}} \approx 6.40 \times 10^{-16} \text{ bits}$$

This holds because WS ($M = M^T$) + CS ($M_{ij} = M_{4-i,4-j}$) force all reading directions to traverse the same multiset of symbols.

**Generalization question:** For which groups $G$ acting on $\Sigma^{n \times n}$ does $\text{Fix}(G)$ belong to $\mathcal{F}$?

## Formal Framing

**Theorem (RL3-T1, conjectured):** A matrix $M \in \text{Fix}(G)$ satisfies omnidirectional entropy parity if and only if every canonical reading direction $d$ induces the same symbol frequency multiset on $M$.

**Corollary:** Any group $G$ that includes both a transpose-like and a 180°-rotation-like element forces $M \in \mathcal{F}$ for all $M \in \text{Fix}(G)$.

## Generalization Dimensions

| Dimension | Sator | Generalization |
|---|---|---|
| Matrix size | $5 \times 5$ | $n \times n$ for arbitrary $n$ |
| Alphabet | 26 symbols | Any $\Sigma$ |
| Group | $\mathbb{Z}_2 \times \mathbb{Z}_2$ | Any finite group $G \leq S_{n^2}$ |
| Directions | 4 linear | Arbitrary directions (diagonals, spirals) |
| Domain | Symbolic | Physical fields on lattices |

## Key Questions

1. What is the minimum group $G$ that guarantees $\text{Fix}(G) \subset \mathcal{F}$?
2. Is $\mathcal{F}$ closed under direct product? ($M_1, M_2 \in \mathcal{F} \Rightarrow M_1 \otimes M_2 \in \mathcal{F}$?)
3. Does $\mathcal{F}$ appear in statistical physics? (e.g., spin systems on a lattice with dihedral symmetry)
4. Is there an analogous class in quantum systems (density matrices)?

## Connection to Physics

If $\mathcal{F}$ exists in physical systems, it means:

> **Systems with sufficient symmetry have reading-direction-independent information content** — the observer's perspective does not change the entropy measurement.

This is relevant to:
- Isotropy of physical laws
- Frame-independence in information theory
- Quantum contextuality

## Minimum Publishable Result

1. Characterization theorem: which groups $G$ guarantee $\text{Fix}(G) \subset \mathcal{F}$?
2. Computer search: catalogue of $\mathcal{F}$ members for small $n, |\Sigma|$
3. One physical or quantum-mechanical realization

## Open Tasks

- [ ] Prove RL3-T1 (or find counterexample)
- [ ] Implement search for $\mathcal{F}$ members for $n = 3, 4, 5$ and $|\Sigma| = 2, 3, 4$
- [ ] Survey: does classical spin models produce $\mathcal{F}$ members at criticality?
- [ ] Extend entropy directions to include diagonals and circular readings
- [ ] Write draft of Section 1

## Simulation Plan

```
EXP-08: Universal Entropy Invariance Search
- Input: group G, alphabet Σ, matrix size n
- Output: all M ∈ Fix(G) ∩ F, catalogue, statistics
- Figures: heatmap of H_d variance across groups
```

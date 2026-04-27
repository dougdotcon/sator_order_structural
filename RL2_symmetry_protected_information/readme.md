# RL2 — Symmetry-Protected Information

![Status](https://img.shields.io/badge/Status-Open-lightgrey?style=for-the-badge)
![Domain](https://img.shields.io/badge/Domain-Topology_/_QEC-blue?style=for-the-badge)

## Core Question

> Can information robustness emerge purely from structural constraints — without active redundancy, without energy cost?

## Origin from Sator

The Sator Square achieves $\rho(t=1) = 98.8\%$ recovery with zero active mechanism. There is no encoder, no parity check circuit, no energy expenditure. The robustness is entirely **passive** — a consequence of the orbit structure under $G \cong \mathbb{Z}_2 \times \mathbb{Z}_2$.

This suggests a class of structures where:

$$\text{protection} = f(\text{symmetry group}) \quad \text{not} \quad f(\text{active encoding})$$

## Formal Framing

**Definition (Symmetry-Protected Information Structure — SPIS):** A symbolic or physical system $\Sigma$ equipped with group $G$ acting on its state space, such that the recovery rate under stochastic perturbation $\epsilon$ satisfies:

$$\rho(\epsilon) \geq 1 - \epsilon \cdot \frac{1}{|G|} \cdot \text{correction}(G)$$

where $\text{correction}(G)$ depends only on the orbit structure of $G$, not on any active correction procedure.

**Conjecture (RL2-C1):** For any finite group $G$ acting on a symbolic space $\Sigma^n$, the symmetry-constrained subspace $\text{Fix}(G)$ is a SPIS with recovery rate bounded below by a function of $|G|$ and the minimum orbit size $d_{\min}^{\text{orb}}$.

## Connection to Known Physics

| Concept | Relation |
|---|---|
| Topological quantum codes | Protection via topological properties, not local symmetry |
| Symmetry-Protected Topological (SPT) phases | Ground state degeneracy protected by symmetry |
| Kitaev surface code | Passive error correction via topological redundancy |
| Sator (EXP-05, EXP-07) | Passive recovery from orbit structure, $d_{\min}^{\text{orb}} = 2$ |

## Distinction from Classical QEC

Classical QEC requires:
- Active syndrome measurement
- Correction gates (energy)
- Engineered Hamiltonian

SPIS conjecture requires only:
- Symmetry group acting on state space
- Sufficient orbit redundancy

## Key Inequality to Prove

$$\rho_{\text{SPIS}}(\epsilon) \geq \rho_{\text{random}}(\epsilon) \cdot |G|^{\alpha}$$

for some $\alpha > 0$ depending on the group action.

## Minimum Publishable Result

1. Formal definition of SPIS
2. Proof that $\text{Fix}(G)$ is always a SPIS (or counterexample)
3. Explicit formula for $\rho$ as a function of orbit sizes
4. One non-trivial physical realization

## Open Tasks

- [ ] Survey topological codes and SPT phases literature
- [ ] Generalize the $\rho(t)$ curve (EXP-05) to arbitrary finite groups $G$
- [ ] Prove or disprove RL2-C1
- [ ] Identify a quantum mechanical realization of a SPIS
- [ ] Compare with Kitaev code parameters

## Key References to Survey

- Kitaev, A. *Fault-tolerant quantum computation by anyons* (2003)
- Wen, X.-G. *Topological orders and edge excitations in FQH states* (1995)
- Nayak et al. *Non-Abelian anyons and topological quantum computation* (2008)

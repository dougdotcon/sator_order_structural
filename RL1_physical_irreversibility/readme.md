# RL1 — Physical-Informational Reversibility

![Status](https://img.shields.io/badge/Status-Open-lightgrey?style=for-the-badge)
![Domain](https://img.shields.io/badge/Domain-Thermodynamics_/_QM-blue?style=for-the-badge)

## Core Question

> Do physical subsystems exist that preserve information locally, despite global entropy growth?

$$\exists\; \mathcal{S} \subset \mathcal{U} \;\text{ such that }\; H(\mathcal{S}, t) = \text{const} \;\;\text{even when}\;\; H(\mathcal{U}, t) \uparrow$$

## Origin from Sator

The Sator result shows that a symbolic structure governed by $G \cong \mathbb{Z}_2 \times \mathbb{Z}_2$ retains full reconstructibility under noise — its orbit structure acts as a fixed informational skeleton.

The question is whether an analogous phenomenon occurs in physical systems: do symmetry-protected subsystems exist that behave like informational fixed points under thermodynamic evolution?

## Formal Framing

Define an **informationally reversible subsystem** $\mathcal{S}$ of universe $\mathcal{U}$ as:

$$\mathcal{S}^* = \{ \mathcal{S} \subset \mathcal{U} : \exists\, \mathcal{R}_t \text{ s.t. } \mathcal{R}_t(\mathcal{S}(t)) = \mathcal{S}(0) \}$$

where $\mathcal{R}_t$ is a recovery operator acting only on $\mathcal{S}$, not on $\mathcal{U}$.

**Conjecture (RL1-C1):** If $\mathcal{S}$ has a non-trivial symmetry group $G_\mathcal{S}$, then the orbit structure of $G_\mathcal{S}$ induces redundancy sufficient for partial reconstruction of $\mathcal{S}(0)$ from $\mathcal{S}(t)$ for small $t$.

## Connection to Known Physics

| Concept | Relation |
|---|---|
| Bekenstein-Hawking entropy | Information preserved on the boundary (holography) |
| Quantum error correction | Physical qubits with symmetry-based protection |
| TDTR (Fulber 2026) | Regime transitions are semigroup — but subsystems may remain group-reversible |
| Decoherence theory | Loss of phase information vs. loss of symbolic structure |

## What is Not Claimed

- We do NOT claim violation of the Second Law
- We do NOT claim global reversibility
- We claim only: **local informational stability under global entropy increase** is possible if the subsystem has sufficient symmetry

## Minimum Publishable Result

1. Formal definition of an informationally reversible subsystem
2. At least one physical model (e.g., quantum spin chain with dihedral symmetry) exhibiting the property
3. Bound on reconstruction fidelity as a function of group order $|G_\mathcal{S}|$

## Open Tasks

- [ ] Literature review: quantum error correction, symmetry-protected topological phases
- [ ] Identify candidate physical systems (Ising model, spin chains, quantum codes)
- [ ] Formalize the recovery operator $\mathcal{R}_t$ for a specific system
- [ ] Simulate: does orbit structure of $G$ predict $\rho(t)$ in physical noise models?
- [ ] Write Section 1 draft

## Key References to Survey

- Zurek, W. H. *Decoherence, einselection, and the quantum origins of the classical* (2003)
- Preskill, J. *Quantum Information and Computation* (1998)
- Fulber, D.H.M. *Thermodynamic Time Reversal* (TDTR, 2026)

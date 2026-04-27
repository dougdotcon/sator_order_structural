# RL5 — Local Arrow of Time Breaking

![Status](https://img.shields.io/badge/Status-Open-lightgrey?style=for-the-badge)
![Domain](https://img.shields.io/badge/Domain-QM_/_Decoherence-purple?style=for-the-badge)

## Core Question

> Do symmetry-protected informational structures exhibit local time-reversal, even within a globally irreversible system?

## Origin from Sator + TDTR

TDTR (Fulber 2026) establishes that physical regime transitions form a **semigroup** (irreversible):

$$T_{Q \to C} \neq T_{C \to Q}^{-1}$$

The Sator result shows that within a symbolic space, it is possible to construct a substructure where:

$$\mathcal{R}(\mathcal{T}(M)) = M$$

i.e., the composition of degradation with recovery is the identity — the structure is **locally group-reversible**, even though the ambient space is irreversible.

**Conjecture (RL5-C1):** Physical systems with sufficient internal symmetry can exhibit locally time-reversible information dynamics, even when embedded in a globally irreversible (semigroup) thermodynamic evolution.

## Formal Framing

Let $\mathcal{U}(t)$ be the global state under irreversible evolution (semigroup $\mathcal{S}$). Let $\mathcal{P} \subset \mathcal{U}$ be a subsystem.

**Definition (Local time-reversal):** $\mathcal{P}$ is locally time-reversible under $\mathcal{S}$ if:

$$\exists \mathcal{R}_\mathcal{P} : \mathcal{R}_\mathcal{P}(\mathcal{P}(t)) = \mathcal{P}(0) \quad \text{for } t \leq t^*$$

where $t^*$ is the coherence time of $\mathcal{P}$.

**Key:** $\mathcal{R}_\mathcal{P}$ operates only on $\mathcal{P}$, not on $\mathcal{U}$.

## Analogy Chain

| Level | Irreversible system | Reversible subsystem |
|---|---|---|
| Symbolic (Sator) | Full $\Sigma^{25}$ space | $\text{Fix}(G)$ under Isfet/Ma'at |
| Physical (classical) | Thermodynamic evolution | Poincaré recurrence in integrable subsystem |
| Physical (quantum) | Decoherence | Error-corrected logical qubit |
| TDTR | $T_{Q \to C}$ (semigroup) | Boundary subsystem preserving quantum info |

## What Would Break the Arrow Locally

Not the Second Law — which holds globally. But locally:

> A subsystem with $G$-symmetry may retain enough redundancy that $\mathcal{R}_\mathcal{P}$ can reconstruct its state — effectively reversing the local information flow despite the global entropy increase.

## Connection to Quantum Information

- Quantum error correction achieves this actively (with energy)
- RL5 asks: **can this occur passively**, as a structural consequence of symmetry?
- If yes: this defines a new class of physical objects — **passive local time-reversal structures**

## Minimum Publishable Result

1. Formal definition of locally time-reversible subsystem
2. Constructive existence proof (model with finite group)
3. Bound on $t^*$ (coherence time) as a function of $|G|$ and $d_{\min}^{\text{orb}}$
4. Connection to TDTR framework

## Open Tasks

- [ ] Formalize the definition of local time-reversal within TDTR language
- [ ] Identify candidate quantum systems (trapped ions, photonic lattices)
- [ ] Simulate: generate an orbit-structured matrix, apply stochastic perturbation, measure $t^*$
- [ ] Identify the critical perturbation rate at which local reversibility breaks
- [ ] Write formal connection to decoherence theory

## Key References to Survey

- Zurek, W.H. *Decoherence and the transition from quantum to classical* (1991)
- Plenio & Virmani *An introduction to entanglement measures* (2007)
- Fulber, D.H.M. *Thermodynamic Time Reversal* (TDTR, 2026) — directly relevant

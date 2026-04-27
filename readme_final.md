# Tamesis Research Program

![Program](https://img.shields.io/badge/Program-TAMESIS-purple?style=for-the-badge)
![Institution](https://img.shields.io/badge/UFRJ-Rio_de_Janeiro-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![Experiments](https://img.shields.io/badge/Experiments-EXP_01--15-blue?style=for-the-badge)

> Douglas H. M. Fulber — Universidade Federal do Rio de Janeiro, 2026

---

## Program Structure

```
sator_research/
├── ajuste_fino/           ← Phase 1–3: Sator Foundation (COMPLETE)
│   ├── index.html         ← Published paper (Tamesis format)
│   ├── readme.md          ← Sator program documentation
│   ├── simulations/       ← EXP-01 to EXP-07
│   ├── figures/           ← All Sator figures and GIFs
│   └── results/           ← All Sator numerical results
│
└── research_lines/        ← Phase 4: Generalization (ACTIVE)
    ├── readme.md          ← Master index of all 7 lines
    ├── DISCOVERY_universal_invariant.md  ← Key finding
    ├── run_all_research_lines.py         ← Master runner
    ├── RL1_physical_irreversibility/
    ├── RL2_symmetry_protected_information/
    ├── RL3_universal_entropy_invariance/
    ├── RL4_variational_information_principle/
    ├── RL5_local_arrow_of_time/
    ├── RL6_compression_limit/
    ├── RL7_symbolic_physical_codes/
    ├── figures/           ← All RL figures (EXP-08 to EXP-15)
    └── results/           ← All RL numerical results
```

---

## Phase 1–3: Sator Foundation (Complete)

**Directory:** `ajuste_fino/`

The Sator Square was formally characterized as a symmetry-constrained symbolic structure under:

$$G \cong \mathbb{Z}_2 \times \mathbb{Z}_2 \quad (Klein\ group)$$

| Result | Value | Type |
|---|---|---|
| Symmetry group | $G \cong \mathbb{Z}_2 \times \mathbb{Z}_2$ | Theorem |
| Independent orbits | 9 over $[5]^2$ | Proved |
| Compression | $26^{25} \to 26^9$ | Derived |
| $\|\Delta H_{\text{dir}}\|$ | $< 6.40 \times 10^{-16}$ bits | Computational |
| $d_{\min}^{\text{orb}}$ | 2 | Computed |
| Recovery $\rho(t=1)$ | $98.8\% \pm 1.8\%$ | Empirical |
| Upper bound $\|\Omega''\|$ | $\leq \|L_5^{\text{rev}}\|^2 \cdot \|L_5^{\text{pal}}\|$ | Proved |

**Published paper:** `ajuste_fino/index.html`

---

## Phase 4: Research Lines (Active)

**Directory:** `research_lines/`

7 research lines escalating from combinatorics to fundamental physics.

| RL | Title | EXP | Key Result |
|---|---|---|---|
| RL1 | Physical-Informational Reversibility | EXP-11 | $H(S)$ < $H(U)$ — local stability confirmed |
| RL2 | Symmetry-Protected Information | EXP-10 | $d_{\min}^{\text{orb}}=4 \Rightarrow \rho \geq 99.6\%$ |
| RL3 | Universal Entropy Invariance | EXP-08 | **13/13 groups in $\mathcal{F}$** |
| RL4 | Variational Information Principle | EXP-12 | $\mathcal{A}[M,G]$ exact identity |
| RL5 | Local Arrow of Time | EXP-13 | $r(d_{\min}^{\text{orb}}, t^*) = +0.87$ |
| RL6 | Fundamental Compression Limit | EXP-09 | Burnside LB violated — refined conjecture |
| RL7 | Symbolic Codes / Holography | EXP-14 | Sator $\kappa = 0.36 \approx 1/3 = \kappa_{\text{AdS}}(N=3)$ |

---

## Cross-Cutting Discovery

> $d_{\min}^{\text{orb}}$ predicts all structural metrics simultaneously across all research lines.

$$\text{corr}(d_{\min}^{\text{orb}},\, \rho) = +0.868 \qquad \text{corr}(d_{\min}^{\text{orb}},\, t^*) = +0.868$$

**See:** `research_lines/DISCOVERY_universal_invariant.md`

---

## Theoretical Framework

- **TAMESIS** — Spectral Geometry and Regime Transitions
- **TDTR** — Thermodynamic Time Reversal (Fulber 2026)
- **TRI** — Regime Incompatibility

All research lines connect to the TDTR framework:
the local group-reversibility of Fix(G) is the informational analog
of the boundary condition that TDTR posits at regime transitions.

---

## Running the Experiments

```powershell
# Run all RL experiments (EXP-08 to EXP-15)
python research_lines/run_all_research_lines.py

# Run a specific experiment
python research_lines/RL3_universal_entropy_invariance/simulations/EXP08_entropy_invariance.py
```

---

## Author

Douglas H. M. Fulber
Universidade Federal do Rio de Janeiro
April 2026

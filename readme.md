# Research Lines — Tamesis Program

![Lines](https://img.shields.io/badge/Research_Lines-7-blue?style=for-the-badge)
![Experiments](https://img.shields.io/badge/EXPs_Complete-7-success?style=for-the-badge)
![Discovery](https://img.shields.io/badge/Universal_Invariant-d_min_orb-red?style=for-the-badge)
![Institution](https://img.shields.io/badge/UFRJ-Tamesis-purple?style=for-the-badge)

> The Sator Square is not the destination. It is the proof of concept.

---

## Program Status

| ID | Title | EXP | Key Result | Status |
|---|---|---|---|---|
| [RL1](RL1_physical_irreversibility/readme.md) | Physical-Informational Reversibility | EXP-11 | Local $H(S)$ more ordered than global $H(U)$ | **Complete** |
| [RL2](RL2_symmetry_protected_information/readme.md) | Symmetry-Protected Information | EXP-10 | $d_{\min}^{\text{orb}}=4$ achieves $\rho\geq99.6\%$ | **Complete** |
| [RL3](RL3_universal_entropy_invariance/readme.md) | Universal Entropy Invariance Class | EXP-08 | **13/13 groups in $\mathcal{F}$** — universal | **Complete** |
| [RL4](RL4_variational_information_principle/readme.md) | Variational Information Principle | EXP-12 | $\mathcal{A}[M,G]$ exact identity, 14 groups | **Complete** |
| [RL5](RL5_local_arrow_of_time/readme.md) | Local Arrow of Time Breaking | EXP-13 | $d_{\min}^{\text{orb}}$ predicts $t^*$, $r=+0.87$ | **Complete** |
| [RL6](RL6_compression_limit/readme.md) | Fundamental Compression Limit | EXP-09 | Burnside LB violated — refined conjecture | **Complete** |
| [RL7](RL7_symbolic_physical_codes/readme.md) | Symbolic Codes and Physical Information | EXP-14 | Holographic comparison | Pending |

---

## ★ Cross-Cutting Discovery

**See full document:** [DISCOVERY_universal_invariant.md](DISCOVERY_universal_invariant.md)

**Emerged from EXP-15:** $d_{\min}^{\text{orb}}$ predicts all structural metrics simultaneously.

$$d_{\min}^{\text{orb}}(G) = \min_{\substack{O \in \text{orbits}(G) \\ |O|>1}} |O|$$

| Correlation | Value |
|---|---|
| $\text{corr}(d_{\min}^{\text{orb}},\;\rho(t=1))$ | $+0.868$ |
| $\text{corr}(d_{\min}^{\text{orb}},\;t^*)$ | $+0.868$ |
| $\text{corr}(d_{\min}^{\text{orb}},\;\mathcal{A})$ | $+0.825$ |
| $\text{corr}(d_{\min}^{\text{orb}},\;\kappa)$ | $-0.825$ |

Higher $d_{\min}^{\text{orb}}$ → better recovery, longer coherence, more action, lower compression ratio.

---

## Escalation Path (updated)

```
Sator (combinatorial result)
          │
          ▼
RL3: Entropy invariance generalize?    ✓ 13/13 groups in F
          │
          ▼
RL6: Universal compression bound?      ✓ Burnside violated — refined conjecture
          │
          ▼
RL2: Symmetry protect info passively?  ✓ d_orb=4 → ρ≥99.6%
          │
          ▼
RL1: Physical subsystems stable?       ✓ H(S) < H(U) confirmed
          │
          ▼
RL4: Variational principle?            ✓ A[M,G] = (n²-k)·log₂σ exact
          │
          ▼
RL5: Local arrow of time?              ✓ d_orb predicts t* (r=0.87)
          │
          ▼
★ UNIVERSAL INVARIANT: d_min_orb
          │
          ▼
RL7: Physical codes / holography?      → Pending (EXP-14)
```

---

## Shared Infrastructure

- **Core results:** `../simulations/` (EXP-01 to EXP-07) — Sator foundation
- **RL results:** `figures/`, `results/` — EXP-08 to EXP-15
- **Synthesis:** `figures/SYNTHESIS/15_universal_invariant.png`
- **Theoretical framework:** `../ajuste_fino/`
- **Published paper:** `../index.html`

---

## Files per Research Line

Each RL folder contains:

```
RL*/
├── readme.md      — core question, framing, open tasks
├── checklist.md   — live progress tracker
├── roadmap.md     — milestones and publication targets
└── simulations/   — Python scripts (EXP-NN_*.py)
```

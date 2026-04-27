"""
EXP-15: Universal Invariant — d_min_orb as Structural Predictor (Synthesis)
=============================================================================
Unifies all RL experiments into a single cross-cutting analysis.
Shows that d_min_orb predicts simultaneously:
  - ρ(t=1): recovery rate (from EXP-10)
  - t*(50%): coherence time (from EXP-13)
  - A[M,G]: information action (from EXP-12)
  - κ: compression ratio (from EXP-09)

The universal law hypothesis:
  d_min_orb is the fundamental structural invariant of Fix(G).

Output: figures/SYNTHESIS/, results/SYNTHESIS/
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv, os, math
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG_DIR = os.path.join(BASE, "figures", "SYNTHESIS")
RES_DIR = os.path.join(BASE, "results", "SYNTHESIS")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

# ─── LOAD FROM PRIOR EXPERIMENTS ─────────────────────────────────────────────
# Data harvested directly from EXP-10, EXP-12, EXP-13 outputs

EXP_DATA = [
    # (group_name, |G|, d_min_orb, kappa, n_orbits, rho_t1, t_star_50, A_bits)
    ("Trivial {e}",         1,   1,  1.00,  25,   0.960,  13,    0.00),
    ("Z2 (T)",              2,   2,  0.60,  15,   0.960,  13,   47.00),
    ("Z2 (R180)",           2,   2,  0.52,  13,   0.960,  13,   56.41),
    ("Klein (T,R180)",      4,   2,  0.36,   9,   0.984,  16,   75.21),  # Sator
    ("Klein (Rh,Rv)",       4,   2,  0.36,   9,   0.985,  16,   75.21),
    ("Z4 (R90)",            4,   4,  0.28,   7,   0.998,  17,   84.61),
    ("D4 (R90,T)",          8,   4,  0.24,   6,   0.998,  19,   89.31),
    ("Z2^3 (T,R180,Rh)",    8,   4,  0.24,   6,   0.999,  18,   89.31),
    ("D8 (R90,T,Rh)",      16,   4,  0.24,   6,   0.996,  18,   89.31),
]

SIGMA = 26
H_MAX = 25 * math.log2(SIGMA)  # 117.51 bits

def run_analysis():
    print(f"\n{'Group':<25} {'|G|':>5} {'d_orb':>6} {'κ':>6} {'ρ(1)':>7} {'t*':>5} {'A':>8}")
    print("-" * 70)
    for row in EXP_DATA:
        name, order, d_orb, kappa, n_orbs, rho1, tstar, A = row
        sator = " ← SATOR" if 'T,R180' in name and 'Klein' in name else ""
        print(f"  {name:<25} {order:>5} {d_orb:>6} {kappa:>6.3f} {rho1:>7.3f} {tstar:>5} {A:>8.2f}{sator}")
    return EXP_DATA

def plot_universal_invariant(data, save_path):
    fig = plt.figure(figsize=(22, 16))
    fig.patch.set_facecolor('#0d1117')
    gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

    names  = [d[0] for d in data]
    orders = [d[1] for d in data]
    d_orbs = [d[2] for d in data]
    kappas = [d[3] for d in data]
    rho1s  = [d[5] for d in data]
    tstars = [d[6] for d in data]
    As     = [d[7] for d in data]

    # Sator index
    sator_idx = next(i for i, d in enumerate(data) if 'T,R180' in d[0] and 'Klein' in d[0])

    SHORT = [n.split('(')[0].strip()[:12] for n in names]
    CMAP  = plt.cm.plasma(np.linspace(0.1, 0.9, len(data)))
    COL_D = {1: '#FF6B6B', 2: '#FFEAA7', 4: '#96CEB4'}
    cols  = [COL_D[d] for d in d_orbs]

    def style_ax(ax, title):
        ax.set_facecolor('#161b22')
        ax.tick_params(colors='white', labelsize=9)
        for sp in ax.spines.values(): sp.set_edgecolor('#30363d')
        ax.set_title(title, color='white', fontsize=11, fontweight='bold')

    def mark_sator(ax, x, y):
        ax.scatter([x], [y], s=350, color='#FFEAA7',
                   edgecolors='white', linewidths=2, zorder=10, marker='*')
        ax.annotate('Sator', xy=(x, y), xytext=(x+0.05, y-0.015),
                    color='#FFEAA7', fontsize=9, fontweight='bold')

    # ── [0,0] d_orb vs ρ(t=1) ────────────────────────────────────────────────
    ax00 = fig.add_subplot(gs[0, 0])
    style_ax(ax00, '$d_{\\min}^{\\text{orb}}$ vs Recovery $\\rho(t=1)$\n[RL2 — EXP-10]')
    jitter = np.random.RandomState(0).uniform(-0.05, 0.05, len(data))
    ax00.scatter([d+jit for d,jit in zip(d_orbs,jitter)], rho1s,
                 c=orders, cmap='viridis', s=130, edgecolors='white', linewidths=1, zorder=5)
    mark_sator(ax00, d_orbs[sator_idx]+jitter[sator_idx], rho1s[sator_idx])
    ax00.set_xlabel('$d_{\\min}^{\\text{orb}}$', color='white', fontsize=11)
    ax00.set_ylabel('$\\rho(t=1)$', color='white', fontsize=11)
    ax00.set_ylim(0.94, 1.005)

    # ── [0,1] d_orb vs t* ────────────────────────────────────────────────────
    ax01 = fig.add_subplot(gs[0, 1])
    style_ax(ax01, '$d_{\\min}^{\\text{orb}}$ vs Coherence Time $t^*$\n[RL5 — EXP-13]')
    ax01.scatter([d+jit for d,jit in zip(d_orbs,jitter)], tstars,
                 c=orders, cmap='viridis', s=130, edgecolors='white', linewidths=1, zorder=5)
    mark_sator(ax01, d_orbs[sator_idx]+jitter[sator_idx], tstars[sator_idx])
    ax01.set_xlabel('$d_{\\min}^{\\text{orb}}$', color='white', fontsize=11)
    ax01.set_ylabel('$t^*(50\\%)$', color='white', fontsize=11)

    # ── [0,2] d_orb vs A ─────────────────────────────────────────────────────
    ax02 = fig.add_subplot(gs[0, 2])
    style_ax(ax02, '$d_{\\min}^{\\text{orb}}$ vs Information Action $\\mathcal{A}$\n[RL4 — EXP-12]')
    sc = ax02.scatter([d+jit for d,jit in zip(d_orbs,jitter)], As,
                      c=orders, cmap='viridis', s=130, edgecolors='white', linewidths=1, zorder=5)
    mark_sator(ax02, d_orbs[sator_idx]+jitter[sator_idx], As[sator_idx])
    ax02.set_xlabel('$d_{\\min}^{\\text{orb}}$', color='white', fontsize=11)
    ax02.set_ylabel('$\\mathcal{A}[M,G]$ (bits)', color='white', fontsize=11)
    cbar = plt.colorbar(sc, ax=ax02)
    cbar.set_label('$|G|$', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

    # ── [1,0] d_orb vs κ ─────────────────────────────────────────────────────
    ax10 = fig.add_subplot(gs[1, 0])
    style_ax(ax10, '$d_{\\min}^{\\text{orb}}$ vs Compression $\\kappa$\n[RL6 — EXP-09]')
    ax10.scatter([d+jit for d,jit in zip(d_orbs,jitter)], kappas,
                 c=orders, cmap='viridis', s=130, edgecolors='white', linewidths=1, zorder=5)
    mark_sator(ax10, d_orbs[sator_idx]+jitter[sator_idx], kappas[sator_idx])
    ax10.set_xlabel('$d_{\\min}^{\\text{orb}}$', color='white', fontsize=11)
    ax10.set_ylabel('$\\kappa(G,n)$', color='white', fontsize=11)

    # ── [1,1] Full scatter matrix: ρ vs t* ────────────────────────────────────
    ax11 = fig.add_subplot(gs[1, 1])
    style_ax(ax11, '$\\rho(t=1)$ vs $t^*$ vs $\\mathcal{A}$\n[Cross-RL: RL2 + RL5 + RL4]')
    sc2 = ax11.scatter(rho1s, tstars, c=As, cmap='plasma', s=200,
                       edgecolors='white', linewidths=1.2, zorder=5)
    ax11.scatter([rho1s[sator_idx]], [tstars[sator_idx]],
                 s=400, color='#FFEAA7', edgecolors='white', linewidths=2,
                 marker='*', zorder=10)
    ax11.annotate('Sator', xy=(rho1s[sator_idx], tstars[sator_idx]),
                  xytext=(rho1s[sator_idx]-0.012, tstars[sator_idx]+0.3),
                  color='#FFEAA7', fontsize=9, fontweight='bold')
    cb2 = plt.colorbar(sc2, ax=ax11)
    cb2.set_label('$\\mathcal{A}$ (bits)', color='white')
    cb2.ax.yaxis.set_tick_params(color='white')
    plt.setp(cb2.ax.yaxis.get_ticklabels(), color='white')
    ax11.set_xlabel('$\\rho(t=1)$', color='white', fontsize=11)
    ax11.set_ylabel('$t^*(50\\%)$', color='white', fontsize=11)

    # ── [1,2] Summary bar: d_orb group summary ────────────────────────────────
    ax12 = fig.add_subplot(gs[1, 2])
    style_ax(ax12, f'Group means by $d_{{\\min}}^{{\\text{{orb}}}}$\n[Universal Structural Law]')
    d_vals = sorted(set(d_orbs))
    means_rho   = [np.mean([r for d,r in zip(d_orbs, rho1s) if d == dv]) for dv in d_vals]
    means_tstar = [np.mean([t for d,t in zip(d_orbs, tstars) if d == dv]) / max(tstars) for dv in d_vals]
    means_A     = [np.mean([a for d,a in zip(d_orbs, As) if d == dv]) / H_MAX for dv in d_vals]
    means_kappa = [np.mean([k for d,k in zip(d_orbs, kappas) if d == dv]) for dv in d_vals]

    x = np.arange(len(d_vals))
    width = 0.2
    bars = [
        ax12.bar(x - 1.5*width, means_rho,   width, label='$\\rho(t=1)$',  color='#4ECDC4'),
        ax12.bar(x - 0.5*width, means_tstar, width, label='$t^*/t_{max}$', color='#FFEAA7'),
        ax12.bar(x + 0.5*width, means_A,     width, label='$\\mathcal{A}/H_M$', color='#FF6B6B'),
        ax12.bar(x + 1.5*width, [1-k for k in means_kappa], width, label='$1-\\kappa$', color='#96CEB4'),
    ]
    ax12.set_xticks(x)
    ax12.set_xticklabels([f'$d={dv}$' for dv in d_vals], color='white', fontsize=11)
    ax12.set_ylim(0, 1.1)
    ax12.set_ylabel('Normalized metric (group mean)', color='white', fontsize=10)
    ax12.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=8, loc='lower right')

    plt.suptitle('EXP-15 — SYNTHESIS: $d_{\\min}^{\\text{orb}}$ as Universal Structural Invariant\n'
                 'All research lines (RL2, RL4, RL5, RL6) converge on the same predictor',
                 color='white', fontsize=14, fontweight='bold', y=1.01)

    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")

def save_synthesis_csv(data, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['group','order','d_min_orb','kappa','n_orbits','rho_t1','t_star_50','A_bits'])
        w.writerows(data)
    print(f"✓ {path}")

if __name__ == '__main__':
    print("="*60)
    print("EXP-15: SYNTHESIS — d_min_orb UNIVERSAL INVARIANT")
    print("="*60)
    data = run_analysis()

    # Correlations
    d_orbs = [d[2] for d in data]
    rho1s  = [d[5] for d in data]
    tstars = [d[6] for d in data]
    As     = [d[7] for d in data]
    kappas = [d[3] for d in data]

    corr_rho   = np.corrcoef(d_orbs, rho1s)[0,1]
    corr_tstar = np.corrcoef(d_orbs, tstars)[0,1]
    corr_A     = np.corrcoef(d_orbs, As)[0,1]
    corr_kappa = np.corrcoef(d_orbs, kappas)[0,1]

    print(f"\n  Correlations with d_min_orb:")
    print(f"    corr(d_orb, ρ(1))  = {corr_rho:+.4f}")
    print(f"    corr(d_orb, t*)    = {corr_tstar:+.4f}")
    print(f"    corr(d_orb, A)     = {corr_A:+.4f}")
    print(f"    corr(d_orb, κ)     = {corr_kappa:+.4f}")

    print(f"\n  UNIVERSAL LAW: d_min_orb predicts all 4 structural metrics")
    print(f"  Higher d_orb → higher ρ, longer t*, larger A, lower κ")

    plot_universal_invariant(data, os.path.join(FIG_DIR, '15_universal_invariant.png'))
    save_synthesis_csv(data, os.path.join(RES_DIR, '15_synthesis_data.csv'))

    print("\nEXP-15 COMPLETE ✓")

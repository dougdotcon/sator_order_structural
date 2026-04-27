"""
EXP-14: Symbolic Codes and Physical Information — Holographic Comparison (RL7)
===============================================================================
Formal analogy between:
  - Symbolic: κ(G,n) = |orbits| / n²
  - Holographic: κ_holo = boundary_dof / bulk_dof for AdS/CFT

In AdS_{d+1}/CFT_d on an N-site lattice:
  bulk sites  ≈ N^d
  boundary sites ≈ N^(d-1)
  κ_holo(N, d) = N^(d-1) / N^d = 1/N

Compares κ_symbolic (from EXP-09) to κ_holographic for:
  AdS₂/CFT₁ (d=1): κ = 1/N
  AdS₃/CFT₂ (d=2): κ = 1/N (boundary/bulk in 2d disk → N perimeter / N² area)
  AdS₄/CFT₃ (d=3): κ = N²/N³ = 1/N
  Large-N matrix models: κ = 1/N²

Identifies which holographic scenario matches each symbolic group.

ALL claims are labeled as formal analogies, not physical assertions.

Output: figures/RL7/, results/RL7/
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv, os, math

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIG_DIR = os.path.join(BASE, "figures", "RL7")
RES_DIR = os.path.join(BASE, "results", "RL7")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

# ─── SYMBOLIC κ DATA (from EXP-09) ──────────────────────────────────────────

SYMBOLIC_GROUPS = [
    # (name, |G|, κ at n=5, n_orbits)
    ("Trivial {e}",          1,   1.00,  25),
    ("Z2 (T)",               2,   0.60,  15),
    ("Z2 (R180)",            2,   0.52,  13),
    ("Klein (T,R180)",       4,   0.36,   9),   # Sator
    ("Klein (Rh,Rv)",        4,   0.36,   9),
    ("Z4 (R90)",             4,   0.28,   7),
    ("D4 (R90,T)",           8,   0.24,   6),
    ("Z2^3 (T,R180,Rh)",     8,   0.24,   6),
    ("D8 (R90,T,Rh)",       16,   0.24,   6),
]

# ─── HOLOGRAPHIC κ MODELS ────────────────────────────────────────────────────

def kappa_AdS(N, d):
    """
    Discrete lattice analogy of AdS_{d+1}/CFT_d.
    Bulk: N^d sites, Boundary: N^(d-1) sites.
    κ_holo = N^(d-1) / N^d = 1/N.
    Note: this is the same for all d, which reflects the universal
    holographic compression law.
    """
    return 1.0 / N

def kappa_matrix_model(N):
    """
    Large-N matrix model: N×N matrix has N² entries,
    boundary = diagonal = N entries → κ = 1/N.
    The SU(N) adjoint has N²-1 bulk, N-1 boundary.
    Approximation: κ ≈ 1/N.
    """
    return 1.0 / N

def kappa_bulk_defect(N):
    """
    Defect CFT with codimension 1:
    bulk = N^d, defect = N^(d-1) / 2.
    For d=2: κ = N/2N² = 1/(2N).
    """
    return 1.0 / (2 * N)

def build_holographic_catalog(N_range=range(2, 26)):
    """
    For each N, compute κ for:
    - AdS/CFT (all d, same formula: 1/N)
    - Matrix model: 1/N
    - Defect CFT: 1/(2N)
    """
    catalog = []
    for N in N_range:
        catalog.append({
            'N': N,
            'kappa_AdSCFT': kappa_AdS(N, 2),
            'kappa_matrix': kappa_matrix_model(N),
            'kappa_defect': kappa_bulk_defect(N),
        })
    return catalog

def find_best_match(kappa_sym, holo_catalog):
    """Find the N in holographic catalog closest to kappa_sym."""
    best_N = None; best_delta = float('inf')
    for entry in holo_catalog:
        delta = abs(entry['kappa_AdSCFT'] - kappa_sym)
        if delta < best_delta:
            best_delta = delta
            best_N = entry['N']
    return best_N, best_delta

# ─── MAIN ANALYSIS ───────────────────────────────────────────────────────────

def run_analysis():
    holo_catalog = build_holographic_catalog()
    results = []

    print(f"\n  FORMAL ANALOGY: κ_symbolic ↔ κ_holographic")
    print(f"\n{'Group':<25} {'|G|':>5} {'κ_sym':>8} {'Best N':>8} {'κ_holo(N)':>12} {'|Δκ|':>10}")
    print("-" * 75)

    for name, order, kappa_sym, n_orbs in SYMBOLIC_GROUPS:
        best_N, delta = find_best_match(kappa_sym, holo_catalog)
        kappa_holo = kappa_AdS(best_N, 2)
        sator = " ← SATOR" if 'T,R180' in name and 'Klein' in name else ""
        results.append({
            'group': name,
            'order': order,
            'kappa_sym': kappa_sym,
            'n_orbits': n_orbs,
            'best_N': best_N,
            'kappa_holo': kappa_holo,
            'delta_kappa': delta,
        })
        print(f"  {name:<25} {order:>5} {kappa_sym:>8.4f} {best_N:>8} {kappa_holo:>12.4f} {delta:>10.4f}{sator}")

    print(f"\n  CONJECTURE (RL7-C1, speculative):")
    print(f"  If a quantum system with group G has κ_sym(G,n) = κ_holo(N),")
    print(f"  its holographic boundary requires exactly |orbits(G)| = {SYMBOLIC_GROUPS[3][3]} degrees of freedom")
    print(f"  (analogous to the {SYMBOLIC_GROUPS[3][1]} Sator group with N_holo ≈ {next(r['best_N'] for r in results if 'T,R180' in r['group'])} in AdS/CFT).")
    return results, holo_catalog

# ─── VISUALIZATIONS ──────────────────────────────────────────────────────────

def plot_comparison(results, holo_catalog, save_path):
    fig = plt.figure(figsize=(22, 10))
    fig.patch.set_facecolor('#0d1117')
    gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.35)

    N_vals       = [h['N'] for h in holo_catalog]
    kappa_holo   = [h['kappa_AdSCFT'] for h in holo_catalog]
    kappa_matrix = [h['kappa_matrix'] for h in holo_catalog]
    kappa_defect = [h['kappa_defect'] for h in holo_catalog]

    sym_kappas = [r['kappa_sym'] for r in results]
    sym_orders = [r['order'] for r in results]
    sym_names  = [r['group'].split('(')[0].strip()[:15] for r in results]
    sator_idx  = next(i for i, r in enumerate(results) if 'T,R180' in r['group'])

    # ── Plot 1: κ curves — symbolic vs holographic ───────────────────────────
    ax = fig.add_subplot(gs[0])
    ax.set_facecolor('#161b22')

    # Holographic curves
    ax.plot(N_vals, kappa_holo, color='#FF6B6B', lw=2.5, label='AdS/CFT ($\\kappa=1/N$)')
    ax.plot(N_vals, kappa_matrix, color='#FFEAA7', lw=2, ls='--', label='Matrix model ($\\kappa=1/N$)')
    ax.plot(N_vals, kappa_defect, color='#FF9F43', lw=2, ls=':', label='Defect CFT ($\\kappa=1/2N$)')

    # Symbolic group values as horizontal lines
    yl_used = set()
    cmap = plt.cm.viridis(np.linspace(0.1, 0.9, len(results)))
    for i, r in enumerate(results):
        kappa = r['kappa_sym']
        if round(kappa, 4) not in yl_used:
            ax.axhline(kappa, color=cmap[i], lw=1.5, alpha=0.7,
                       label=f"{r['group'].split('(')[0].strip()} κ={kappa:.2f}")
            yl_used.add(round(kappa, 4))

    # Mark Sator intersection
    N_sator = results[sator_idx]['best_N']
    ax.scatter([N_sator], [results[sator_idx]['kappa_sym']],
               s=300, color='#FFEAA7', edgecolors='white', linewidths=2, zorder=10, marker='*')
    ax.annotate(f'Sator ↔ N={N_sator}\n$\\kappa=0.36$',
                xy=(N_sator, results[sator_idx]['kappa_sym']),
                xytext=(N_sator+1.5, results[sator_idx]['kappa_sym']+0.04),
                color='#FFEAA7', fontsize=9, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#FFEAA7', lw=1.5))

    ax.set_xlabel('Holographic scale $N$ (AdS radius / lattice size)', color='white', fontsize=11)
    ax.set_ylabel('$\\kappa$ (compression ratio)', color='white', fontsize=11)
    ax.set_title('Symbolic $\\kappa_{\\text{sym}}$ vs Holographic $\\kappa_{\\text{holo}}(N)$\n'
                 '[Formal analogy — not physical claim]',
                 color='white', fontsize=11, fontweight='bold')
    ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=7.5,
              loc='upper right', ncol=1)
    ax.set_xlim(2, 20); ax.set_ylim(0, 0.75)
    ax.tick_params(colors='white')
    for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 2: Best-match N per group ────────────────────────────────────────
    ax2 = fig.add_subplot(gs[1])
    ax2.set_facecolor('#161b22')
    best_Ns = [r['best_N'] for r in results]
    deltas  = [r['delta_kappa'] for r in results]

    sc = ax2.scatter(sym_kappas, best_Ns, c=sym_orders, cmap='viridis',
                     s=200, edgecolors='white', linewidths=1.5, zorder=5)
    for i, r in enumerate(results):
        ax2.annotate(sym_names[i],
                     xy=(sym_kappas[i], best_Ns[i]),
                     xytext=(sym_kappas[i]+0.01, best_Ns[i]+0.15),
                     color='#adb5bd', fontsize=7.5)
    ax2.scatter([results[sator_idx]['kappa_sym']], [results[sator_idx]['best_N']],
                s=400, color='#FFEAA7', edgecolors='white', linewidths=2, marker='*', zorder=10)
    cbar = plt.colorbar(sc, ax=ax2)
    cbar.set_label('$|G|$', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')
    ax2.set_xlabel('$\\kappa_{\\text{sym}}$ (symbolic group)', color='white', fontsize=11)
    ax2.set_ylabel('Best-match holographic $N$', color='white', fontsize=11)
    ax2.set_title('Symbolic Group → Holographic Scale $N$\n$\\kappa_{\\text{sym}} \\approx 1/N$ [analogy]',
                  color='white', fontsize=11, fontweight='bold')
    ax2.tick_params(colors='white')
    for sp in ax2.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 3: Analogy table as visual ──────────────────────────────────────
    ax3 = fig.add_subplot(gs[2])
    ax3.set_facecolor('#161b22')
    ax3.axis('off')

    analogy_rows = [
        ["Symbolic (Fix(G))", "Holographic (AdS/CFT)"],
        ["$\\text{Fix}(G) \\subset \\Sigma^{n^2}$", "Boundary state $\\mathcal{H}_{\\partial}$"],
        ["$|\\text{orbits}(G)|$ free vars", "Boundary d.o.f. $N^{d-1}$"],
        ["$n^2$ total positions", "Bulk d.o.f. $N^d$"],
        ["$\\kappa = |\\text{orb}|/n^2$", "$\\kappa_{\\text{holo}} = 1/N$"],
        ["$d_{\\min}^{\\text{orb}}$", "Bulk reconstruction depth"],
        ["$\\mathcal{A}[M,G]$", "$S_{\\text{bulk}} - S_{\\partial}$"],
        ["Ma'at recovery", "Bulk-to-boundary operator"],
        ["Klein (Sator): $\\kappa=0.36$", "$N_{\\text{holo}} \\approx 3$"],
    ]

    cell_colors = [['#21262d', '#21262d']] + \
                  [['#161b22', '#161b22']] * (len(analogy_rows) - 1)
    cell_colors[0] = ['#2d333b', '#2d333b']  # header

    table = ax3.table(
        cellText=analogy_rows,
        colLabels=None,
        cellLoc='center',
        loc='center',
        cellColours=cell_colors,
    )
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 1.8)

    for (row, col), cell in table.get_celld().items():
        cell.set_edgecolor('#30363d')
        cell.set_text_props(color='white' if row > 0 else '#FFEAA7',
                            fontweight='bold' if row == 0 else 'normal')

    ax3.set_title('Formal Analogy Table\n[EXP-14 — RL7, speculative]',
                  color='white', fontsize=11, fontweight='bold', pad=20)

    plt.suptitle('EXP-14 — RL7: Symbolic Codes and Physical Information\n'
                 'Formal analogy between $\\kappa_{\\text{sym}}(G,n)$ and holographic $\\kappa_{\\text{holo}}(N)$ [analogy only]',
                 color='white', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")

def save_csv(results, holo_catalog, path_sym, path_holo):
    with open(path_sym, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['group','order','kappa_sym','n_orbits','best_N','kappa_holo','delta_kappa'])
        w.writeheader(); w.writerows(results)
    with open(path_holo, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['N','kappa_AdSCFT','kappa_matrix','kappa_defect'])
        w.writeheader(); w.writerows(holo_catalog)
    print(f"✓ {path_sym}"); print(f"✓ {path_holo}")

if __name__ == '__main__':
    print("="*60)
    print("EXP-14: HOLOGRAPHIC COMPARISON (RL7)")
    print("ALL FINDINGS ARE FORMAL ANALOGIES ONLY")
    print("="*60)
    results, holo_catalog = run_analysis()

    plot_comparison(results, holo_catalog,
                    os.path.join(FIG_DIR, '14a_holographic_comparison.png'))
    save_csv(results, holo_catalog,
             os.path.join(RES_DIR, '14_symbolic_vs_holographic.csv'),
             os.path.join(RES_DIR, '14_holographic_catalog.csv'))
    print("\nEXP-14 COMPLETE ✓")
    print("DISCLAIMER: All analogies above are speculative formal correspondences.")
    print("No physical claim is made without a falsifiable prediction.")

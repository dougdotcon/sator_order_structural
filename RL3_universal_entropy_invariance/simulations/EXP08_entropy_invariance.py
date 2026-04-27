"""
EXP-08: Universal Entropy Invariance Class — RL3
=================================================
Tests which finite groups G, acting on [n]^2, guarantee
that Fix(G) ⊂ F (omnidirectional entropy parity class).

For each group G in a catalog:
  1. Compute orbits of G acting on [5]^2
  2. Generate 200 random matrices in Fix(G)
  3. Measure Var(H_d) across 4 reading directions
  4. Flag groups where Var(H_d) < epsilon

Output:
  figures/RL3/ — heatmaps, bar charts, GIF
  results/RL3/ — CSV catalog
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
import csv, os, math
from collections import Counter
from itertools import permutations

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIG_DIR = os.path.join(BASE, "figures", "RL3")
RES_DIR = os.path.join(BASE, "results", "RL3")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

N = 5
EPSILON = 1e-10
RNG = np.random.RandomState(42)

# ─── ORBIT ENGINE ────────────────────────────────────────────────────────────

def orbits_from_generators(generators, positions):
    """Compute orbit partition of positions under <generators>."""
    visited = set()
    orbits = []
    pos_set = set(positions)

    def closure(pos):
        """BFS to find full orbit of pos."""
        orbit = set()
        queue = [pos]
        while queue:
            p = queue.pop()
            if p in orbit: continue
            orbit.add(p)
            for g in generators:
                np_ = g(p)
                if np_ in pos_set and np_ not in orbit:
                    queue.append(np_)
        return frozenset(orbit)

    for pos in positions:
        if pos in visited: continue
        orb = closure(pos)
        orbits.append(orb)
        visited.update(orb)
    return sorted(orbits, key=lambda o: min(o))

def build_fix_g(orbits, n_positions=25, n=N):
    """Build a random matrix in Fix(G) given orbits. Orbits contain (i,j) tuples."""
    M = [None] * n_positions
    for orb in orbits:
        val = RNG.randint(0, 26)
        for pos in orb:
            idx = pos[0] * n + pos[1] if isinstance(pos, tuple) else pos
            M[idx] = val
    return M

def pos_to_idx(i, j, n=N):
    return i * n + j

def idx_to_pos(idx, n=N):
    return (idx // n, idx % n)

# ─── GROUPS TO TEST ──────────────────────────────────────────────────────────

def make_group_catalog():
    """
    Catalog of groups defined by their generators acting on [5]^2.
    Each entry: (name, order, generators_as_functions)
    """
    positions = [(i,j) for i in range(N) for j in range(N)]

    def T(p):   return (p[1], p[0])           # Transpose
    def R180(p): return (N-1-p[0], N-1-p[1])  # Rotation 180°
    def R90(p):  return (p[1], N-1-p[0])      # Rotation 90°
    def Rh(p):   return (p[0], N-1-p[1])      # Horizontal reflection
    def Rv(p):   return (N-1-p[0], p[1])      # Vertical reflection
    def Rd(p):   return (N-1-p[1], N-1-p[0]) # Anti-diagonal reflection
    def Id(p):   return p

    catalog = [
        ("Trivial {e}",           1,  [Id]),
        ("Z2 (Transpose)",        2,  [T]),
        ("Z2 (R180)",             2,  [R180]),
        ("Z2 (Horiz refl)",       2,  [Rh]),
        ("Z2 (Vert refl)",        2,  [Rv]),
        ("Klein Z2×Z2 (T,R180)",  4,  [T, R180]),   # ← Sator group
        ("Klein Z2×Z2 (Rh,Rv)",   4,  [Rh, Rv]),
        ("Z2×Z2 (T,Rh)",          4,  [T, Rh]),
        ("Z4 (R90)",              4,  [R90]),
        ("D4 (R90,T)",            8,  [R90, T]),
        ("D4 (R90,Rh)",           8,  [R90, Rh]),
        ("Z2×Z2×Z2 (T,R180,Rh)", 8,  [T, R180, Rh]),
        ("D8 (R90,T,Rh)",        16, [R90, T, Rh]),
    ]
    return catalog, positions

# ─── ENTROPY MEASUREMENT ─────────────────────────────────────────────────────

def shannon_H(symbols):
    if not symbols: return 0.0
    cnt = Counter(symbols)
    n = len(symbols)
    return -sum((c/n)*math.log2(c/n) for c in cnt.values() if c > 0)

def read_directions(M_flat, n=N):
    """Return symbol lists for 4 canonical reading directions."""
    M = [[M_flat[i*n+j] for j in range(n)] for i in range(n)]
    LR = [M[i][j] for i in range(n) for j in range(n)]
    RL = [M[i][n-1-j] for i in range(n) for j in range(n)]
    TB = [M[i][j] for j in range(n) for i in range(n)]
    BT = [M[n-1-i][j] for j in range(n) for i in range(n)]
    return LR, RL, TB, BT

def measure_entropy_variance(orbits, n_samples=300):
    """
    For n_samples random matrices in Fix(G), measure mean and variance of
    H_d across 4 directions. Returns (mean_H, std_H, mean_var_across_dirs).
    """
    all_H = []
    all_var = []
    for _ in range(n_samples):
        M = build_fix_g(orbits)
        dirs = read_directions(M)
        Hs = [shannon_H(d) for d in dirs]
        all_H.append(np.mean(Hs))
        all_var.append(np.var(Hs))
    return float(np.mean(all_H)), float(np.std(all_H)), float(np.mean(all_var))

# ─── MAIN ANALYSIS ───────────────────────────────────────────────────────────

def run_analysis():
    catalog, positions = make_group_catalog()
    results = []

    print(f"{'Group':<30} {'Order':>5} {'Orbits':>7} {'κ':>6} {'H_mean':>8} {'Var(H_d)':>12} {'In F?':>8}")
    print("-" * 82)

    for name, order, generators in catalog:
        orbs = orbits_from_generators(generators, positions)
        n_orbits = len(orbs)
        kappa = n_orbits / (N*N)
        mean_H, std_H, mean_var = measure_entropy_variance(orbs, n_samples=300)
        in_F = mean_var < EPSILON

        results.append({
            'group': name,
            'order': order,
            'n_orbits': n_orbits,
            'kappa': kappa,
            'H_mean': mean_H,
            'H_std': std_H,
            'mean_var_Hd': mean_var,
            'in_F': in_F,
            'orbits': [sorted(o) for o in orbs],
        })
        marker = "✓" if in_F else "✗"
        print(f"{name:<30} {order:>5} {n_orbits:>7} {kappa:>6.3f} {mean_H:>8.4f} {mean_var:>12.2e} {marker:>8}")

    return results

# ─── VISUALIZATIONS ──────────────────────────────────────────────────────────

def plot_main(results, save_path_base):
    groups   = [r['group'] for r in results]
    orders   = [r['order'] for r in results]
    kappas   = [r['kappa'] for r in results]
    vars_Hd  = [r['mean_var_Hd'] for r in results]
    in_F     = [r['in_F'] for r in results]
    n_orbits = [r['n_orbits'] for r in results]

    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.patch.set_facecolor('#0d1117')

    COLS_F   = ['#96CEB4' if f else '#FF6B6B' for f in in_F]
    COLS_ORD = plt.cm.viridis(np.linspace(0.2, 0.9, len(groups)))

    short_names = [g.split('(')[0].strip() for g in groups]

    # ── Plot 1: Var(H_d) per group ───────────────────────────────────────────
    ax = axes[0]
    ax.set_facecolor('#161b22')
    x = np.arange(len(groups))
    bars = ax.bar(x, vars_Hd, color=COLS_F, edgecolor='#30363d', width=0.7)
    ax.axhline(EPSILON, color='white', lw=1.5, ls='--', label=f'$\\varepsilon = 10^{{-10}}$')
    ax.set_yscale('symlog', linthresh=1e-15)
    ax.set_xticks(x)
    ax.set_xticklabels(short_names, rotation=45, ha='right', color='white', fontsize=7)
    ax.set_ylabel('$\\overline{\\text{Var}(H_d)}$', color='white', fontsize=11)
    ax.set_title('Direcional Entropy Variance\nby Group — $\\mathcal{F}$ membership test',
                 color='white', fontsize=11, fontweight='bold')
    ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
    ax.tick_params(colors='white')
    for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    patch_yes = mpatches.Patch(color='#96CEB4', label='In $\\mathcal{F}$ (invariant)')
    patch_no  = mpatches.Patch(color='#FF6B6B', label='Not in $\\mathcal{F}$')
    ax.legend(handles=[patch_yes, patch_no], facecolor='#21262d',
              edgecolor='#30363d', labelcolor='white', fontsize=8, loc='upper right')

    # ── Plot 2: κ vs Var(H_d) scatter ────────────────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor('#161b22')
    sc = ax2.scatter(kappas, vars_Hd, c=orders, cmap='viridis',
                     s=120, edgecolors='white', linewidths=0.8, zorder=5)
    ax2.set_yscale('symlog', linthresh=1e-15)
    ax2.axhline(EPSILON, color='white', lw=1.5, ls='--', alpha=0.7)
    ax2.set_xlabel('$\\kappa = \\text{orbits}/n^2$', color='white', fontsize=11)
    ax2.set_ylabel('$\\overline{\\text{Var}(H_d)}$', color='white', fontsize=11)
    ax2.set_title('$\\kappa$ vs Entropy Variance\n(color = group order)',
                  color='white', fontsize=11, fontweight='bold')
    cbar = plt.colorbar(sc, ax=ax2)
    cbar.set_label('Group order $|G|$', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')
    ax2.tick_params(colors='white')
    for sp in ax2.spines.values(): sp.set_edgecolor('#30363d')

    # Annotate Sator point
    sator_r = next(r for r in results if 'Klein' in r['group'] and 'T,R180' in r['group'])
    ax2.annotate('Sator / Klein\n$G\\cong\\mathbb{Z}_2\\times\\mathbb{Z}_2$',
                 xy=(sator_r['kappa'], sator_r['mean_var_Hd']),
                 xytext=(sator_r['kappa']+0.05, sator_r['mean_var_Hd']*100),
                 color='#FFEAA7', fontsize=8, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#FFEAA7', lw=1.5))

    # ── Plot 3: Orbit count per group ─────────────────────────────────────────
    ax3 = axes[2]
    ax3.set_facecolor('#161b22')
    bars3 = ax3.bar(x, n_orbits, color=COLS_ORD, edgecolor='#30363d', width=0.7)
    for bar, v in zip(bars3, n_orbits):
        ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.15,
                 str(v), ha='center', color='white', fontsize=8, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(short_names, rotation=45, ha='right', color='white', fontsize=7)
    ax3.set_ylabel('Number of orbits', color='white', fontsize=11)
    ax3.set_title(f'Orbit Count per Group\n$n = {N}$, positions $= {N*N}$',
                  color='white', fontsize=11, fontweight='bold')
    ax3.tick_params(colors='white')
    for sp in ax3.spines.values(): sp.set_edgecolor('#30363d')

    plt.suptitle('EXP-08 — RL3: Universal Entropy Invariance Class\nWhich groups guarantee $\\text{Fix}(G)\\subset\\mathcal{F}$?',
                 color='white', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    out = os.path.join(FIG_DIR, '08a_entropy_invariance.png')
    plt.savefig(out, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {out}")

def plot_orbit_maps(results, save_path):
    """Grid showing orbit structure for each group."""
    n_groups = len(results)
    cols = 4
    rows = math.ceil(n_groups / cols)
    fig, axes = plt.subplots(rows, cols, figsize=(cols*4, rows*4))
    fig.patch.set_facecolor('#0d1117')
    axes = axes.flatten()

    COLORMAP = plt.cm.tab20

    for idx, (r, ax) in enumerate(zip(results, axes)):
        ax.set_facecolor('#161b22')
        orbs = r['orbits']
        n_orbs = len(orbs)
        colors = COLORMAP(np.linspace(0, 1, n_orbs))
        pos_color = {}
        for oi, orb in enumerate(orbs):
            for pos in orb:
                pos_color[tuple(pos)] = oi

        for i in range(N):
            for j in range(N):
                oi = pos_color.get((i,j), 0)
                rect = plt.Rectangle([j, N-1-i], 1, 1,
                                      facecolor=colors[oi],
                                      edgecolor='#0d1117', linewidth=2)
                ax.add_patch(rect)

        ax.set_xlim(0, N); ax.set_ylim(0, N)
        ax.set_xticks([]); ax.set_yticks([])
        in_F = r['in_F']
        border_col = '#96CEB4' if in_F else '#FF6B6B'
        for sp in ax.spines.values():
            sp.set_edgecolor(border_col)
            sp.set_linewidth(3)

        short = r['group'].replace('Z2×Z2', '$\\mathbb{Z}_2^2$').replace('Z2', '$\\mathbb{Z}_2$').replace('Z4','$\\mathbb{Z}_4$')
        title = f"{short}\n|G|={r['order']}, orbits={n_orbs}, κ={r['kappa']:.2f}\n{'✓ In  𝓕' if in_F else '✗ Not in 𝓕'}"
        ax.set_title(title, color=border_col, fontsize=7.5, fontweight='bold')

    for ax in axes[n_groups:]:
        ax.set_visible(False)

    plt.suptitle('EXP-08B — RL3: Orbit Maps per Group\n(green border = in $\\mathcal{F}$, red = not)',
                 color='white', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig(save_path, dpi=130, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")

def make_gif(results, save_path):
    """GIF: bar chart of Var(H_d) for increasing group order."""
    sorted_r = sorted(results, key=lambda r: r['order'])
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')

    def update(frame):
        ax.clear(); ax.set_facecolor('#161b22')
        subset = sorted_r[:frame+1]
        names  = [r['group'].split('(')[0].strip() for r in subset]
        vars_  = [max(r['mean_var_Hd'], 1e-16) for r in subset]
        cols   = ['#96CEB4' if r['in_F'] else '#FF6B6B' for r in subset]
        ax.bar(range(len(subset)), vars_, color=cols, edgecolor='#30363d')
        ax.set_yscale('symlog', linthresh=1e-15)
        ax.axhline(EPSILON, color='white', lw=1.5, ls='--', alpha=0.7)
        ax.set_xticks(range(len(subset)))
        ax.set_xticklabels(names, rotation=40, ha='right', color='white', fontsize=7)
        ax.set_ylabel('$\\overline{\\text{Var}(H_d)}$', color='white')
        ax.set_title(f'RL3 — Groups tested: {frame+1}/{len(sorted_r)} | In $\\mathcal{{F}}$: {sum(r["in_F"] for r in subset)}',
                     color='white', fontweight='bold')
        ax.tick_params(colors='white')
        for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    ani = animation.FuncAnimation(fig, update, frames=len(sorted_r), interval=600)
    ani.save(save_path, writer='pillow', dpi=100)
    plt.close(); print(f"✓ {save_path}")

def save_csv(results, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['group','order','n_orbits','kappa','H_mean','H_std','mean_var_Hd','in_F'])
        w.writeheader()
        for r in results:
            w.writerow({k: r[k] for k in ['group','order','n_orbits','kappa','H_mean','H_std','mean_var_Hd','in_F']})
    print(f"✓ {path}")

if __name__ == '__main__':
    print("="*60)
    print("EXP-08: UNIVERSAL ENTROPY INVARIANCE CLASS (RL3)")
    print("="*60)

    results = run_analysis()

    n_in_F = sum(r['in_F'] for r in results)
    print(f"\n  Groups in F (entropy invariant): {n_in_F} / {len(results)}")
    print(f"  Groups NOT in F:                 {len(results)-n_in_F} / {len(results)}")

    in_F_groups  = [r['group'] for r in results if r['in_F']]
    not_F_groups = [r['group'] for r in results if not r['in_F']]
    print(f"\n  In F: {in_F_groups}")
    print(f"  Not:  {not_F_groups}")

    plot_main(results, FIG_DIR)
    plot_orbit_maps(results, os.path.join(FIG_DIR, '08b_orbit_maps.png'))
    make_gif(results, os.path.join(FIG_DIR, '08c_invariance_animation.gif'))
    save_csv(results, os.path.join(RES_DIR, '08_entropy_variance.csv'))

    print("\nEXP-08 COMPLETE ✓")

"""
EXP-09: Fundamental Compression Limit via Symmetry — RL6
=========================================================
Computes the symmetry compression ratio κ(G, n) for all groups
in our catalog, across n = 3, 4, 5.

κ(G, n) = |orbits(G ↷ [n]^2)| / n^2

Verifies the Burnside lower bound: κ ≥ 1/|G|
Identifies which group minimizes κ for fixed n.

Output:
  figures/RL6/ — landscape plots, GIF
  results/RL6/ — CSV catalog
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import csv, os, math
from itertools import product as iproduct

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIG_DIR = os.path.join(BASE, "figures", "RL6")
RES_DIR = os.path.join(BASE, "results", "RL6")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)


def orbits_from_generators(generators, positions):
    visited = set()
    orbits = []
    pos_set = set(positions)
    def closure(pos):
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
    return orbits


def make_catalog(n):
    """Group catalog for grid [n]^2."""
    positions = [(i,j) for i in range(n) for j in range(n)]

    def T(p):    return (p[1], p[0])
    def R180(p): return (n-1-p[0], n-1-p[1])
    def R90(p):  return (p[1], n-1-p[0])
    def Rh(p):   return (p[0], n-1-p[1])
    def Rv(p):   return (n-1-p[0], p[1])
    def Rd(p):   return (n-1-p[1], n-1-p[0])
    def Id(p):   return p

    return [
        ("Trivial {e}",            1,  [Id]),
        ("Z2 (T)",                 2,  [T]),
        ("Z2 (R180)",              2,  [R180]),
        ("Z2 (Rh)",                2,  [Rh]),
        ("Z2 (Rv)",                2,  [Rv]),
        ("Z2 (Rd)",                2,  [Rd]),
        ("Klein T,R180",           4,  [T, R180]),    # Sator group
        ("Klein Rh,Rv",            4,  [Rh, Rv]),
        ("Z2×Z2 T,Rh",             4,  [T, Rh]),
        ("Z4 (R90)",               4,  [R90]),
        ("D4 (R90,T)",             8,  [R90, T]),
        ("D4 (R90,Rh)",            8,  [R90, Rh]),
        ("Z2^3 (T,R180,Rh)",       8,  [T, R180, Rh]),
        ("D8 full (R90,T,Rh)",    16,  [R90, T, Rh]),
        ("Z2^4 (T,R180,Rh,Rd)",   16,  [T, R180, Rh, Rd]),
    ], positions


def compute_kappa_catalog(ns=(3, 4, 5)):
    """For each n and each group, compute κ and Burnside bound."""
    all_results = []
    for n in ns:
        catalog, positions = make_catalog(n)
        total_pos = n * n
        for name, order, gens in catalog:
            orbs = orbits_from_generators(gens, positions)
            n_orbs = len(orbs)
            kappa = n_orbs / total_pos
            burnside_lb = 1.0 / order
            above_bound = kappa >= burnside_lb - 1e-12
            all_results.append({
                'n': n,
                'group': name,
                'order': order,
                'n_positions': total_pos,
                'n_orbits': n_orbs,
                'kappa': kappa,
                'burnside_lb': burnside_lb,
                'kappa_ge_burnside': above_bound,
            })
    return all_results


def print_table(results):
    print(f"\n{'n':>3} {'Group':<28} {'|G|':>5} {'pos':>4} {'orb':>4} {'κ':>7} {'1/|G|':>7} {'κ≥1/|G|':>9}")
    print("-" * 75)
    prev_n = None
    for r in results:
        if r['n'] != prev_n:
            print(f"\n  === n = {r['n']} ===")
            prev_n = r['n']
        ok = "✓" if r['kappa_ge_burnside'] else "✗"
        print(f"  {r['group']:<28} {r['order']:>5} {r['n_positions']:>4} {r['n_orbits']:>4} "
              f"{r['kappa']:>7.4f} {r['burnside_lb']:>7.4f} {ok:>9}")


# ─── VISUALIZATIONS ──────────────────────────────────────────────────────────

def plot_kappa_landscape(results, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.patch.set_facecolor('#0d1117')

    ns = sorted(set(r['n'] for r in results))
    group_names_all = []
    for n in ns:
        sub = [r for r in results if r['n'] == n]
        gnames = [r['group'] for r in sub]
        if len(gnames) > len(group_names_all):
            group_names_all = gnames

    for ax_idx, n in enumerate(ns):
        ax = axes[ax_idx]
        ax.set_facecolor('#161b22')
        sub = [r for r in results if r['n'] == n]
        names = [r['group'].split('(')[0].strip().replace('Klein ','') for r in sub]
        kappas = [r['kappa'] for r in sub]
        lbs    = [r['burnside_lb'] for r in sub]
        orders = [r['order'] for r in sub]

        cmap_vals = plt.cm.viridis(np.linspace(0.2, 0.9, len(sub)))
        bars = ax.bar(range(len(sub)), kappas, color=cmap_vals, edgecolor='#30363d', width=0.7)
        ax.step(range(len(sub)), lbs, color='#FF6B6B', lw=2.5, where='mid',
                label='Burnside LB $1/|G|$')

        # Mark Sator point (Klein T,R180 at n=5)
        for i, r in enumerate(sub):
            if 'Klein T,R180' in r['group'] or 'Klein' in r['group'] and 'T,R180' in r['group']:
                ax.bar(i, kappas[i], color='#FFEAA7', edgecolor='white', linewidth=2, width=0.7)
                ax.text(i, kappas[i]+0.01, 'Sator', ha='center',
                        color='#FFEAA7', fontsize=7, fontweight='bold')

        ax.set_xticks(range(len(sub)))
        ax.set_xticklabels(names, rotation=45, ha='right', color='white', fontsize=7)
        ax.set_ylabel('$\\kappa(G, n)$', color='white', fontsize=11)
        ax.set_title(f'$n = {n}$ ($n^2 = {n*n}$ positions)\nCompression Ratio $\\kappa$ per Group',
                     color='white', fontsize=11, fontweight='bold')
        ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
        ax.set_ylim(0, 1.05)
        ax.tick_params(colors='white')
        for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    plt.suptitle('EXP-09 — RL6: Fundamental Compression Limit via Symmetry\n$\\kappa(G,n) = |\\text{orbits}| / n^2$ for all groups, $n \\in \\{3,4,5\\}$',
                 color='white', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")


def plot_kappa_vs_order(results, save_path):
    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')

    ns = sorted(set(r['n'] for r in results))
    markers = ['o', 's', '^']
    colors  = ['#4ECDC4', '#FF6B6B', '#FFEAA7']

    for ni, n in enumerate(ns):
        sub = [r for r in results if r['n'] == n]
        orders = [r['order'] for r in sub]
        kappas = [r['kappa'] for r in sub]
        lbs    = [r['burnside_lb'] for r in sub]

        ax.scatter(orders, kappas, marker=markers[ni], color=colors[ni],
                   s=100, label=f'$n = {n}$', zorder=5, edgecolors='white', linewidths=0.8)

        # Burnside bound curve
        order_range = np.linspace(1, max(orders)+2, 200)
        ax.plot(order_range, 1/order_range, color=colors[ni], lw=1.5, ls='--', alpha=0.5)

    # Sator point
    sator_r = next((r for r in results if r['n']==5 and 'Klein T,R180' in r['group']), None)
    if sator_r:
        ax.annotate('Sator\n$\\kappa=0.36$',
                    xy=(sator_r['order'], sator_r['kappa']),
                    xytext=(sator_r['order']+2, sator_r['kappa']+0.1),
                    color='#FFEAA7', fontsize=10, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='#FFEAA7', lw=1.5))

    ax.set_xlabel('Group order $|G|$', color='white', fontsize=12)
    ax.set_ylabel('$\\kappa(G, n)$', color='white', fontsize=12)
    ax.set_title('Compression Ratio $\\kappa$ vs Group Order\nDashed = Burnside Lower Bound $1/|G|$',
                 color='white', fontsize=13, fontweight='bold')
    ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=10)
    ax.tick_params(colors='white')
    for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")


def make_gif(results, save_path):
    """GIF: κ landscape for n=3,4,5 animated."""
    ns = sorted(set(r['n'] for r in results))
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor('#0d1117')

    def update(frame):
        ax.clear(); ax.set_facecolor('#161b22')
        n = ns[frame]
        sub = [r for r in results if r['n'] == n]
        names  = [r['group'].split('(')[0].strip()[:20] for r in sub]
        kappas = [r['kappa'] for r in sub]
        lbs    = [r['burnside_lb'] for r in sub]
        cols   = plt.cm.viridis(np.linspace(0.2, 0.9, len(sub)))

        ax.bar(range(len(sub)), kappas, color=cols, edgecolor='#30363d', width=0.7)
        ax.step(range(len(sub)), lbs, color='#FF6B6B', lw=2.5, where='mid')
        ax.set_xticks(range(len(sub)))
        ax.set_xticklabels(names, rotation=45, ha='right', color='white', fontsize=7)
        ax.set_ylabel('$\\kappa(G,n)$', color='white', fontsize=11)
        ax.set_ylim(0, 1.1)
        ax.set_title(f'RL6 — Compression Ratio $n = {n}$ | Total positions $= {n*n}$ | Min $\\kappa$ = {min(kappas):.3f}',
                     color='white', fontweight='bold')
        ax.tick_params(colors='white')
        for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    ani = animation.FuncAnimation(fig, update, frames=len(ns), interval=1200)
    ani.save(save_path, writer='pillow', dpi=100)
    plt.close(); print(f"✓ {save_path}")


def save_csv(results, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['n','group','order','n_positions','n_orbits','kappa','burnside_lb','kappa_ge_burnside'])
        w.writeheader()
        w.writerows(results)
    print(f"✓ {path}")


if __name__ == '__main__':
    print("="*60)
    print("EXP-09: FUNDAMENTAL COMPRESSION LIMIT (RL6)")
    print("="*60)

    results = compute_kappa_catalog(ns=(3, 4, 5))
    print_table(results)

    # Summary stats
    for n in (3, 4, 5):
        sub = [r for r in results if r['n'] == n]
        min_r = min(sub, key=lambda r: r['kappa'])
        max_r = max(sub, key=lambda r: r['kappa'])
        all_ok = all(r['kappa_ge_burnside'] for r in sub)
        print(f"\n  n={n}: min κ={min_r['kappa']:.4f} ({min_r['group']}), "
              f"max κ={max_r['kappa']:.4f}, Burnside holds: {all_ok}")

    sator = next(r for r in results if r['n']==5 and 'Klein T,R180' in r['group'])
    print(f"\n  SATOR (Klein Z2×Z2, n=5): κ = {sator['kappa']:.4f} "
          f"| Burnside LB = {sator['burnside_lb']:.4f} "
          f"| Ratio = {sator['kappa']/sator['burnside_lb']:.2f}× above bound")

    plot_kappa_landscape(results, os.path.join(FIG_DIR, '09a_kappa_landscape.png'))
    plot_kappa_vs_order(results, os.path.join(FIG_DIR, '09b_kappa_vs_order.png'))
    make_gif(results, os.path.join(FIG_DIR, '09c_kappa_animation.gif'))
    save_csv(results, os.path.join(RES_DIR, '09_kappa_catalog.csv'))

    print("\nEXP-09 COMPLETE ✓")

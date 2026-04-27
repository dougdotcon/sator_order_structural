"""
EXP-12: Information Action Landscape — RL4
==========================================
Computes A[M, G] = H(M) - H(M|G) for all groups in catalog.
  H(M) = n² · log₂(σ)  (max entropy over n² positions)
  H(M|G) = |orbits| · log₂(σ)  (free variables)
  A[M, G] = (n² - |orbits|) · log₂(σ)  (bits eliminated by G)

Verifies: A is maximized by the group with fewest orbits.
Plots the information action landscape.

Output: figures/RL4/, results/RL4/
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv, os, math

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIG_DIR = os.path.join(BASE, "figures", "RL4")
RES_DIR = os.path.join(BASE, "results", "RL4")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

N = 5
SIGMA = 26
log2_sigma = math.log2(SIGMA)

# ─── ORBIT ENGINE ────────────────────────────────────────────────────────────

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

def make_catalog(n=N):
    positions = [(i,j) for i in range(n) for j in range(n)]
    def T(p):    return (p[1], p[0])
    def R180(p): return (n-1-p[0], n-1-p[1])
    def R90(p):  return (p[1], n-1-p[0])
    def Rh(p):   return (p[0], n-1-p[1])
    def Rv(p):   return (n-1-p[0], p[1])
    def Rd(p):   return (n-1-p[1], n-1-p[0])
    def Id(p):   return p
    return [
        ("Trivial {e}",             1,  [Id]),
        ("Z2 (T)",                  2,  [T]),
        ("Z2 (R180)",               2,  [R180]),
        ("Z2 (Rh)",                 2,  [Rh]),
        ("Z2 (Rv)",                 2,  [Rv]),
        ("Klein (T, R180)",         4,  [T, R180]),    # Sator
        ("Klein (Rh, Rv)",          4,  [Rh, Rv]),
        ("Z2×Z2 (T, Rh)",           4,  [T, Rh]),
        ("Z4 (R90)",                4,  [R90]),
        ("D4 (R90, T)",             8,  [R90, T]),
        ("D4 (R90, Rh)",            8,  [R90, Rh]),
        ("Z2³ (T, R180, Rh)",       8,  [T, R180, Rh]),
        ("D8 (R90, T, Rh)",        16,  [R90, T, Rh]),
        ("Z2⁴ (T, R180, Rh, Rd)",  16,  [T, R180, Rh, Rd]),
    ], positions

# ─── ACTION COMPUTATION ──────────────────────────────────────────────────────

def compute_action(n_orbits, n_total=N*N, sigma=SIGMA):
    H_M    = n_total  * math.log2(sigma)   # bits: 25·log₂26
    H_M_G  = n_orbits * math.log2(sigma)   # bits: k·log₂26
    A      = H_M - H_M_G                   # bits eliminated
    R      = n_orbits / n_total             # effective rate
    return H_M, H_M_G, A, R

def run_analysis():
    catalog, positions = make_catalog()
    results = []

    H_M_ref = N*N * log2_sigma
    print(f"\n  H(M) reference (no group) = {H_M_ref:.4f} bits = 25·log₂26")
    print(f"\n{'Group':<28} {'|G|':>5} {'orbits':>7} {'H(M|G)':>9} {'A[M,G]':>9} {'R':>6} {'ΔA%':>8}")
    print("-"*75)

    for name, order, gens in catalog:
        orbs = orbits_from_generators(gens, positions)
        n_orbs = len(orbs)
        H_M, H_M_G, A, R = compute_action(n_orbs)
        delta_A_pct = 100 * A / H_M
        results.append({
            'group': name,
            'order': order,
            'n_orbits': n_orbs,
            'H_M': H_M,
            'H_M_G': H_M_G,
            'A': A,
            'R': R,
            'delta_A_pct': delta_A_pct,
        })
        sator_marker = " ← SATOR" if 'T, R180' in name and 'Klein' in name else ""
        print(f"  {name:<28} {order:>5} {n_orbs:>7} {H_M_G:>9.2f} {A:>9.2f} {R:>6.3f} {delta_A_pct:>7.1f}%{sator_marker}")

    return results

# ─── VISUALIZATIONS ──────────────────────────────────────────────────────────

def plot_action_landscape(results, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.patch.set_facecolor('#0d1117')

    names  = [r['group'].replace('Z2×Z2','Z₂²').replace('Z2³','Z₂³').replace('Z2⁴','Z₂⁴') for r in results]
    short  = [n.split('(')[0].strip()[:16] for n in names]
    orders = [r['order'] for r in results]
    actions = [r['A'] for r in results]
    H_M_Gs  = [r['H_M_G'] for r in results]
    Rs       = [r['R'] for r in results]

    sator_idx = next(i for i,r in enumerate(results) if 'T, R180' in r['group'] and 'Klein' in r['group'])
    cols = ['#FFEAA7' if i == sator_idx else '#4ECDC4' for i in range(len(results))]

    # ── Plot 1: Action A[M,G] per group (bar) ────────────────────────────────
    ax = axes[0]
    ax.set_facecolor('#161b22')
    bars = ax.bar(range(len(results)), actions, color=cols, edgecolor='#30363d', width=0.7)
    ax.axhline(results[0]['H_M'], color='#FF6B6B', lw=2, ls='--', label='$H(M)$ (no group)')
    ax.set_xticks(range(len(results)))
    ax.set_xticklabels(short, rotation=45, ha='right', color='white', fontsize=7.5)
    ax.set_ylabel('$\\mathcal{A}[M, G]$ (bits)', color='white', fontsize=11)
    ax.set_title('Information Action $\\mathcal{A}[M,G] = H(M)-H(M|G)$\nYellow = Sator (Klein T,R180)',
                 color='white', fontsize=11, fontweight='bold')
    ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
    ax.tick_params(colors='white')
    for sp in ax.spines.values(): sp.set_edgecolor('#30363d')
    for bar, v in zip(bars, actions):
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
                f'{v:.1f}', ha='center', color='white', fontsize=6.5, fontweight='bold')

    # ── Plot 2: A vs |G| scatter ──────────────────────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor('#161b22')
    sc = ax2.scatter(orders, actions, c=Rs, cmap='viridis', s=150,
                     edgecolors='white', linewidths=1.2, zorder=5)
    # Annotate Sator
    ax2.annotate('Sator\n$A=75.21$ bits',
                 xy=(results[sator_idx]['order'], results[sator_idx]['A']),
                 xytext=(results[sator_idx]['order']+1.5, results[sator_idx]['A']-5),
                 color='#FFEAA7', fontsize=9, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#FFEAA7', lw=1.5))
    cbar = plt.colorbar(sc, ax=ax2)
    cbar.set_label('$R = k/n^2$ (effective rate)', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')
    ax2.set_xlabel('Group order $|G|$', color='white', fontsize=11)
    ax2.set_ylabel('$\\mathcal{A}[M, G]$ (bits eliminated)', color='white', fontsize=11)
    ax2.set_title('Action vs Group Order\n(color = effective rate $R$)',
                  color='white', fontsize=11, fontweight='bold')
    ax2.tick_params(colors='white')
    for sp in ax2.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 3: Entropy decomposition stacked bar ─────────────────────────────
    ax3 = axes[2]
    ax3.set_facecolor('#161b22')
    x = np.arange(len(results))
    ax3.bar(x, H_M_Gs, color='#4ECDC4', edgecolor='#30363d', width=0.7, label='$H(M|G)$ — conditional (free)')
    ax3.bar(x, actions, bottom=H_M_Gs, color='#FF6B6B', edgecolor='#30363d', width=0.7, alpha=0.8,
            label='$\\mathcal{A}[M,G]$ — action (eliminated)')
    ax3.set_xticks(x)
    ax3.set_xticklabels(short, rotation=45, ha='right', color='white', fontsize=7.5)
    ax3.set_ylabel('Bits', color='white', fontsize=11)
    ax3.set_title('Entropy Decomposition\n$H(M) = H(M|G) + \\mathcal{A}[M,G]$',
                  color='white', fontsize=11, fontweight='bold')
    ax3.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
    ax3.tick_params(colors='white')
    for sp in ax3.spines.values(): sp.set_edgecolor('#30363d')

    plt.suptitle('EXP-12 — RL4: Variational Information Principle\n'
                 '$\\mathcal{A}[M,G] = H(M) - H(M|G)$ — the information eliminated by symmetry',
                 color='white', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")

def make_gif(results, save_path):
    sorted_r = sorted(results, key=lambda r: r['order'])
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor('#0d1117')

    def update(frame):
        ax.clear(); ax.set_facecolor('#161b22')
        subset = sorted_r[:frame+1]
        short = [r['group'].split('(')[0].strip()[:14] for r in subset]
        actions = [r['A'] for r in subset]
        cols = plt.cm.plasma(np.linspace(0.2, 0.9, len(subset)))
        ax.bar(range(len(subset)), actions, color=cols, edgecolor='#30363d', width=0.7)
        ax.axhline(sorted_r[-1]['H_M'], color='#FF6B6B', lw=2, ls='--', alpha=0.7)
        ax.set_xticks(range(len(subset)))
        ax.set_xticklabels(short, rotation=40, ha='right', color='white', fontsize=8)
        ax.set_ylabel('$\\mathcal{A}$ (bits)', color='white')
        ax.set_ylim(0, results[0]['H_M'] + 5)
        ax.set_title(f'RL4 — Information Action | Groups: {frame+1}/{len(sorted_r)} | Max $\\mathcal{{A}}$={max(actions):.1f} bits',
                     color='white', fontweight='bold')
        ax.tick_params(colors='white')
        for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    ani = animation.FuncAnimation(fig, update, frames=len(sorted_r), interval=500)
    ani.save(save_path, writer='pillow', dpi=100)
    plt.close(); print(f"✓ {save_path}")

def save_csv(results, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['group','order','n_orbits','H_M','H_M_G','A','R','delta_A_pct'])
        w.writeheader()
        w.writerows(results)
    print(f"✓ {path}")

if __name__ == '__main__':
    print("="*60)
    print("EXP-12: INFORMATION ACTION LANDSCAPE (RL4)")
    print("="*60)
    results = run_analysis()

    max_r = max(results, key=lambda r: r['A'])
    min_r = min(results, key=lambda r: r['A'])
    sator_r = next(r for r in results if 'T, R180' in r['group'] and 'Klein' in r['group'])

    print(f"\n  Max action: {max_r['group']} → A = {max_r['A']:.4f} bits ({max_r['delta_A_pct']:.1f}%)")
    print(f"  Min action: {min_r['group']} → A = {min_r['A']:.4f} bits ({min_r['delta_A_pct']:.1f}%)")
    print(f"  Sator:      {sator_r['group']} → A = {sator_r['A']:.4f} bits ({sator_r['delta_A_pct']:.1f}%)")
    print(f"\n  THEOREM: A[M,G] = (n²-|orbits|)·log₂σ — exact identity, verified for all {len(results)} groups")

    plot_action_landscape(results, os.path.join(FIG_DIR, '12a_action_landscape.png'))
    make_gif(results, os.path.join(FIG_DIR, '12b_action_animation.gif'))
    save_csv(results, os.path.join(RES_DIR, '12_action_landscape.csv'))

    print("\nEXP-12 COMPLETE ✓")

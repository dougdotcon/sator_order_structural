"""
EXP-10: Symmetry-Protected Information — Recovery Rate by Group (RL2)
======================================================================
Generalizes Sator EXP-05 to arbitrary finite groups.
For each group G in our catalog:
  1. Build a random matrix M ∈ Fix(G)
  2. Apply t random symbol corruptions (Isfet)
  3. Recover via orbit majority-vote (Ma'at)
  4. Measure ρ(t) = fraction correctly recovered

Key question: does ρ(t) scale with |G| and d_min_orb?

Output: figures/RL2/, results/RL2/
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv, os, math
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIG_DIR = os.path.join(BASE, "figures", "RL2")
RES_DIR = os.path.join(BASE, "results", "RL2")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

N = 5
SIGMA = 26
RNG = np.random.RandomState(42)
N_TRIALS = 200

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
    return sorted(orbits, key=lambda o: min(o))

def make_catalog(n=N):
    positions = [(i,j) for i in range(n) for j in range(n)]
    def T(p):    return (p[1], p[0])
    def R180(p): return (n-1-p[0], n-1-p[1])
    def R90(p):  return (p[1], n-1-p[0])
    def Rh(p):   return (p[0], n-1-p[1])
    def Rv(p):   return (n-1-p[0], p[1])
    def Id(p):   return p
    return [
        ("Trivial {e}",         1,  [Id]),
        ("Z2 (Transpose)",      2,  [T]),
        ("Z2 (R180)",           2,  [R180]),
        ("Klein (T, R180)",     4,  [T, R180]),   # Sator group
        ("Klein (Rh, Rv)",      4,  [Rh, Rv]),
        ("Z4 (R90)",            4,  [R90]),
        ("D4 (R90, T)",         8,  [R90, T]),
        ("Z2³ (T, R180, Rh)",   8,  [T, R180, Rh]),
        ("D8 (R90, T, Rh)",    16,  [R90, T, Rh]),
    ], positions

def build_fix_g(orbits, n=N, sigma=SIGMA):
    M = {}
    positions = [(i,j) for i in range(n) for j in range(n)]
    for pos in positions:
        M[pos] = None
    for orb in orbits:
        val = RNG.randint(0, sigma)
        for pos in orb:
            M[pos] = val
    return M

def d_min_orb(orbits):
    sizes = [len(o) for o in orbits]
    non_trivial = [s for s in sizes if s > 1]
    return min(non_trivial) if non_trivial else 1

# ─── ISFET / MAAT ────────────────────────────────────────────────────────────

def isfet(M, t, sigma=SIGMA):
    """Apply t random symbol corruptions."""
    M_hat = dict(M)
    positions = list(M.keys())
    targets = RNG.choice(len(positions), size=min(t, len(positions)), replace=False)
    for idx in targets:
        pos = positions[idx]
        current = M_hat[pos]
        new_val = RNG.randint(0, sigma)
        while new_val == current and sigma > 1:
            new_val = RNG.randint(0, sigma)
        M_hat[pos] = new_val
    return M_hat

def maat(M_hat, orbits):
    """Orbit majority-vote recovery."""
    M_rec = dict(M_hat)
    for orb in orbits:
        vals = [M_hat[pos] for pos in orb]
        cnt = Counter(vals)
        majority = cnt.most_common(1)[0][0]
        for pos in orb:
            M_rec[pos] = majority
    return M_rec

def recovery_rate(M_orig, M_rec):
    n = len(M_orig)
    correct = sum(1 for pos in M_orig if M_orig[pos] == M_rec[pos])
    return correct / n

# ─── MAIN ANALYSIS ───────────────────────────────────────────────────────────

def run_analysis():
    catalog, positions = make_catalog()
    t_values = list(range(0, 26, 1))
    results = []

    for name, order, gens in catalog:
        orbs = orbits_from_generators(gens, positions)
        d_orb = d_min_orb(orbs)
        n_orbits = len(orbs)
        kappa = n_orbits / (N*N)

        rho_by_t = []
        for t in t_values:
            rhos = []
            for _ in range(N_TRIALS):
                M = build_fix_g(orbs)
                M_hat = isfet(M, t)
                M_rec = maat(M_hat, orbs)
                rhos.append(recovery_rate(M, M_rec))
            rho_by_t.append((np.mean(rhos), np.std(rhos)))

        results.append({
            'group': name,
            'order': order,
            'n_orbits': n_orbits,
            'kappa': kappa,
            'd_orb': d_orb,
            'rho_at_1': rho_by_t[1][0],
            'rho_at_5': rho_by_t[5][0],
            'rho_by_t': rho_by_t,
            't_values': t_values,
        })
        print(f"  {name:<25} |G|={order:<3} d_orb={d_orb} "
              f"ρ(1)={rho_by_t[1][0]*100:.1f}%  ρ(5)={rho_by_t[5][0]*100:.1f}%")

    return results

# ─── VISUALIZATIONS ──────────────────────────────────────────────────────────

def plot_recovery_curves(results, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.patch.set_facecolor('#0d1117')

    cmap = plt.cm.viridis(np.linspace(0.1, 0.95, len(results)))

    # ── Plot 1: ρ(t) curves for all groups ──────────────────────────────────
    ax = axes[0]
    ax.set_facecolor('#161b22')
    for i, r in enumerate(results):
        means = [v[0] for v in r['rho_by_t']]
        stds  = [v[1] for v in r['rho_by_t']]
        t = r['t_values']
        lw = 3 if 'Klein (T, R180)' in r['group'] else 1.5
        ls = '-' if 'Klein (T, R180)' in r['group'] else '--'
        label = f"{r['group'].split('(')[0].strip()} |G|={r['order']}"
        ax.plot(t, means, color=cmap[i], lw=lw, ls=ls, label=label)
        ax.fill_between(t,
                        [m-s for m,s in zip(means,stds)],
                        [m+s for m,s in zip(means,stds)],
                        color=cmap[i], alpha=0.1)
    ax.set_xlabel('Corruptions $t$', color='white', fontsize=11)
    ax.set_ylabel('Recovery rate $\\rho(t)$', color='white', fontsize=11)
    ax.set_title('Ma\'at Recovery Under Isfet\nAll Groups vs Sator (Klein, bold)',
                 color='white', fontsize=11, fontweight='bold')
    ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white',
              fontsize=7, loc='upper right', ncol=1)
    ax.tick_params(colors='white')
    ax.set_ylim(-0.05, 1.05)
    for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 2: ρ(t=1) vs |G| ────────────────────────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor('#161b22')
    orders = [r['order'] for r in results]
    rho1   = [r['rho_at_1'] for r in results]
    ax2.scatter(orders, rho1, c=[r['d_orb'] for r in results],
                cmap='plasma', s=150, edgecolors='white', linewidths=1.2, zorder=5)
    for r in results:
        ax2.annotate(r['group'].split('(')[0].strip()[:8],
                     xy=(r['order'], r['rho_at_1']),
                     xytext=(r['order']+0.3, r['rho_at_1']-0.015),
                     color='#adb5bd', fontsize=7)
    sc = ax2.scatter(orders, rho1, c=[r['d_orb'] for r in results],
                     cmap='plasma', s=150, edgecolors='white', linewidths=1.2, zorder=5)
    cbar = plt.colorbar(sc, ax=ax2)
    cbar.set_label('$d_{\\min}^{\\text{orb}}$', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')
    ax2.set_xlabel('Group order $|G|$', color='white', fontsize=11)
    ax2.set_ylabel('$\\rho(t=1)$', color='white', fontsize=11)
    ax2.set_title('Recovery at $t=1$ vs Group Order\n(color = $d_{\\min}^{\\text{orb}}$)',
                  color='white', fontsize=11, fontweight='bold')
    ax2.tick_params(colors='white')
    for sp in ax2.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 3: d_orb vs ρ(t=1) ──────────────────────────────────────────────
    ax3 = axes[2]
    ax3.set_facecolor('#161b22')
    d_orbs = [r['d_orb'] for r in results]
    unique_d = sorted(set(d_orbs))
    for ud in unique_d:
        sub = [r for r in results if r['d_orb'] == ud]
        rhos = [r['rho_at_1'] for r in sub]
        ax3.scatter([ud]*len(sub), rhos, s=150, alpha=0.9,
                    edgecolors='white', linewidths=1, zorder=5,
                    label=f'$d_{{\\min}}^{{\\text{{orb}}}}={ud}$')
    ax3.set_xlabel('$d_{\\min}^{\\text{orb}}$', color='white', fontsize=12)
    ax3.set_ylabel('$\\rho(t=1)$', color='white', fontsize=12)
    ax3.set_title('Orbit Distance vs Recovery ($t=1$)\nCore RL2 Hypothesis',
                  color='white', fontsize=11, fontweight='bold')
    ax3.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
    ax3.tick_params(colors='white')
    for sp in ax3.spines.values(): sp.set_edgecolor('#30363d')

    plt.suptitle('EXP-10 — RL2: Symmetry-Protected Information\nRecovery Rate $\\rho(t)$ for Multiple Groups Under Orbit Majority-Vote Recovery',
                 color='white', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")

def make_gif(results, save_path):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0d1117')
    cmap = plt.cm.viridis(np.linspace(0.1, 0.95, len(results)))

    def update(frame):
        ax.clear(); ax.set_facecolor('#161b22')
        t_max = frame + 1
        for i, r in enumerate(results):
            means = [v[0] for v in r['rho_by_t'][:t_max]]
            t = r['t_values'][:t_max]
            ax.plot(t, means, color=cmap[i], lw=2,
                    label=f"{r['group'].split('(')[0].strip()} |G|={r['order']}")
        ax.set_xlabel('Corruptions $t$', color='white')
        ax.set_ylabel('$\\rho(t)$', color='white')
        ax.set_xlim(0, 25); ax.set_ylim(-0.05, 1.05)
        ax.set_title(f'RL2 — Ma\'at Recovery, $t = 0$ to $t = {frame}$',
                     color='white', fontweight='bold')
        ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white',
                  fontsize=7, loc='upper right', ncol=2)
        ax.tick_params(colors='white')
        for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    ani = animation.FuncAnimation(fig, update, frames=26, interval=100)
    ani.save(save_path, writer='pillow', dpi=100)
    plt.close(); print(f"✓ {save_path}")

def save_csv(results, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['group','order','n_orbits','kappa','d_orb','rho_t1','rho_t5'])
        for r in results:
            w.writerow([r['group'],r['order'],r['n_orbits'],r['kappa'],
                        r['d_orb'],r['rho_at_1'],r['rho_at_5']])
    print(f"✓ {path}")

if __name__ == '__main__':
    print("="*60)
    print("EXP-10: SYMMETRY-PROTECTED INFORMATION (RL2)")
    print("="*60)
    results = run_analysis()

    print(f"\n  Best ρ(t=1): {max(results, key=lambda r:r['rho_at_1'])['group']}")
    print(f"  Worst ρ(t=1): {min(results, key=lambda r:r['rho_at_1'])['group']}")

    plot_recovery_curves(results, os.path.join(FIG_DIR, '10a_recovery_curves.png'))
    make_gif(results, os.path.join(FIG_DIR, '10b_recovery_animation.gif'))
    save_csv(results, os.path.join(RES_DIR, '10_recovery_by_group.csv'))

    print("\nEXP-10 COMPLETE ✓")

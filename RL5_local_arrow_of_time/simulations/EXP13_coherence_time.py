"""
EXP-13: Local Arrow of Time — Coherence Time vs Symmetry (RL5)
==============================================================
For each group G, simulates stochastic perturbation over time.
Measures t* = time until ρ(t) < threshold (0.5).

Key question: does t* scale with |G| and d_min_orb?
Connects to TDTR: local reversibility within global irreversibility.

Output: figures/RL5/, results/RL5/
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv, os, math
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIG_DIR = os.path.join(BASE, "figures", "RL5")
RES_DIR = os.path.join(BASE, "results", "RL5")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

N = 5
SIGMA = 26
RNG = np.random.RandomState(42)
N_TRIALS = 200
THRESHOLD = 0.5   # ρ drops below this → locally reversible window broken

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
        ("Z2 (T)",              2,  [T]),
        ("Z2 (R180)",           2,  [R180]),
        ("Klein (T, R180)",     4,  [T, R180]),   # Sator
        ("Klein (Rh, Rv)",      4,  [Rh, Rv]),
        ("Z4 (R90)",            4,  [R90]),
        ("D4 (R90, T)",         8,  [R90, T]),
        ("Z2³ (T,R180,Rh)",     8,  [T, R180, Rh]),
        ("D8 (R90,T,Rh)",      16,  [R90, T, Rh]),
    ], positions

def build_fix_g(orbits, n=N):
    M = {}
    for orb in orbits:
        val = RNG.randint(0, SIGMA)
        for pos in orb:
            M[pos] = val
    return M

def d_min_orb(orbits):
    sizes = [len(o) for o in orbits]
    non_trivial = [s for s in sizes if s > 1]
    return min(non_trivial) if non_trivial else 1

def isfet(M, t):
    M_hat = dict(M)
    positions = list(M.keys())
    targets = RNG.choice(len(positions), size=min(t, len(positions)), replace=False)
    for idx in targets:
        pos = positions[idx]
        curr = M_hat[pos]
        nv = RNG.randint(0, SIGMA)
        while nv == curr and SIGMA > 1: nv = RNG.randint(0, SIGMA)
        M_hat[pos] = nv
    return M_hat

def maat(M_hat, orbits):
    M_rec = dict(M_hat)
    for orb in orbits:
        vals = [M_hat[pos] for pos in orb]
        cnt = Counter(vals)
        majority = cnt.most_common(1)[0][0]
        for pos in orb:
            M_rec[pos] = majority
    return M_rec

def recovery_rate(M_orig, M_rec):
    return sum(1 for pos in M_orig if M_orig[pos] == M_rec[pos]) / len(M_orig)

def find_t_star(rho_curve, t_values, threshold=THRESHOLD):
    """First t where ρ drops below threshold."""
    for t, rho in zip(t_values, rho_curve):
        if rho < threshold:
            return t
    return t_values[-1]  # never drops below: t* = max

def run_analysis():
    catalog, positions = make_catalog()
    t_values = list(range(0, 26))
    results = []

    for name, order, gens in catalog:
        orbs = orbits_from_generators(gens, positions)
        d_orb = d_min_orb(orbs)
        n_orbs = len(orbs)

        rho_means = []
        rho_stds  = []
        for t in t_values:
            rhos = []
            for _ in range(N_TRIALS):
                M = build_fix_g(orbs)
                M_hat = isfet(M, t)
                M_rec = maat(M_hat, orbs)
                rhos.append(recovery_rate(M, M_rec))
            rho_means.append(np.mean(rhos))
            rho_stds.append(np.std(rhos))

        t_star = find_t_star(rho_means, t_values, THRESHOLD)
        t_star_90 = find_t_star(rho_means, t_values, 0.9)

        results.append({
            'group': name,
            'order': order,
            'n_orbits': n_orbs,
            'd_orb': d_orb,
            't_star': t_star,
            't_star_90': t_star_90,
            'rho_means': rho_means,
            'rho_stds': rho_stds,
            't_values': t_values,
        })
        print(f"  {name:<25} |G|={order:<3} d_orb={d_orb} "
              f"t*(50%)={t_star:>3}  t*(90%)={t_star_90:>3}")
    return results

# ─── VISUALIZATIONS ──────────────────────────────────────────────────────────

def plot_coherence(results, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.patch.set_facecolor('#0d1117')
    cmap = plt.cm.viridis(np.linspace(0.1, 0.95, len(results)))

    # ── Plot 1: ρ(t) curves ──────────────────────────────────────────────────
    ax = axes[0]
    ax.set_facecolor('#161b22')
    for i, r in enumerate(results):
        t = r['t_values']
        means = r['rho_means']
        stds  = r['rho_stds']
        lw = 3 if 'Klein (T, R180)' in r['group'] else 1.5
        ax.plot(t, means, color=cmap[i], lw=lw,
                label=f"{r['group'].split('(')[0].strip()} |G|={r['order']} t*={r['t_star']}")
        ax.fill_between(t,
                        [m-s for m,s in zip(means,stds)],
                        [m+s for m,s in zip(means,stds)],
                        color=cmap[i], alpha=0.1)
    ax.axhline(THRESHOLD, color='white', lw=1.5, ls='--', alpha=0.6, label=f'Threshold = {THRESHOLD}')
    ax.set_xlabel('Corruptions $t$', color='white', fontsize=11)
    ax.set_ylabel('$\\rho(t)$', color='white', fontsize=11)
    ax.set_title('Coherence Decay $\\rho(t)$\nLocal reversibility window per group',
                 color='white', fontsize=11, fontweight='bold')
    ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=7.5, ncol=1)
    ax.tick_params(colors='white')
    ax.set_ylim(-0.05, 1.05)
    for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 2: t* vs |G| ─────────────────────────────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor('#161b22')
    orders  = [r['order'] for r in results]
    t_stars = [r['t_star'] for r in results]
    t_90s   = [r['t_star_90'] for r in results]
    d_orbs  = [r['d_orb'] for r in results]
    sc = ax2.scatter(orders, t_stars, c=d_orbs, cmap='plasma',
                     s=180, edgecolors='white', linewidths=1.2, zorder=5, label='$t^*(50\\%)$')
    ax2.scatter(orders, t_90s, c=d_orbs, cmap='plasma',
                s=80, edgecolors='white', linewidths=1, marker='^', zorder=5, alpha=0.8, label='$t^*(90\\%)$')
    cbar = plt.colorbar(sc, ax=ax2)
    cbar.set_label('$d_{\\min}^{\\text{orb}}$', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')
    for r in results:
        ax2.annotate(r['group'].split('(')[0].strip()[:8],
                     xy=(r['order'], r['t_star']),
                     xytext=(r['order']+0.2, r['t_star']+0.2),
                     color='#adb5bd', fontsize=7)
    ax2.set_xlabel('Group order $|G|$', color='white', fontsize=11)
    ax2.set_ylabel('$t^*$ (coherence time)', color='white', fontsize=11)
    ax2.set_title('Coherence Time $t^*$ vs $|G|$\n(color = $d_{\\min}^{\\text{orb}}$)',
                  color='white', fontsize=11, fontweight='bold')
    ax2.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
    ax2.tick_params(colors='white')
    for sp in ax2.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 3: d_orb vs t* ──────────────────────────────────────────────────
    ax3 = axes[2]
    ax3.set_facecolor('#161b22')
    unique_d = sorted(set(d_orbs))
    for ud in unique_d:
        sub = [r for r in results if r['d_orb'] == ud]
        ax3.scatter([ud]*len(sub), [r['t_star'] for r in sub],
                    s=180, edgecolors='white', linewidths=1, zorder=5, alpha=0.9,
                    label=f'$d_{{\\min}}={ud}$')
    ax3.set_xlabel('$d_{\\min}^{\\text{orb}}$', color='white', fontsize=12)
    ax3.set_ylabel('$t^*$ (coherence time at 50%)', color='white', fontsize=12)
    ax3.set_title('Orbit Distance vs Coherence Time\nCore RL5 Hypothesis',
                  color='white', fontsize=11, fontweight='bold')
    ax3.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=10)
    ax3.tick_params(colors='white')
    for sp in ax3.spines.values(): sp.set_edgecolor('#30363d')

    plt.suptitle('EXP-13 — RL5: Local Arrow of Time Breaking\n'
                 'Does $d_{\\min}^{\\text{orb}}$ and $|G|$ predict the coherence window $t^*$?',
                 color='white', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")

def make_gif(results, save_path):
    cmap = plt.cm.viridis(np.linspace(0.1, 0.95, len(results)))
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0d1117')

    def update(frame):
        ax.clear(); ax.set_facecolor('#161b22')
        t_max = frame + 1
        for i, r in enumerate(results):
            t = r['t_values'][:t_max]
            means = r['rho_means'][:t_max]
            ax.plot(t, means, color=cmap[i], lw=2,
                    label=f"{r['group'].split('(')[0].strip()} t*={r['t_star']}")
        ax.axhline(THRESHOLD, color='white', lw=1.5, ls='--', alpha=0.6)
        ax.set_xlabel('$t$', color='white')
        ax.set_ylabel('$\\rho(t)$', color='white')
        ax.set_xlim(0, 25); ax.set_ylim(-0.05, 1.05)
        ax.set_title(f'RL5 — Coherence Decay, $t = 0$ to $t = {frame}$',
                     color='white', fontweight='bold')
        ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white',
                  fontsize=7, ncol=2)
        ax.tick_params(colors='white')
        for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    ani = animation.FuncAnimation(fig, update, frames=26, interval=100)
    ani.save(save_path, writer='pillow', dpi=100)
    plt.close(); print(f"✓ {save_path}")

def save_csv(results, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['group','order','n_orbits','d_orb','t_star_50','t_star_90'])
        for r in results:
            w.writerow([r['group'],r['order'],r['n_orbits'],r['d_orb'],r['t_star'],r['t_star_90']])
    print(f"✓ {path}")

if __name__ == '__main__':
    print("="*60)
    print("EXP-13: LOCAL ARROW OF TIME — COHERENCE TIME (RL5)")
    print("="*60)
    results = run_analysis()

    best = max(results, key=lambda r: r['t_star'])
    worst = min(results, key=lambda r: r['t_star'])
    sator = next(r for r in results if 'T, R180' in r['group'])

    print(f"\n  Longest t*:  {best['group']} → t*={best['t_star']}")
    print(f"  Shortest t*: {worst['group']} → t*={worst['t_star']}")
    print(f"  Sator:       {sator['group']} → t*={sator['t_star']}")

    plot_coherence(results, os.path.join(FIG_DIR, '13a_coherence_decay.png'))
    make_gif(results, os.path.join(FIG_DIR, '13b_coherence_animation.gif'))
    save_csv(results, os.path.join(RES_DIR, '13_coherence_time.csv'))

    print("\nEXP-13 COMPLETE ✓")

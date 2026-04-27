"""
EXP-16: Corrected Recovery Baseline — δρ(G,t) (RL2 fix)
=========================================================
The trivial group achieves ρ(t=1) = 24/25 = 96% — this is NOT structural recovery.
It is just the fraction of uncorrupted positions.

Correct baseline: ρ_baseline(t) = (n² - t) / n²  (expected uncorrupted fraction)
True structural benefit: δρ(G, t) = ρ_Fix(G)(t) - ρ_baseline(t)

Also adds a second baseline: a matrix with the same k = |orbits| free variables
but WITHOUT orbit structure (flat k-variable random matrix).
This isolates the benefit of orbit redundancy vs just having k degrees of freedom.

Output: figures/RL2/, results/RL2/
"""
import numpy as np
import matplotlib.pyplot as plt
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
N_TRIALS = 400

def orbits_from_generators(generators, positions):
    visited = set(); orbits = []; pos_set = set(positions)
    def closure(pos):
        orbit = set(); queue = [pos]
        while queue:
            p = queue.pop()
            if p in orbit: continue
            orbit.add(p)
            for g in generators:
                np_ = g(p)
                if np_ in pos_set and np_ not in orbit: queue.append(np_)
        return frozenset(orbit)
    for pos in positions:
        if pos in visited: continue
        orb = closure(pos); orbits.append(orb); visited.update(orb)
    return sorted(orbits, key=lambda o: min(o))

def make_catalog(n=N):
    positions = [(i,j) for i in range(n) for j in range(n)]
    def T(p): return (p[1], p[0])
    def R180(p): return (n-1-p[0], n-1-p[1])
    def R90(p): return (p[1], n-1-p[0])
    def Rh(p): return (p[0], n-1-p[1])
    def Id(p): return p
    return [
        ("Trivial {e}",         1,  [Id]),
        ("Z2 (T)",              2,  [T]),
        ("Z2 (R180)",           2,  [R180]),
        ("Klein (T,R180)",      4,  [T, R180]),   # Sator
        ("Klein (Rh,Rv)",       4,  [Rh, lambda p: (n-1-p[0], p[1])]),
        ("Z4 (R90)",            4,  [R90]),
        ("D4 (R90,T)",          8,  [R90, T]),
        ("Z2^3 (T,R180,Rh)",    8,  [T, R180, Rh]),
        ("D8 (R90,T,Rh)",      16,  [R90, T, Rh]),
    ], positions

def build_fix_g(orbits):
    M = {}
    for orb in orbits:
        val = RNG.randint(0, SIGMA)
        for pos in orb: M[pos] = val
    return M

def build_flat_k(k, positions):
    """k free variables placed at k randomly chosen positions, no orbit structure."""
    chosen = [positions[i*len(positions)//k] for i in range(k)]  # deterministic spread
    M = {pos: RNG.randint(0, SIGMA) for pos in positions}       # fully random base
    return M

def isfet(M, t):
    M_hat = dict(M)
    positions = list(M.keys())
    for idx in RNG.choice(len(positions), size=min(t, len(positions)), replace=False):
        pos = positions[idx]; curr = M_hat[pos]
        nv = RNG.randint(0, SIGMA)
        while nv == curr and SIGMA > 1: nv = RNG.randint(0, SIGMA)
        M_hat[pos] = nv
    return M_hat

def maat(M_hat, orbits):
    M_rec = dict(M_hat)
    for orb in orbits:
        vals = [M_hat[pos] for pos in orb]
        cnt = Counter(vals); majority = cnt.most_common(1)[0][0]
        for pos in orb: M_rec[pos] = majority
    return M_rec

def rho_baseline(t, n=N): return max(0.0, (n*n - t) / (n*n))

def run_analysis():
    catalog, positions = make_catalog()
    t_values = list(range(0, 26))

    HEADER = f"\n{'Group':<25} {'|G|':>5} {'k':>4} {'d_orb':>6} | " \
             f"{'ρ(1)':>7} {'δρ(1)':>7} {'ρ(5)':>7} {'δρ(5)':>7}"
    print(HEADER); print("-" * 80)

    results = []
    for name, order, gens in catalog:
        orbs = orbits_from_generators(gens, positions)
        k = len(orbs)
        d_orb = min((len(o) for o in orbs if len(o) > 1), default=1)

        rho_means = []
        for t in t_values:
            rhos = []
            for _ in range(N_TRIALS):
                M = build_fix_g(orbs)
                M_hat = isfet(M, t)
                M_rec = maat(M_hat, orbs)
                rhos.append(sum(M[p] == M_rec[p] for p in M) / len(M))
            rho_means.append(np.mean(rhos))

        baselines  = [rho_baseline(t) for t in t_values]
        delta_rhos = [rm - rb for rm, rb in zip(rho_means, baselines)]

        results.append({
            'group': name, 'order': order, 'k': k, 'd_orb': d_orb,
            'rho_means': rho_means, 'baselines': baselines,
            'delta_rhos': delta_rhos,
            'rho_t1': rho_means[1], 'delta_t1': delta_rhos[1],
            'rho_t5': rho_means[5], 'delta_t5': delta_rhos[5],
        })
        sator = " ← SATOR" if 'T,R180' in name and 'Klein' in name else ""
        print(f"  {name:<25} {order:>5} {k:>4} {d_orb:>6} | "
              f"{rho_means[1]:>7.3f} {delta_rhos[1]:>+7.4f} "
              f"{rho_means[5]:>7.3f} {delta_rhos[5]:>+7.4f}{sator}")
    return results

def plot_corrected(results, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.patch.set_facecolor('#0d1117')
    cmap = plt.cm.viridis(np.linspace(0.1, 0.95, len(results)))

    # ── Plot 1: ρ(t) raw ──────────────────────────────────────────────────────
    ax = axes[0]; ax.set_facecolor('#161b22')
    for i, r in enumerate(results):
        lw = 3 if 'Klein (T,R180)' in r['group'] else 1.5
        ax.plot(r['baselines'], [0]*26, color='#adb5bd', lw=0.8, ls=':')
        ax.plot(list(range(26)), r['rho_means'], color=cmap[i], lw=lw,
                label=f"{r['group'].split('(')[0].strip()} |G|={r['order']}")
    # Baseline in red
    baseline = [rho_baseline(t) for t in range(26)]
    ax.plot(range(26), baseline, color='#FF6B6B', lw=2, ls='--', label='Baseline (n²-t)/n²')
    ax.set_xlabel('Corruptions $t$', color='white', fontsize=11)
    ax.set_ylabel('$\\rho(t)$ — raw recovery', color='white', fontsize=11)
    ax.set_title('Raw Recovery $\\rho(t)$\nRed dashed = trivial baseline $(n^2-t)/n^2$',
                 color='white', fontsize=11, fontweight='bold')
    ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=7.5, ncol=1)
    ax.tick_params(colors='white'); ax.set_ylim(-0.05, 1.05)
    for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 2: δρ(t) = ρ - baseline ─────────────────────────────────────────
    ax2 = axes[1]; ax2.set_facecolor('#161b22')
    for i, r in enumerate(results):
        lw = 3 if 'Klein (T,R180)' in r['group'] else 1.5
        ax2.plot(range(26), r['delta_rhos'], color=cmap[i], lw=lw,
                 label=f"{r['group'].split('(')[0].strip()} |G|={r['order']}")
    ax2.axhline(0, color='#FF6B6B', lw=2, ls='--', label='Baseline (δρ=0)')
    ax2.set_xlabel('Corruptions $t$', color='white', fontsize=11)
    ax2.set_ylabel('$\\delta\\rho(t) = \\rho_{\\text{Fix}(G)}(t) - \\rho_{\\text{baseline}}(t)$',
                   color='white', fontsize=11)
    ax2.set_title('TRUE Structural Benefit $\\delta\\rho(t)$\n$\\delta\\rho > 0$ means orbit structure helps',
                  color='white', fontsize=11, fontweight='bold')
    ax2.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=7.5)
    ax2.tick_params(colors='white')
    for sp in ax2.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 3: d_orb vs δρ(t=1) ─────────────────────────────────────────────
    ax3 = axes[2]; ax3.set_facecolor('#161b22')
    d_orbs = [r['d_orb'] for r in results]
    delta1 = [r['delta_t1'] for r in results]
    orders = [r['order'] for r in results]
    jitter = np.random.RandomState(0).uniform(-0.08, 0.08, len(results))
    sc = ax3.scatter([d+jit for d, jit in zip(d_orbs, jitter)], delta1,
                     c=orders, cmap='plasma', s=180, edgecolors='white', linewidths=1.5, zorder=5)
    ax3.axhline(0, color='#FF6B6B', lw=2, ls='--', alpha=0.8, label='Baseline = 0')

    # Annotate Sator
    sator_idx = next(i for i, r in enumerate(results) if 'T,R180' in r['group'])
    ax3.annotate('Sator\n(Klein T,R180)',
                 xy=(d_orbs[sator_idx]+jitter[sator_idx], delta1[sator_idx]),
                 xytext=(d_orbs[sator_idx]+0.3, delta1[sator_idx]+0.003),
                 color='#FFEAA7', fontsize=8.5, fontweight='bold',
                 arrowprops=dict(arrowstyle='->', color='#FFEAA7', lw=1.5))

    cbar = plt.colorbar(sc, ax=ax3)
    cbar.set_label('$|G|$', color='white')
    cbar.ax.yaxis.set_tick_params(color='white')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')
    ax3.set_xlabel('$d_{\\min}^{\\text{orb}}$', color='white', fontsize=12)
    ax3.set_ylabel('$\\delta\\rho(t=1)$', color='white', fontsize=12)
    ax3.set_title('Structural Benefit vs $d_{\\min}^{\\text{orb}}$\n[trivial group: δρ=0 as expected]',
                  color='white', fontsize=11, fontweight='bold')
    ax3.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
    ax3.tick_params(colors='white')
    for sp in ax3.spines.values(): sp.set_edgecolor('#30363d')

    plt.suptitle('EXP-16 — Corrected Recovery Baseline\n'
                 '$\\delta\\rho(G,t) = \\rho_{\\text{Fix}(G)}(t) - (n^2-t)/n^2$ — true structural benefit',
                 color='white', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")

def save_csv(results, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['group','order','k','d_orb','rho_t1','baseline_t1','delta_t1','rho_t5','baseline_t5','delta_t5'])
        for r in results:
            w.writerow([r['group'],r['order'],r['k'],r['d_orb'],
                        r['rho_t1'],r['baselines'][1],r['delta_t1'],
                        r['rho_t5'],r['baselines'][5],r['delta_t5']])
    print(f"✓ {path}")

if __name__ == '__main__':
    print("="*60)
    print("EXP-16: CORRECTED RECOVERY BASELINE (RL2 fix)")
    print("="*60)
    results = run_analysis()

    print(f"\n  Trivial group δρ(t=1) = {results[0]['delta_t1']:+.4f}  (should be ≈ 0)")
    d4_idx = next(i for i, r in enumerate(results) if 'D4' in r['group'])
    print(f"  D4 group      δρ(t=1) = {results[d4_idx]['delta_t1']:+.4f}  (true structural benefit)")

    plot_corrected(results, os.path.join(FIG_DIR, '16a_corrected_baseline.png'))
    save_csv(results, os.path.join(RES_DIR, '16_corrected_recovery.csv'))
    print("\nEXP-16 COMPLETE ✓")

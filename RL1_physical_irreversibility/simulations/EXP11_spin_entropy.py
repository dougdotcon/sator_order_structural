"""
EXP-11: Physical-Informational Reversibility — Symbolic Spin Model (RL1)
=========================================================================
Models RL1 conjecture: a symmetric subsystem S ⊂ U can maintain
local informational stability while global entropy H(U,t) grows.

Approach:
  - Global universe U: 25-symbol string undergoing random walk
    (each step: k random positions receive new random symbols)
  - Symmetric subsystem S: U projected into Fix(G) via Ma'at at each time
    (orbit-enforcement re-projects the state into the symmetric subspace)

Measures:
  - H(U, t): Shannon entropy of global string at each step
  - H(S, t): Shannon entropy of the Ma'at-projected (symmetric) version
  - ΔH(t) = H(U,t) - H(S,t): divergence of global from local

Key observation: if S maintains H(S,t) ≈ H(S,0) while H(U,t) grows,
then S is a "locally stable" informational subsystem.

Output: figures/RL1/, results/RL1/
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv, os, math
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIG_DIR = os.path.join(BASE, "figures", "RL1")
RES_DIR = os.path.join(BASE, "results", "RL1")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

N = 5
SIGMA = 26
RNG = np.random.RandomState(42)
T_MAX = 100
N_RUNS = 50

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

def make_catalog_selected(n=N):
    positions = [(i,j) for i in range(n) for j in range(n)]
    def T(p):    return (p[1], p[0])
    def R180(p): return (n-1-p[0], n-1-p[1])
    def R90(p):  return (p[1], n-1-p[0])
    def Rh(p):   return (p[0], n-1-p[1])
    def Id(p):   return p
    return [
        ("None (global)",     0,  None),             # unconstrained
        ("Z2 (T)",            2,  [T]),
        ("Klein (T, R180)",   4,  [T, R180]),         # Sator
        ("D4 (R90, T)",       8,  [R90, T]),
    ], positions

def build_state(n=N, sigma=SIGMA):
    """Random initial state (global universe)."""
    positions = [(i,j) for i in range(n) for j in range(n)]
    return {pos: RNG.randint(0, sigma) for pos in positions}

def shannon_H(state):
    vals = list(state.values())
    cnt = Counter(vals)
    total = len(vals)
    return -sum((c/total)*math.log2(c/total) for c in cnt.values() if c > 0)

def random_walk_step(state, k=3, sigma=SIGMA):
    """Apply k random symbol changes to the global state."""
    positions = list(state.keys())
    targets = RNG.choice(len(positions), size=k, replace=False)
    new_state = dict(state)
    for idx in targets:
        pos = positions[idx]
        new_state[pos] = RNG.randint(0, sigma)
    return new_state

def maat_project(state, orbits):
    """Project state into Fix(G) via orbit majority vote."""
    proj = dict(state)
    for orb in orbits:
        vals = [state[pos] for pos in orb]
        cnt = Counter(vals)
        majority = cnt.most_common(1)[0][0]
        for pos in orb:
            proj[pos] = majority
    return proj

# ─── MAIN ANALYSIS ───────────────────────────────────────────────────────────

def run_analysis():
    catalog, positions = make_catalog_selected()
    results = []

    for name, order, gens in catalog:
        if gens is not None:
            orbs = orbits_from_generators(gens, positions)
        else:
            orbs = None

        H_global_runs = []
        H_local_runs  = []

        for run in range(N_RUNS):
            state = build_state()

            H_global_t = [shannon_H(state)]
            H_local_t  = [shannon_H(state) if orbs is None else shannon_H(maat_project(state, orbs))]

            for t in range(1, T_MAX):
                state = random_walk_step(state, k=3)
                H_global_t.append(shannon_H(state))
                if orbs is not None:
                    local = maat_project(state, orbs)
                    H_local_t.append(shannon_H(local))
                else:
                    H_local_t.append(shannon_H(state))

            H_global_runs.append(H_global_t)
            H_local_runs.append(H_local_t)

        H_global_mean = np.mean(H_global_runs, axis=0)
        H_local_mean  = np.mean(H_local_runs, axis=0)
        H_global_std  = np.std(H_global_runs, axis=0)
        H_local_std   = np.std(H_local_runs, axis=0)

        delta_H = H_global_mean - H_local_mean

        results.append({
            'name': name,
            'order': order,
            'H_global_mean': H_global_mean,
            'H_local_mean':  H_local_mean,
            'H_global_std':  H_global_std,
            'H_local_std':   H_local_std,
            'delta_H':       delta_H,
            'H_local_stability': np.std(H_local_mean[10:]),  # stability after warmup
            'H_global_stability': np.std(H_global_mean[10:]),
        })
        print(f"  {name:<25} |G|={order:<3} "
              f"H_local_std={np.std(H_local_mean[10:]):.4f}  "
              f"H_global_std={np.std(H_global_mean[10:]):.4f}")

    return results

# ─── VISUALIZATIONS ──────────────────────────────────────────────────────────

def plot_main(results, save_path):
    fig, axes = plt.subplots(1, 3, figsize=(20, 7))
    fig.patch.set_facecolor('#0d1117')

    t = list(range(T_MAX))
    cmap_g  = ['#FF6B6B', '#FF9F43', '#FFEAA7', '#48cae4']
    cmap_l  = ['#f72585', '#7209b7', '#4ECDC4', '#96CEB4']

    # ── Plot 1: H(U,t) and H(S,t) for each group ─────────────────────────────
    ax = axes[0]
    ax.set_facecolor('#161b22')
    for i, r in enumerate(results):
        lw_g = 3 if i == 0 else 1.5
        ax.plot(t, r['H_global_mean'], color=cmap_g[i], lw=lw_g, ls='--',
                label=f"Global U | {r['name'].split(' ')[0]}")
        ax.fill_between(t,
                        r['H_global_mean'] - r['H_global_std'],
                        r['H_global_mean'] + r['H_global_std'],
                        color=cmap_g[i], alpha=0.08)
        ax.plot(t, r['H_local_mean'], color=cmap_l[i], lw=lw_g,
                label=f"Local S | {r['name'].split(' ')[0]}")
        ax.fill_between(t,
                        r['H_local_mean'] - r['H_local_std'],
                        r['H_local_mean'] + r['H_local_std'],
                        color=cmap_l[i], alpha=0.08)
    ax.set_xlabel('Time $t$ (random walk steps)', color='white', fontsize=11)
    ax.set_ylabel('Shannon entropy $H$ (bits)', color='white', fontsize=11)
    ax.set_title('$H(U,t)$ (dashed) vs $H(S,t)$ (solid)\nLocal subsystem vs Global evolution',
                 color='white', fontsize=11, fontweight='bold')
    ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=7, ncol=2)
    ax.tick_params(colors='white')
    for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 2: ΔH(t) = H(U,t) - H(S,t) ─────────────────────────────────────
    ax2 = axes[1]
    ax2.set_facecolor('#161b22')
    for i, r in enumerate(results[1:], 1):  # skip unconstrained (Δ=0)
        ax2.plot(t, r['delta_H'], color=cmap_l[i], lw=2.5,
                 label=f"{r['name']} |G|={r['order']}")
    ax2.axhline(0, color='white', lw=1, ls='--', alpha=0.5)
    ax2.set_xlabel('$t$', color='white', fontsize=11)
    ax2.set_ylabel('$\\Delta H(t) = H(U,t) - H(S,t)$ (bits)', color='white', fontsize=11)
    ax2.set_title('Entropy Gap Between Global and Local\n$\\Delta H > 0$ means S is more ordered than U',
                  color='white', fontsize=11, fontweight='bold')
    ax2.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
    ax2.tick_params(colors='white')
    for sp in ax2.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 3: Local stability vs group order ────────────────────────────────
    ax3 = axes[2]
    ax3.set_facecolor('#161b22')
    for i, r in enumerate(results):
        marker = 'o' if r['order'] > 0 else 's'
        color = cmap_l[i]
        ax3.scatter(r['order'] if r['order'] > 0 else 0,
                    r['H_local_stability'],
                    s=200, color=color, edgecolors='white', linewidths=1.5,
                    marker=marker, zorder=5)
        ax3.scatter(r['order'] if r['order'] > 0 else 0,
                    r['H_global_stability'],
                    s=100, color=cmap_g[i], edgecolors='white', linewidths=1.5,
                    marker='^', zorder=5, alpha=0.8)
        ax3.annotate(r['name'].split('(')[0].strip()[:12],
                     xy=(r['order'] if r['order'] > 0 else 0, r['H_local_stability']),
                     xytext=(1, 0.01), textcoords='offset points',
                     color='#adb5bd', fontsize=8)

    # proxy artists for legend
    from matplotlib.lines import Line2D
    leg = [Line2D([0],[0], marker='o', color='w', markerfacecolor='#4ECDC4', ms=10, label='$H(S,t)$ fluctuation'),
           Line2D([0],[0], marker='^', color='w', markerfacecolor='#FF6B6B', ms=10, label='$H(U,t)$ fluctuation')]
    ax3.legend(handles=leg, facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
    ax3.set_xlabel('Group order $|G|$', color='white', fontsize=11)
    ax3.set_ylabel('$\\text{Std}(H_{t>10})$ — temporal fluctuations', color='white', fontsize=11)
    ax3.set_title('Local vs Global Entropy Stability\nCircle = S (local), Triangle = U (global)',
                  color='white', fontsize=11, fontweight='bold')
    ax3.tick_params(colors='white')
    for sp in ax3.spines.values(): sp.set_edgecolor('#30363d')

    plt.suptitle('EXP-11 — RL1: Physical-Informational Reversibility\n'
                 'Symmetric subsystem S maintains local stability while global U undergoes entropy growth',
                 color='white', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")

def make_gif(results, save_path):
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('#0d1117')
    cmap_g = ['#FF6B6B', '#FF9F43', '#FFEAA7', '#48cae4']
    cmap_l = ['#f72585', '#7209b7', '#4ECDC4', '#96CEB4']

    def update(frame):
        ax.clear(); ax.set_facecolor('#161b22')
        t_now = range(frame + 1)
        for i, r in enumerate(results):
            ax.plot(list(t_now), r['H_global_mean'][:frame+1],
                    color=cmap_g[i], lw=1.8, ls='--')
            ax.plot(list(t_now), r['H_local_mean'][:frame+1],
                    color=cmap_l[i], lw=2.5,
                    label=f"S | {r['name'].split('(')[0].strip()} |G|={r['order']}")
        ax.set_xlim(0, T_MAX)
        ax.set_xlabel('$t$', color='white')
        ax.set_ylabel('$H$ (bits)', color='white')
        ax.set_title(f'RL1 — Local S vs Global U | $t = {frame}$ | dashed = $H(U)$, solid = $H(S)$',
                     color='white', fontweight='bold')
        ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=8)
        ax.tick_params(colors='white')
        for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    ani = animation.FuncAnimation(fig, update, frames=T_MAX, interval=50)
    ani.save(save_path, writer='pillow', dpi=100)
    plt.close(); print(f"✓ {save_path}")

def save_csv(results, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['group','order','H_local_stability','H_global_stability'])
        for r in results:
            w.writerow([r['name'], r['order'], r['H_local_stability'], r['H_global_stability']])
    print(f"✓ {path}")

if __name__ == '__main__':
    print("="*60)
    print("EXP-11: PHYSICAL-INFORMATIONAL REVERSIBILITY (RL1)")
    print("="*60)
    results = run_analysis()

    print(f"\n  Most stable local S: {min(results[1:], key=lambda r: r['H_local_stability'])['name']}")
    for r in results:
        ratio = r['H_local_stability'] / r['H_global_stability'] if r['H_global_stability'] > 0 else 1.0
        print(f"  {r['name']:<25} local_std={r['H_local_stability']:.4f}  "
              f"global_std={r['H_global_stability']:.4f}  ratio={ratio:.3f}")

    plot_main(results, os.path.join(FIG_DIR, '11a_entropy_evolution.png'))
    make_gif(results, os.path.join(FIG_DIR, '11b_entropy_animation.gif'))
    save_csv(results, os.path.join(RES_DIR, '11_entropy_stability.csv'))
    print("\nEXP-11 COMPLETE ✓")

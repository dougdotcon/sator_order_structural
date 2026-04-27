"""
EXP-17: Transition Entropy — Stronger Invariance Test (RL3 fix)
===============================================================
Previous: H_d = Shannon entropy of symbol frequency over all rows/columns.
PROBLEM: this is trivially equal for Fix(G) because all rows share
         the same multiset (the orbit forces it). The result is
         definitionally true, not empirically interesting.

Stronger test: Conditional (transition) entropy H(X_{t+1} | X_t)
  - Read matrix as sequence in each direction d
  - Compute empirical bigram distribution p(X_{t+1}=b | X_t=a)
  - Compute H_trans(d) = - Σ_{a,b} p(a,b) log p(b|a)

This is NOT trivially equal: the joint distribution of adjacent symbols
in different directions can differ even when marginal frequencies agree.

If Fix(G) also produces H_trans(d) = H_trans(d') for all directions,
THAT is a non-trivial invariance theorem.

Output: figures/RL3/, results/RL3/
"""
import numpy as np
import matplotlib.pyplot as plt
import csv, os, math
from collections import Counter, defaultdict

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIG_DIR = os.path.join(BASE, "figures", "RL3")
RES_DIR = os.path.join(BASE, "results", "RL3")
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RES_DIR, exist_ok=True)

N = 5
SIGMA = 26
RNG = np.random.RandomState(42)
N_TRIALS = 500

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
        ("Z4 (R90)",            4,  [R90]),
        ("D4 (R90,T)",          8,  [R90, T]),
        ("Z2^3 (T,R180,Rh)",    8,  [T, R180, Rh]),
        ("D8 (R90,T,Rh)",      16,  [R90, T, Rh]),
    ], positions

def build_fix_g(orbits, n=N):
    M = np.zeros((n, n), dtype=int)
    for orb in orbits:
        val = RNG.randint(0, SIGMA)
        for (i, j) in orb: M[i, j] = val
    return M

def build_random_matrix(n=N):
    return RNG.randint(0, SIGMA, size=(n, n))

def read_directions(M, n=N):
    """Return the four canonical sequences as flat integer lists."""
    rows = [M[i, :] for i in range(n)]
    cols = [M[:, j] for j in range(n)]
    LR = [v for row in rows for v in row]              # left to right
    RL = [v for row in rows for v in reversed(row)]   # right to left
    TB = [v for col in cols for v in col]              # top to bottom
    BT = [v for col in cols for v in reversed(col)]   # bottom to top
    return {'LR': LR, 'RL': RL, 'TB': TB, 'BT': BT}

def shannon_H(seq):
    """Marginal Shannon entropy (standard, trivially equal for Fix(G))."""
    cnt = Counter(seq); total = len(seq)
    return -sum((c/total)*math.log2(c/total) for c in cnt.values() if c > 0)

def transition_entropy(seq):
    """H(X_{t+1} | X_t) — bigram conditional entropy."""
    bigrams = list(zip(seq[:-1], seq[1:]))
    if not bigrams: return 0.0
    total = len(bigrams)
    joint = Counter(bigrams)
    marginal_a = Counter(a for a, b in bigrams)
    H_trans = 0.0
    for (a, b), c_ab in joint.items():
        p_ab = c_ab / total
        p_a  = marginal_a[a] / total
        H_trans -= p_ab * math.log2(p_ab / p_a)
    return H_trans

def compute_variances(M, measure_fn):
    seqs = read_directions(M)
    vals = [measure_fn(seqs[d]) for d in ('LR', 'RL', 'TB', 'BT')]
    return np.var(vals), np.mean(vals), vals

def run_analysis():
    catalog, positions = make_catalog()

    print(f"\n{'Group':<22} {'|G|':>5} | {'Var(H_freq)':>13}  {'Var(H_trans)':>14} | {'In F(freq)?':>12}  {'In F(trans)?':>13}")
    print("-" * 85)

    results = []
    for name, order, gens in catalog:
        orbs = orbits_from_generators(gens, positions)

        var_freq_list   = []; var_trans_list  = []
        var_freq_rand   = []; var_trans_rand  = []

        for _ in range(N_TRIALS):
            M_fix = build_fix_g(orbs)
            M_rnd = build_random_matrix()

            vf, _, _  = compute_variances(M_fix, shannon_H)
            vt, _, _  = compute_variances(M_fix, transition_entropy)
            vf_r, _, _ = compute_variances(M_rnd, shannon_H)
            vt_r, _, _ = compute_variances(M_rnd, transition_entropy)

            var_freq_list.append(vf)
            var_trans_list.append(vt)
            var_freq_rand.append(vf_r)
            var_trans_rand.append(vt_r)

        mean_vf    = np.mean(var_freq_list)
        mean_vt    = np.mean(var_trans_list)
        mean_vf_r  = np.mean(var_freq_rand)
        mean_vt_r  = np.mean(var_trans_rand)

        in_F_freq  = "YES" if mean_vf < 1e-10 else "NO"
        in_F_trans = "YES" if mean_vt < 1e-3 else "~YES" if mean_vt < 0.05 else "NO"

        results.append({
            'group': name, 'order': order,
            'var_freq_fix': mean_vf,     'var_trans_fix': mean_vt,
            'var_freq_rnd': mean_vf_r,   'var_trans_rnd': mean_vt_r,
            'in_F_freq': in_F_freq,      'in_F_trans': in_F_trans,
        })
        sator_tag = " ← SATOR" if 'T,R180' in name and 'Klein' in name else ""
        print(f"  {name:<22} {order:>5} | {mean_vf:>13.2e}  {mean_vt:>14.6f} | "
              f"{in_F_freq:>12}  {in_F_trans:>13}{sator_tag}")

    return results

def plot_comparison(results, save_path):
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor('#0d1117')

    names = [r['group'].split('(')[0].strip()[:16] for r in results]
    orders = [r['order'] for r in results]
    vf_fix = [r['var_freq_fix'] for r in results]
    vt_fix = [r['var_trans_fix'] for r in results]
    vf_rnd = [r['var_freq_rnd'] for r in results]
    vt_rnd = [r['var_trans_rnd'] for r in results]

    x = np.arange(len(results)); width = 0.35

    # ── Plot 1: Var(H_freq) — trivially zero ─────────────────────────────────
    ax = axes[0]; ax.set_facecolor('#161b22')
    ax.bar(x - width/2, vf_fix, width, label='Fix(G) — orbits',
           color='#4ECDC4', edgecolor='#30363d', alpha=0.9)
    ax.bar(x + width/2, vf_rnd, width, label='Random matrices',
           color='#FF6B6B', edgecolor='#30363d', alpha=0.9)
    ax.axhline(1e-10, color='white', lw=1.5, ls='--', alpha=0.6, label='$\\varepsilon$ threshold')
    ax.set_xticks(x)
    ax.set_xticklabels(names, rotation=45, ha='right', color='white', fontsize=7.5)
    ax.set_ylabel('$\\overline{\\mathrm{Var}(H_{\\mathrm{freq}})}$', color='white', fontsize=11)
    ax.set_title('Marginal Frequency Entropy Variance\n[CAUTION: trivially zero for Fix(G) by construction]',
                 color='white', fontsize=11, fontweight='bold')
    ax.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
    ax.set_yscale('log')
    ax.tick_params(colors='white')
    for sp in ax.spines.values(): sp.set_edgecolor('#30363d')

    # ── Plot 2: Var(H_trans) — nontrivial ─────────────────────────────────────
    ax2 = axes[1]; ax2.set_facecolor('#161b22')
    ax2.bar(x - width/2, vt_fix, width, label='Fix(G) — orbits',
            color='#4ECDC4', edgecolor='#30363d', alpha=0.9)
    ax2.bar(x + width/2, vt_rnd, width, label='Random matrices',
            color='#FF6B6B', edgecolor='#30363d', alpha=0.9)
    ax2.axhline(1e-3, color='white', lw=1.5, ls='--', alpha=0.6, label='$\\varepsilon=0.001$ threshold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, rotation=45, ha='right', color='white', fontsize=7.5)
    ax2.set_ylabel('$\\overline{\\mathrm{Var}(H_{\\mathrm{trans}})}$ — bigram entropy variance',
                   color='white', fontsize=11)
    ax2.set_title('Transition (Bigram) Entropy Variance $H(X_{t+1}|X_t)$\n'
                  '[NOT trivial: this tests joint bigram structure across directions]',
                  color='white', fontsize=11, fontweight='bold')
    ax2.legend(facecolor='#21262d', edgecolor='#30363d', labelcolor='white', fontsize=9)
    ax2.tick_params(colors='white')
    for sp in ax2.spines.values(): sp.set_edgecolor('#30363d')

    plt.suptitle('EXP-17 — Stronger Entropy Test: Marginal vs Transition\n'
                 'Left: trivially zero | Right: non-trivial invariance test',
                 color='white', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='#0d1117')
    plt.close(); print(f"✓ {save_path}")

def save_csv(results, path):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['group','order','var_freq_fix','var_trans_fix',
                                           'var_freq_rnd','var_trans_rnd','in_F_freq','in_F_trans'])
        w.writeheader(); w.writerows(results)
    print(f"✓ {path}")

if __name__ == '__main__':
    print("="*60)
    print("EXP-17: TRANSITION ENTROPY — STRONGER INVARIANCE TEST")
    print("="*60)
    results = run_analysis()

    n_strong = sum(1 for r in results if r['in_F_trans'] == 'YES')
    n_total  = len(results)
    print(f"\n  Marginal entropy F-members: {n_total}/{n_total} (trivially true)")
    print(f"  Transition entropy F-members: {n_strong}/{n_total} (non-trivial)")

    if n_strong < n_total:
        print(f"\n  IMPORTANT: Not all groups produce H_trans invariance.")
        print(f"  This distinguishes structurally rich groups from trivial ones.")
    else:
        print(f"\n  INTERESTING: H_trans invariance may also be universal for orbit structures.")

    plot_comparison(results, os.path.join(FIG_DIR, '17a_transition_entropy.png'))
    save_csv(results, os.path.join(RES_DIR, '17_transition_entropy.csv'))
    print("\nEXP-17 COMPLETE ✓")

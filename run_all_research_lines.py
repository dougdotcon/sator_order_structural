"""
run_all_research_lines.py
=========================
Master script: runs all Research Line experiments (EXP-08 to EXP-15) in sequence.
Generates a consolidated execution report.

Usage:
    python run_all_research_lines.py
"""
import subprocess, sys, os, time, csv
from datetime import datetime

PYTHON = sys.executable
BASE = os.path.dirname(os.path.abspath(__file__))

EXPERIMENTS = [
    ("EXP-08", "RL3",       "RL3_universal_entropy_invariance/simulations/EXP08_entropy_invariance.py"),
    ("EXP-09", "RL6",       "RL6_compression_limit/simulations/EXP09_kappa_compression.py"),
    ("EXP-10", "RL2",       "RL2_symmetry_protected_information/simulations/EXP10_recovery_by_group.py"),
    ("EXP-11", "RL1",       "RL1_physical_irreversibility/simulations/EXP11_spin_entropy.py"),
    ("EXP-12", "RL4",       "RL4_variational_information_principle/simulations/EXP12_action_landscape.py"),
    ("EXP-13", "RL5",       "RL5_local_arrow_of_time/simulations/EXP13_coherence_time.py"),
    ("EXP-14", "RL7",       "RL7_symbolic_physical_codes/simulations/EXP14_holographic_comparison.py"),
    ("EXP-15", "SYNTHESIS", "simulations/EXP15_universal_invariant.py"),
]

SEPARATOR = "=" * 60

def run_experiment(exp_id, rl_id, script_rel):
    script = os.path.join(BASE, script_rel)
    print(f"\n{SEPARATOR}")
    print(f"  {exp_id} ({rl_id}): {os.path.basename(script)}")
    print(SEPARATOR)

    if not os.path.exists(script):
        print(f"  [SKIP] Script not found: {script}")
        return {"exp": exp_id, "rl": rl_id, "status": "SKIP", "duration": 0}

    start = time.time()
    result = subprocess.run(
        [PYTHON, script],
        capture_output=False,
        text=True,
        encoding='utf-8',
        cwd=BASE,
    )
    duration = time.time() - start
    status = "OK" if result.returncode == 0 else "FAIL"
    print(f"\n  [{status}] {exp_id} completed in {duration:.1f}s")
    return {"exp": exp_id, "rl": rl_id, "status": status, "duration": round(duration, 1)}

def save_report(results):
    report_path = os.path.join(BASE, "results", "EXECUTION_REPORT_RL.csv")
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['exp', 'rl', 'status', 'duration'])
        w.writeheader(); w.writerows(results)
    print(f"\n✓ Report: {report_path}")

if __name__ == '__main__':
    print(f"\n{SEPARATOR}")
    print(f"  TAMESIS RESEARCH LINES — MASTER RUNNER")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(SEPARATOR)

    all_results = []
    for exp_id, rl_id, script in EXPERIMENTS:
        r = run_experiment(exp_id, rl_id, script)
        all_results.append(r)

    print(f"\n{SEPARATOR}")
    print(f"  SUMMARY")
    print(SEPARATOR)
    ok   = [r for r in all_results if r['status'] == 'OK']
    fail = [r for r in all_results if r['status'] == 'FAIL']
    skip = [r for r in all_results if r['status'] == 'SKIP']
    total_time = sum(r['duration'] for r in all_results)

    for r in all_results:
        icon = "✓" if r['status'] == 'OK' else ("✗" if r['status'] == 'FAIL' else "—")
        print(f"    {icon} {r['exp']} ({r['rl']:<12}) {r['status']:>5}  {r['duration']:>6.1f}s")

    print(f"\n  Total: {len(ok)} OK | {len(fail)} FAIL | {len(skip)} SKIP | {total_time:.1f}s")
    save_report(all_results)
    print(f"\n  ALL RESEARCH LINE EXPERIMENTS COMPLETE ✓")

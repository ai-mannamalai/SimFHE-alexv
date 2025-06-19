# Demo of FHE Polynomial evaluation using HEIR

from simfhe import params, evaluator
from simfhe.perf_counter import PerfCounter
from simfhe.experiment import run_mutiple, print_table, Target

def linear_polynomial(ct, scheme_params : params.SchemeParams):
  breakpoint()
  ct3 = ct
  stats = PerfCounter()
  stats += evaluator.multiply(ct, scheme_params.arch_param, not False, True, True)
  ct4 = ct
  stats += evaluator.key_switch(ct4, scheme_params.fresh_ctxt, scheme_params.arch_param, True, True)
  ct5 = ct4
  stats += evaluator.add(ct3, scheme_params.arch_param, True, True)
  ct6 = ct3
  stats += evaluator.add(ct6, scheme_params.arch_param, True, True)
  ct7 = ct6
  return stats


if __name__ == "__main__":
  targets = []

  # Note: Ideally, the parameters here would depend on the specific workload,
  # but currently, the emitter just uses the same parameters for all workloads.
  for scheme_params in [
#      params.Alg_benchmark_baseline,
#      params.Alg_benchmark_mod_down_merge,
#      params.Alg_benchmark_mod_down_hoist,
      params.BEST_PARAMS,
  ]:
    print(scheme_params)
    targets.append(Target("demo_heir.linear_polynomial",1, [scheme_params.fresh_ctxt,scheme_params]))

  # Run and print
  headers, data = run_mutiple(targets)
  print_table(headers, data)
  print()



from simfhe import params, evaluator
from simfhe.perf_counter import PerfCounter
from simfhe.experiment import run_mutiple, print_table, Target


def test_ops(
    input_ctxt: params.PolyContext,
    scheme_params: params.SchemeParams,
):
    stats = PerfCounter()

    # Hand-written example, to be replaced by auto-generated code

    # Let's assume our program is a*b + c*d for fresh ctxts
    # The simulator does not really care about the actual values,
    # just their sizes/etc, which is what poly_ctxt contains

    # a*b
    stats += evaluator.multiply(input_ctxt, scheme_params.arch_param)

    # c*d
    stats += evaluator.multiply(input_ctxt, scheme_params.arch_param)

    # a*b + c*d
    stats += evaluator.add(input_ctxt, scheme_params.arch_param)

    # Finally, we relinearize and rescale:
    key_ctxt = input_ctxt  # Assuming keys are the same size/etc as input ctxts
    stats += evaluator.key_switch(input_ctxt, key_ctxt, scheme_params.arch_param)
    stats += evaluator.mod_reduce_rescale(input_ctxt, scheme_params.arch_param)
    after_mul_ctxt = input_ctxt.drop()

    # Now we can do another multiplication (a*b + c*d)^2
    stats += evaluator.multiply(after_mul_ctxt, scheme_params.arch_param)
    # And finally, we can do a final relin and rescale
    stats += evaluator.key_switch(after_mul_ctxt, key_ctxt, scheme_params.arch_param)
    stats += evaluator.mod_reduce_rescale(after_mul_ctxt, scheme_params.arch_param)

    return stats


if __name__ == "__main__":
    targets = []

    # Note: Ideally, the parameters here would depend on the specific workload,
    # but currently, the emitter just uses the same parameters for all workloads.
    for scheme_params in [
        params.Alg_benchmark_baseline,
        params.Alg_benchmark_mod_down_merge,
        params.Alg_benchmark_mod_down_hoist,
        params.BEST_PARAMS,
    ]:
        print(scheme_params)

        targets.append(
            Target("generated.test_ops", 1, [scheme_params.fresh_ctxt, scheme_params])
        )

    # Run and print
    print(scheme_params)
    headers, data = run_mutiple(targets)
    print_table(headers, data)
    print()

"""Recalculate SCRUM-15 scenarios from the reviewed inputs; no AWS calls."""
import json
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    model = json.loads((root / 'docs/week2/cost-model.json').read_text())
    rates = {k: D(v) for k, v in model['rates'].items()}
    val = lambda k: D(model[k])
    ebs = val('ebs_gb') * rates['gp3_gb_month']
    storage = val('s3_total_gb') * rates['s3_gb_month']
    puts = val('s3_put_requests') * rates['s3_put_request']
    gets = val('s3_get_requests') * rates['s3_get_request']
    hourly = rates['ec2_hour'] + rates['ipv4_hour']
    allowances = model['assumed_remaining_allowances']
    usage_rates = [
        ('cloudfront_gb', 'cloudfront_gb_after_allowance'),
        ('cloudfront_https_requests', 'cloudfront_https_request_after_allowance'),
        ('invalidation_paths', 'invalidation_path_after_allowance'),
        ('ec2_egress_gb', 'ec2_egress_gb_after_allowance'),
    ]
    included = sum((max(D(0), val(k)-D(allowances[k])) * rates[r] for k, r in usage_rates), D(0))
    exhausted = sum((val(k)*rates[r] for k,r in usage_rates), D(0))
    fixed = ebs + storage + puts + gets
    results = {}
    for name, hours in [('lab',val('runtime_hours')), ('continuous',val('continuous_hours'))]:
        rows = {'ec2':hours*rates['ec2_hour'], 'ebs':ebs, 'ipv4':hours*rates['ipv4_hour'],
                's3_storage':storage, 's3_put':puts, 's3_get':gets,
                'cloudfront_and_egress_with_allowances':included}
        results[name] = {'rows':rows, 'before_account_credits':sum(rows.values(),D(0)),
                         'shared_allowances_exhausted':hours*hourly+fixed+exhausted}
    current = model['current_month']
    projection = D(current['actual_mtd']) + D(current['remaining_lab_hours'])*hourly + (ebs+storage)*D(current['retained_days'])/D(current['month_days']) + puts + gets + included
    results['current_month_conditional'] = {'projection':projection,'budget_headroom':D(5)-projection,'alert_headroom':D(4)-projection}
    results['lab_headroom'] = {'budget':D(5)-results['lab']['before_account_credits'],'alert':D(4)-results['lab']['before_account_credits']}
    results['runtime_boundaries_with_no_other_costs'] = {'hours_at_4_dollars':(D(4)-fixed-included)/hourly,'hours_at_5_dollars':(D(5)-fixed-included)/hourly}
    results['sensitivity'] = {'additional_10_running_hours':D(10)*hourly,'additional_1_gb_ebs':rates['gp3_gb_month'],'additional_1_gb_s3':rates['s3_gb_month'],'retained_ipv4_730_hours':D(730)*rates['ipv4_hour']}
    def encode(x):
        if isinstance(x,D): return str(x)
        raise TypeError(type(x).__name__)
    output = root / 'docs/week2/cost-results.json'
    output.write_text(json.dumps(results,indent=2,default=encode)+'\n')
    for name in ['lab','continuous']:
        print(name, results[name]['before_account_credits'].quantize(D('.01'),rounding=ROUND_HALF_UP))
    print('October conditional projection', projection.quantize(D('.01'),rounding=ROUND_HALF_UP))
    print('Results saved:', output)


if __name__ == '__main__':
    main()

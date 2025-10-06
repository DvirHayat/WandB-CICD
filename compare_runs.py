import os
import wandb
import wandb.apis.reports as wr

# Ensure WANDB_API_KEY is set
assert os.getenv('WANDB_API_KEY'), 'You must set the WANDB_API_KEY environment variable'


def get_baseline_run(entity='hamelsmu', project='my-report-project', tag='baseline'):
    """Get exactly one baseline run by tag, or handle gracefully if not found."""
    api = wandb.Api()
    runs = api.runs(f'{entity}/{project}', {"tags": {"$in": [tag]}})

    if len(runs) == 0:
        raise RuntimeError(f'❌ No runs found in {entity}/{project} with tag "{tag}"')
    elif len(runs) > 1:
        print(f'⚠️ Warning: Found {len(runs)} runs with tag "{tag}". Using the most recent one.')
        runs = sorted(runs, key=lambda r: r.created_at, reverse=True)

    return runs[0]


def compare_runs(entity='dvir-hayat-kla',
                 project='cicd_quickstart',
                 tag='baseline',
                 run_id=None):
    """Compare the given run to the baseline run and create a W&B report."""

    # Read environment variables if available
    entity = os.getenv('WANDB_ENTITY', entity)
    project = os.getenv('WANDB_PROJECT', project)
    tag = os.getenv('BASELINE_TAG', tag)
    run_id = os.getenv('RUN_ID', run_id)

    assert run_id, 'You must set the RUN_ID environment variable or pass a `run_id` argument'

    baseline = get_baseline_run(entity=entity, project=project, tag=tag)
    report = wr.Report(
        entity=entity,
        project=project,
        title='Compare Runs',
        description=f"A comparison of runs — baseline: {baseline.name}"
    )

    pg = wr.PanelGrid(
        runsets=[wr.Runset(entity, project, "Run Comparison")
                 .set_filters({
    'id': {'$in': [run_id, baseline.id]}}),
        panels=[wr.RunComparer(diff_only='split', layout={'w': 24, 'h': 15})]
    )

    report.blocks = report.blocks[:1] + [pg] + report.blocks[1:]
    report.save()

    # Output the report URL for GitHub Actions
    if os.getenv('CI'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as f:
            print(f'REPORT_URL={report.url}', file=f)

    return report.url


if __name__ == '__main__':
    try:
        print(f'The comparison report can be found at: {compare_runs()}')
    except Exception as e:
        print(f'❌ Error generating comparison report: {e}')
        raise

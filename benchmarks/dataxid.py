import time

from dataxid_profiling import ProfileReport

from benchmarks.utils import export_html


def profile(df, config, output_path: str):
    """
    Run DataXID profiling and export HTML.

    Returns
    -------
    report : the DataXID report object
    elapsed : float, total time in seconds (profiling + export)
    """

    start = time.perf_counter()

    report = ProfileReport(df, config=config)

    export_html(report, output_path)

    elapsed = time.perf_counter() - start

    return report, elapsed
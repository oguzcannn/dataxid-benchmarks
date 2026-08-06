import time

from data_profiling import ProfileReport

from benchmarks.utils import export_html


def profile(
    df,
    output_path: str,
    config_file: str = None,
    title: str = None,
    progress_bar: bool = False,
):
    """
    Run FG Data (YData) profiling and export HTML.

    Returns
    -------
    report : the FG Data report object
    elapsed : float, total time in seconds (profiling + export)
    """

    start = time.perf_counter()

    kwargs = {"progress_bar": progress_bar}

    if config_file is not None:
        kwargs["config_file"] = config_file

    if title is not None:
        kwargs["title"] = title

    report = ProfileReport(df, **kwargs)

    export_html(report, output_path)

    elapsed = time.perf_counter() - start

    return report, elapsed
import os

import psutil


def export_html(report, path: str) -> None:
    """
    Save a profiling report as HTML.

    Both DataXID and FG Data reports are lazy: the actual
    profiling computation only runs once an export method is
    called. This must happen inside the timed section, or the
    benchmark only measures object construction, not the real
    profiling work.
    """

    if hasattr(report, "to_file"):

        report.to_file(path)

    elif hasattr(report, "to_html"):

        html = report.to_html()

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

    else:

        raise AttributeError(
            "Report object has no to_file/to_html method, "
            "check the library's export API."
        )


def get_ram_usage_mb() -> float:
    """Current process RSS memory usage in MB."""

    process = psutil.Process(os.getpid())

    return process.memory_info().rss / 1024 / 1024
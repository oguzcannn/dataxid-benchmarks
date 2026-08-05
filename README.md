# DataXID Profiling Benchmarks

Benchmark studies for evaluating **DataXID Profiling** performance.

## Benchmarks

This repository contains comparisons between:

- DataXID Profiling vs Pandas
- DataXID Profiling vs YData Profiling

The provided benchmark scripts can be used to compare profiling performance by running the tests on different datasets.

## Metrics

Measured metrics:

- Execution time
- Memory usage
- Profiling performance
- Scalability

## Result

DataXID Profiling vs Pandas:

![DataXID vs Pandas](benchmark_dataxid_vs_pandas.png)

## Installation

```bash
pip install -r requirements.txt
```

## Run

```bash
python benchmark_dataxid_vs_pandas.py
```

```bash
python benchmark_fgdata_profiling.py
```

## Technologies

- Python
- DataXID Profiling
- Pandas
- YData Profiling
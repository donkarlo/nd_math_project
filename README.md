# ND Math

## Purpose

ND Math is an object-oriented research library for mathematical structures and operations used by the ND robotics, physics and sociomind repositories. It contains implemented numerical procedures **alongside** type abstractions, plotting prototypes and incomplete classes. Its goal is broad coverage, not a claim that every mathematical operation is implemented.

Python package: **nd_math**, under src/nd_math/.

## Module map

| Area | Code location | Representative content |
| --- | --- | --- |
| Linear algebra | src/nd_math/linear_algebra/ | Tensor, scalar, vector, matrix and vector operations |
| Geometry | src/nd_math/geometry/ | Euclidean points in multiple coordinate systems, segments, polygons, polyline paths and geometry types |
| Probability | src/nd_math/probability/ | Bayesian prior/posterior, distributions, population/statistics and discrepancy abstractions |
| Distribution distances | src/nd_math/probability/distribution/discrepancy/ | Wasserstein, Mahalanobis and Kullback–Leibler classes, including Gaussian-specific variants |
| Sequences and time series | src/nd_math/sequence/ | Periodic sequences, time-series similarity, dynamic time warping and motif discovery |
| Sets and graphs | src/nd_math/set/; src/nd_math/graph/ | Countable sets, partitions, graph/tree models |
| Visualization | src/nd_math/view/ | Shapes, point clouds, axes, scatter/bar/polar views, animation and decorators |
| Optimization wrappers | src/nd_math/platforms/ | Pyomo and Gurobi-related integration scaffolding |

### Concrete numerical work

- Dynamic time warping and alignment-path computation: src/nd_math/sequence/stocastic_process/time_series/similarity_measure/kind/dynamic_time_warping/dynamic_time_warping.py
- Variable-length motif discovery for GPS-like time series: src/nd_math/sequence/stocastic_process/time_series/similarity_measure/kind/motif_discovery/kind/period_limited_variable_length_motif_discoverer.py
- Gaussian Wasserstein distance experiment: src/nd_math/probability/distribution/discrepancy/kind/distance/kind/wasserstein/gaussian/gaussian.py

**Important:** The current Gaussian Wasserstein source contains malformed indentation/string syntax, so it is not presently importable without repair. Other files contain placeholders; the names of classes do not imply that they have complete implementations.

## Development

The project uses a src-based setuptools configuration in pyproject.toml.

~~~bash
python -m pip install -e .
~~~

There is currently no comprehensive top-level test suite. Several test/example-like modules are distributed inside the package tree. Static syntax issues should be repaired before treating package-wide test discovery as reliable. The manifest declares ruamel.yaml, but functionality in different modules also imports NumPy, Matplotlib, nd_utility, nd_physics, and additional research packages that require separate installation or source-path configuration.

The pyproject.toml script named robotix refers to nd_math.__main__:main, but src/nd_math/__main__.py is empty. It is not an operational CLI.

## Known limitations

- Five tracked Python modules failed static syntax parsing in the reviewed checkout, including the Gaussian Wasserstein distance implementation.
- Multiple packages provide abstraction/class skeletons rather than usable methods.
- Some legacy imports use older package names; import paths are not fully normalized.
- No end-to-end verification of every mathematical subsystem is implied.
- The root LICENSE file is empty; the licensing status is not specified there.

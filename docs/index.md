# Hierarchical Text Generator

A simple generator to help process free-form text data that uses
indentation to express hierarchy.  An example of data with hierarchy by indentation is:

```
USA
    Washington
        Seattle
    Wisconsin
        Madison
Canada
    British Columbia
        Vancouver
    Alberta
        Calgary
```

## Installation

### pip

``` bash
$ pip install hiergen
```

### uv

``` bash
$ uv add hiergen
$ uv sync
```

## Import

``` py
from hiergen import HierGen
```

## Quick Start and Usage

See the [Getting Started](getting_started.md) guide for a quick overview or [Usage](usage.md) for a more comprehensive look at HierGen.

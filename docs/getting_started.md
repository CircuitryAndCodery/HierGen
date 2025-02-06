# Getting Started

This is a package that allows you to take some form of hierarchical data
whose relationships are formed by indenting and creates a generator that
yields each line at a given level and, if necessary, a generator that
iterates over the the children of each line.

For example, consider the data:

``` linenums="1"
stuff
    a thing
    another thing
        color is red
    a third thind
        color is green
        shape is round
more stuff
    yet another thing
        count is 5
```

There are 2 elements: `stuff` and `more stuff`. Under `stuff` there are 3 elements: `a thing`, `another thing`, and `a third thing`. Then under `more stuff` there is just one element: `yet another thing`. Naturally, it should now be clear that, for example, under `a third thing`, there are 2 elements: `color is green` and `shape is round`.

This isn't as structured as yaml -- it is simply free-form text data that has lines and uses indentation to express parent/child relationships.

If we use a generator of class `HierGen`, then we can loop through the levels. Here is an example:

``` py title="A Basic Example" linenums="1"
from hiergen import HierGen

def process(hg: HierGen, depth: int = 0):
    for line_info in hg:
        print(f"At {depth=}, {line_info.line_no}: {line_info.line_content}")
        process(hg.children, depth + 1)

hg = HierGen.from_any(lines)  # (1)!
process(hg)
```

1.  Create the HierGen.

The output looks like:

```
```

!!! note

    This is a note.

=== "Input"

    ``` linenums="1"
    sdfss
    gfffg
    ```

=== "Processing"

    ``` py linenums="1"
    def thing():
        pass
    ```

=== "Output"

    ``` linenums="1"
    asd
    asdf
    ```

There are a handful of additional classes to make this library more useful.

The `Tokenizer` takes a line, the start, and the end, and allows you to extract tokens.

The `CommentFinder` has classes with .find(...) that look for comments in the lines and
limits the tokens. There are detectors for '#', '//', and ';'. You can make custom
comment detectors and even have detectors that span lines so you could use /* and */.

# A Full Example

This section uses a full example.


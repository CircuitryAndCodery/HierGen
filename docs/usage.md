# Usage

This section shows how to use the classes in the `hiergen` package.

This package exists to help in processing free-form text data that uses indentation
as a way to express hierarchy. That is, if a line is followed by lines that are further
indented, those are owned by the current line.

The source may contain comments that are not meant to be processed and may contain
blank lines or lines containing only whitespace.

The source can be:

* a multi-line python string
* list of lines
* a line iterator
* a text file that contains the lines

!!! warning
    This is a generator in the sense that the input is consumed once. Also each
    set of children must be consumed before advancing to the next line.

## Create a HierGen Object

The way to create a HierGen object is with the `HierGen.from_*(...)` factory methods.

The factory methods are:

* `HierGen.from_line_with_newlines(...)`
* `HierGen.from_line_list(...)`
* `HierGen.from_line_generator(...)`
* `HierGen.from_text_file(...)`
* `HierGen.from_any(...)`

The first argument is always the source of the lines to process.

The `comment_finder` argument is used to pass an object that can be used
to exclude comments in the source text.

the `source_name` can be used to specify a name of the source. For
`from_text_file` the name of the file is the default. This allows
errors to be located quickly.

=== "input.py"

    ``` py linenums="1" title="A string of hierachical data "
        STRING = """
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
        """.strip()
    ```

=== "code.py"

    ``` py linenums="1" title="Create a HierGenObject"
    from hiergen import HierGen
    from input import STRING

    hg_STRING = HierGen.from_str_with_newlines(STRING)

    for lineInfo in hg_STRING:
        print(lineInfo.line)
    ```

=== "Output"

    ```
    USA
    Canada
    ```

## Use the HierGen Object to Generate LineInfo's

There are 3 ways to get the next line in the hierarchical level from
 a `HierGen` object. Say the object is called `hg`.

 * `line_info = next(hg)` which uses `__next__()`
 * `line_info = hg.next()`
 * `for line_info in hg: ...`

## Use the LineInfo to Process A Line

The LineInfo class is for objects that have information about a single
line and its children.

It has the following properties:
* `line_info.whole_line` -- gets the whole line including the indenation and commments
* `line_info.content` -- gets the actual content part of the line
* `line_info.line_no` -- gets the 1 based line number
* `line_info.source` -- gets the name of the source
* `line_info.children` -- gets another HierGen object that covers the children of the line

### Use the Line Contents

The `line_info.content` is the content that can be processed manually. For example,
maybe the line is expected to be just one word. In that case `line_info.content` is
all that is needed to get at the line.

### Use a Tokenizer

A LineInfo also has a `create_tokenizer()` that returns a `Tokenizer`.

A Tokenizer lets you grab the next token from the content of a line. There are three
types of tokens:

* `TokenType.Normal` -- all non-whitespace characters up until the end of content or first whitespace
* `TokenType.SingleQuote` --  the token *must* start with `'` and end with `'` and everything in between is the token
* `TokenType.DoubleQuote` --  the token *must* start with `"` and end with `"` and everything in between is the token

The `TokenType` values are bitwise and can be `|`ed together. The default is the or of the three token types.

The `Tokenizer` is iterable and can return tokens in a `for token in tokenizer: ...` loop. Or for more control, `tokenizer.next(TokenType...)` can be used to get a next token of a single
type.

A cursor is stored internally and indicates where in the line content the next
processing will start. Calls to get the next token will advance to the next non-whitespace
character so the cursor is not typically sitting on whitespace.

The `Tokenizer` has some useful properties:

* `Tokenizer.cursor` -- get or set the current cursor location
* `Tokenizer.source` -- get the source_name from `LineInfo` (or filename if using a file)
* `Tokenizer.line_no` -- get the 1 based line number from `LineInfo`
* `Tokenizer.line` -- get the entire line which includes indent, content, and comment
* `Tokenizer.content` -- get just the content part of the line
* `Tokenizer.start` -- get the index of the first non-indent character
* `Tokenizer.end` -- get the index of the first comment character or the end of the line
* `Tokenizer.remaining` -- get the string that goes from the `.cursor` to the `.end`
* `Tokenizer.is_at_end` -- get a bool that is True if there are no more tokens
* `Tokenizer.char_at_cursor` -- get the character at the cursor location

The methods of `Tokenizer` are:

* `next(TokenType)` -- get the next token and advance the cursor
* `peek(TokenType)` --  get the next token without advancing the cursor

!!! note
    You can also create a tokenizer using `Tokenizer(line:str)` to tokenize the string `line`.

## Use the LineInfo.children to Process the Children

=== "cities.txt"
    ``` linenums="1" title="Input data"
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

=== "code.py"
    ``` py linenums="1" title="Process Children"
        from pathlib import Path
        from hiergen import HierGen

        def process(hg: HierGen, depth: int = 0):
            for line_info in hg:
                print(f"At {depth=}, {line_info.line_no}: {line_info.content}")
                process(line_info.children, depth + 1)

        hg = HierGen.from_any(Path("cities.txt"))  # (1)!
        process(hg)
    ```

=== "stdout"
    ```
        At depth=0, 1: USA
        At depth=1, 2: Washington
        At depth=2, 3: Seattle
        At depth=1, 4: Wisconsin
        At depth=2, 5: Madison
        At depth=0, 6: Canada
        At depth=1, 7: British Columbia
        At depth=2, 8: Vancouver
        At depth=1, 9: Alberta
        At depth=2, 10: Calgary
    ```

### Handling Comments

When there is data to be processed, there is often a desire to
explain that data inline without processing that explanation.

The `*CommentFinder` classes are used to locate comments and exclude
them from processing. The supported comment types currently are
inline `#`, `;`, and `//`.

!!! Note

    The `CommentFinder` objects will recognize strings that contain a single or double
    quote and ignore any comment starters inside the string.

=== "Code Example"

    ``` py linenums="1" title="Create a HierGenObject"
        from hiergen import HierGen, HashtagCommentFinder

        STRING = """
        USA
            Washington
                Seattle  # Not the capital--that is Olympia
            Wisconsin
        # Add more cities
                Madison
        # Some Canadian cities
        Canada
            British Columbia  # Be sure to treat this as a single token
                Vancouver
            Alberta
                Calgary
        """
        hg_STRING = HierGen.from_line_with_newlines(STRING, comment_finder=HashtagCommentFinder())

        for country_line in hg_STRING:
            for state_province_line in country_line.children:
                for city_line in state_province_line.children:
                    print(f"{city_line.content}, {state_province_line.content}, {country_line.content},")
    ```

=== "Output"

    ```
        Seattle , Washington, USA,
        Madison, Wisconsin, USA,
        Vancouver, British Columbia , Canada,
        Calgary, Alberta, Canada,
    ```
# Code Documentation

The [documentation](public_code.md) for the code is available so you don't have open up site_packages in your virtual environment.
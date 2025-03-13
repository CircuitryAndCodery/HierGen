import sys

from version import __version__

# Get tag information
expected_tag = f"/ref/tags/v{__version__}"
actual_tag = sys.argv[1]

# Test if tags match or if actual tag has suffix
if expected_tag == actual_tag or (
    actual_tag.startswith(expected_tag) and actual_tag[len(expected_tag)] == "-"
):
    # OK
    sys.exit(0)

else:
    # Is tag correct?
    print(f"Expected {expected_tag}(-.*)+ but got {actual_tag}", file=sys.stderr)
    sys.exit(1)

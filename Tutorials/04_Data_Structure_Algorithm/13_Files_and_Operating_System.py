import marimo

__generated_with = "0.13.15"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    # Table 3-3. Python file modes
    # Mode Description
    # r Read-only mode
    # w Write-only mode; creates a new file (erasing the data for any file with the same name)
    # x Write-only mode; creates a new file but fails if the file path already exists
    # a Append to existing file (creates the file if it does not already exist)
    # r+ Read and write
    # b Add to mode for binary files (i.e., "rb" or "wb")
    # t Text mode for files (automatically decoding bytes to Unicode); this is the default if not specified
    return


@app.cell
def _():
    import sys

    sys.getdefaultencoding()
    return


if __name__ == "__main__":
    app.run()

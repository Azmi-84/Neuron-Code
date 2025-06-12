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

    _path = "Tutorials/04_Data_Structure_Algorithm/file.txt"
    _f = open(_path, encoding="utf-8", mode="r")

    # for _line in _f:
    #     print(_line.strip())

    # _line = [_line.strip() for _line in open(_path, encoding="utf-8", mode="r")]
    # _line
    # _f.close()

    # with open(_path, encoding="utf-8", mode="r") as _f:
    #     _lines = [_line.strip() for _line in _f]
    # _lines
    # The `with` statement ensures that the file is properly closed after its suite finishes, even if an exception is raised.

    _f.read(100)  # Read the first 100 characters

    _f = open(_path, mode="rb")  # Opening as binary mode
    _f.read(100)
    return


@app.cell
def _():
    # Important Python file methods or attributes
    # Method/attribute Description
    # read([size]) Return data from file as bytes or string depending on the file mode, with optional size
    # argument indicating the number of bytes or string characters to read
    # readable() Return True if the file supports read operations
    # readlines([size]) Return list of lines in the file, with optional size argument
    # write(string) Write passed string to file
    # writable() Return True if the file supports write operations
    # writelines(strings) Write passed sequence of strings to the file
    # close() Close the file object
    # flush() Flush the internal I/O buffer to disk
    # seek(pos) Move to indicated file position (integer)
    # seekable() Return True if the file object supports seeking and thus random access (some file-like objects
    # do not)
    # tell() Return current file position as integer
    # closed True if the file is closed
    # encoding The encoding used to interpret bytes in the file as Unicode (typically UTF-8)
    return


@app.cell
def _():
    _path = "Tutorials/04_Data_Structure_Algorithm/file.txt"
    _f = open(_path, encoding="utf-8", mode="r")

    _f.readable()
    _f.readlines(1)
    _f.writable()
    _f.seekable()
    # _f.tell()
    _f.closed
    _f.close()
    return


if __name__ == "__main__":
    app.run()

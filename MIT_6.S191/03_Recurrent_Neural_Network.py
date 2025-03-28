import marimo

__generated_with = "0.11.0"
app = marimo.App(
    width="full",
    app_title="Recurrent Neural Network",
    auto_download=["html", "ipynb"],
)


@app.cell
def _(mo):
    mo.md(r"""# Recurrent Neural Networks (RNN)""")
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()

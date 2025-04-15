import marimo

__generated_with = "0.11.21"
app = marimo.App(width="medium", auto_download=["html", "ipynb"])


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np
    import seaborn as sns

    plt.style.use("seaborn-v0_8-whitegrid")
    return mo, np, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Material Selection for Ship Rudders""")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Abdullah al Azmi (220011230), ME 4325, Material Engineering  
        Department of Mechanical and Production Engineering, Islamic University of Technology,  
        Gazipur 1704, Bangladesh

        Ship rudders must balance mechanical performance, corrosion resistance, and sustainability in
        harsh marine environments. This paper applies Ashby's method to evaluate candidate materials
        using performance indices, trade-offs, and lifecycle considerations. Digital Ashby charts and
        property tables support the analysis.
        """
    )
    return


if __name__ == "__main__":
    app.run()

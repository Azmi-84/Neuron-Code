# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.15.0"
app = marimo.App(width="full")


@app.cell
def _(mo):
    mo.md(r"""# Design and thermodynamic analysis of a thermal power plant""")
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    In this project, you, as an individual student, are expected to design a thermal power plant which
    can generate **220 MW power** and supply electricity to the regional grid by applying the knowledge
    of thermodynamics taught in ME 4405 Applied Thermodynamics. With appropriate realistic
    assumptions, you are expected to **size the individual components** and conduct thermodynamic
    analyses, **both from 1st law and 2nd law perspectives**, **on the system components and the system
    as a whole.** The detailed calculation of the system components needs to be presented. You have
    the flexibility to decide the thermodynamic cycle the power plant will run on and the working fluid
    it will be using. You will **have to provide the specific model of the various components available in
    the market** you plan to use in your design. **The 1st law efficiency should be more than 43%.** Carry
    out a two-parameter sensitivity study (parametric analysis) and identify an optimized operating
    point. _For a Rankine cycle, vary condenser pressure and turbine inlet temperature_; for a
    _Brayton cycle, vary compressor pressure ratio and turbine inlet temperature._ On the optimized
    point, re-do the full exergy analysis and compare ηII and component exergy destructions against
    a non-optimized baseline with the same configuration.


    The following are the tasks:

    - State the thermodynamic power cycle, the operation parameters, and the assumptions you
    have considered and justify them.
    - Draw the appropriate property diagrams for the designed cycle.
    - Size the individual components and provide the specific models available in the market.
    - Develop a process flow diagram including the working components of the cycle
    - Analyze the designed cycle from 1st law and 2nd law perspectives considering individual
    components, and the cycle (heat added/rejected, work consumed/produced, exergy
    change, exergy destruction, 1st law efficiency, 2nd law efficiency etc.).
    - Show the detailed calculation.
    - Select two operating parameters appropriate to the chosen cycle. Implement the sweep in
    code and produce plots: (i) efficiency vs each parameter (other fixed) and (ii) a 2D
    map/contour of efficiency over the parameter grid.
    - From the sensitivity results, identify the optimized operating point. Recalculate full cycle
    metrics at this point (including ηI and ηII) and perform an exergetic breakdown. Compare
    ηII and component exergy destructions with a non-optimized baseline of the same
    configuration; summarize key improvements and trade-offs.
    - Provide the specific model for all commercially available power plant components you
    select, and show (with catalog specs) that they meet your calculated duties, operating
    limits, and materials constraints.
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    Components needed for the combined Brayton and Rankine Cycle:

    - For Brayton Cycle stage:
        - Compressor
        - Combustor
        - Gas turbine

    - For Rankine Cycle
        - Steam turbine
        - Condenser
        - Feedwater pumps

    - Heat Recovery Steam Generator

    - Auxilliary Systems
        - Air cooling system
        - Fuel supply system
        - Electrical generator
        - Control Systems
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    <!-- # Gas Turbine
    # https://www.siemens-energy.com/global/en/home/products-services/product/sgt5-2000e.html#/

    # Heat Recovery System
    # https://cicgroup.com/nooter-eriksen/heat-recovery-steam-generators-hrsgs/

    # Steam Turbine
    # https://www.siemens-energy.com/global/en/home/products-services/product/industrial-steam-turbines.html#Description-tab

    # Feedwater Pump
    # https://www.sulzer.com/en/shared/products/mc-high-pressure-stage-casing-pump

    # Condenser
    # https://spxcooling.com/evaporative-condensers/

    # Cooling Tower
    # https://spxcooling.com/

    # Generator
    # https://www.siemens-energy.com/global/en/home/products-services/product-offerings/generators.html

    # Control System
    # https://www.siemens-energy.com/global/en/home/products-services/product/omnivise-t3000.html -->
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import CoolProp.CoolProp as CP
    return CP, mo


@app.cell
def _():
    Pr = 12.8
    return


@app.cell
def _(CP):
    def efficiency_of_combined_brayton_and_rankine_cycle(
        P1, T3, P3, eff_pump, eff_tur
    ):
        fluid = "Water"
        h1 = CP.PropsSI("H", "P", P1, "Q", 0, fluid)
        v1 = 1 / CP.PropsSI("D", "P", P1, "Q", 0, fluid)
        P2 = P3
        w_pump = (v1 * (P2 - P1)) / eff_pump
        h2 = h1 + w_pump
        h3 = CP.PropsSI("H", "T", T3, "P", P3, fluid)
        s3 = CP.PropsSI("S", "T", T3, "P", P3, fluid)
        P4 = P1
        sg = CP.PropsSI("S", "P", P4, "Q", 1, fluid)
        sf = CP.PropsSI("S", "P", P4, "Q", 0, fluid)
        hg = CP.PropsSI("H", "P", P4, "Q", 1, fluid)
        hf = CP.PropsSI("H", "P", P4, "Q", 0, fluid)
        x4 = (s3 - sf) / (sg - sf)
        h4s = hf + x4 * (hg - hf)
        h4a = h3 - eff_tur * (h3 - h4s)
        w_tur = h3 - h4a
        # Return results for further use and plotting
        return h1, h2, h3, h4a, w_pump, w_tur
    return (efficiency_of_combined_brayton_and_rankine_cycle,)


@app.cell
def _(efficiency_of_combined_brayton_and_rankine_cycle):
    efficiency_of_combined_brayton_and_rankine_cycle(75000, 350+273, 3000000, .85, .87)
    return


if __name__ == "__main__":
    app.run()

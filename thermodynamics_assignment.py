# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "marimo",
# ]
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="full")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Design and thermodynamic analysis of a thermal power plant""")
    return


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import CoolProp.CoolProp as CP
    return CP, mo, plt


@app.cell(hide_code=True)
def _(CP):
    def get_state_properties_from_TP(T, P, fluid):
        """
        Evaluates state properties given Temperature and Pressure.
        Returns a dictionary of properties.
        """
        h = CP.PropsSI("H", "T", T, "P", P, fluid)
        s = CP.PropsSI("S", "T", T, "P", P, fluid)
        return {"T": T, "P": P, "h": h, "s": s, "fluid": fluid}
    return (get_state_properties_from_TP,)


@app.cell(hide_code=True)
def _(CP):
    def get_state_properties_from_Ps(P, s, fluid):
        """
        Evaluates state properties given Pressure and Entropy.
        Returns a dictionary of properties.
        """
        T = CP.PropsSI("T", "P", P, "S", s, fluid)
        h = CP.PropsSI("H", "P", P, "S", s, fluid)
        return {"T": T, "P": P, "h": h, "s": s, "fluid": fluid}
    return (get_state_properties_from_Ps,)


@app.cell(hide_code=True)
def _(CP):
    def get_state_properties_from_hP(h, P, fluid):
        """
        Evaluates state properties given Enthalpy and Pressure.
        Returns a dictionary of properties.
        """
        T = CP.PropsSI("T", "H", h, "P", P, fluid)
        s = CP.PropsSI("S", "H", h, "P", P, fluid)
        return {"T": T, "P": P, "h": h, "s": s}
    return (get_state_properties_from_hP,)


@app.cell(hide_code=True)
def _(
    CP,
    get_state_properties_from_Ps,
    get_state_properties_from_TP,
    get_state_properties_from_hP,
):
    def brayton_cycle_analysis(
        T1, P1, Pr, T3, fluid, eff_compressor, eff_turbine, effictiveness
    ):
        # State 1 (T, P are given)
        state1 = get_state_properties_from_TP(T1, P1, fluid)

        # State 2s (P and s from state 1)
        P2 = Pr * P1
        state2s = get_state_properties_from_Ps(P2, state1["s"], fluid)

        # State 2a (Actual state after compressor)
        h2a = state1["h"] + (state2s["h"] - state1["h"]) / eff_compressor
        # To find T and s at state 2a, we need h and P
        T2a = CP.PropsSI("T", "H", h2a, "P", P2, fluid)
        s2a = CP.PropsSI("S", "H", h2a, "P", P2, fluid)
        state2a = {"T": T2a, "P": P2, "h": h2a, "s": s2a, "fluid": fluid}

        # State 3 (T, P are given)
        P3 = P2
        state3 = get_state_properties_from_TP(T3, P3, fluid)

        # State 4s (P and s from state 3)
        P4 = P1
        state4s = get_state_properties_from_Ps(P4, state3["s"], fluid)

        # State 4a (Actual state after turbine)
        h4a = state3["h"] - eff_turbine * (state3["h"] - state4s["h"])
        # To find T and s at state 4a, we need h and P
        T4a = CP.PropsSI("T", "H", h4a, "P", P4, fluid)
        s4a = CP.PropsSI("S", "H", h4a, "P", P4, fluid)
        state4a = {"T": T4a, "P": P4, "h": h4a, "s": s4a, "fluid": fluid}

        # State 5 (after regeneration)
        h5 = state2a["h"] + effictiveness * (state4a["h"] - state2a["h"])
        # To find T and s at state 5, we need h and P
        T5 = CP.PropsSI("T", "H", h5, "P", P2, fluid)
        s5 = CP.PropsSI("S", "H", h5, "P", P2, fluid)
        state5 = {"T": T5, "P": P2, "h": h5, "s": s5, "fluid": fluid}

        # State 6 (After regeneration - heat rejected)
        # Heat absorbed by cold fluid = Heat rejected by hot fluid
        h6 = state4a["h"] - (state5["h"] - state2a["h"])
        state6 = get_state_properties_from_hP(h6, P1, fluid)

        # Calculate cycle performance metrics
        w_net = (state3["h"] - state4a["h"]) - (state2a["h"] - state1["h"])
        q_in = state3["h"] - state5["h"]
        thermal_eff = (w_net / q_in) * 100
        back_work_ratio = (state2a["h"] - state1["h"]) / (
            state3["h"] - state4a["h"]
        )

        return {
            "states": {
                "1": state1,
                "2s": state2s,
                "2a": state2a,
                "3": state3,
                "4s": state4s,
                "4a": state4a,
                "5": state5,
                "6": state6,
            },
            "metrics": {
                "w_net": w_net,
                "q_in": q_in,
                "thermal_eff": thermal_eff,
                "back_work_ratio": back_work_ratio,
            },
        }
    return (brayton_cycle_analysis,)


@app.cell
def _(mo):
    pressure_ratio_slider = mo.ui.slider(
        start=8,
        stop=30,
        step=1,
        show_value=True,
        full_width=True,
        label="Pressure Ratio",
    )

    turbine_inlet_temperature_slider = mo.ui.slider(
        start=1200,
        stop=1600,
        step=50,
        show_value=True,
        full_width=True,
        label="Turbine Inlet Temperature",
    )

    regenerator_effectiveness_slider = mo.ui.slider(
        start=0.45,
        stop=0.90,
        step=0.1,
        show_value=True,
        full_width=True,
        label="Regenerator Effectiveness",
    )
    return (
        pressure_ratio_slider,
        regenerator_effectiveness_slider,
        turbine_inlet_temperature_slider,
    )


@app.cell
def _(
    mo,
    pressure_ratio_slider,
    regenerator_effectiveness_slider,
    turbine_inlet_temperature_slider,
):
    mo.vstack(
        [
            pressure_ratio_slider,
            turbine_inlet_temperature_slider,
            regenerator_effectiveness_slider,
        ]
    )
    return


@app.cell
def _(
    pressure_ratio_slider,
    regenerator_effectiveness_slider,
    turbine_inlet_temperature_slider,
):
    T1_in = 300  # K
    P1_in = 101325  # Pa
    Pr_in = pressure_ratio_slider  # Pressure ratio
    T3_in = turbine_inlet_temperature_slider  # K
    fluid_in = "Air"
    eff_c_in = 0.88  # Compressor efficiency
    eff_t_in = 0.92  # Turbine efficiency
    eff_r_in = regenerator_effectiveness_slider  # Regenerator effectiveness
    return P1_in, Pr_in, T1_in, T3_in, eff_c_in, eff_r_in, eff_t_in, fluid_in


@app.cell
def _(
    P1_in,
    Pr_in,
    T1_in,
    T3_in,
    brayton_cycle_analysis,
    eff_c_in,
    eff_r_in,
    eff_t_in,
    fluid_in,
):
    results = brayton_cycle_analysis(
        T1_in,
        P1_in,
        Pr_in.value,
        T3_in.value,
        fluid_in,
        eff_c_in,
        eff_t_in,
        eff_r_in.value,
    )
    return (results,)


@app.cell(hide_code=True)
def _(results):
    # Print results
    print("Cycle Analysis Results:")
    print(f"Net Work (w_net): {results['metrics']['w_net']:.2f} J/kg")
    print(f"Heat Input (q_in): {results['metrics']['q_in']:.2f} J/kg")
    print(f"Thermal Efficiency: {results['metrics']['thermal_eff']:.2f}%")
    print(f"Back Work Ratio: {results['metrics']['back_work_ratio']:.2f}")
    return


@app.cell(hide_code=True)
def _(plt):
    def plot_ts_diagram(analysis_results):
        """Generates and displays a T-s diagram from analysis results."""
        states = analysis_results["states"]

        # Extracting points for plotting
        T_actual = [
            states["1"]["T"],
            states["2a"]["T"],
            states["5"]["T"],
            states["3"]["T"],
            states["4a"]["T"],
            states["6"]["T"],
            states["1"]["T"],
        ]
        s_actual = [
            states["1"]["s"],
            states["2a"]["s"],
            states["5"]["s"],
            states["3"]["s"],
            states["4a"]["s"],
            states["6"]["s"],
            states["1"]["s"],
        ]

        # Extracting points for ideal processes
        T_ideal_comp = [states["1"]["T"], states["2s"]["T"]]
        s_ideal_comp = [states["1"]["s"], states["2s"]["s"]]
        T_ideal_turb = [states["3"]["T"], states["4s"]["T"]]
        s_ideal_turb = [states["3"]["s"], states["4s"]["s"]]

        fig, ax = plt.subplots(figsize=(10, 8))

        # Plot the actual cycle (solid blue line)
        ax.plot(s_actual, T_actual, "b-o", linewidth=2, label="Actual Cycle")

        # Plot the ideal compressor and turbine processes (dashed black lines)
        ax.plot(
            s_ideal_comp, T_ideal_comp, "k--", linewidth=1, label="Ideal Processes"
        )
        ax.plot(s_ideal_turb, T_ideal_turb, "k--", linewidth=1)

        # Label all state points
        points_to_label = [
            ("1", states["1"]),
            ("2a", states["2a"]),
            ("2s", states["2s"]),
            ("3", states["3"]),
            ("4a", states["4a"]),
            ("4s", states["4s"]),
            ("5", states["5"]),
            ("6", states["6"]),
        ]

        for label, state in points_to_label:
            ax.text(
                state["s"],
                state["T"],
                f"  {label}",
                fontsize=12,
                ha="left",
                va="bottom",
            )

        # Set plot aesthetics
        ax.set_xlabel("Entropy, s (J/kg·K)", fontsize=12)
        ax.set_ylabel("Temperature, T (K)", fontsize=12)
        ax.set_title(
            "T-s Diagram of a Regenerative Brayton Cycle", fontsize=14
        )
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend()
        plt.tight_layout()
        plt.show()
    return (plot_ts_diagram,)


@app.cell(hide_code=True)
def _(plot_ts_diagram, results):
    # Generate and show the T-s diagram
    plot_ts_diagram(results)
    return


@app.cell
def _(CP):
    def calculate_saturated_liquid_state(P, fluid):
        h = CP.PropsSI("H", "P", P, "Q", 0, fluid)
        s = CP.PropsSI("S", "P", P, "Q", 0, fluid)
        d = CP.PropsSI("D", "P", P, "Q", 0, fluid)
        v = 1 / d
        T = CP.PropsSI("T", "P", P, "Q", 0, fluid)
        return {"P": P, "T": T, "h": h, "s": s, "v": v}
    return


@app.cell
def _(CP):
    def calculate_saturated_vapor_state(P, fluid):
        h = CP.PropsSI("H", "P", P, "Q", 1, fluid)
        s = CP.PropsSI("S", "P", P, "Q", 1, fluid)
        d = CP.PropsSI("D", "P", P, "Q", 1, fluid)
        v = 1 / d
        T = CP.PropsSI("T", "P", P, "Q", 1, fluid)
        return {"P": P, "T": T, "h": h, "s": s, "v": v}
    return


@app.cell
def _(CP, T):
    def calculate_superheated_vapor_state(P, fluid):
        h = CP.PropsSI("H", "P", P, "T", T, fluid)
        s = CP.PropsSI("S", "P", P, "T", T, fluid)
        d = CP.PropsSI("D", "P", P, "T", T, fluid)
        v = 1 / d
        return {"P": P, "T": T, "h": h, "s": s, "v": v}
    return


@app.cell
def _(CP):
    def boiler_outlet(P, T, fluid):
        h = CP.PropsSI("H", "P", P, "T", T, fluid)
        s = CP.PropsSI("S", "P", P, "T", T, fluid)
        d = CP.PropsSI("D", "P", P, "T", T, fluid)
        v = 1 / d
        return {"P": P, "T": T, "h": h, "s": s, "v": v}
    return


if __name__ == "__main__":
    app.run()

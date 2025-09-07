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


@app.cell
def _():
    import math
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import CoolProp.CoolProp as CP
    return CP, math, mo, np, pd, plt


@app.cell
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


@app.cell
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


@app.cell
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


@app.cell
def _(
    CP,
    get_state_properties_from_Ps,
    get_state_properties_from_TP,
    get_state_properties_from_hP,
    math,
):
    def brayton_cycle_analysis(
        T1, P1, Pr, T5, fluid, eff_compressor, eff_turbine, effectiveness
    ):
        # State 1: Initial conditions (inlet to first compressor)
        state1 = get_state_properties_from_TP(T1, P1, fluid)

        # State 2s: Isentropic compression (first stage)
        P2 = math.sqrt(Pr) * P1
        state2s = get_state_properties_from_Ps(P2, state1["s"], fluid)
        # State 2a: Actual compression with isentropic efficiency
        h2a = state1["h"] + (state2s["h"] - state1["h"]) / eff_compressor
        T2a = CP.PropsSI("T", "H", h2a, "P", P2, fluid)
        s2a = CP.PropsSI("S", "H", h2a, "P", P2, fluid)
        state2a = {"T": T2a, "P": P2, "h": h2a, "s": s2a, "fluid": fluid}

        # State 3: After intercooling (T3 equals inlet temperature T1, P3 equals P2)
        T3 = T1
        P3 = P2
        state3 = get_state_properties_from_TP(T3, P3, fluid)

        # State 4s: Isentropic compression (second stage)
        P4 = math.sqrt(Pr) * P3
        state4s = get_state_properties_from_Ps(P4, state3["s"], fluid)
        # State 4a: Actual compression after 2nd stage
        h4a = state3["h"] + (state4s["h"] - state3["h"]) / eff_compressor
        T4a = CP.PropsSI("T", "H", h4a, "P", P4, fluid)
        s4a = CP.PropsSI("S", "H", h4a, "P", P4, fluid)
        state4a = {"T": T4a, "P": P4, "h": h4a, "s": s4a, "fluid": fluid}

        # State 5: After first heat addition (first turbine inlet)
        P5 = P4
        state5 = get_state_properties_from_TP(T5, P5, fluid)

        # State 6s: Isentropic expansion (first turbine stage)
        P6 = P5 / math.sqrt(Pr)
        state6s = get_state_properties_from_Ps(P6, state5["s"], fluid)
        # State 6a: Actual expansion (first turbine, with efficiency)
        h6a = state5["h"] - eff_turbine * (state5["h"] - state6s["h"])
        T6a = CP.PropsSI("T", "H", h6a, "P", P6, fluid)
        s6a = CP.PropsSI("S", "H", h6a, "P", P6, fluid)
        state6a = {"T": T6a, "P": P6, "h": h6a, "s": s6a, "fluid": fluid}

        # State 7: Second heat addition (second turbine inlet, reheat)
        P7 = P6
        T7 = T5
        state7 = get_state_properties_from_TP(T7, P7, fluid)

        # State 8s: Isentropic expansion (second turbine stage)
        P8 = P7 / math.sqrt(Pr)
        state8s = get_state_properties_from_Ps(P8, state7["s"], fluid)
        # State 8a: Actual expansion (second turbine, with efficiency)
        h8a = state7["h"] - eff_turbine * (state7["h"] - state8s["h"])
        T8a = CP.PropsSI("T", "H", h8a, "P", P8, fluid)
        s8a = CP.PropsSI("S", "H", h8a, "P", P8, fluid)
        state8a = {"T": T8a, "P": P8, "h": h8a, "s": s8a, "fluid": fluid}

        # State 9: Regeneration—preheated air before main combustor (using effectiveness)
        h9 = state4a["h"] + effectiveness * (state8a["h"] - state4a["h"])
        T9 = CP.PropsSI("T", "H", h9, "P", P4, fluid)
        s9 = CP.PropsSI("S", "H", h9, "P", P4, fluid)
        state9 = {"T": T9, "P": P4, "h": h9, "s": s9, "fluid": fluid}

        # State 10: Air after heat rejected in regenerator
        h10 = state8a["h"] - (state9["h"] - state4a["h"])
        state10 = get_state_properties_from_hP(h10, P1, fluid)

        # Net specific work output
        w_comp = (state2a["h"] - state1["h"]) + (state4a["h"] - state3["h"])
        w_turb = (state5["h"] - state6a["h"]) + (state7["h"] - state8a["h"])
        w_net = w_turb - w_comp

        # Total heat input (Q_in)
        q_in = (state5["h"] - state9["h"]) + (state7["h"] - state6a["h"])

        # Cycle thermal efficiency (%)
        thermal_eff = (w_net / q_in) * 100

        # Back work ratio (fraction of turbine output consumed by compressor)
        back_work_ratio = w_comp / w_turb

        # Exhaust gas temperature after last turbine stage
        exhaust_gas_temperature = state10["T"]

        return {
            "states": {
                "1": state1,
                "2s": state2s,
                "2a": state2a,
                "3": state3,
                "4s": state4s,
                "4a": state4a,
                "5": state5,
                "6s": state6s,
                "6a": state6a,
                "7": state7,
                "8s": state8s,
                "8a": state8a,
                "9": state9,
                "10": state10,
            },
            "metrics": {
                "w_net": w_net,
                "q_in": q_in,
                "thermal_eff": thermal_eff,
                "back_work_ratio": back_work_ratio,
                "exhaust_gas_temperature": exhaust_gas_temperature,
            },
        }
    return (brayton_cycle_analysis,)


@app.cell
def _(mo):
    pressure_ratio_slider = mo.ui.slider(
        start=8,
        stop=25,
        step=0.5,
        show_value=True,
        full_width=True,
        label="Pressure Ratio",
    )

    turbine_inlet_temperature_slider = mo.ui.slider(
        start=1200,
        stop=1700,
        step=50,
        show_value=True,
        full_width=True,
        label="Turbine Inlet Temperature",
    )

    # regenerator_effectiveness_slider = mo.ui.slider(
    #     start=0.45,
    #     stop=0.90,
    #     step=0.1,
    #     show_value=True,
    #     full_width=True,
    #     label="Regenerator Effectiveness",
    # )
    return pressure_ratio_slider, turbine_inlet_temperature_slider


@app.cell
def _(mo, pressure_ratio_slider, turbine_inlet_temperature_slider):
    mo.vstack(
        [
            pressure_ratio_slider,
            turbine_inlet_temperature_slider,
            # regenerator_effectiveness_slider,
        ]
    )
    return


@app.cell
def _(pressure_ratio_slider, turbine_inlet_temperature_slider):
    T1_in = 300  # K
    P1_in = 101325  # Pa
    Pr_in = pressure_ratio_slider  # Pressure ratio
    T3_in = turbine_inlet_temperature_slider  # K
    fluid_in = "Air"
    eff_c_in = 0.88  # Compressor efficiency
    eff_t_in = 0.92  # Turbine efficiency
    eff_r_in = 0.9  # regenerator_effectiveness_slider  # Regenerator effectiveness
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
        eff_r_in,  # .value,
    )
    return (results,)


@app.cell
def _(pd, results):
    # Create a DataFrame from the state data for display
    table_data = []
    for state_name, properties in results["states"].items():
        row = {
            "State": state_name,
            "Temperature (K)": f"{properties['T']:.2f}",
            "Pressure (kPa)": f"{properties['P'] / 1000:.2f}",
            "Enthalpy (kJ/kg)": f"{properties['h'] / 1000:.2f}",
            "Entropy (kJ/kg·K)": f"{properties['s'] / 1000:.2f}",
        }
        table_data.append(row)

    df_states = pd.DataFrame(table_data).set_index("State")

    # Display the table
    df_states
    return


@app.cell
def _(plt):
    def plot_ts_diagram(analysis_results):
        states = analysis_results["states"]

        # Actual cycle points (using relevant key sequence)
        s_actual = [
            states["1"]["s"] / 1000,
            states["2a"]["s"] / 1000,
            states["3"]["s"] / 1000,
            states["4a"]["s"] / 1000,
            states["9"]["s"] / 1000,
            states["5"]["s"] / 1000,
            states["6a"]["s"] / 1000,
            states["7"]["s"] / 1000,
            states["8a"]["s"] / 1000,
            states["10"]["s"] / 1000,
            states["1"]["s"] / 1000,
        ]
        T_actual = [
            states["1"]["T"],
            states["2a"]["T"],
            states["3"]["T"],
            states["4a"]["T"],
            states["9"]["T"],
            states["5"]["T"],
            states["6a"]["T"],
            states["7"]["T"],
            states["8a"]["T"],
            states["10"]["T"],
            states["1"]["T"],
        ]

        # Ideal compressor and turbine expansion
        s_ideal = [
            states["1"]["s"] / 1000,
            states["2s"]["s"] / 1000,
            states["3"]["s"] / 1000,
            states["4s"]["s"] / 1000,
            states["5"]["s"] / 1000,
            states["6s"]["s"] / 1000,
            states["7"]["s"] / 1000,
            states["8s"]["s"] / 1000,
            states["1"]["s"] / 1000,
        ]
        T_ideal = [
            states["1"]["T"],
            states["2s"]["T"],
            states["3"]["T"],
            states["4s"]["T"],
            states["5"]["T"],
            states["6s"]["T"],
            states["7"]["T"],
            states["8s"]["T"],
            states["1"]["T"],
        ]

        fig, ax = plt.subplots(figsize=(10, 7))

        # Actual cycle: solid blue
        ax.plot(
            s_actual,
            T_actual,
            "b-o",
            linewidth=2,
            markersize=6,
            label="Actual States",
        )

        # Ideal cycle: dashed red
        ax.plot(
            s_ideal,
            T_ideal,
            "r--s",
            linewidth=2,
            markersize=6,
            label="Ideal States (Isentropic)",
        )

        # Label actual states
        state_labels = ["1", "2a", "3", "4a", "9", "5", "6a", "7", "8a", "10", "1"]
        for s, T, label in zip(s_actual, T_actual, state_labels):
            ax.text(
                s,
                T,
                f" {label}",
                fontsize=11,
                ha="left",
                va="bottom",
                color="blue",
            )

        # Label ideal states
        ideal_labels = ["1", "2s", "3", "4s", "5", "6s", "7", "8s", "1"]
        for s, T, label in zip(s_ideal, T_ideal, ideal_labels):
            ax.text(
                s, T, f" {label}", fontsize=11, ha="right", va="top", color="red"
            )

        # Axis, title, legend
        ax.set_xlabel("Entropy, $s$ (kJ/kg·K)", fontsize=13)
        ax.set_ylabel("Temperature, $T$ (K)", fontsize=13)
        ax.set_title("T-s Diagram: Brayton Cycle (Ideal vs. Actual)", fontsize=16)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend(loc="best", fontsize=12)
        plt.tight_layout()
        plt.show()
    return (plot_ts_diagram,)


@app.cell
def _(mo, results):
    mo.vstack(
        [
            mo.md("## Cycle Analysis Results:"),
            mo.md(f"### Net Work (w_net): {results['metrics']['w_net']:.2f} J/kg"),
            mo.md(f"### Heat Input (q_in): {results['metrics']['q_in']:.2f} J/kg"),
            mo.md(
                f"### Thermal Efficiency: {results['metrics']['thermal_eff']:.2f}%"
            ),
            mo.md(
                f"### Back Work Ratio: {results['metrics']['back_work_ratio']:.2f}"
            ),
        ]
    )
    return


@app.cell(hide_code=True)
def _(plot_ts_diagram, results):
    # Generate and show the T-s diagram
    plot_ts_diagram(results)
    return


@app.cell
def _(brayton_cycle_analysis, np):
    def sweep_efficiency(
        pr_range, t_inlet_range, fluid, eff_c, eff_t, eff_r, T1=300, P1=101325
    ):
        eff_map = np.zeros((len(pr_range), len(t_inlet_range)))
        for i, pr in enumerate(pr_range):
            for j, t_inlet in enumerate(t_inlet_range):
                results = brayton_cycle_analysis(
                    T1=T1,
                    P1=P1,
                    Pr=pr,
                    T5=t_inlet,
                    fluid=fluid,
                    eff_compressor=eff_c,
                    eff_turbine=eff_t,
                    effectiveness=eff_r,
                )
                eff_map[i, j] = results["metrics"]["thermal_eff"]
        return eff_map
    return (sweep_efficiency,)


@app.cell
def _(np):
    pr_values = np.arange(8, 26, 2)  # Pressure ratio from 8 to 24 step 2
    t_inlet_values = np.arange(
        1200, 1701, 50
    )  # Turbine inlet temp from 1200 K to 1700 K step 50
    return pr_values, t_inlet_values


@app.cell
def _(
    P1_in,
    T1_in,
    eff_c_in,
    eff_r_in,
    eff_t_in,
    fluid_in,
    pr_values,
    sweep_efficiency,
    t_inlet_values,
):
    efficiency_map = sweep_efficiency(
        pr_values,
        t_inlet_values,
        fluid_in,
        eff_c_in,
        eff_t_in,
        eff_r_in,
        T1_in,
        P1_in,
    )
    return (efficiency_map,)


@app.cell
def _(efficiency_map, np, plt, pr_values, t_inlet_values):
    # Plot 1: Efficiency vs Pressure Ratio (for selected turbine inlet temps)
    plt.figure(figsize=(10, 6))
    for idx, t_inlet in enumerate([1200, 1400, 1600, 1700]):
        if t_inlet in t_inlet_values:
            col_index = np.where(t_inlet_values == t_inlet)[0][0]
            plt.plot(
                pr_values,
                efficiency_map[:, col_index],
                marker="o",
                label=f"Turbine inlet T = {t_inlet} K",
            )
    plt.xlabel("Compressor Pressure Ratio")
    plt.ylabel("Thermal Efficiency (%)")
    plt.title("Efficiency vs Compressor Pressure Ratio")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(efficiency_map, np, plt, pr_values, t_inlet_values):
    # Plot 2: Efficiency vs Turbine Inlet Temperature (for selected pressure ratios)
    plt.figure(figsize=(10, 6))
    for pr_sel in [8, 14, 20, 24]:
        if pr_sel in pr_values:
            row_index = np.where(pr_values == pr_sel)[0][0]
            plt.plot(
                t_inlet_values,
                efficiency_map[row_index, :],
                marker="s",
                label=f"Pressure Ratio = {pr_sel}",
            )
    plt.xlabel("Turbine Inlet Temperature (K)")
    plt.ylabel("Thermal Efficiency (%)")
    plt.title("Efficiency vs Turbine Inlet Temperature")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(efficiency_map, np, plt, pr_values, t_inlet_values):
    # Plot 3: 2D Contour Map of Efficiency
    plt.figure(figsize=(12, 8))
    X, Y = np.meshgrid(t_inlet_values, pr_values)
    contour = plt.contourf(X, Y, efficiency_map, levels=30, cmap="viridis")
    plt.colorbar(contour, label="Thermal Efficiency (%)")
    plt.xlabel("Turbine Inlet Temperature (K)")
    plt.ylabel("Compressor Pressure Ratio")
    plt.title("Thermal Efficiency Contour Map")
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _():
    T0 = 298
    R = 0.287 * 1000
    return R, T0


@app.cell
def _(P1, P2, R, T0, analysis_results, math):
    # Exergy analysis
    states = analysis_results["states"]
    exergy_destruction_compressor = T0(
        states["2a"]["s"] - states["1"]["s"] - R * math.log(P2 / P1)
    )
    return


if __name__ == "__main__":
    app.run()

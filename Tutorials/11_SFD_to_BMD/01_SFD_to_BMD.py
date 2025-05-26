import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, integrate, lambdify, sympify
import sympy as sp


class SFD_to_BMD:
    def __init__(self):
        self.x = symbols("x")
        self.sfd_pieces = []
        self.bmd_pieces = []
        self.intervals = []

    def add_sfd_piece(self, equation, start, end):
        """
        Add a piece of the shear force diagram

        Parameters:
        equation (str): Shear force equation as string (e.g., '10-2*x', '5', '-3*x+15')
        start (float): Start of interval
        end (float): End of interval
        """
        try:
            # Convert string equation to sympy expression
            expr = sympify(equation)
            self.sfd_pieces.append(expr)
            self.intervals.append((start, end))
            print(f"Added SFD piece: V = {expr} for {start} ≤ x ≤ {end}")
        except Exception as e:
            print(f"Error parsing equation '{equation}': {e}")

    def calculate_bmd(self, initial_moment=0):
        """
        Calculate bending moment diagram from shear force diagram

        Parameters:
        initial_moment (float): Initial bending moment at x=0 (default: 0)
        """
        self.bmd_pieces = []
        current_moment = initial_moment

        print("\nCalculating Bending Moment Diagram:")
        print("Using relationship: dM/dx = V, so M = ∫V dx + C")
        print("-" * 50)

        for i, (sfd_expr, (start, end)) in enumerate(
            zip(self.sfd_pieces, self.intervals)
        ):
            # Integrate shear force to get bending moment
            integrated_expr = integrate(sfd_expr, self.x)

            # Determine integration constant for continuity
            if i == 0:
                # For first piece, use initial moment at start point
                C = current_moment - integrated_expr.subs(self.x, start)
            else:
                # For subsequent pieces, ensure continuity with previous piece
                prev_bmd_end = self.bmd_pieces[-1].subs(
                    self.x, self.intervals[i - 1][1]
                )
                new_bmd_start = integrated_expr.subs(self.x, start)
                C = prev_bmd_end - new_bmd_start

            # Complete bending moment expression for this piece
            bmd_expr = integrated_expr + C
            self.bmd_pieces.append(bmd_expr)

            print(f"Piece {i+1}: ({start} ≤ x ≤ {end})")
            print(f"  SFD: V = {sfd_expr}")
            print(f"  BMD: M = {bmd_expr}")
            print(f"  Integration constant C = {C}")
            print()

            # Update current moment for next piece
            current_moment = bmd_expr.subs(self.x, end)

    def plot_diagrams(self, num_points=1000):
        """
        Plot both SFD and BMD
        """
        if not self.sfd_pieces or not self.bmd_pieces:
            print("No data to plot. Please add SFD pieces and calculate BMD first.")
            return

        # Create x values for plotting
        x_min = min(interval[0] for interval in self.intervals)
        x_max = max(interval[1] for interval in self.intervals)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        # Plot each piece
        for i, ((start, end), sfd_expr, bmd_expr) in enumerate(
            zip(self.intervals, self.sfd_pieces, self.bmd_pieces)
        ):
            # Create x values for this piece
            x_vals = np.linspace(start, end, num_points // len(self.intervals))

            # Convert sympy expressions to numpy functions
            sfd_func = lambdify(self.x, sfd_expr, "numpy")
            bmd_func = lambdify(self.x, bmd_expr, "numpy")

            # Calculate y values (handle both array and scalar outputs)
            sfd_vals = sfd_func(x_vals)
            bmd_vals = bmd_func(x_vals)

            # Ensure arrays are properly shaped
            if np.isscalar(sfd_vals):
                sfd_vals = np.full_like(x_vals, sfd_vals)
            if np.isscalar(bmd_vals):
                bmd_vals = np.full_like(x_vals, bmd_vals)

            # Plot SFD
            ax1.plot(
                x_vals,
                sfd_vals,
                "b-",
                linewidth=2,
                label=f"Piece {i+1}" if i == 0 else "",
            )
            ax1.fill_between(x_vals, 0, sfd_vals, alpha=0.3, color="blue")

            # Plot BMD
            ax2.plot(
                x_vals,
                bmd_vals,
                "r-",
                linewidth=2,
                label=f"Piece {i+1}" if i == 0 else "",
            )
            ax2.fill_between(x_vals, 0, bmd_vals, alpha=0.3, color="red")

        # Format SFD plot
        ax1.set_title("Shear Force Diagram (SFD)", fontsize=14, fontweight="bold")
        ax1.set_ylabel("Shear Force (kN)", fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.axhline(y=0, color="k", linewidth=0.5)
        ax1.set_xlim(x_min, x_max)

        # Format BMD plot
        ax2.set_title("Bending Moment Diagram (BMD)", fontsize=14, fontweight="bold")
        ax2.set_xlabel("Distance (m)", fontsize=12)
        ax2.set_ylabel("Bending Moment (kN⋅m)", fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.axhline(y=0, color="k", linewidth=0.5)
        ax2.set_xlim(x_min, x_max)

        plt.tight_layout()
        plt.show()

    def get_bmd_equations(self):
        """
        Return the BMD equations as strings
        """
        equations = []
        for i, (bmd_expr, (start, end)) in enumerate(
            zip(self.bmd_pieces, self.intervals)
        ):
            equations.append(
                {
                    "piece": i + 1,
                    "equation": str(bmd_expr),
                    "interval": f"{start} ≤ x ≤ {end}",
                    "start": start,
                    "end": end,
                }
            )
        return equations

    def clear(self):
        """
        Clear all data
        """
        self.sfd_pieces = []
        self.bmd_pieces = []
        self.intervals = []
        print("All data cleared.")


# Example usage and demonstration
def example_usage():
    """
    Example demonstrating how to use the SFD to BMD converter
    """
    print("=" * 60)
    print("SHEAR FORCE TO BENDING MOMENT DIAGRAM CONVERTER")
    print("=" * 60)

    # Create converter instance
    converter = SFD_to_BMD()

    # Example 1: Simply supported beam with point load
    print("\nExample 1: Simply supported beam with point load at center")
    print("Beam length: 6m, Point load: 20kN at 3m from left support")

    converter.clear()

    # SFD pieces for this example:
    # From 0 to 3m: V = 10 kN (constant)
    # From 3 to 6m: V = -10 kN (constant)
    converter.add_sfd_piece("10", 0, 3)
    converter.add_sfd_piece("-10", 3, 6)

    # Calculate BMD
    converter.calculate_bmd(initial_moment=0)

    # Display BMD equations
    print("Resulting BMD equations:")
    bmd_equations = converter.get_bmd_equations()
    for eq in bmd_equations:
        print(f"Piece {eq['piece']}: M = {eq['equation']} for {eq['interval']}")

    # Plot diagrams
    converter.plot_diagrams()

    # Example 2: Beam with distributed load
    print("\n" + "=" * 60)
    print("\nExample 2: Cantilever beam with uniformly distributed load")
    print("Beam length: 4m, UDL: 5 kN/m")

    converter.clear()

    # For cantilever with UDL w=5 kN/m from fixed end:
    # SFD: V = -5*x (linear decrease from 0 to -20)
    converter.add_sfd_piece("-5*x", 0, 4)

    # Calculate BMD (fixed end moment will be calculated)
    converter.calculate_bmd(initial_moment=0)

    # Display results
    print("Resulting BMD equations:")
    bmd_equations = converter.get_bmd_equations()
    for eq in bmd_equations:
        print(f"Piece {eq['piece']}: M = {eq['equation']} for {eq['interval']}")

    # Plot diagrams
    converter.plot_diagrams()


# Interactive function for user input
def interactive_mode():
    """
    Interactive mode for user to input their own SFD equations
    """
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    print("Enter your piecewise shear force diagram equations.")
    print("Example equations: '10', '-5*x+20', '3*x**2-10*x+5'")
    print("Type 'done' when finished entering pieces.")
    print("Type 'help' for more information.")

    converter = SFD_to_BMD()

    while True:
        print("\nCurrent pieces:", len(converter.sfd_pieces))

        command = (
            input("\nEnter command (add/calculate/plot/clear/done/help): ")
            .strip()
            .lower()
        )

        if command == "help":
            print(
                """
Available commands:
- add: Add a new SFD piece
- calculate: Calculate BMD from current SFD pieces
- plot: Plot both SFD and BMD
- clear: Clear all data
- done: Exit interactive mode
- help: Show this help message

Equation format examples:
- Constant: '10' or '-5'
- Linear: '2*x-3' or '-0.5*x+10'
- Quadratic: 'x**2-4*x+3'
- Use * for multiplication, ** for power
            """
            )

        elif command == "add":
            try:
                equation = input("Enter SFD equation: ").strip()
                start = float(input("Enter start of interval: "))
                end = float(input("Enter end of interval: "))
                converter.add_sfd_piece(equation, start, end)
            except ValueError:
                print("Error: Please enter valid numbers for interval boundaries.")
            except Exception as e:
                print(f"Error: {e}")

        elif command == "calculate":
            if not converter.sfd_pieces:
                print("No SFD pieces added yet. Use 'add' command first.")
                continue
            try:
                initial_moment = float(
                    input("Enter initial bending moment at start (default 0): ") or "0"
                )
                converter.calculate_bmd(initial_moment)

                print("\nBMD Equations:")
                bmd_equations = converter.get_bmd_equations()
                for eq in bmd_equations:
                    print(
                        f"Piece {eq['piece']}: M = {eq['equation']} for {eq['interval']}"
                    )

            except ValueError:
                print("Error: Please enter a valid number for initial moment.")

        elif command == "plot":
            if not converter.bmd_pieces:
                print("BMD not calculated yet. Use 'calculate' command first.")
                continue
            converter.plot_diagrams()

        elif command == "clear":
            converter.clear()

        elif command == "done":
            print("Exiting interactive mode.")
            break

        else:
            print("Unknown command. Type 'help' for available commands.")


if __name__ == "__main__":
    # Run example
    example_usage()

    # Ask if user wants interactive mode
    choice = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
    if choice in ["y", "yes"]:
        interactive_mode()

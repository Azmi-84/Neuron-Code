import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sympy import symbols, integrate, lambdify, sympify
import sympy as sp


class SFD_BMD_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SFD to BMD Converter - GUI")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        # Initialize variables
        self.x = symbols("x")
        self.sfd_pieces = []
        self.bmd_pieces = []
        self.intervals = []

        # Create main frame
        self.setup_gui()

        # Initialize plot
        self.setup_plot()

    def setup_gui(self):
        """Setup the GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame, text="SFD to BMD Converter", font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Input SFD Pieces", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Equation input
        ttk.Label(input_frame, text="SFD Equation:").grid(
            row=0, column=0, sticky=tk.W, pady=2
        )
        self.equation_var = tk.StringVar()
        self.equation_entry = ttk.Entry(
            input_frame, textvariable=self.equation_var, width=30
        )
        self.equation_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=2)

        # Range inputs
        ttk.Label(input_frame, text="Start (x₁):").grid(
            row=1, column=0, sticky=tk.W, pady=2
        )
        self.start_var = tk.StringVar()
        self.start_entry = ttk.Entry(input_frame, textvariable=self.start_var, width=15)
        self.start_entry.grid(row=1, column=1, sticky=tk.W, pady=2)

        ttk.Label(input_frame, text="End (x₂):").grid(
            row=2, column=0, sticky=tk.W, pady=2
        )
        self.end_var = tk.StringVar()
        self.end_entry = ttk.Entry(input_frame, textvariable=self.end_var, width=15)
        self.end_entry.grid(row=2, column=1, sticky=tk.W, pady=2)

        # Initial moment input
        ttk.Label(input_frame, text="Initial Moment:").grid(
            row=3, column=0, sticky=tk.W, pady=2
        )
        self.initial_moment_var = tk.StringVar(value="0")
        self.initial_moment_entry = ttk.Entry(
            input_frame, textvariable=self.initial_moment_var, width=15
        )
        self.initial_moment_entry.grid(row=3, column=1, sticky=tk.W, pady=2)

        # Buttons frame
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Add Piece", command=self.add_piece).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(button_frame, text="Calculate BMD", command=self.calculate_bmd).pack(
            side=tk.LEFT, padx=2
        )
        ttk.Button(button_frame, text="Clear All", command=self.clear_all).pack(
            side=tk.LEFT, padx=2
        )

        # Current pieces display
        pieces_frame = ttk.LabelFrame(
            input_frame, text="Current SFD Pieces", padding="5"
        )
        pieces_frame.grid(
            row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
        )

        self.pieces_text = scrolledtext.ScrolledText(pieces_frame, height=8, width=40)
        self.pieces_text.pack(fill=tk.BOTH, expand=True)

        # BMD equations display
        bmd_frame = ttk.LabelFrame(input_frame, text="BMD Equations", padding="5")
        bmd_frame.grid(
            row=6, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10
        )

        self.bmd_text = scrolledtext.ScrolledText(bmd_frame, height=6, width=40)
        self.bmd_text.pack(fill=tk.BOTH, expand=True)

        # Configure column weights for input frame
        input_frame.columnconfigure(1, weight=1)
        input_frame.rowconfigure(5, weight=1)
        input_frame.rowconfigure(6, weight=1)

        # Help text
        help_text = """
Examples of equations:
• Constant: 10, -5
• Linear: 2*x-3, -0.5*x+10
• Quadratic: x**2-4*x+3
• Use * for multiplication
• Use ** for power
        """
        help_label = ttk.Label(
            input_frame, text=help_text, font=("Arial", 8), foreground="gray"
        )
        help_label.grid(row=7, column=0, columnspan=2, pady=5)

    def setup_plot(self):
        """Setup the matplotlib plot"""
        # Plot frame
        plot_frame = ttk.LabelFrame(
            self.root.children["!frame"], text="Diagrams", padding="10"
        )
        plot_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create matplotlib figure
        self.fig = Figure(figsize=(8, 8), dpi=100)
        self.ax1 = self.fig.add_subplot(211)  # SFD
        self.ax2 = self.fig.add_subplot(212)  # BMD

        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initial empty plot
        self.update_plot()

    def add_piece(self):
        """Add a piece to the SFD"""
        try:
            equation = self.equation_var.get().strip()
            start = float(self.start_var.get())
            end = float(self.end_var.get())

            if not equation:
                messagebox.showerror("Error", "Please enter an equation")
                return

            if start >= end:
                messagebox.showerror("Error", "Start must be less than end")
                return

            # Validate equation
            expr = sympify(equation)

            # Add piece
            self.sfd_pieces.append(expr)
            self.intervals.append((start, end))

            # Update display
            self.update_pieces_display()

            # Clear input fields
            self.equation_var.set("")
            self.start_var.set("")
            self.end_var.set("")

            # Auto-calculate if this is not the first piece
            if len(self.sfd_pieces) > 0:
                self.calculate_bmd()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid number format: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid equation: {e}")

    def calculate_bmd(self):
        """Calculate BMD from SFD pieces"""
        if not self.sfd_pieces:
            messagebox.showwarning("Warning", "No SFD pieces added")
            return

        try:
            initial_moment = float(self.initial_moment_var.get())
        except ValueError:
            initial_moment = 0

        self.bmd_pieces = []
        current_moment = initial_moment

        for i, (sfd_expr, (start, end)) in enumerate(
            zip(self.sfd_pieces, self.intervals)
        ):
            # Integrate shear force to get bending moment
            integrated_expr = integrate(sfd_expr, self.x)

            # Determine integration constant for continuity
            if i == 0:
                C = current_moment - integrated_expr.subs(self.x, start)
            else:
                prev_bmd_end = self.bmd_pieces[-1].subs(
                    self.x, self.intervals[i - 1][1]
                )
                new_bmd_start = integrated_expr.subs(self.x, start)
                C = prev_bmd_end - new_bmd_start

            # Complete bending moment expression
            bmd_expr = integrated_expr + C
            self.bmd_pieces.append(bmd_expr)

            # Update current moment for next piece
            current_moment = bmd_expr.subs(self.x, end)

        # Update displays
        self.update_bmd_display()
        self.update_plot()

    def update_pieces_display(self):
        """Update the current pieces display"""
        self.pieces_text.delete(1.0, tk.END)
        for i, (expr, (start, end)) in enumerate(zip(self.sfd_pieces, self.intervals)):
            text = f"Piece {i+1}: V = {expr}\n"
            text += f"  Range: {start} ≤ x ≤ {end}\n\n"
            self.pieces_text.insert(tk.END, text)

    def update_bmd_display(self):
        """Update the BMD equations display"""
        self.bmd_text.delete(1.0, tk.END)
        for i, (expr, (start, end)) in enumerate(zip(self.bmd_pieces, self.intervals)):
            text = f"Piece {i+1}: M = {expr}\n"
            text += f"  Range: {start} ≤ x ≤ {end}\n\n"
            self.bmd_text.insert(tk.END, text)

    def update_plot(self):
        """Update the plot with current data"""
        # Clear axes
        self.ax1.clear()
        self.ax2.clear()

        if not self.sfd_pieces:
            # Empty plot
            self.ax1.set_title("Shear Force Diagram (SFD)", fontweight="bold")
            self.ax1.set_ylabel("Shear Force (kN)")
            self.ax1.grid(True, alpha=0.3)

            self.ax2.set_title("Bending Moment Diagram (BMD)", fontweight="bold")
            self.ax2.set_xlabel("Distance (m)")
            self.ax2.set_ylabel("Bending Moment (kN⋅m)")
            self.ax2.grid(True, alpha=0.3)

            self.canvas.draw()
            return

        # Plot data
        colors = ["blue", "red", "green", "orange", "purple", "brown"]

        for i, ((start, end), sfd_expr) in enumerate(
            zip(self.intervals, self.sfd_pieces)
        ):
            # Create x values for this piece
            x_vals = np.linspace(start, end, 100)
            color = colors[i % len(colors)]

            # SFD
            sfd_func = lambdify(self.x, sfd_expr, "numpy")
            sfd_vals = sfd_func(x_vals)

            # Handle scalar case
            if np.isscalar(sfd_vals):
                sfd_vals = np.full_like(x_vals, sfd_vals)

            self.ax1.plot(
                x_vals, sfd_vals, color=color, linewidth=2, label=f"Piece {i+1}"
            )
            self.ax1.fill_between(x_vals, 0, sfd_vals, alpha=0.3, color=color)

            # BMD (if calculated)
            if i < len(self.bmd_pieces):
                bmd_func = lambdify(self.x, self.bmd_pieces[i], "numpy")
                bmd_vals = bmd_func(x_vals)

                # Handle scalar case
                if np.isscalar(bmd_vals):
                    bmd_vals = np.full_like(x_vals, bmd_vals)

                self.ax2.plot(
                    x_vals, bmd_vals, color=color, linewidth=2, label=f"Piece {i+1}"
                )
                self.ax2.fill_between(x_vals, 0, bmd_vals, alpha=0.3, color=color)

        # Format plots
        self.ax1.set_title("Shear Force Diagram (SFD)", fontweight="bold")
        self.ax1.set_ylabel("Shear Force (kN)")
        self.ax1.grid(True, alpha=0.3)
        self.ax1.axhline(y=0, color="k", linewidth=0.5)
        if len(self.sfd_pieces) > 1:
            self.ax1.legend()

        self.ax2.set_title("Bending Moment Diagram (BMD)", fontweight="bold")
        self.ax2.set_xlabel("Distance (m)")
        self.ax2.set_ylabel("Bending Moment (kN⋅m)")
        self.ax2.grid(True, alpha=0.3)
        self.ax2.axhline(y=0, color="k", linewidth=0.5)
        if len(self.bmd_pieces) > 1:
            self.ax2.legend()

        # Set x-axis limits
        if self.intervals:
            x_min = min(interval[0] for interval in self.intervals)
            x_max = max(interval[1] for interval in self.intervals)
            self.ax1.set_xlim(x_min, x_max)
            self.ax2.set_xlim(x_min, x_max)

        plt.tight_layout()
        self.canvas.draw()

    def clear_all(self):
        """Clear all data"""
        self.sfd_pieces = []
        self.bmd_pieces = []
        self.intervals = []

        # Clear displays
        self.pieces_text.delete(1.0, tk.END)
        self.bmd_text.delete(1.0, tk.END)

        # Clear input fields
        self.equation_var.set("")
        self.start_var.set("")
        self.end_var.set("")
        self.initial_moment_var.set("0")

        # Update plot
        self.update_plot()

        messagebox.showinfo("Success", "All data cleared")


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = SFD_BMD_GUI(root)

    # Add some example data on startup
    example_choice = messagebox.askyesno(
        "Load Example",
        "Would you like to load an example?\n\n"
        "Simply supported beam (6m) with 20kN point load at center",
    )

    if example_choice:
        # Add example pieces
        app.sfd_pieces = [sympify("10"), sympify("-10")]
        app.intervals = [(0, 3), (3, 6)]
        app.update_pieces_display()
        app.calculate_bmd()

    root.mainloop()


if __name__ == "__main__":
    main()

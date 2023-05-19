import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def check_drift_ratios():
    try:
        levels = [int(level.strip()) for level in level_entry.get().split(",")]
        seismic_drift_ratios = [float(drift_ratio.strip()) for drift_ratio in seismic_entry.get().split(",")]
        wind_drift_ratios = [float(drift_ratio.strip()) for drift_ratio in wind_entry.get().split(",")]

        result_text = ""
        for level, seismic_ratio, wind_ratio in zip(levels, seismic_drift_ratios, wind_drift_ratios):
            result_text += f"Level {level}:\n"
            if seismic_ratio > 0.01:
                result_text += f"  - Seismic drift ratio exceeds the value recommended by Eurocode.\n"
            else:
                result_text += f"  - Seismic drift ratio is within the allowable limit.\n"

            if wind_ratio > 0.02:
                result_text += f"  - Wind drift ratio exceeds the value recommended by Eurocode.\n"
            else:
                result_text += f"  - Wind drift ratio is within the allowable limit.\n"

            result_text += "\n"

        result_label.configure(text=result_text)
        export_button.configure(state=tk.NORMAL)  # Enable export button

        # Clear existing items in treeview
        tree.delete(*tree.get_children())

        # Insert new items in treeview
        for level, seismic_ratio, wind_ratio in zip(levels, seismic_drift_ratios, wind_drift_ratios):
            tree.insert("", tk.END, values=(level, seismic_ratio, wind_ratio))

    except ValueError:
        result_label.configure(text="Error: Invalid input. Please enter valid levels and drift ratios.")
        export_button.configure(state=tk.DISABLED)  # Disable export button

def export_results():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
    if file_path:
        with open(file_path, "w") as file:
            file.write(result_label.cget("text"))

# Create the main window
window = tk.Tk()
window.title("Drift Ratio Checker")

# Create level input
level_label = ttk.Label(window, text="Levels:")
level_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
level_entry = ttk.Entry(window, width=30)
level_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Create seismic drift ratio input
seismic_label = ttk.Label(window, text="Seismic Drift Ratios:")
seismic_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
seismic_entry = ttk.Entry(window, width=30)
seismic_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Create wind drift ratio input
wind_label = ttk.Label(window, text="Wind Drift Ratios:")
wind_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
wind_entry = ttk.Entry(window, width=30)
wind_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

# Create check button
check_button = ttk.Button(window, text="Check", command=check_drift_ratios)
check_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

# Create result label
result_label = ttk.Label(window, text="")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Create export button
export_button = ttk.Button(window, text="Export Results", command=export_results, state=tk.DISABLED)
export_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

# Create treeview for displaying levels and drift ratios
tree = ttk.Treeview(window)
tree.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
tree["columns"] = ("level", "seismic_drift_ratio", "wind_drift_ratio")
tree.column("level", width=100, anchor="center")
tree.column("seismic_drift_ratio", width=150, anchor="center")
tree.column("wind_drift_ratio", width=150, anchor="center")
tree.heading("level", text="Level")
tree.heading("seismic_drift_ratio", text="Seismic Drift Ratio")
tree.heading("wind_drift_ratio", text="Wind Drift Ratio")

# Configure treeview to show alternating row colors
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25)
style.map("Treeview", background=[("selected", "#347083")])
style.map("Treeview", foreground=[("selected", "white")])

# Configure scrollbars for the treeview
scroll_y = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
scroll_y.grid(row=6, column=2, sticky="ns")
tree.configure(yscrollcommand=scroll_y.set)

# Apply styling
window.configure(bg="#f0f0f0")
level_label.configure(font=("Arial", 12))
level_entry.configure(font=("Arial", 12))
seismic_label.configure(font=("Arial", 12))
seismic_entry.configure(font=("Arial", 12))
wind_label.configure(font=("Arial", 12))
wind_entry.configure(font=("Arial", 12))
check_button.configure(style="Accent.TButton")
result_label.configure(font=("Arial", 12), wraplength=400)
tree.configure(style="Custom.Treeview")
export_button.configure(style="Accent.TButton")

# Start the GUI event loop
window.mainloop()

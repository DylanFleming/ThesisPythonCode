# =========================================================================
#           VNA Calibration Device Graphic User Interface
#           By Dylan Fleming, 45313345
# =========================================================================

# Imports required
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import socket
import skrf as rf
from skrf.calibration import SOLT
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


def show_error_popup(message):
    """
    show_error_popup displays a message popup window with a given error message
    :param message: A text string regarding the error or popup to be displayed
    :return: NULL
    """
    messagebox.showerror("Error", message)


def log_message(message):
    """
    log_message displays a message received as a chat log
    :param message: A text string regarding the message to be added to log
    :return: NULL
    """
    message_window.insert(tk.END, message + '\n')
    message_window.see(tk.END)


def vna_setup(connection):
    """
    vna_setup initiates the VNA through a series of SCPI commands
    :param connection: The LAN or USB connection details
    :return: NULL
    """

    # Set-up commands for VNA
    commands = [
        "SYST:PRES\n", "SENS:SWE:POIN 100\n", "CALC:PAR1:DEF S21\n",
        "CALC:PAR1:SEL\n", "CALC:FORM MLOG\n", "SENS:BAND 10\n",
        ":TRIG:SOUR BUS\n", ":TRIG:SING\n", "*OPC?\n"
    ]

    # Iterate through commands, send to VNA device
    for command in commands:
        connection.sendall(command.encode('utf-8'))
        response = connection.recv(1024)
        log_message(f"Sent: {command.strip()}")
        log_message(f"Received: {response.decode('utf-8').strip()}")


def update_frequency_range(connection, start_freq, end_freq):
    """
    update_frequency_range updates the VNA operating frequency range
    :param connection: The LAN or USB connection details
    :param start_freq: The starting frequency value
    :param end_freq: The ending frequency value
    :return: NULL
    """

    # Commands for updating start and end frequency
    commands = [
        f"SENS:FREQ:START {start_freq}\n", f"SENS:FREQ:STOP {end_freq}\n"
    ]

    # Iterate through commands, send to VNA device
    for command in commands:
        connection.sendall(command.encode('utf-8'))
        response = connection.recv(1024)
        log_message(f"Sent: {command.strip()}")
        log_message(f"Received: {response.decode('utf-8').strip()}")


def start_calibration_type(connection, command):
    """
    start_calibration_type sends commands to the VNA to initiate calibration
    :param connection: The LAN or USB connection details
    :param command: The command message to send to the VNA
    :return: NULL
    """

    # Command from input, wait command and response from VNA
    commands = [command, "*WAI\n", "*OPC?\n"]
    for cmd in commands:
        connection.sendall(cmd.encode('utf-8'))
        response = connection.recv(1024)
        log_message(f"Sent: {cmd.strip()}")
        log_message(f"Received: {response.decode('utf-8').strip()}")

def calibrate():
    """
    calibrate provides the implementation to conduct calibration with the VNA through the GUI
    :return: NULL
    """

    # Obtain the details from the given user inputs
    selected_methods = [method for method, var in method_vars.items() if var.get()]
    start_freq_counter_value = int(start_freq_counter_var.get())
    end_freq_counter_value = int(end_freq_counter_var.get())
    start_freq_unit = start_freq_unit_var.get()
    end_freq_unit = end_freq_unit_var.get()
    num_ports = ports_entry.get()

    # Add multiplication weightings to frequency
    if start_freq_unit == "Hz":
        start_freq_counter_value *= 1
    elif start_freq_unit == "kHz":
        start_freq_counter_value *= 1e3
    elif start_freq_unit == "MHz":
        start_freq_counter_value *= 1e6
    elif start_freq_unit == "GHz":
        start_freq_counter_value *= 1e9

    if end_freq_unit == "Hz":
        end_freq_counter_value *= 1
    elif end_freq_unit == "kHz":
        end_freq_counter_value *= 1e3
    elif end_freq_unit == "MHz":
        end_freq_counter_value *= 1e6
    elif end_freq_unit == "GHz":
        end_freq_counter_value *= 1e9

    # Error checking and handling
    if start_freq_counter_value <= 0:
        show_error_popup("Start frequency must be greater than 0.")
        return
    if end_freq_counter_value <= 0:
        show_error_popup("End frequency must be greater than 0.")
        return
    if start_freq_counter_value >= end_freq_counter_value:
        show_error_popup("Start frequency must be less than end frequency.")
        return
    if start_freq_counter_value > 6e9 or end_freq_counter_value > 6e9:
        show_error_popup("Frequency values cannot exceed 6 GHz.")
        return
    if not num_ports.isdigit():
        show_error_popup("Number of ports must be a valid number.")
        return

    # Try the LAN connection
    try:
        # LAN Details
        host = '127.0.0.1'
        port = 5025
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((host, port))

        # Conduct VNA setup
        vna_setup(connection)
        update_frequency_range(connection, start_freq_counter_value, end_freq_counter_value)

        # Display a loading bar while calibrating
        loading_bar_popup = tk.Toplevel(root)
        loading_bar_popup.title("Calibration Progress")
        loading_bar_popup.geometry("300x50")

        progress_label = ttk.Label(loading_bar_popup, text="Calibrating...", style='Custom.TLabel')
        progress_label.pack()

        progress = ttk.Progressbar(loading_bar_popup, orient='horizontal', length=200, mode='determinate')
        progress.pack()

        def update_progress():
            """
            update_progress updates the progress bar according to the calibration progress
            :return: NULL
            """
            progress.step(100 / len(selected_methods))

        for method in selected_methods:
            start_calibration_type(connection, f"CALIBRATION:{method.upper()}")
            update_progress()

        # Close the connection when finished
        connection.close()

        # Remove the loading bar
        loading_bar_popup.destroy()

        # Plot the calibration results
        plot_calibration_results()

    except Exception as e:
        show_error_popup(f"Error communicating with instrument: {e}")


def plot_calibration_results():
    """
    plot_calibration_results plots an example of the calibration results
    :return: NULL
    """
    de = rf.Network('SParam/De_embed/de-embed.s2p')
    ideals = [
        rf.Network('SParam/Ideals/Short_Ideal.s2p'),
        rf.Network('SParam/Ideals/Open_Ideal.s2p'),
        rf.Network('SParam/Ideals/Load_Ideal.s2p'),
        rf.Network('SParam/Ideals/Thru_Ideal.s2p'),
    ]
    measured = [
        rf.Network('SParam/Meas/1000mm_line_short.s2p'),
        rf.Network('SParam/Meas/1000mm_line_open.s2p'),
        rf.Network('SParam/Meas/1000mm_line_load.s2p'),
        rf.Network('SParam/Meas/1000mm_line_thru.s2p'),
    ]

    cal1 = SOLT(
        ideals=ideals,
        measured=measured,
    )

    cal1.run()

    dut = rf.Network('SParam/DUTs/1m_cable_LPF_1-35P_3dbRipple.s2p')
    dut_calibrated = cal1.apply_cal(dut)
    dut_calibrated.t = np.linalg.inv(de.t) @ dut_calibrated.t @ np.linalg.inv(de.t)

    # Clear the existing plot
    ax.clear()
    dut_calibrated.plot_s_smith(ax=ax)

    # Draw the updated plot on the canvas
    canvas.draw()


def update_start_freq_counter(change):
    """
    update_start_freq_counter updates the frequency counter staring point
    :param change: The value of the change in frequency for start frequency
    :return: NULL
    """
    current_value = int(start_freq_counter_var.get())
    new_value = current_value + change
    start_freq_counter_var.set(str(new_value))


def update_end_freq_counter(change):
    """
    update_end_freq_counter updates the frequency counter ending point
    :param change: The value of the change in frequency for end frequency
    :return: NULL
    """
    current_value = int(end_freq_counter_var.get())
    new_value = current_value + change
    end_freq_counter_var.set(str(new_value))


def clear_selection():
    """
    clear_selection removes calibration method variables
    :return: NULL
    """
    for var in method_vars.values():
        var.set(False)


def select_standard(methods):
    """
    select_standard sets the calibration standards to be conducted
    :return: NULL
    """
    clear_selection()
    for method in methods:
        method_vars[method].set(True)


def on_exit():
    """
    on_exit displays a message box to confirm GUI closure
    :return: NULL
    """
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()


# Create a Tkinter window
root = tk.Tk()
root.title("VNA Calibration Tool")

root.configure(background='white')
root.protocol("WM_DELETE_WINDOW", on_exit)

# Define style for labels, buttons, etc.
style = ttk.Style()
style.configure('Custom.TLabel', foreground='#49075e', background='white', font=('Arial', 12, 'bold'))
style.configure('Custom.TEntry', fieldbackground='white', font=('Arial', 12))
style.configure('Custom.TButton', foreground='#49075e', background='white', font=('Arial', 12, 'bold'))
style.configure('Custom.TCheckbutton', background='white', font=('Arial', 12))
style.configure('Title.TLabel', foreground='white', background='#49075e', font=('Arial', 12, 'bold'))

# Create a title header
title_frame = ttk.Frame(root)
title_frame.grid(row=0, column=0, columnspan=7, sticky=tk.EW)
title_label = ttk.Label(title_frame, text="VNA Calibration Tool", style='Title.TLabel')
title_label.grid(row=0, column=0, columnspan=7, sticky=tk.EW)
title_label.pack()

# Calibration method selection panel
method_label = ttk.Label(root, text="Calibration Method:", style='Custom.TLabel')
method_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)

method_vars = {}
methods = ["Short", "Open", "Load", "Thru", "DUT"]
for i, method in enumerate(methods):
    var = tk.BooleanVar()
    method_vars[method] = var
    chk = ttk.Checkbutton(root, text=method, variable=var, style='Custom.TCheckbutton')
    chk.grid(row=i % 4 + 2, column=i // 4, sticky=tk.W, padx=10, pady=5)

# Standard Calibration Methods section
standard_label = ttk.Label(root, text="Standard Calibration Methods:", style='Custom.TLabel')
standard_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)

solt_button = ttk.Button(root, text="SOLT", command=lambda: select_standard(["Short", "Open", "Load", "Thru"]),
                         style='Custom.TButton')
solt_button.grid(row=7, column=0, padx=10, pady=5)

sl_button = ttk.Button(root, text="DUT", command=lambda: select_standard(["DUT"]),
                       style='Custom.TButton')
sl_button.grid(row=7, column=1, padx=10, pady=5)

# Frequency range panel
frequency_label = ttk.Label(root, text="Frequency Range:", style='Custom.TLabel')
frequency_label.grid(row=8, column=0, columnspan=2, sticky=tk.W, padx=10, pady=10)

start_freq_label = ttk.Label(root, text="Start Frequency:", style='Custom.TLabel')
start_freq_label.grid(row=9, column=0, sticky=tk.W, padx=10, pady=5)

start_freq_counter_var = tk.StringVar(value='1')
start_freq_counter = ttk.Entry(root, textvariable=start_freq_counter_var, width=10, style='Custom.TEntry')
start_freq_counter.grid(row=9, column=1, sticky=tk.W, padx=10, pady=5)

start_freq_unit_var = tk.StringVar(value='kHz')
start_freq_unit_menu = ttk.OptionMenu(root, start_freq_unit_var, 'kHz', 'Hz','kHz', 'MHz', 'GHz')
start_freq_unit_menu.grid(row=9, column=2, sticky=tk.W, padx=10, pady=5)

end_freq_label = ttk.Label(root, text="End Frequency:", style='Custom.TLabel')
end_freq_label.grid(row=10, column=0, sticky=tk.W, padx=10, pady=5)

end_freq_counter_var = tk.StringVar(value='1')
end_freq_counter = ttk.Entry(root, textvariable=end_freq_counter_var, width=10, style='Custom.TEntry')
end_freq_counter.grid(row=10, column=1, sticky=tk.W, padx=10, pady=5)

end_freq_unit_var = tk.StringVar(value='kHz')
end_freq_unit_menu = ttk.OptionMenu(root, end_freq_unit_var, 'kHz', 'Hz','kHz', 'MHz', 'GHz')
end_freq_unit_menu.grid(row=10, column=2, sticky=tk.W, padx=10, pady=5)

# Port entry panel
ports_label = ttk.Label(root, text="Number of Ports:", style='Custom.TLabel')
ports_label.grid(row=11, column=0, sticky=tk.W, padx=10, pady=5)

ports_entry = ttk.Entry(root, width=10, style='Custom.TEntry')
ports_entry.grid(row=11, column=1, sticky=tk.W, padx=10, pady=5)

# Calibrate button
calibrate_button = ttk.Button(root, text="Calibrate", command=calibrate, style='Custom.TButton')
calibrate_button.grid(row=12, column=0, columnspan=2, padx=10, pady=10)

# Smith Chart Label
smith_chart_label = ttk.Label(root, text="Calibration Output:", style='Custom.TLabel')
smith_chart_label.grid(row=1, column=4, columnspan=2, sticky=tk.W, padx=10, pady=10)

# Create a Figure and Axis for Smith Chart
fig, ax = plt.subplots(figsize=(2,2))  # Fixed size for Smith chart
s = rf.Network()  # Create an empty Network object
s.plot_s_smith(ax=ax)

# Add the figure to the Tkinter window using a Canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=2, column=4, rowspan=4, columnspan=2, sticky='nsew')

# Set column and row weights to prevent stretching
root.grid_columnconfigure(4, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=0)

# Message window for SCPI commands
message_window_label = ttk.Label(root, text="SCPI Command Log:", style='Custom.TLabel')
message_window_label.grid(row=7, column=4, columnspan=2, sticky=tk.W, padx=10, pady=10)

message_window = scrolledtext.ScrolledText(root, width=80, height=10, wrap=tk.WORD)
message_window.grid(row=8, rowspan=6, column=4, columnspan=3, padx=10, pady=5)

# Clear selection button
clear_button = ttk.Button(root, text="Clear Selection", command=clear_selection, style='Custom.TButton')
clear_button.grid(row=13, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
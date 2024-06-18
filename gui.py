import tkinter as tk
from tkinter import filedialog
from uvsim import UVSim

# Show Help Frame
def show_help():
    """
    Function to display a help window with instructions for using the UVSim.
    """
    help_window = tk.Toplevel(root)
    help_window.title("Help and Instructions")
    help_label = tk.Label(help_window, text="Instructions\n\n1. Select a test file to load the program.\n"
                                            "2. Use the Start button to begin simulation.\n"
                                            "3. Use Step button to execute instructions one at a time.\n"
                                            "4. Use the Halt button to stop the simulation.\n"
                                            "5. Refer to the opcode definitions for specific actions (e.g., READ, WRITE, LOAD, etc.).")
    help_label.pack(pady=20, padx=20)
    close_button = tk.Button(help_window, text="CLOSE", command=help_window.destroy)
    close_button.pack(pady=10)

def start_program():
    """
    Function to transition from the title screen to the file selection screen.
    """
    title_frame.pack_forget()
    file_selection_frame.pack()

def browse_files():
    """
    Function to open a file dialog for selecting a test file.
    """
    file_path = filedialog.askopenfilename(initialdir="./bml_examples", title="Select a File",
                                           filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

def load_file():
    """
    Function to load the selected file into the UVSim and transition to the main control screen.
    """
    file_path = file_entry.get()
    if file_path:
        print(f"Attempting to load file: {file_path}")
        uvsim.load(file_path)
        print(f"File loaded successfully: {file_path}")
        file_selection_frame.pack_forget()
        main_control_frame.pack()
        update_main_control_frame()

def update_main_control_frame():
    """
    Function to update the memory display and current instruction display in the main control frame.
    """
    for widget in memory_display_frame.winfo_children():
        widget.destroy()
    memory_contents = "\n".join([f"{i:02}: {uvsim.mem.read(i):+05d}" for i in range(100)])
    memory_label = tk.Label(memory_display_frame, text=memory_contents, justify=tk.LEFT, font=("Courier", 10))
    memory_label.pack()
    current_instruction_label.config(text=f"[ {uvsim.cpu.current:04d} ]")

def start_simulation():
    """
    Function to start the simulation by running the UVSim.
    """
    uvsim.cpu.run(uvsim.mem, uvsim.io_device)
    update_main_control_frame()

def execute_step():
    """
    Function to execute a single step of the simulation.
    """
    uvsim.cpu.step(uvsim.mem, uvsim.io_device)
    update_main_control_frame()

# Initialize the UVSim instance
uvsim = UVSim()

root = tk.Tk()
root.title("UVSim - BasicML Simulator")

# Title Screen Frame
title_frame = tk.Frame(root)
title_frame.pack()

title_label = tk.Label(title_frame, text="Welcome to UVSim", font=("Helvetica", 24))
title_label.pack(pady=20)

start_button = tk.Button(title_frame, text="START", command=start_program)
start_button.pack(side=tk.LEFT, padx=20, pady=20)

help_button = tk.Button(title_frame, text="HELP", command=show_help)
help_button.pack(side=tk.RIGHT, padx=20, pady=20)

# File Selection Screen Frame
file_selection_frame = tk.Frame(root)

file_selection_label = tk.Label(file_selection_frame, text="Select a Test File", font=("Helvetica", 24))
file_selection_label.pack(pady=20)

file_entry = tk.Entry(file_selection_frame)
file_entry.pack(pady=10)

browse_button = tk.Button(file_selection_frame, text="Browse Files", command=browse_files)
browse_button.pack(pady=10)

load_file_button = tk.Button(file_selection_frame, text="LOAD FILE", command=load_file)
load_file_button.pack(pady=10)

# Main Control Screen Frame
main_control_frame = tk.Frame(root)

program_control_panel = tk.Frame(main_control_frame)
program_control_panel.pack(side=tk.LEFT, padx=10)

start_simulation_button = tk.Button(program_control_panel, text="Start Simulation", command=start_simulation)
start_simulation_button.pack(pady=5)

step_execution_button = tk.Button(program_control_panel, text="Step Execution", command=execute_step)
step_execution_button.pack(pady=5)

halt_button = tk.Button(program_control_panel, text="Halt", command=lambda: print("Halt"))
halt_button.pack(pady=5)

help_button_main = tk.Button(program_control_panel, text="Help", command=show_help)
help_button_main.pack(pady=5)

select_test_file_button = tk.Button(program_control_panel, text="Select Test File", command=start_program)
select_test_file_button.pack(pady=5)

memory_display_frame = tk.Frame(main_control_frame)
memory_display_frame.pack(side=tk.LEFT, padx=10)

current_instruction_frame = tk.Frame(main_control_frame)
current_instruction_frame.pack(pady=5)

current_instruction_label = tk.Label(current_instruction_frame, text="[ +0000 ]", font=("Courier", 14))
current_instruction_label.pack()

output_panel = tk.Frame(main_control_frame)
output_panel.pack(pady=5)

output_label = tk.Label(output_panel, text="N/A", font=("Courier", 12))
output_label.pack()

user_input_panel = tk.Frame(main_control_frame)
user_input_panel.pack(pady=5)

user_input_label = tk.Label(user_input_panel, text="Input: ", font=("Courier", 12))
user_input_label.pack(side=tk.LEFT)

user_input_entry = tk.Entry(user_input_panel)
user_input_entry.pack(side=tk.LEFT)

root.mainloop()
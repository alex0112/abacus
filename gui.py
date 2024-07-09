#!/usr/bin/env python

import tkinter as tk
from tkinter import filedialog
from uvsim import UVSim


class Window:
    # Initialize the UVSim instance
    def __init__(self, root):
        self.root = root
        self.input_var = tk.StringVar()
        self.root.title("UVSim - BasicML Simulator")

        self.title_screen_frame()
        self.select_screen_frame()

        self.uvsim = UVSim(reader=self.tk_reader, writer=self.tk_writer, out_line=self.tk_out_line)

        self.main_screen_frame()

    # Show Help Frame
    def show_help(self):
        """
        Function to display a help window with instructions for using the UVSim.
        """
        help_window = tk.Toplevel(self.root)
        help_window.title("Help and Instructions")
        help_label = tk.Label(help_window, text="Instructions\n\n1. Select a test file to load the program.\n"
                                                "2. Use the Start button to begin simulation.\n"
                                                "3. Use Step button to execute instructions one at a time.\n"
                                                "4. Use the Halt button to stop the simulation.\n"
                                                "5. Refer to the opcode definitions for specific actions (e.g., READ, WRITE, LOAD, etc.).")
        help_label.pack(pady=20, padx=20)
        close_button = tk.Button(help_window, text="CLOSE", command=help_window.destroy)
        close_button.pack(pady=10)

    def start_program(self):
        """
        Function to transition from the title screen to the file selection screen.
        """
        self.title_frame.pack_forget()
        self.file_selection_frame.pack()

    def browse_files(self):
        """
        Function to open a file dialog for selecting a test file.
        """
        file_path = filedialog.askopenfilename(initialdir="./bml_examples", title="Select a File",
                                            filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def load_file(self):
        """
        Function to load the selected file into the UVSim and transition to the main control screen.
        """
        file_path = self.file_entry.get()
        if file_path:
            print(f"Attempting to load file: {file_path}")
            self.uvsim.load(file_path)
            print(f"File loaded successfully: {file_path}")
            self.file_selection_frame.pack_forget()
            self.main_control_frame.pack()
            self.update_main_control_frame()

    def update_main_control_frame(self):
        """
        Function to update the memory display and current instruction display in the main control frame.
        """
        for widget in self.memory_display_frame.winfo_children():
            widget.destroy()

        memory_contents = self.uvsim.cpu.preview_state(self.uvsim.mem)
        #memory_contents = self.uvsim.io_device.last_err
        memory_label = tk.Label(self.memory_display_frame, text=memory_contents, justify=tk.LEFT, font=("Courier", 10))
        memory_label.pack()
        self.current_instruction_label.config(text=f"[ {self.uvsim.cpu.current:04d} ]")

    def start_simulation(self):
        """
        Function to start the simulation by running the UVSim.
        """
        self.uvsim.cpu.run(self.uvsim.mem, self.uvsim.io_device)
        self.update_main_control_frame()

        # self.simulation_running = True
        # self.run_simulation_step()
        
    def run_simulation_step(self):
        if self.simulation_running and not self.uvsim.cpu.waiting_for_input:
            self.execute_step()

            if not self.uvsim.cpu.waiting_for_input:
                self.run_simulation_step

    def execute_step(self):
        """
        Function to execute a single step of the simulation.
        """
        self.uvsim.cpu.step(self.uvsim.mem, self.uvsim.io_device)
        self.update_main_control_frame()

    def tk_reader(self):
        self.input_var.set("")
        self.user_input_entry.focus() 
        self.root.wait_variable(self.input_var)
        return self.input_var.get()

    def submit_input(self):
        # if self.uvsim.cpu.waiting_for_input:
            user_input = self.user_input_entry.get()
            self.user_input_entry.delete(0, tk.END)
            self.input_var.set(user_input)
            # self.uvsim.cpu.waiting_for_input = False
            # self.simulation_running = True
            # self.run_simulation_step()

    def tk_writer(self, text):
        self.output_label.config(text=text)

    def tk_out_line(self, text):
        self.current_instruction_label.config(text=text)


        # Title Screen Frame
    def title_screen_frame(self):
        self.title_frame = tk.Frame(self.root)
        self.title_frame.pack()

        title_label = tk.Label(self.title_frame, text="Welcome to UVSim", font=("Helvetica", 24))
        title_label.pack(pady=20)

        start_button = tk.Button(self.title_frame, text="START", command=self.start_program)
        start_button.pack(side=tk.LEFT, padx=20, pady=20)

        help_button = tk.Button(self.title_frame, text="HELP", command=self.show_help)
        help_button.pack(side=tk.RIGHT, padx=20, pady=20)

        # File Selection Screen Frame
    def select_screen_frame(self):
        self.file_selection_frame = tk.Frame(self.root)

        file_selection_label = tk.Label(self.file_selection_frame, text="Select a Test File", font=("Helvetica", 24))
        file_selection_label.pack(pady=20)

        self.file_entry = tk.Entry(self.file_selection_frame)
        self.file_entry.pack(pady=10)

        browse_button = tk.Button(self.file_selection_frame, text="Browse Files", command=self.browse_files)
        browse_button.pack(pady=10)

        load_file_button = tk.Button(self.file_selection_frame, text="LOAD FILE", command=self.load_file)
        load_file_button.pack(pady=10)

        # Main Control Screen Frame
    def main_screen_frame(self):
        self.main_control_frame = tk.Frame(self.root)

        program_control_panel = tk.Frame(self.main_control_frame)
        program_control_panel.pack(side=tk.LEFT, padx=10)

        start_simulation_button = tk.Button(program_control_panel, text="Start Simulation", command=self.start_simulation)
        start_simulation_button.pack(pady=5)

        step_execution_button = tk.Button(program_control_panel, text="Step Execution", command=self.execute_step)
        step_execution_button.pack(pady=5)

        halt_button = tk.Button(program_control_panel, text="Halt", command=lambda: print("Halt"))
        halt_button.pack(pady=5)

        help_button_main = tk.Button(program_control_panel, text="Help", command=self.show_help)
        help_button_main.pack(pady=5)

        select_test_file_button = tk.Button(program_control_panel, text="Select Test File", command=self.start_program)
        select_test_file_button.pack(pady=5)

        self.memory_display_frame = tk.Frame(self.main_control_frame)
        self.memory_display_frame.pack(side=tk.LEFT, padx=10)

        current_instruction_frame = tk.Frame(self.main_control_frame)
        current_instruction_frame.pack(pady=5)

        self.current_instruction_label = tk.Label(current_instruction_frame, text="[ +0000 ]", font=("Courier", 14))
        self.current_instruction_label.pack()

        output_panel = tk.Frame(self.main_control_frame)
        output_panel.pack(pady=5)

        self.output_label = tk.Label(output_panel, text="N/A", font=("Courier", 12))
        self.output_label.pack()

        user_input_panel = tk.Frame(self.main_control_frame)
        user_input_panel.pack(pady=5)

        user_input_label = tk.Label(user_input_panel, text="Input: ", font=("Courier", 12))
        user_input_label.pack(side=tk.LEFT)

        self.user_input_entry = tk.Entry(user_input_panel)
        self.user_input_entry.pack(side=tk.LEFT)
        self.user_input_entry.bind("<Return>", self.submit_input)

        input_button = tk.Button(user_input_panel, text="Input", command=self.submit_input)
        input_button.pack(pady=5)


root = tk.Tk()
window = Window(root)
root.mainloop()

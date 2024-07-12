import json
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from uvsim import UVSim

class Window:
    def __init__(self, root):
        self.root = root
        self.input_var = tk.StringVar()
        self.root.title("UVSim - BasicML Simulator")

        self.default_primary_color = "#275D38"
        self.default_off_color = "#FFFFFF"

        self.load_config()
        
        self.title_screen_frame()
        self.select_screen_frame()
        self.main_screen_frame()

        self.uvsim = UVSim(reader=self.tk_reader, writer=self.tk_writer, out_line=self.tk_out_line)

    def load_config(self):
        try:
            with open("config.json", "r") as config_file:
                config = json.load(config_file)
                self.primary_color = config.get("primary_color", self.default_primary_color)
                self.off_color = config.get("off_color", self.default_off_color)
        except FileNotFoundError:
            self.primary_color = self.default_primary_color
            self.off_color = self.default_off_color
        
        self.update_colors()

    def save_config(self):
        config = {
            "primary_color": self.primary_color,
            "off_color": self.off_color
        }
        with open("config.json", "w") as config_file:
            json.dump(config, config_file)
    
    def update_colors(self):
        self.root.configure(bg=self.primary_color)
    
    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Help and Instructions")
        help_window.configure(bg=self.primary_color)
        help_label = tk.Label(help_window, text="Instructions\n\n1. Select a test file to load the program.\n"
                                                "2. Use the Start button to begin simulation.\n"
                                                "3. Use Step button to execute instructions one at a time.\n"
                                                "4. Use the Halt button to stop the simulation.\n"
                                                "5. Refer to the opcode definitions for specific actions (e.g., READ, WRITE, LOAD, etc.).",
                              bg=self.primary_color, fg=self.off_color)
        help_label.pack(pady=20, padx=20)
        close_button = tk.Button(help_window, text="CLOSE", command=help_window.destroy,
                                 bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                 highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        close_button.pack(pady=10)

    def show_color_selection(self):
        color_selection_window = tk.Toplevel(self.root)
        color_selection_window.title("Color Selection")
        color_selection_window.configure(bg=self.primary_color)

        header_label = tk.Label(color_selection_window, text="Color Selection", font=("Helvetica", 24),
                                bg=self.primary_color, fg=self.off_color)
        header_label.pack(pady=20)

        explanation_label = tk.Label(color_selection_window, text="Select new colors for the simulator interface or reset to default.",
                                     bg=self.primary_color, fg=self.off_color)
        explanation_label.pack(pady=10)

        change_color_button = tk.Button(color_selection_window, text="Change Colors", command=self.change_colors,
                                        bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                        highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        change_color_button.pack(pady=10)

        reset_color_button = tk.Button(color_selection_window, text="Reset Colors", command=self.reset_colors,
                                       bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                       highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        reset_color_button.pack(pady=10)

        close_button = tk.Button(color_selection_window, text="CLOSE", command=color_selection_window.destroy,
                                 bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                 highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        close_button.pack(pady=10)

    def start_program(self):
        self.title_frame.pack_forget()
        self.file_selection_frame.pack(padx=20, pady=20)
        self.root.update_idletasks()  # Force the window to update its size

    def browse_files(self):
        file_path = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                               filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def load_file(self):
        file_path = self.file_entry.get()
        if file_path:
            self.uvsim.load(file_path)
            self.file_selection_frame.pack_forget()
            self.main_control_frame.pack(padx=20, pady=20)
            self.update_main_control_frame()
            self.root.update_idletasks()  # Force the window to update its size

    def update_main_control_frame(self):
        for widget in self.memory_display_frame.winfo_children():
            widget.destroy()

        memory_contents = self.uvsim.cpu.preview_state(self.uvsim.mem)
        memory_label = tk.Label(self.memory_display_frame, text=memory_contents, justify=tk.LEFT, font=("Courier", 10),
                                bg=self.primary_color, fg=self.off_color)
        memory_label.pack(padx=10, pady=(10, 0))

        self.current_instruction_label.config(text=f"[ {self.uvsim.cpu.current:04d} ]")

    def start_simulation(self):
        self.uvsim.cpu.run(self.uvsim.mem, self.uvsim.io_device)
        self.update_main_control_frame()

    def halt_simulation(self):
        self.uvsim.cpu.halted = True
        self.update_main_control_frame()
        messagebox.showinfo("Simulation Halted", "The simulation has been halted.")

    def execute_step(self):
        self.uvsim.cpu.step(self.uvsim.mem, self.uvsim.io_device)
        self.update_main_control_frame()

    def tk_reader(self):
        self.input_var.set("")
        self.user_input_entry.focus()
        self.root.wait_variable(self.input_var)
        return self.input_var.get()

    def submit_input(self):
        user_input = self.user_input_entry.get()
        self.user_input_entry.delete(0, tk.END)
        self.input_var.set(user_input)

    def tk_writer(self, text):
        self.output_label.config(text=text)

    def tk_out_line(self, text):
        self.current_instruction_label.config(text=text)

    def title_screen_frame(self):
        self.title_frame = tk.Frame(self.root, bg=self.primary_color)
        self.title_frame.pack()

        title_label = tk.Label(self.title_frame, text="Welcome to UVSim", font=("Helvetica", 24),
                               bg=self.primary_color, fg=self.off_color)
        title_label.pack(pady=20)

        buttons_frame = tk.Frame(self.title_frame, bg=self.primary_color)
        buttons_frame.pack()

        start_button = tk.Button(buttons_frame, text="START", command=self.start_program,
                                 bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                 highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        start_button.pack(side=tk.LEFT, padx=20, pady=20)

        help_button = tk.Button(buttons_frame, text="HELP", command=self.show_help,
                                bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        help_button.pack(side=tk.RIGHT, padx=20, pady=20)

        color_selection_button = tk.Button(self.title_frame, text="Color Selection", command=self.show_color_selection,
                                           bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                           highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        color_selection_button.pack(pady=20)

    def select_screen_frame(self):
        self.file_selection_frame = tk.Frame(self.root, bg=self.primary_color)

        file_selection_label = tk.Label(self.file_selection_frame, text="Select a Test File", font=("Helvetica", 24),
                                        bg=self.primary_color, fg=self.off_color)
        file_selection_label.pack(pady=20)

        self.file_entry = tk.Entry(self.file_selection_frame)
        self.file_entry.pack(pady=10)

        browse_button = tk.Button(self.file_selection_frame, text="Browse Files", command=self.browse_files,
                                  bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                  highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        browse_button.pack(pady=10)

        load_file_button = tk.Button(self.file_selection_frame, text="LOAD FILE", command=self.load_file,
                                     bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                     highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        load_file_button.pack(pady=10)

    def main_screen_frame(self):
        self.main_control_frame = tk.Frame(self.root, bg=self.primary_color)

        # Add the header here
        title_label = tk.Label(self.main_control_frame, text="UVSim - Control Panel", font=("Helvetica", 24),
                               bg=self.primary_color, fg=self.off_color)
        title_label.pack(pady=10)

        top_frame = tk.Frame(self.main_control_frame, bg=self.primary_color)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        bottom_frame = tk.Frame(self.main_control_frame, bg=self.primary_color)
        bottom_frame.pack(side=tk.TOP, fill=tk.X)

        # Top row of panels
        program_control_panel = tk.LabelFrame(top_frame, text="Program Control Panel", bg=self.primary_color, fg=self.off_color, font=("Helvetica", 12), padx=10, labelanchor='n')
        program_control_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        start_simulation_button = tk.Button(program_control_panel, text="Start Simulation", command=self.start_simulation,
                                            bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                            highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        start_simulation_button.pack(pady=5)

        step_execution_button = tk.Button(program_control_panel, text="Step Execution", command=self.execute_step,
                                          bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                          highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        step_execution_button.pack(pady=5)

        halt_button = tk.Button(program_control_panel, text="Halt", command=self.halt_simulation,
                                bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        halt_button.pack(pady=5)

        help_button_main = tk.Button(program_control_panel, text="Help", command=self.show_help,
                                     bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                     highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        help_button_main.pack(pady=5)

        select_test_file_button = tk.Button(program_control_panel, text="Select Test File", command=self.start_program,
                                            bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                            highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        select_test_file_button.pack(pady=5)

        self.memory_display_frame = tk.LabelFrame(top_frame, text="Memory Display", bg=self.primary_color, fg=self.off_color, font=("Helvetica", 12), labelanchor='n')
        self.memory_display_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        control_panel = tk.LabelFrame(top_frame, text="Control Panel", bg=self.primary_color, fg=self.off_color, font=("Helvetica", 12), labelanchor='n')
        control_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        self.current_instruction_label = tk.Label(control_panel, text="[ +0000 ]", font=("Courier", 14),
                                                  bg=self.primary_color, fg=self.off_color)
        self.current_instruction_label.pack(padx=10, pady=(10, 0))

        # Bottom row of panels
        current_instruction_panel = tk.LabelFrame(bottom_frame, text="Current Instruction", bg=self.primary_color, fg=self.off_color, font=("Helvetica", 12), labelanchor='n')
        current_instruction_panel.pack(fill=tk.BOTH, padx=10, pady=10)

        self.current_instruction_display = tk.Label(current_instruction_panel, text="[ 0000 ]", font=("Courier", 12),
                                                    bg=self.primary_color, fg=self.off_color)
        self.current_instruction_display.pack(padx=10, pady=(10, 0))

        output_panel = tk.LabelFrame(bottom_frame, text="Output Panel", bg=self.primary_color, fg=self.off_color, font=("Helvetica", 12), labelanchor='n')
        output_panel.pack(fill=tk.BOTH, padx=10, pady=10)

        self.output_label = tk.Label(output_panel, text="N/A", font=("Courier", 12),
                                     bg=self.primary_color, fg=self.off_color)
        self.output_label.pack(padx=10, pady=(10, 0))

        user_input_panel = tk.LabelFrame(bottom_frame, text="User Input Panel", bg=self.primary_color, fg=self.off_color, font=("Helvetica", 12), labelanchor='n')
        user_input_panel.pack(fill=tk.BOTH, padx=10, pady=10)

        user_input_label = tk.Label(user_input_panel, text="Input: ", font=("Courier", 12),
                                    bg=self.primary_color, fg=self.off_color)
        user_input_label.pack(side=tk.LEFT, padx=10, pady=(10, 0))

        self.user_input_entry = tk.Entry(user_input_panel)
        self.user_input_entry.pack(side=tk.LEFT, padx=10, pady=(10, 0))
        self.user_input_entry.bind("<Return>", self.submit_input)

        input_button = tk.Button(user_input_panel, text="Input", command=self.submit_input,
                                 bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                 highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        input_button.pack(padx=10, pady=(10, 0))

    def change_colors(self):
        primary_color = colorchooser.askcolor(title="Choose Primary Color")[1]
        off_color = colorchooser.askcolor(title="Choose Off Color")[1]

        if primary_color and off_color:
            self.primary_color = primary_color
            self.off_color = off_color
            self.save_config()
            self.update_colors()
            self.root.destroy()
            self.__init__(tk.Tk())

    def reset_colors(self):
        self.primary_color = self.default_primary_color
        self.off_color = self.default_off_color
        self.save_config()
        self.update_colors()
        self.root.destroy()
        self.__init__(tk.Tk())

root = tk.Tk()
window = Window(root)
root.mainloop()
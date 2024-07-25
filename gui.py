import json
import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, ttk
from uvsim import UVSim, Opcode

class Window:
    def __init__(self, root):
        self.simulation_running = False
        self.uvsim_instances = {}
        self.root = root
        self.input_var = tk.StringVar()
        self.root.title("UVSim - BasicML Simulator")
        self.output_log = []

        self.default_primary_color = "#275D38"
        self.default_off_color = "#FFFFFF"
        self.style = ttk.Style()
    
        self.style.configure('Custom.TFrame',
                    background=self.default_primary_color,
                    foreground=self.default_off_color,
                    padding=[10, 5])
        
        self.load_config()

        self.tab_control = ttk.Notebook(root)

        self.tab_setup()
        self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        if self.simulation_running:
            # Revert to the previous tab
            self.tab_control.select(self.current_tab)
            messagebox.showwarning("Simulation Running", "You cannot switch tabs while simulation is running.")
        else:
            self.current_tab = self.tab_control.select()
            self.uvsim = self.uvsim_instances[self.tab_control.index("current")]

    
    def tab_setup(self):
        if not self.simulation_running:
            tab_index = len(self.uvsim_instances)
            new_uvsim = UVSim(reader=self.tk_reader, writer=self.tk_writer, out_line=self.tk_out_line)
            self.uvsim_instances[tab_index] = new_uvsim

            newTab = ttk.Frame(self.tab_control)
            newTab.configure(style='Custom.TFrame')

            self.tab_control.add(newTab, text='New Tab')
            self.tab_control.pack(expand=1, fill="both")
            
            self.title_screen_frame(newTab)
            self.main_screen_frame(newTab)

            self.tab_control.select(newTab)
            self.current_tab = self.tab_control.select()
        else:
            messagebox.showwarning("Simulation Running", "You cannot create tabs while simulation is running.")
    
    def close_tab(self):
        if not self.simulation_running:
            current_tab_index = self.tab_control.index("current")
            
            if len(self.uvsim_instances) <= 1:
                self.root.quit()
                return

            if current_tab_index == 0:
                self.tab_control.select(1)
            else:
                self.tab_control.select(0)
            
            self.uvsim_instances.pop(current_tab_index)

            self.tab_control.forget(current_tab_index)

            updated_uvsim_instances = {}
            for new_index, old_index in enumerate(sorted(self.uvsim_instances.keys())):
                updated_uvsim_instances[new_index] = self.uvsim_instances[old_index]

            self.uvsim_instances = updated_uvsim_instances

            self.current_tab = self.tab_control.select()
        else:
            messagebox.showwarning("Simulation Running", "You cannot create tabs while simulation is running.")


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
    
        self.style.configure('Custom.TFrame',
                    background=self.primary_color,)
    
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
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").pack_forget()
        self.tab_control.nametowidget(self.current_tab).nametowidget("title_frame").pack()
        self.root.update_idletasks()  # Force the window to update its size

    def browse_files(self):
        file_path = filedialog.askopenfilename(initialdir="./bml_examples", title="Select a File",
                                               filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        self.tab_control.nametowidget(self.current_tab).nametowidget("title_frame").nametowidget("file_entry").delete(0, tk.END)
        self.tab_control.nametowidget(self.current_tab).nametowidget("title_frame").nametowidget("file_entry").insert(0, file_path)

    def load_file(self):
        file_path = self.tab_control.nametowidget(self.current_tab).nametowidget("title_frame").nametowidget("file_entry").get()
        if file_path:
            self.uvsim.load(file_path)

            self.tab_control.nametowidget(self.current_tab).nametowidget("title_frame").pack_forget()
            self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").pack(padx=20, pady=20)
            self.tab_control.tab(self.tab_control.index(self.tab_control.select()), text=file_path.split('/')[-1])
            for widget in self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").nametowidget("memory_inner_frame").winfo_children():
                widget.destroy()
            self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").create_window((0, 0), window=self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").nametowidget("memory_inner_frame"))
            self.update_main_control_frame()
            self.root.update_idletasks()  # Force the window to update its size
            self.uvsim.cpu.current = 0
            self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("bottom_frame").nametowidget("current_instruction_panel").nametowidget("current_instruction_display").config(text=f"[ {str(self.uvsim.cpu.current)} ]")
    
    def store_file(self):
        '''Store the contents of memory to a file using the file dialog.'''
        file_path = filedialog.asksaveasfilename(initialdir="./bml_examples", title="Save File",
                                                    filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        self.uvsim.store(file_path)


    def submit_memory_edit(self):
        '''Submit the memory edit to the memory.'''
        opcode_list = []
        text_content = self.tab_control.nametowidget(self.current_tab).edit_field.get("1.0", tk.END).strip().split("\n")
        try:
            for line in text_content:
                line = Opcode(line)
                opcode_list.append(line)
            if len(opcode_list) - 1 not in self.uvsim.mem.ADDRESSABLE_SPACE:
                raise ValueError("Too many opcodes")
            for address in range(len(opcode_list)):
                self.uvsim.mem.write(address, opcode_list[address])
            print("memory updated succesfully")
            self.update_main_control_frame()
            self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("program_control_panel").nametowidget("advanced_editor_button").config(text="Advanced Edit", command=self.edit_memory)
        except ValueError as e:
            print(f"text passed invalid: {e}")
            messagebox.showerror("Error", f"The submited code is invalid.\n{e}")


    def edit_memory(self):
        '''Open the advanced editor for memory editing.'''
        content = self.uvsim.cpu.gui_preview_state(self.uvsim.mem)
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("program_control_panel").nametowidget("advanced_editor_button").config(text="Submit Changes", command=self.submit_memory_edit)
        for widget in self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").nametowidget("memory_inner_frame").winfo_children():
            widget.destroy()
            
        self.tab_control.nametowidget(self.current_tab).edit_field = tk.Text(self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").nametowidget("memory_inner_frame"), font=("Courier", 10), bg=self.primary_color, fg=self.off_color, width=6, height=16)
        self.tab_control.nametowidget(self.current_tab).edit_field.grid(row=0, column=0, padx=10, pady=4, sticky="nsew")
        
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").nametowidget("memory_inner_frame").grid_columnconfigure(0, weight=1)
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").nametowidget("memory_inner_frame").grid_rowconfigure(0, weight=1)
        
        text_to_show = ""
        for thing in content:
            text_to_show += f"{thing[1]}\n"
        self.tab_control.nametowidget(self.current_tab).edit_field.insert(tk.END, text_to_show)
        
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").nametowidget("memory_inner_frame").update_idletasks()
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").config(scrollregion=self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").bbox("all"))


    def modify_memory(self, slot, entry):
            '''Modify the memory slot with the given entry.'''
            try:
                entry = int(entry)
                self.uvsim.mem.write(slot[0], entry)
                self.update_main_control_frame()
                print("Memory updated.")
            except ValueError as e:
                messagebox.showerror("Error", f"Please enter a valid integer value.\n{e}")
                self.update_main_control_frame()

    def on_click_opcode(self, slot, label):
        label.forget()
        entry = tk.Entry(self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("memory_display_frame").nametowidget("memory_canvas").nametowidget("memory_inner_frame"), font=("Courier", 10), width=5, bg=self.primary_color, fg=self.off_color)
        entry.insert(0, slot[1])
        entry.bind("<Return>", lambda event: self.modify_memory(slot, entry.get()))
        entry.grid(row=slot[0], column=1, padx=10, pady=5)

    def update_main_control_frame(self):

        
        # for child in self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("bottom_frame").winfo_children():
        #     print(child.winfo_name())

        main_control_frame = self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame")
        top_frame = main_control_frame.nametowidget("top_frame")
        memory_canvas = top_frame.nametowidget("memory_display_frame").nametowidget("memory_canvas")
        memory_inner_frame = memory_canvas.nametowidget("memory_inner_frame")
        current_instruction_display = main_control_frame.nametowidget("bottom_frame").nametowidget("current_instruction_panel").nametowidget("current_instruction_display")

        if not self.uvsim.cpu.halted:
            for widget in memory_inner_frame.winfo_children():
                widget.destroy()
            current_instruction_display.config(text=f"[ {str(self.uvsim.cpu.current)} ]")
            contents = self.uvsim.cpu.gui_preview_state(self.uvsim.mem)
            memory_canvas.create_window((0, 0), window=memory_inner_frame, anchor="nw")
            for slot in contents:
                memory_address_label = tk.Label(memory_inner_frame, text=slot[0], font=("Courier", 10),
                                         bg=self.primary_color, fg=self.off_color)
                memory_address_label.grid(row=slot[0], column=0, padx=10, pady=5)
                if self.uvsim.cpu.current == slot[0]:
                    memory_address_label.config(bg=self.off_color, fg=self.primary_color)
                    memory_canvas.yview_moveto(slot[0] / len(contents))  # Focus on the current address label
                memory_value_label = tk.Label(memory_inner_frame, text=slot[1], font=("Courier", 10), cursor="xterm",
                                       bg=self.primary_color, fg=self.off_color)
                memory_value_label.grid(row=slot[0], column=1, padx=10, pady=5)
                memory_value_label.bind("<Button-1>", lambda event, slot=slot, label=memory_value_label: self.on_click(slot, label))
                memory_value_friendly_label = tk.Label(memory_inner_frame, text=slot[2], font=("Courier", 10),
                                               bg=self.primary_color, fg=self.off_color)
                memory_value_friendly_label.grid(row=slot[0], column=2, padx=10, pady=5)
     
                memory_inner_frame.update_idletasks()
                memory_canvas.config(scrollregion=memory_canvas.bbox("all"))

    def start_simulation(self):
        if not hasattr(self.tab_control.nametowidget(self.current_tab), 'edit_field'):
            self.edit_memory()  # Ensure edit_field is created
        self.submit_memory_edit()
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("program_control_panel").nametowidget("advanced_editor_button").config(state="disabled")
        self.simulation_running = True
        self.run_simulation_step()

    def run_simulation_step(self):
        if self.simulation_running and not self.uvsim.cpu.waiting_for_input:
            self.execute_step()
            self.root.after(200, self.run_simulation_step)

    def halt_simulation(self):
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("program_control_panel").nametowidget("advanced_editor_button").config(state="normal")
        self.simulation_running = False
        self.uvsim.cpu.halted = True
        self.uvsim.cpu.current = 0
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("bottom_frame").nametowidget("current_instruction_panel").nametowidget("current_instruction_display").config(text=f"[ {str(self.uvsim.cpu.current)} ]")
        messagebox.showinfo("Simulation Halted", "The simulation has been halted.")


    def execute_step(self):
        self.update_main_control_frame() #this is causing the program to refresh memory every step which makes it take longer to load
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("program_control_panel").nametowidget("advanced_editor_button").config(state="disabled")
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("bottom_frame").nametowidget("current_instruction_panel").nametowidget("current_instruction_display").config(text=f"[ {str(self.uvsim.cpu.current)} ]")
        self.uvsim.cpu.step(self.uvsim.mem, self.uvsim.io_device)
        if self.uvsim.cpu.halted:
            self.simulation_running = False
        

    def tk_reader(self):
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("prompt_label").pack(side=tk.BOTTOM, padx=10, pady=(10, 0))
        self.input_var.set("")
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("bottom_frame").nametowidget("user_input_label").nametowidget("user_input").focus()
        self.root.wait_variable(self.input_var)
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("prompt_label").pack_forget()
        return self.input_var.get()

    def submit_input(self, event=None):
        user_input = self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("bottom_frame").nametowidget("user_input_label").nametowidget("user_input").get()
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("bottom_frame").nametowidget("user_input_label").nametowidget("user_input").delete(0, tk.END)
        self.input_var.set(user_input)

    def tk_writer(self, text):
        self.output_log.append(str(text))  # Append the new output to the log
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("bottom_frame").nametowidget("output_panel").nametowidget("output_label").config(text="\n".join(self.output_log)) # Update the output display with the entire log


    def tk_out_line(self, text):
        self.output_log.append(str(text)) # Append the new output to the log
        self.tab_control.nametowidget(self.current_tab).nametowidget("main_control_frame").nametowidget("top_frame").nametowidget("control_panel").nametowidget("current_instruction_label").config(text="\n".join(self.output_log))  # Update the output display with the entire log

    def title_screen_frame(self, tab, event=None):
        title_frame = tk.Frame(tab, bg=self.primary_color, name="title_frame")
        title_frame.pack()

        title_label = tk.Label(title_frame, text="Welcome to UVSim", font=("Helvetica", 24),
                               bg=self.primary_color, fg=self.off_color)
        title_label.pack(pady=20)

        file_entry = tk.Entry(title_frame, name="file_entry")
        file_entry.pack(pady=10)

        browse_button = tk.Button(title_frame, text="Browse Files", command=self.browse_files,
                                  bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                  highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        browse_button.pack(pady=10)

        load_file_button = tk.Button(title_frame, text="LOAD FILE", command=self.load_file,
                                     bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                     highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        load_file_button.pack(pady=10)

        buttons_frame = tk.Frame(title_frame, bg=self.primary_color)
        buttons_frame.pack()

        help_button = tk.Button(buttons_frame, text="HELP", command=self.show_help,
                                bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        help_button.pack(side=tk.LEFT, padx=10, pady=20)

        close_button = tk.Button(buttons_frame, text="Close Tab", command=self.close_tab,
                                bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        close_button.pack(side=tk.LEFT, padx=10, pady=20)

        color_selection_button = tk.Button(buttons_frame, text="Color Selection", command=self.show_color_selection,
                                           bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                           highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        color_selection_button.pack(side=tk.RIGHT, padx=10, pady=20)

    def main_screen_frame(self, tab):
        main_control_frame = tk.Frame(tab, bg=self.primary_color, name="main_control_frame")

        # Add the header here
        title_label = tk.Label(main_control_frame, text="UVSim - Control Panel", font=("Helvetica", 24),
                               bg=self.primary_color, fg=self.off_color)
        title_label.pack(pady=10)

        top_frame = tk.Frame(main_control_frame, bg=self.primary_color, name="top_frame")
        top_frame.pack(side=tk.TOP, fill=tk.X)

        bottom_frame = tk.Frame(main_control_frame, bg=self.primary_color, name="bottom_frame")
        bottom_frame.pack(side=tk.TOP, fill=tk.X)

        # Top row of panels
        program_control_panel = tk.LabelFrame(top_frame, text="Program Control Panel", bg=self.primary_color, fg=self.off_color, font=("Helvetica", 12), padx=10, labelanchor='n', name="program_control_panel")
        program_control_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        start_simulation_button = tk.Button(program_control_panel, text="Start Simulation", command=self.start_simulation,
                                            bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                            highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        start_simulation_button.pack(pady=5)

        step_execution_button = tk.Button(program_control_panel, text="Step Execution", command=self.execute_step,
                                          bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                          highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        step_execution_button.pack(pady=5)

        halt_button = tk.Button(program_control_panel, text="Pause", command=self.halt_simulation,
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

        save_test_file_button = tk.Button(program_control_panel, text="Save Test File", command=self.store_file,
                                            bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                            highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        save_test_file_button.pack(pady=5)

        advanced_editor_button = tk.Button(program_control_panel, text="Advanced Edit", command=self.edit_memory,
                                            bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                            highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat", name="advanced_editor_button")
        advanced_editor_button.pack(pady=5)

        new_file_button = tk.Button(program_control_panel, text="New File Tab", command=self.tab_setup,
                                            bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                            highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        new_file_button.pack(pady=5)

        memory_display_frame = tk.LabelFrame(top_frame, text="Memory Display", bg=self.primary_color, fg=self.off_color, font=("Helvetica", 12), labelanchor='n', name="memory_display_frame")
        memory_display_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        memory_canvas = tk.Canvas(memory_display_frame, bg=self.primary_color, highlightthickness=0, width=240, name="memory_canvas")
        memory_canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        memory_scrollbar = tk.Scrollbar(memory_display_frame, orient="vertical", command=memory_canvas.yview)
        memory_scrollbar.pack(side=tk.RIGHT, fill='y')
        
        memory_canvas.configure(yscrollcommand=memory_scrollbar.set)
        memory_canvas.bind('<Configure>', lambda e: memory_canvas.configure(scrollregion=memory_canvas.bbox("all")))

        memory_inner_frame = tk.Frame(memory_canvas, bg=self.primary_color, name="memory_inner_frame")
        memory_canvas.create_window((0, 0), window=memory_inner_frame)

        control_panel = tk.LabelFrame(top_frame, text="Control Panel", bg=self.primary_color, fg=self.off_color, font=("Helvetica", 12), labelanchor='n', name="control_panel")
        control_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        current_instruction_label = tk.Label(control_panel, text="[ +0000 ]", font=("Courier", 14),
                                                  bg=self.primary_color, fg=self.off_color, name="current_instruction_label")
        current_instruction_label.pack(padx=10, pady=(10, 0))

        # Bottom row of panels
        current_instruction_panel = tk.LabelFrame(bottom_frame, text="Current Instruction", bg=self.primary_color, fg=self.off_color, 
                                                  font=("Helvetica", 12), labelanchor='n', name="current_instruction_panel")
        current_instruction_panel.pack(fill=tk.BOTH, padx=10, pady=10)

        current_instruction_display = tk.Label(current_instruction_panel, text="[ 0000 ]", font=("Courier", 12),
                                                    bg=self.primary_color, fg=self.off_color, name="current_instruction_display")
        current_instruction_display.pack(padx=10, pady=(10, 0))

        output_panel = tk.LabelFrame(bottom_frame, text="Output Panel", bg=self.primary_color, fg=self.off_color, font=("Helvetica", 12), labelanchor='n', name="output_panel")
        output_panel.pack(fill=tk.BOTH, padx=10, pady=10)

        output_label = tk.Label(output_panel, text="N/A", font=("Courier", 12),
                                     bg=self.primary_color, fg=self.off_color, name="output_label")
        output_label.pack(padx=10, pady=(10, 0))

        user_input_panel = tk.LabelFrame(bottom_frame, text="User Input Panel", bg=self.primary_color, fg=self.off_color, 
                                         font=("Helvetica", 12), labelanchor='n', name="user_input_label")
        user_input_panel.pack(fill=tk.BOTH, padx=10, pady=10)

        user_input_label = tk.Label(user_input_panel, text="Input: ", font=("Courier", 12),
                                    bg=self.primary_color, fg=self.off_color)
        user_input_label.pack(side=tk.LEFT, padx=10, pady=(10, 0))

        user_input_entry = tk.Entry(user_input_panel, name="user_input")
        user_input_entry.pack(side=tk.LEFT, padx=10, pady=(10, 0))
        user_input_entry.bind("<Return>", self.submit_input)

        input_button = tk.Button(user_input_panel, text="Input", command=self.submit_input,
                                 bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                 highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat", name="input_button")
        input_button.pack(padx=10, pady=(10, 0))

        prompt_label = tk.Label(main_control_frame, text="Please input a four digit command or a four digit value.", font=("Courier", 12),
                                    bg=self.primary_color, fg=self.off_color, name="prompt_label")
        prompt_label.pack_forget()

         # Add Color Selection button at the bottom
        color_selection_button = tk.Button(main_control_frame, text="Color Selection", command=self.show_color_selection,
                                           bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                           highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        color_selection_button.pack(pady=20)

        close_button = tk.Button(main_control_frame, text="Close Tab", command=self.close_tab,
                                bg=self.off_color, fg=self.primary_color, highlightbackground=self.primary_color,
                                highlightcolor=self.primary_color, activebackground=self.primary_color, borderwidth=0, relief="flat")
        close_button.pack(pady=10)

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
# Proposed Architecture of UVSim machine

High level overview of the design of our machine.

### Project Organization:

Bird's eye view:
```
├── README.md ## The README
├── ARCH.md ## You're reading it
│
├── bml_examples ## Example programs for test cases
│ └── ...
├── test ## Unit Tests
│ └── ...
│
├── src
│ ├── cpu.py ## Abstraction representing the CPU and its single register, processes opcodes and modifies memory
│ ├── io_device.py ## Represents input and output to the console (separated for testing)
│ ├── memory.py ## The program memory, methods for addressing and checks against overflowing available memory
│ └── opcode.py ## Type that processes and reads an opcode like +1007 and ensures it's valid
│
├── basm.py ## Assembler that turns the human-friendly representation of BasicML into numbers
├── uvsim.py ## Integrates the memory, CPU, IO, etc., into one object
├── gui.py ## Graphical user interface for UVSim that allows users to load, execute, and debug BasicML programs interactively
└── main.py ## Bootstraps everything and gets it running
```


## File Descriptions

### `uvsim.py`

This module integrates the memory, CPU, and IO device into a single cohesive unit. It is responsible for loading programs into memory and processing them using the CPU.

### `src/cpu.py`

An abstraction of the processor, containing a function called `process()` which takes an `Opcode` and a `Memory` object as input, modifying the memory according to the instruction contained in the `Opcode`.

### `src/memory.py`

Provides utilities for:

- Writing data to specific locations in memory
- Creating new memory locations if they do not exist
- Warning the user if the machine runs out of memory (e.g., when reaching location `99`)

### `src/opcode.py`

Represents an opcode or piece of memory. Includes utility methods for getting the sign of the number it represents and handles exceptions for invalid opcodes.

### `basm.py`

An optional program that converts a human-friendly representation of BasicML into numeric machine code. This is useful for assembling and running BasicML programs on the UVSim.

### `main.py`

The entry point for the UVSim. This script initializes the system, loads programs, and executes them.

### `gui.py`

The graphical user interface for UVSim, implemented using Tkinter. The GUI allows users to interactively load, execute, and debug BasicML programs. Key features include:

- **Title Frame**: Welcome screen with options to start, get help, and customize colors.
- **File Selection Frame**: Interface for browsing and loading test files.
- **Main Control Frame**: Displays controls for simulation, memory display, and current instruction.
- **Help / Instructions Frame**: Provides instructions and guidance on using the program.
- **Color Customization Frame**: Allows users to customize interface colors and reset to defaults.

## Recent Updates

- **Tab Management**: Added support for managing multiple UVSim instances in separate tabs, each running independently.
- **Advanced Memory Editing**: Users can edit memory contents directly within the GUI.
- **Enhanced Program Control**: New buttons for saving test files, advanced memory editing, and creating new file tabs.
- **Color Customization**: Users can now choose primary and off colors for the interface, with options to reset to default colors.
- **Improved Error Handling**: Enhanced error messages and handling mechanisms across various components.

This architecture aims to provide a modular and scalable framework for simulating the BasicML virtual machine, with a focus on ease of use and extensibility.


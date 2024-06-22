### Project Organization:
```
├── README.md    ## The README
├── ARCH.md      ## You're reading it
│
├── bml_examples ## Example testing files 
│   └── ...
├── test         ## Unit Tests
│   ├── test_cpu.py     ## Verifies the CPU's operations and memory modifications.
│   ├── test_io.py      ## Tests console input and output operations.
│   ├── test_memory.py  ## Ensures accurate memory addressing and data handling.
│   ├── test_opcode.py  ## Validates opcode processing and execution.
├── src
│   ├── cpu.py       ## An abstraction representing the CPU and its single register, processes opcodes and modifies memory
│   ├── io_device.py ## Represents input and output to the console (wanted to separate this for testing)
│   ├── memory.py    ## The program memory, has methods for addressing and checks against overflowing available memory
│   └── opcode.py    ## Basically a type that processes and reads an opcode like `+1007` and makes sure that it's valid.
│
├── basm.py  ## An optional program that turns the human friendly representation of BasicML into numbers
├── uvsim.py ## The main abstraction which integrates the memory/cpu/io etc. into one object
├── gui.py   ## A graphical user interface for UVSim that allows users to load, execute, and debug BasicML programs interactively
└── main.py  ## Bootstrap everything and get it running
```
#### Files:

#### `src/cpu.py`

##### Purpose: The CPU class represents the central processing unit of the UVSim virtual machine. It contains an accumulator register for arithmetic and data manipulation operations and processes opcodes to perform various operations.

- **__init__**: Initializes the CPU with an accumulator set to 0000 and a halted flag.
    - **Post-conditions**: The CPU is initialized with the accumulator set to 0000 and halted flag set to False.
- **acc**: (val) Property for the accumulator, with setter and getter.
    - **val**: value to store as accumulator
    - **Post-conditions**: Returns or updates the value of the accumulator.
- **current**: (val) Property for the current memory address being read, with setter and getter.
    - **val**: value to be current address
    - **Pre-conditions**: `val` must be an integer between 0 and 99 inclusive.
    - **Post-conditions**: Returns or updates the current memory address.
- **halted**: (Val) Property for the halted flag.
    - **val**: used to change flag status
    - **Post-conditions**: Returns or updates the halted flag.
- **run**: (memory, io_device, address=0) Executes the program starting at a specified address.
    - **memory**: The memory object where data will be processed.
    - **io_device**: The I/O device used for input/output.
    - **address**: The memory address where the data will be processed.
    - **Pre-conditions**: `memory` and `io_device` must be valid objects. `address` must be a valid memory address.
    - **Post-conditions**: Executes the program, modifying memory and I/O device as needed.
- **process**: (opcode, memory, io_device) Processes a given opcode and modifies memory and I/O devices according to the instruction.
    - **opcode**: The opcode to be processed.
    - **memory**: The memory object involved in the operation.
    - **io_device**: The I/O device involved in the operation.
    - **Pre-conditions**: `opcode`, `memory`, and `io_device` must be valid objects.
    - **Post-conditions**: Modifies memory and I/O device based on the opcode.
- **read**: (memory, io_device, address) Reads a word from the keyboard into a specific location in memory.
    - **memory**: The memory object where data will be written.
    - **io_device**: The I/O device used for reading input.
    - **address**: The memory address where the input data will be stored.
    - **Pre-conditions**: `memory` and `io_device` must be valid objects. `address` must be a valid memory address.
    - **Post-conditions**: Writes input data to the specified memory address.
- **write**: (memory, io_device, address) Writes a word from a specific location in memory to the screen.
    - **memory**: The memory object where data will be read from.
    - **io_device**: The I/O device used for writing output.
    - **address**: The memory address from which the data will be read.
    - **Pre-conditions**: `memory` and `io_device` must be valid objects. `address` must be a valid memory address.
    - **Post-conditions**: Outputs data from the specified memory address to the I/O device.
- **load**: (memory, address) Loads a word from a specific location in memory into the accumulator.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address from which the data will be loaded into the accumulator.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The accumulator is updated with the value from the specified memory address.
- **store**: (memory, address) Stores a word from the accumulator into a specific location in memory.
    - **memory**: The memory object where data will be written.
    - **address**: The memory address where the accumulator data will be stored.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The value in the accumulator is stored in the specified memory address.
- **add**: (memory, address) Adds a word from a specific location in memory to the accumulator.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address from which the data will be added to the accumulator.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The accumulator is updated with the sum of its current value and the value from the specified memory address.
- **subtract**: (memory, address) Subtracts a word from a specific location in memory from the accumulator.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address from which the data will be subtracted from the accumulator.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The accumulator is updated with the result of subtracting the value from the specified memory address from its current value.
- **multiply**: (memory, address) Multiplies a word from a specific location in memory with the accumulator.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address from which the data will be multiplied with the accumulator.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The accumulator is updated with the product of its current value and the value from the specified memory address.
- **divide**: (memory, address) Divides the accumulator by a word from a specific location in memory.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address from which the data will be used to divide the accumulator.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address. The value at the specified memory address must not be zero.
    - **Post-conditions**: The accumulator is updated with the quotient of its current value divided by the value from the specified memory address.
- **branch**: (memory, address) Branches to a specific location in memory.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address to branch to.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The current address is updated to the specified memory address.
- **branchneg**: (memory, address) Branches to a specific location in memory if the accumulator is negative.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address to branch to.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The current address is updated to the specified memory address if the accumulator is negative.
- **branchzero**: (memory, address) Branches to a specific location in memory if the accumulator is zero.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address to branch to.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The current

 address is updated to the specified memory address if the accumulator is zero.
- **halt**: Halts the execution of the program.
    - **Post-conditions**: The halted flag is set to True.
- **noop**: No operation, used to treat the opcode as raw data and not an instruction.
- **step**: (memory, io_device) Executes a single instruction.
    - **memory**: The memory object where data will be processed.
    - **io_device**: The I/O device used for input/output.
    - **Pre-conditions**: `memory` and `io_device` must be valid objects.
    - **Post-conditions**: Executes a single instruction, modifying memory and I/O device as needed.

#### `src/io_device.py`

##### Purpose: The IODevice class represents an input/output device for the UVSim virtual machine. It handles reading input from the user and writing output to the console.

- **__init__**: Initializes the IODevice with optional reader and writer functions.
    - **reader**: Function for reading input. Defaults to `input()`.
    - **writer**: Function for writing output. Defaults to `print()`.
    - **Post-conditions**: Initializes the IODevice with the given reader and writer functions or defaults if none are provided.
- **last_read**: Property that returns the last read input.
- **last_write**: Property that returns the last written output.
- **read**: Reads input using the reader function.
    - **Returns**: The input read from the user.
    - **Post-conditions**: Updates the last read input.
- **write**: Writes output using the writer function.
    - **data**: The data to be written to the console.
    - **Post-conditions**: Updates the last written output.

#### `src/memory.py`

##### Purpose: The Memory class represents the memory of the UVSim virtual machine. It provides methods to read from and write to memory, ensuring proper memory management and addressing.

- **__init__**: Initializes the memory with 100 locations set to 0.
    - **Post-conditions**: The memory is initialized with 100 locations set to 0.
- **__len__**: Returns the length of the memory.
    - **Returns**: The length of the memory.
- **mem**: Property that returns the memory.
    - **Returns**: The memory as a list.
- **write**: Writes a value to a specific memory address.
    - **address**: The memory address to write to.
    - **value**: The value to write to the memory address.
    - **Pre-conditions**: `address` must be within the range of the memory size. `value` must be an integer.
    - **Post-conditions**: Writes the value to the specified memory address. Raises `IndexError` if the address is out of range.
- **read**: Reads a value from a specific memory address.
    - **address**: The memory address to read from.
    - **Returns**: The value read from the memory address.
    - **Pre-conditions**: `address` must be within the range of the memory size.
    - **Post-conditions**: Returns the value from the specified memory address. Raises `IndexError` if the address is out of range.
- **__next**: Finds the next available memory address.
    - **Returns**: The next available memory address.
- **writenext**: Writes a value to the next available memory address.
    - **value**: The value to write to the memory.
    - **Pre-conditions**: `value` must be an integer.
    - **Post-conditions**: Writes the value to the next available memory address. Raises `IndexError` if there are no available memory addresses.

#### `src/opcode.py`

##### Purpose: The Opcode class represents an opcode in the UVSim virtual machine. It handles the parsing and validation of opcodes and provides methods to access the operation name, sign, and operand.

- **__init__**: Initializes the Opcode with a raw string value.
    - **raw**: The raw string value of the opcode.
    - **Pre-conditions**: `raw` must be a valid string representing an opcode.
    - **Post-conditions**: The opcode is initialized with the given raw value. Raises `ValueError` if the raw value is invalid.
- **name**: Property that returns the name of the operation corresponding to the opcode.
    - **Returns**: The name of the operation.
- **sign**: Property that returns the sign of the opcode.
    - **Returns**: The sign of the opcode.
- **operand**: Property that returns the operand of the opcode.
    - **Returns**: The operand of the opcode.
- **__str__**: Returns the string representation of the opcode.
    - **Returns**: The string representation of the opcode.
- **__eq__**: Checks if two opcodes are equal.
    - **other**: The other opcode to compare with.
    - **Returns**: `True` if the opcodes are equal, `False` otherwise.
- **__add__**: Adds two opcodes.
    - **other**: The other opcode to add.
    - **Returns**: The resulting opcode from the addition.
    - **Pre-conditions**: `other` must be a valid Opcode object.
    - **Post-conditions**: Returns a new Opcode representing the sum of the two opcodes. Raises `OverflowError` if the resulting value is out of bounds.
- **__sub**: Subtracts two opcodes.
    - **other**: The other opcode to subtract.
    - **Returns**: The resulting opcode from the subtraction.
    - **Pre-conditions**: `other` must be a valid Opcode object.
    - **Post-conditions**: Returns a new Opcode representing the difference of the two opcodes. Raises `OverflowError` if the resulting value is out of bounds.
- **__mul__**: Multiplies two opcodes.
    - **other**: The other opcode to multiply.
    - **Returns**: The resulting opcode from the multiplication.
    - **Pre-conditions**: `other` must be a valid Opcode object.
    - **Post-conditions**: Returns a new Opcode representing the product of the two opcodes. Raises `OverflowError` if the resulting value is out of bounds.
- **__truediv__**: Divides two opcodes.
    - **other**: The other opcode or integer to divide by.
    - **Returns**: The resulting opcode from the division.
    - **Pre-conditions**: `other` must be a valid Opcode object or integer. Must not be zero.
    - **Post-conditions**: Returns a new Opcode representing the quotient of the division. Raises `ZeroDivisionError` if division by zero is attempted.

#### `gui.py`

##### Purpose: The `gui.py` file implements a graphical user interface for the UVSim using `tkinter`. It allows users to load, execute, and debug BasicML programs interactively.

- **show_help**: Function to display a help window with instructions for using the UVSim.
    - **Post-conditions**: A help window is displayed.
- **start_program**: Function to transition from the title screen to the file selection screen.
    - **Pre-conditions**: None.
    - **Post-conditions**: The file selection screen is displayed.
- **browse_files**: Function to open a file dialog for selecting a test file.
    - **Post-conditions**: A file dialog is opened, and the selected file path is displayed in the file entry field.
- **load_file**: Function to load the selected file into the UVSim and transition to the main control screen.
    - **Pre-conditions**: A valid file path must be provided.
    - **Post-conditions**: The selected file is loaded into the UVSim, and the main control screen is displayed.
- **update_main_control_frame**: Function to update the memory display and current instruction display in the main control frame.
    - **Post-conditions**: The memory display and current instruction display are updated with the latest information from the UVSim.
- **start_simulation**: Function to start the simulation by running the UVSim.
    - **Pre-conditions**: The UVSim must be properly initialized and loaded with a program.
    - **Post-conditions**: The UVSim runs the loaded program, and the memory display is updated accordingly.
- **execute_step**: Function to execute a single step of the simulation.
    - **Pre-conditions**: The UVSim must be properly initialized and loaded with a program.
    - **Post-conditions**: The UVSim executes a single instruction, and the memory display is updated accordingly.

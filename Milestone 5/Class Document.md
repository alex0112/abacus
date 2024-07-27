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
│   └── opcode.py    ## Basically a type that processes and reads an opcode lik 1007 and makes sure that it's valid.
│
├── basm.py  ## An optional program that turns the human friendly representation of BasicML into numbers
├── uvsim.py ## The main abstraction which integrates the memory/cpu/io etc. into one object
├── gui.py   ## A graphical user interface for UVSim that allows users to load, execute, and debug BasicML programs interactively
└── main.py  ## Bootstrap everything and get it running
```

#### Files:

#### `gui.py`

##### Purpose: The `gui.py` file implements a graphical user interface for the UVSim using `tkinter`. It allows users to load, execute, and debug BasicML programs interactively.

- **show_help**: Displays a help window with instructions for using the UVSim.
    - Post-conditions: A help window is displayed.
- **start_program**: Transitions from the title screen to the file selection screen.
    - Post-conditions: The file selection screen is displayed.
- **browse_files**: Opens a file dialog for selecting a test file.
    - **Post-conditions**: A file dialog is opened, and the selected file path is displayed in the file entry field.
- **load_file**: Loads the selected file into the UVSim and transitions to the main control screen.
    - **Pre-conditions**: A valid file path must be provided.
    - **Post-conditions**: The selected file is loaded into the UVSim, and the main control screen is displayed.
- **store_file**: Saves the current state of the UVSim memory to a file using the file dialog.
    - **Pre-conditions**: A file must be loaded into the UVSim program.
    - **Post-conditions**: The memory contents are saved to the specified file.
- **update_main_control_frame**: Updates the memory display and current instruction display in the main control frame.
    - **Post-conditions**: The memory display and current instruction display are updated with the latest information from the UVSim.
- **start_simulation**: Starts the simulation by running the UVSim.
    - **Pre-conditions**: The UVSim must be properly initialized and loaded with a program.
    - **Post-conditions**: The UVSim runs the loaded program, and the memory display is updated accordingly.
- **execute_step**: Executes a single step of the simulation.
    - **Pre-conditions**: The UVSim must be properly initialized and loaded with a program.
    - **Post-conditions**: The UVSim executes a single instruction, and the memory display is updated accordingly.
- **pause**: Pauses or resumes the simulation.
    - **Pre-conditions**: The simulation must be started.
    - **Post-conditions**: The simulation is paused or resumed.
- **halt_simulation**: Halts the simulation.
    - **Post-conditions**: The simulation is halted, and the current instruction is reset.

#### `main.py`

##### Purpose: The main entry point for the UVSim virtual machine. It loads and executes a BasicML program.

- **main**: The main function starts the simulator and executes a program.
    - **Pre-conditions**: A program file must be specified as a command-line argument.
    - **Post-conditions**: The program is loaded and executed by the UVSim.
- **banner**: Displays a banner for the UVSim.
    - **Post-conditions**: The banner is displayed in the console.

#### `uvsim.py`

##### Purpose: The UVSim class represents the UVSim virtual machine, including its memory, CPU, and I/O devices.

- **init**: Initializes the UVSim with memory, I/O devices, and a CPU.
    - **reader**: Function for reading input, defaulting to `input()`.
    - **writer**: Function for writing output, defaulting to `print()`.
    - **out_line**: Optional function for handling output line formatting.
    - **Post-conditions**: UVSim is initialized with memory, CPU, and I/O devices.
- **mem**: Property to access the memory object.
- **cpu**: Property to access the CPU object.
- **io_device**: Property to access the I/O device object.
- **load**: Loads a program from a file into memory.
    - **filename**: The file containing the program to load.
    - **Pre-conditions**: The file must exist and be accessible.
    - **Post-conditions**: The program is loaded into memory starting at location 0.
- **execute**: Executes the loaded program.
    - **Pre-conditions**: The program must be loaded into memory.
    - **Post-conditions**: The program is executed by the CPU.
- **store**: Saves the contents of memory to a file.
    - **filename**: The file to save the memory contents to.
    - **Post-conditions**: The memory contents are saved to the specified file.

#### `basm.py`

##### Purpose: The `basm.py` file assembles a BasicML program into executable machine code for the UVSim CPU.

- **main**: The main function reads a BasicML program and assembles it into machine code.
    - **Pre-conditions**: A BasicML program file must be specified as a command-line argument.
    - **Post-conditions**: The program is assembled and written to `a.out.basm`.
- **read_file**: Reads a BasicML program from a file and returns a list of opcodes.
    - **filename**: The file containing the BasicML program.
    - **Returns**: A list of Opcode objects representing the program.
    - **Post-conditions**: The file is read, and the program is returned as a list of opcodes.
- **assemble**: Translates a BasicML program into machine code and writes it to a file.
    - **program**: The list of Opcode objects representing the program.
    - **filename**: The output file for the assembled machine code.
    - **Post-conditions**: The assembled machine code is written to the specified file.

#### `src/cpu.py`

##### Purpose: The CPU class represents the central processing unit of the UVSim virtual machine. It contains an accumulator register for arithmetic and data manipulation operations and processes opcodes to perform various operations.

- **init**: Initializes the CPU with an accumulator set to 0000 and a halted flag.
    - Post-conditions: The CPU is initialized with the accumulator set to 0000 and the halted flag set to False.
- **acc**: Property for the accumulator, with getter and setter.
    - **val**: Value to store as accumulator.
    - **Post-conditions**: Returns or updates the value of the accumulator.
- **current**: Property for the current memory address being read, with getter and setter.
    - **val**: Value to be the current address.
    - **Pre-conditions**: `val` must be an integer within the addressable memory space.
    - **Post-conditions**: Returns or updates the current memory address.
- **halted** Property for the halted flag.
    - **val**: Value to change the flag status.
    - **Post-conditions**: Returns or updates the halted flag.
- **run**: Executes the program starting at a specified address.
    - **memory**: The memory object where data will be processed.
    - **io_device**: The I/O device used for input/output.
    - **address**: The memory address where the program starts.
    - **Pre-conditions**: `memory` and `io_device` must be valid objects. `address` must be a valid memory address.
    - **Post-conditions**: Executes the program, modifying memory and I/O device as needed.
- **process**: Processes a given opcode and modifies memory and I/O devices according to the instruction.
    - **opcode**: The opcode to be processed.
    - **memory**: The memory object involved in the operation.
    - **io_device**: The I/O device involved in the operation.
    - **Pre-conditions**: `opcode`, `memory`, and `io_device` must be valid objects.
    - **Post-conditions**: Modifies memory and I/O device based on the opcode.
- **read**: Reads a word from the keyboard into a specific location in memory.
    - **memory**: The memory object where data will be written.
    - **io_device**: The I/O device used for reading input.
    - **address**: The memory address where the input data will be stored.
    - **Pre-conditions**: `memory` and `io_device` must be valid objects. `address` must be a valid memory address.
    - **Post-conditions**: Writes input data to the specified memory address.
- **write**: Writes a word from a specific location in memory to the screen.
    - **memory**: The memory object where data will be read from.
    - **io_device**: The I/O device used for writing output.
    - **address**: The memory address from which the data will be read.
    - **Pre-conditions**: `memory` and `io_device` must be valid objects. `address` must be a valid memory address.
    - **Post-conditions**: Outputs data from the specified memory address to the I/O device.
- **load**: Loads a word from a specific location in memory into the accumulator.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address from which the data will be loaded into the accumulator.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The accumulator is updated with the value from the specified memory address.
- **store**: Stores a word from the accumulator into a specific location in memory.
    - **memory**: The memory object where data will be written.
    - **address**: The memory address where the accumulator data will be stored.
    - **Pre-conditions**: memory must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The value in the accumulator is stored in the specified memory address.
- **add** Adds a word from a specific location in memory to the accumulator.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address from which the data will be added to the accumulator.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The accumulator is updated with the sum of its current value and the value from the specified memory address.
- **subtract**: Subtracts a word from a specific location in memory from the accumulator.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address from which the data will be subtracted from the accumulator.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The accumulator is updated with the result of subtracting the value from the specified memory address from its current value.
- **multiply**: Multiplies a word from a specific location in memory with the accumulator.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address from which the data will be multiplied with the accumulator.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-condition**: The accumulator is updated with the product of its current value and the value from the specified memory address.
- **divide**: Divides the accumulator by a word from a specific location in memory.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address from which the data will be used to divide the accumulator.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address. The value at the specified memory address must not be zero.
    - **Post-conditions**: The accumulator is updated with the quotient of its current value divided by the value from the specified memory address.
- **branch**: Branches to a specific location in memory.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address to branch to.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The current address is updated to the specified memory address.
- **branchneg**: Branches to a specific location in memory if the accumulator is negative.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address to branch to.
    - **Pre-conditions**: `memory` must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The current address is updated to the specified memory address if the accumulator is negative.
- **branchzero:** Branches to a specific location in memory if the accumulator is zero.
    - **memory**: The memory object where data will be read from.
    - **address**: The memory address to branch to.
    - **Pre-conditions**: `memory `must be a valid object. `address` must be a valid memory address.
    - **Post-conditions**: The current address is updated to the specified memory address if the accumulator is zero.
- **halt**: Halts the execution of the program.
    - **Post-conditions**: The halted flag is set to True.
- **noop**: No operation, used to treat the opcode as raw data and not an instruction.
- **step**: Executes a single instruction.
    - **memory**: The memory object where data will be processed.
    - **io_device**: The I/O device used for input/output.
    - **Pre-conditions**: `memory` and `io_device` must be valid objects.
    - **Post-conditions**: Executes a single instruction, modifying memory and I/O device as needed.

#### `src/io_device.py`

##### Purpose: The IODevice class represents an input/output device for the UVSim virtual machine. It handles reading input from the user and writing output to the console.

- **init**: Initializes the IODevice with optional reader and writer functions.
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

- **init**: Initializes the memory with 100 locations set to 0.
    - **Post-conditions**: The memory is initialized with 100 locations set to 0.
- **len**: Returns the length of the memory.
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

#### `src/opcodes.py`

##### Purpose: The Opcode class represents an opcode in the UVSim virtual machine. It handles the parsing and validation of opcodes and provides methods to access the operation name, sign, and operand.

- **init**: Initializes the Opcode with a raw string value.
    - **raw**: The raw string value of the opcode.
    - **Pre-conditions**: `raw` must be a valid string representing an opcode.
    - **Post-conditions**: The opcode is initialized with the given raw value. Raises `ValueError` if the raw value is invalid.
- **name**: Property that returns the name of the operation corresponding to the opcode.
    - Returns: The name of the operation.
- **sign**: Property that returns the sign of the opcode.
    - Returns: The sign of the opcode.
- **operand**: Property that returns the operand of the opcode.
    - **Returns**: The operand of the opcode.
- **str**: Returns the string representation of the opcode.
    - **Returns**: The string representation of the opcode.
- **eq**: Checks if two opcodes are equal.
    - **other:** The other opcode to compare with.
    - **Returns**: `True` if the opcodes are equal, `False` otherwise.
- **add**: Adds two opcodes.
    - **other**: The other opcode to add.
    - **Returns**: The resulting opcode from the addition.
    - **Pre-conditions**: `other` must be a valid Opcode object.
    - **Post-conditions**: Returns a new Opcode representing the sum of the two opcodes. Raises `OverflowError` if the resulting value is out of bounds.
 - **__sub**: Subtracts two opcodes.
    - **other**: The other opcode to subtract.
    - **Returns**: The resulting opcode from the subtraction.
    - **Pre-conditions**: `other` must be a valid Opcode object.
    - **Post-conditions**: Returns a new Opcode representing the difference of the two opcodes. Raises `OverflowError` if the resulting value is out of bounds.
- **__mul**: Multiplies two opcodes.
    - **other**: The other opcode to multiply.
    - **Returns**: The resulting opcode from the multiplication.
    - **Pre-conditions**: `other `must be a valid Opcode object.
    - **Post-conditions**: Returns a new Opcode representing the product of the two opcodes. Raises `OverflowError` if the resulting value is out of bounds.
- **truediv**: Divides two opcodes.
    - **other**: The other opcode or integer to divide by.
    - **Returns**: The resulting opcode from the division.
    - **Pre-conditions**: `other` must be a valid Opcode object or integer. Must not be zero.
    - **Post-conditions**: Returns a new Opcode representing the quotient of the division. Raises `ZeroDivisionError` if division by zero is attempted.

#### `test/test_cpu.py`

##### Purpose: The test_cpu.py file contains unit tests for the CPU class of the UVSim virtual machine. These tests verify the correct implementation of the CPU's functionalities, including instruction processing and error handling.

- **test_init**: Verifies that a CPU instance initializes correctly with the expected default states.
    - **Post-conditions**: The CPU should not be halted, the current address should be 0, and the accumulator should be `+0000`.
- **test_overflow**: Tests that setting the current address beyond the memory bounds raises an `IndexError`.
    - **Post-conditions**: An IndexError is raised if the current address is set to 100 or more.
- **test_underflow**: Tests that setting the current address below the lower bound raises an `IndexError`.
    - **Post-conditions**: An IndexError is raised if the current address is set below 0.
- **test_halt_from_index**: Tests that the CPU halts when the current address reaches 99.
    - Post-conditions: The halted flag should be set to True.
- **test_halt_from_instruction**: Verifies that a HALT opcode correctly stops the CPU.
    - **Post-conditions**: The CPU should be halted after processing the HALT opcode.
- **test_read_good_word**: Verifies that a READ instruction correctly inputs data into memory.
    - **Post-conditions**: The specified memory location should store the value entered.
- **test_read_bad_word**: Tests that a malformed READ instruction raises a ValueError.
    - **Post-conditions**: A `ValueError` is raised if the opcode format is incorrect.
- **test_write**: Verifies that a WRITE instruction outputs data from memory correctly.
    - **Post-conditions**: The data read from memory should match the expected output.
- **test_write_bad_word**: Tests that a malformed WRITE instruction raises a ValueError.
    - **Post-conditions**: A `ValueError` is raised if the opcode format is incorrect.
- **test_load**: Verifies that a LOAD instruction correctly sets the accumulator from memory.
    - **Post-conditions**: The accumulator should reflect the loaded value.
- **test_load_bad_word**: Tests that a malformed LOAD instruction raises a ValueError.
    - **Post-conditions**: A `ValueError` is raised if the opcode format is incorrect.
- **test_store**: Verifies that a STORE instruction saves the accumulator's value to memory.
    - **Post-conditions**: The specified memory location should store the accumulator's value.
- **test_store_bad_word**: Tests that a malformed STORE instruction raises a ValueError.
    - **Post-conditions**: A `ValueError` is raised if the opcode format is incorrect.
- **test_add**: Verifies that an ADD instruction correctly adds a value from memory to the accumulator.
    - **Post-conditions**: The accumulator should reflect the sum of its current value and the memory value.
- **test_add_bad_word**: Tests that a malformed ADD instruction raises a ValueError.
    - **Post-conditions**: A `ValueError` is raised if the opcode format is incorrect.
- **test_subtract**: Verifies that a SUBTRACT instruction correctly subtracts a value from the accumulator.
    - **Post-conditions**: The accumulator should reflect the difference between its current value and the memory value.
- **test_subtract_bad_word**: Tests that a malformed SUBTRACT instruction raises a ValueError.
    - **Post-conditions**: A `ValueError` is raised if the opcode format is incorrect.
- **test_multiply**: Verifies that a MULTIPLY instruction correctly multiplies the accumulator by a memory value.
    - **Post-conditions**: The accumulator should reflect the product of its current value and the memory value.
- **test_multiply_bad_word**: Tests that a malformed MULTIPLY instruction raises a ValueError.
    - **Post-conditions**: A `ValueError` is raised if the opcode format is incorrect.
- **test_divide:** Verifies that a DIVIDE instruction correctly divides the accumulator by a memory value.
    - **Post-conditions**: The accumulator should reflect the quotient of its current value divided by the memory value.
- **test_divide_rem**: Verifies that a DIVIDE instruction handles remainders correctly.
    - **Post-conditions**: The accumulator should reflect the integer quotient.
- **test_divide_bad_word**: Tests that a malformed DIVIDE instruction raises a ValueError.
    - **Post-conditions**: A `ValueError` is raised if the opcode format is incorrect.
- **test_divide_by_zero**: Verifies that dividing by zero raises a ZeroDivisionError.
    - **Post-conditions**: A `ZeroDivisionError` is raised if the divisor is zero.
- **test_branch**: Verifies that a BRANCH instruction correctly updates the current address.
    - **Post-conditions**: The current address should be set to the specified memory address.

#### `test/test_io.py`

##### Purpose: The `test_io.py` file contains unit tests for the IODevice class, which manages input and output operations for the UVSim virtual machine.

- **test_init**: Verifies that an IODevice instance initializes correctly.
    - **Post-conditions**: The IODevice should be initialized with default or provided reader and writer functions.
- **test_read**: Tests that the IODevice can correctly read input data.
    - **Post-conditions**: The input data should match the expected output.
- **test_write**: Tests that the IODevice can correctly write output data.
    - **Post-conditions**: The written data should match the expected output.
- **test_err**: Tests that the IODevice can correctly handle error messages.
    - **Post-conditions**: The error message should be correctly handled and displayed.

#### `test/test_memory.py`

##### Purpose: The `test_memory.py` file contains unit tests for the Memory class, which manages the memory of the UVSim virtual machine.

- **test_init:** Verifies that a Memory instance initializes correctly.
    - **Post-conditions**: The Memory should be initialized with default values.
- **test_init_from_list**: Verifies that Memory can be initialized from a list of Opcodes.
    - **Post-conditions**: The Memory should contain the Opcodes provided in the list.
- **test_init_from_exact_list**: Tests Memory initialization with a list of the maximum size.
    - **Post-conditions**: The Memory should correctly store the Opcodes from the list.
- **test_bad_init_from_list**: Verifies that initializing Memory with an invalid list raises an `IndexError`.
    - **Post-conditions**: An `IndexError` is raised for out-of-bounds memory initialization.
- **test_bad_init_from_large_list**: Verifies that initializing Memory with an oversized list raises an `IndexError`.
    - **Post-conditions**: An `IndexError` is raised for lists larger than the memory capacity.
- **test_default_read**: Verifies that reading from uninitialized memory returns a default Opcode.
    - **Post-conditions**: The returned Opcode should be `+0000`.
- **test_read**: Verifies that values can be read correctly from Memory.
    - **Post-condition**: The returned values should match those stored in Memory.
- **test_write**: Verifies that values can be written correctly to Memory.
    - **Post-conditions**: The Memory should store the written values correctly.
- **test_writenext_empty**: Verifies that the `writenext` method writes to the next available address.
    - **Post-conditions**: The first address should be written with the provided value.
- **test_writenext**: Verifies that the `writenext` method continues writing to the next available address.
    - **Post-conditions**: Memory should continue to store values sequentially.
- **test_index**: Verifies that Memory can be accessed using an index.
    - **Post-conditions**: The returned Opcode should match the stored value.
- **test_slice**: Verifies that Memory can be accessed using slicing.
    - **Post-conditions**: The returned list should match the slice of Memory.
- **test_preview_full**: Verifies that the `preview` method provides a full range preview of Memory.
    - **Post-conditions**: The preview should match the expected memory content.
- **test_preview_empty**: Verifies that the preview method provides a default preview when Memory is empty.
    - **Post-conditions**: The `preview` should show default values.
- **test_preview_begin_odd**: Tests preview behavior at the start of Memory with an odd range.
    - **Post-conditions**: The `preview` should include initial memory addresses.
- **test_preview_near_begin_odd**: Tests preview behavior near the start of Memory with an odd range.
    - **Post-conditions**: The preview should include early memory addresses.
- **test_preview_begin_even**: Tests preview behavior at the start of Memory with an even range.
    - **Post-conditions**: The preview should include initial memory addresses.
- **test_preview_near_begin_even**: Tests preview behavior near the start of Memory with an even range.
    - **Post-conditions**: The preview should include early memory addresses.
- **test_preview_end_odd**: Tests preview behavior at the end of Memory with an odd range.
    - **Post-conditions**: The preview should include final memory addresses.
- **test_preview_near_end_odd**: Tests preview behavior near the end of Memory with an odd range.
    - **Post-conditions**: The preview should include later memory addresses.
- **test_preview_near_end_even**: Tests preview behavior near the end of Memory with an even range.
    - **Post-conditions**: The preview should include later memory addresses.
- **test_preview_end_even**: Tests preview behavior at the end of Memory with an even range.
    - **Post-conditions**: The preview should include final memory addresses.
- **test_memory_iteration**: Verifies that Memory can be iterated over correctly.
    - **Post-conditions**: The iteration should correctly access all stored Opcodes.

#### `test/test_opcode.py`

##### Purpose: The `test_opcode.py` file contains unit tests for the Opcode class, which handles the parsing, validation, and manipulation of opcodes in the UVSim virtual machine.

- **test_init_with_plus**: Verifies that an Opcode instance initializes correctly with a positive sign.
    - **Post-conditions**: The Opcode should be correctly initialized as `+1234`.
- **test_init_with_minu**s: Verifies that an Opcode instance initializes correctly with a negative sign.
    - **Post-conditions**: The Opcode should be correctly initialized as `-1234`.
- **test_init_with_no_sign**: Verifies that an Opcode instance initializes correctly without a specified sign.
    - **Post-conditions**: The Opcode should default to a positive sign and be `+1234`.
- **test_init_with_too_long**: Verifies that an Opcode with too many digits raises a `ValueError`.
    - **Post-conditions**: A ValueError is raised for Opcodes longer than 5 characters.
- **test_init_with_too_short**: Verifies that an Opcode with too few digits raises a `ValueError`.
    - **Post-conditions**: A ValueError is raised for Opcodes shorter than 4 digits.
- **test_init_with_non_num**: Verifies that an Opcode with non-numeric characters raises a `ValueError`.
    - **Post-conditions**: A ValueError is raised for Opcodes containing non-numeric characters.
- **test_init_with_empty**: Verifies that an empty Opcode raises a `ValueError`.
    - **Post-conditions**: A ValueError is raised for empty Opcode strings.
- **test_init_with_too_large**: Verifies that an Opcode with too large a number raises a `ValueError`.
    - **Post-condition**s: A ValueError is raised for numbers exceeding the allowed range.
- **test_init_with_too_small**: Verifies that an Opcode with too small a number raises a `ValueError`.
    - **Post-conditions**: A ValueError is raised for numbers below the allowed range.
- **test_name**: Verifies that the `name` property correctly identifies the operation.
    - **Post-conditions**: The name should match the expected operation (e.g., "READ").
- **test_noop**: Verifies that an unrecognized opcode defaults to "NOOP".
    - Post-conditions: The operation name should be "NOOP".
- **test_plus**: Verifies that the `sign` property correctly identifies a positive sign.
    - **Post-conditions**: The sign should be `+`.
- **test_minus**: Verifies that the `sign` property correctly identifies a negative sign.
    - **Post-conditions**: The sign should be `-`.
- **test_operand**: Verifies that the operand property correctly extracts the operand from the opcode.
    - **Post-conditions**: The operand should match the last two digits of the Opcode.
- **test_str_from_minus**: Verifies that the string representation of a negative Opcode is correct.
    - **Post-conditions**: The string representation should be `-1234`.
- **test_str_from_plus**: Verifies that the string representation of a positive Opcode is correct.
    - **Post-conditions**: The string representation should be `+1234`.
- **test_str_from_no_sign**: Verifies that the string representation of an unsigned Opcode is correct.
    - **Post-conditions**: The string representation should default to `+1234`.
- **test_basic_equality**: Verifies that two Opcodes with the same value are equal.
    - **Post-conditions**: The equality check should return True.
- **test_basic_inequality**: Verifies that two Opcodes with different values are not equal.
    - **Post-conditions**: The equality check should return False.
- **test_basic_add**: Verifies that the addition of two Opcodes yields the correct result.
    - **Post-conditions**: The sum should match the expected value.
- **test_add_negative_and_positive**: Verifies that adding a negative and positive Opcode yields the correct result.
    - **Post-conditions**: The result should correctly account for the sign.
- **test_add_negative_and_negative**: Verifies that adding two negative Opcodes yields the correct result.
    - **Post-conditions**: The result should be negative and match the expected value.
- **test_basic_subtraction**: Verifies that subtracting one Opcode from another yields the correct result.
    - **Post-conditions**: The difference should match the expected value.
- **test_subtract_a_negative**: Verifies that subtracting a negative Opcode yields the correct result.
    - **Post-conditions**: The result should be positive if subtracting a negative Opcode.
- **test_mul**: Verifies that multiplying two Opcodes yields the correct result.
    - **Post-conditions**: The product should match the expected value.
- **test_mul_neg**: Verifies that multiplying a positive and a negative Opcode yields the correct result.
    - **Post-conditions**: The result should be negative and match the expected value.
- **test_integer_div**: Verifies that dividing an Opcode by an integer yields the correct result.
    - **Post-conditions**: The quotient should match the expected value.
- **test_opcode_div**: Verifies that dividing two Opcodes yields the correct result.
    - **Post-conditions**: The quotient should match the expected value.
- **test_opcode_div_with_remainder**: Verifies that division with a remainder is handled correctly.
    - **Post-conditions**: The quotient should be an integer and match the expected value.
- **test_overflow_addition**: Verifies that adding Opcodes handles overflow correctly.
    - **Post-conditions**: The result should wrap around and match the expected overflow behavior.
- **test_underflow_subtraction**: Verifies that subtracting Opcodes handles underflow correctly.
    - **Post-conditions**: The result should wrap around and match the expected underflow behavior.
- **test_overflow_product**: Verifies that multiplying Opcodes handles overflow correctly.
    - **Post-conditions**: The result should wrap around and match the expected overflow behavior.
- **test_underflow_product**: Verifies that multiplying Opcodes handles underflow correctly.
    - **Post-conditions**: The result should wrap around and match the expected underflow behavior.
- **test_named_opcode**: Verifies that named Opcodes are correctly identified.
    - **Post-conditions**: The `human_friendly` property should return the correct operation name.
- **test_unamed_opcode**: Verifies that unnamed Opcodes are correctly identified as "NOOP".
    - **Post-conditions**: The `human_friendly` property should return "NOOP".


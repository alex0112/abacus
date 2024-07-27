# **Group Project Milestone 5**

---

## **<span style="text-decoration:underline;">Design Document</span>**

### **User Stories:**

* **User Story 1**: As an accountant, I want a calculator with a memory, so that I can keep track of values and easily make modifications on those values if I want to.
* **User Story 2**: As a physicist, I want a way to automate calculation, so that I can automatically input values and get the resulting appropriate values for that calculation.

---

### **Use Cases:**

**Use Case 1: Read from I/O device**

1. Store Read command in memory
2. Load Read command to CPU accumulator
3. Execute Read command to retrieve data from I/O device
4. Store retrieved data in memory

**Use Case 2: Write to I/O device**

1. Store Write command in memory
2. Load Write command to CPU accumulator
3. Execute Write command to send data from memory to I/O device and store the result in the accumulator

**Use Case 3: Load**

1. Store Load command in memory
2. Load Load command to CPU accumulator
3. Execute Load command to move data from memory into the CPU accumulator

**Use Case 4: Store**

1. Store Store command in memory
2. Load Store command to CPU accumulator
3. Execute Store command to transfer the value from the accumulator to a specified memory location

**Use Case 5: Arithmetic Operations (General)**

**Use Case 5a: Divide**

1. Store Divide command in memory
2. Load Divide command to CPU accumulator
3. Execute Divide command to divide the value in the accumulator by a value from a specific location in memory, storing the result back in the accumulator

**Use Case 5b: Add**

1. Store Add command in memory
2. Load Add command to CPU accumulator
3. Execute Add command to add a value from a specific location in memory to the value in the accumulator, storing the result back in the accumulator

**Use Case 5c: Subtract**

1. Store Subtract command in memory
2. Load Subtract command to CPU accumulator
3. Execute Subtract command to subtract a value from a specific location in memory from the value in the accumulator, storing the result back in the accumulator

**Use Case 5d: Multiply**

1. Store Multiply command in memory
2. Load Multiply command to CPU accumulator
3. Execute Multiply command to multiply the value in the accumulator by a value from a specific location in memory, storing the result back in the accumulator

**Use Case 6: Branch**

1. Store Branch command in memory
2. Load Branch command to CPU accumulator
3. Execute Branch command to set the program counter to a specific location in memory

**Use Case 7: BranchNeg**

1. Store BranchNeg command in memory
2. Load BranchNeg command to CPU accumulator
3. Execute BranchNeg command to set the program counter to a specific location in memory if the accumulator is negative

**Use Case 8: BranchZero**

1. Store BranchZero command in memory
2. Load BranchZero command to CPU accumulator
3. Execute BranchZero command to set the program counter to a specific location in memory if the accumulator is zero

**Use Case 9: Halt**

1. Store Halt command in memory
2. Load Halt command to CPU accumulator
3. Execute Halt command to stop the CPU from processing further instructions

**Use Case 10: GUI Tab Management**

1. User initiates the creation of a new tab in the GUI.
2. The system initializes a new UVSim instance for the new tab.
3. Each tab operates independently, allowing multiple programs to be loaded and run simultaneously.
4. The user can close a tab, which will terminate the associated UVSim instance.

**Use Case 11: Memory Edit via GUI**

1. User selects an option to edit memory from the GUI.
2. The GUI displays the current memory contents in a text editor format.
3. User makes changes to the memory content as needed.
4. The changes are submitted and updated in the UVSim instance’s memory.

**Use Case 12: Color Customization in GUI**

1. User accesses the color customization settings in the GUI.
2. The system displays a color picker for primary and secondary interface colors.
3. User selects new colors from the color picker.
4. The interface updates to reflect the new color choices.

**Use Case 13: File Operations in GUI**

1. User selects the option to load a program file in the GUI.
2. The system opens a file dialog for the user to choose a file.
3. The chosen file is loaded into the UVSim memory for execution.
4. User can also save the current state of memory to a file using the GUI's save option, specifying a file name and location.

**Use Case 14: Command Line Interface for Main Program**

1. User runs the main program from the command line with the program file as an argument.
2. The main program displays a banner and loads the specified program file.
3. The UVSim system executes the loaded program, handling operations according to the commands in the file.

**Use Case 15: Assembling BasicML Code**

1. User provides a BasicML code file to the assembler.
2. The assembler reads the BasicML instructions and converts them into machine-readable format.
3. The assembled code is written to an output file named "a.out.basm".

**Use Case 16: CPU Error Handling**

1. The CPU encounters an invalid operation or memory address during execution.
2. The system raises an appropriate exception (e.g., IndexError for out-of-bounds memory access, ZeroDivisionError for division by zero).
3. Error messages are logged and displayed to the user.
4. The UVSim system halts safely to prevent further errors.

**Use Case 17: Memory Preview in GUI**

1. User requests a preview of the current memory state.
2. The GUI provides a scrolling view of memory addresses around the current instruction pointer.
3. The current instruction and its address are highlighted for clarity.
4. Users can scroll to see more memory content and edit memory values if needed.

---
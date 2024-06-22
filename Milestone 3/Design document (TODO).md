# **Group Project Milestone 2 **


---


## **<span style="text-decoration:underline;">Design Document</span>**


### **User Stories**:



* **User Story 1**: As an accountant,  I want a calculator with a memory, so that I can keep track of values and easily make modifications on those values if I want to.
* **User Story 2**: As a physicist,  I want a way to automate calculation, so that I can automatically input values and get the resulting appropriate values for that calculation.

**Use Case 1: Read from I/O device**



1. Store Read command in memory
2. Load Read command to CPU accumulator
3. Execute Read command to retrieve data from I/O device
4. Store retrieved data in memory

**Use Case 2: Write to I/O device**



1. Store Write command in memory
2. Load Write command to CPU accumulator
3. Execute Write command to send data from I/O device and store result in accumulator

**Use Case 3: Load**



1. Store Load command in memory
2. Make the Load command move to CPU accumulator
3. Execute Write command to load from memory into the CPU accumulator

**Use Case 4: Store**



1. Load Store command to memory
2. Load Store command to CPU accumulator
3. Execute command to store the accumulator in the specified memory location

**Use Case 5: Arithmetic Operations (General)**

**Use Case 5a: Divide**



1. Store Divide command in memory
2. Load Divide command to CPU accumulator
3. Execute Divide command to divide the word in the accumulator by a word from a specific location in memory leaving the result in the accumulator

**Use Case 5b: Add**



1. Store Add command in memory
2. Load Add command to CPU accumulator
3. Execute Add command to add a word from a specific location in memory to the word in the accumulator leaving the result in the accumulator

**Use Case 5c: Subtract**



1. Store Subtract command in memory
2. Load Subtract command to CPU accumulator
3. Execute Subtract command to subtract a word from a specific location in memory from the word in the accumulator leaving the result in the accumulator

**Use Case 5d: Multiply**



1. Store Multiply command in memory
2. Load Multiply command to CPU accumulator
3. Execute Multiply command to multiply a word from a specific location in memory by the word in the accumulator leaving the result in the accumulator

**Use Case 6: Branch**



1. Store Branch command in memory
2. Load Branch command to CPU accumulator
3. Execute Branch command to branch to a specific location in memory

**Use Case 7: BranchNeg**



1. Store BranchNeg command in memory
2. Load BranchNeg command to CPU accumulator
3. Execute BranchNeg command to branch to a specific location in memory if the accumulator is negative

**Use Case 8: BranchZero**



1. Store BranchZero command in memory
2. Load BranchZero command to CPU accumulator
3. Execute BranchZero command to branch to a specific location in memory if the accumulator is zero

**Use Case 9: Halt**



1. Store Halt command in memory
2. Load Halt command to CPU accumulator
3. Execute Halt command to stop the CPU from parsing through memory

<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works
The CRC-3 Module with Latch-Based Clock Gating is a compact error detection system designed for a 1x1 tile chip. It uses a 3-bit Linear Feedback Shift Register (LFSR) to compute a Cyclic Redundancy Check (CRC) based on the polynomial (x^3 + x + 1) (binary 1011). Data is fed serially via the data_in input, and the module processes it bit-by-bit on each clock cycle when enabled. A latch-based clock gating mechanism reduces power consumption by disabling the clock when the enable signal (ui_in[0]) is low, using a latch to stabilize the enable signal and prevent glitches. The resulting 3-bit CRC value is output on uo_out[2:0], which can be compared at the receiver to detect data errors.

Below is the simple block diagram:

![Block Diagram](https://github.com/user-attachments/assets/fd13fa8a-a8f8-4421-8138-2ae1b1dac20d)


## How to test

To test the CRC-3 module, use a Verilog testbench to simulate the design. Set rst_n low to reset the module, then drive ui_in[0] high to enable clock gating and feed serial data through ui_in[1]. For example, input the data 110100 (padded with 3 zeros as 110100000) and verify that the output uo_out[2:0] matches the expected CRC (e.g., 101 for this sequence). Toggle ui_in[0] to test power-saving behavior by observing clock activity. Use a waveform viewer (e.g., GTKWave) to confirm the CRC computation and clock gating functionality after each clock cycle.

Below is a sample simulation waveform showing CRC computation and clock gating:

<img width="1814" height="425" alt="WaveformCRC" src="https://github.com/user-attachments/assets/784cad7d-13d3-4976-b8ed-648e7bc8b234" />


## External hardware

List external hardware used in your project (e.g. PMOD, LED display, etc), if any

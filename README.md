![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) ![](../../workflows/fpga/badge.svg)

# CRC-3 Module with Latch-Based Clock Gating

Overview

This project implements a CRC-3 (Cyclic Redundancy Check) module optimized with Latch-Based Clock Gating for low-power operation. It is designed for integration into a 1×1 Tiny Tapeout tile chip.

The system computes a 3-bit CRC using a Linear Feedback Shift Register (LFSR) based on the polynomial:

P(x) = x^3 + x + 1 \quad (binary\ 1011)

The latch-based clock gating technique reduces power by disabling the clock when not needed, while preventing glitches with a transparent latch.


---

Features

Error detection using CRC-3 polynomial (1011)

Serial data input (ui_in[1]) processed bit-by-bit per clock cycle

Latch-based clock gating controlled by ui_in[0] (enable signal)

Low-power design by stopping clock activity when not enabled

Compact implementation for Tiny Tapeout tile constraints



---

Block Diagram


![17572599072393043403612168572490](https://github.com/user-attachments/assets/5d237886-0e05-495c-8e1a-3583079dd057)


---

I/O Description

| Signal        | Direction | Description                                |
| ------------- | --------- | ------------------------------------------ |
| `clk`         | Input     | System clock                               |
| `rst_n`       | Input     | Active-low reset                           |
| `ui_in[0]`    | Input     | Enable signal for latch-based clock gating |
| `ui_in[1]`    | Input     | Serial data input                          |
| `uo_out[2:0]` | Output    | 3-bit CRC value                            |




---

How It Works

1. When ui_in[0] = 1, the gated clock is enabled and data bits from ui_in[1] are shifted into the LFSR.


2. The CRC-3 calculation follows the polynomial (x^3 + x + 1).


3. When ui_in[0] = 0, the gated clock is disabled, freezing internal logic to save power.


4. The final 3-bit CRC result is available at uo_out[2:0].




---

How to Test

1. Reset the module by setting rst_n = 0, then release (rst_n = 1).


2. Enable clock gating by driving ui_in[0] = 1.


3. Feed serial data through ui_in[1].

Example: input sequence 110100 (pad with 3 zeros → 110100000)

Expected CRC output = 101



4. Disable clock gating (ui_in[0] = 0) and observe that the internal clock stops toggling.


5. Check results using a simulation tool (e.g., Icarus Verilog + GTKWave).




---

Sample Simulation Waveform

<img width="1814" height="425" alt="17572599598632259848741214954965" src="https://github.com/user-attachments/assets/a5511f60-9539-49d0-b847-ce9dfe3c1bd8" />


The waveform shows:

Proper CRC computation (uo_out[2:0] = 101 for example sequence)

Clock gating effect when ui_in[0] is toggled



---

File Structure

src/          → Verilog source (CRC module + latch gating)  
test/         → Testbench and simulation files  
docs/         → Documentation (block diagram, waveform, info.md)  
info.yaml     → Metadata (top module, sources, etc.)  
README.md     → This documentation


---

References

Tiny Tapeout Documentation

Digital Design and LFSR theory for CRC computation



---

Credits & Acknowledgments

Prof. Dr. JayaGowri – Guidance and Mentorship

BMS College of Engineering – Institutional support

IEEE EDS – Knowledge sharing and community support

Tiny Tapeout Team – Providing the platform for open-source chip design



---

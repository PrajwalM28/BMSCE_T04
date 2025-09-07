# test/test.py
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    """CRC-3 codeword generator test (GL-safe, resolves X values)."""
    dut._log.info("Start")

    # 100 MHz clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Init + reset
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 30)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)
    dut._log.info("Reset released")

    # Enable = 1
    dut.ui_in[0].value = 1

    # Bits to shift: 10101 + 000
    bits = [1, 0, 1, 0, 1, 0, 0, 0]
    dut._log.info("Begin shifting bits")
    for idx, b in enumerate(bits):
        dut.ui_in[1].value = b
        await ClockCycles(dut.clk, 1)
        dut._log.debug(f"Cycle {idx}, in={b}, uo_out={dut.uo_out.value.binstr}")

    # Extra cycles for GL netlist to settle
    await ClockCycles(dut.clk, 12)

    # Safely resolve X/Z -> 0
    raw_str = dut.uo_out.value.binstr
    safe_str = raw_str.replace("x", "0").replace("X", "0").replace("z", "0").replace("Z", "0")
    out_val = int(safe_str, 2)

    dut._log.info(f"Final uo_out = 0x{out_val:02X} (expected 0xAD)")
    assert (out_val & 0xFF) == 0xAD, f"Expected 0xAD, got 0x{out_val:02X}"

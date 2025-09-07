# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # 100 MHz clock (10 ns period)
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 5)
    dut.rst_n.value = 1

    dut._log.info("Begin shifting bits")

    # Enable = 1
    dut.ui_in[0].value = 1

    # Send message bits: 10101 (MSB-first) + 000 padding
    bits = [1, 0, 1, 0, 1, 0, 0, 0]
    for b in bits:
        dut.ui_in[1].value = b
        await ClockCycles(dut.clk, 1)

    # One more cycle for DUT to latch output
    await ClockCycles(dut.clk, 1)

    # Log and check result
    out_val = int(dut.uo_out.value)
    dut._log.info(f"uo_out = 0x{out_val:02X} (expected 0xAD)")
    assert out_val == 0xAD, f"Expected 0xAD, got 0x{out_val:02X}"

    # Disable
    dut.ui_in[0].value = 0
    await ClockCycles(dut.clk, 1)

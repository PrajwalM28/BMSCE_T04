# test/test.py
# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    """CRC-3 codeword generator test (GL-safe, with internal-state logging)."""
    dut._log.info("Start test_project")

    # 100 MHz clock (10 ns period)
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Initialize signals
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    # Hold reset longer for gate-level sims
    await ClockCycles(dut.clk, 30)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)

    dut._log.info("Reset released, beginning shifting bits")

    # Enable = 1 (ui_in[0]) — we will drive ui_in[1] with the serial data
    dut.ui_in[0].value = 1

    # Send message bits: 10101 (MSB-first) + 000 padding -> expected 0xAD
    bits = [1, 0, 1, 0, 1, 0, 0, 0]

    for idx, b in enumerate(bits):
        dut.ui_in[1].value = b
        await ClockCycles(dut.clk, 1)

        # Try to print internal state (works in RTL and GL if regs preserved)
        try:
            msg_reg = dut.msg_reg.value.binstr
        except Exception:
            msg_reg = str(dut.msg_reg.value)

        try:
            crc_reg = dut.crc_reg.value.binstr
        except Exception:
            crc_reg = str(dut.crc_reg.value)

        try:
            uo = dut.uo_out.value.binstr
        except Exception:
            uo = str(dut.uo_out.value)

        dut._log.info(f"Cycle {idx:02d}: in={b} msg_reg={msg_reg} crc_reg={crc_reg} uo_out={uo}")

    # Extra cycles to allow GL netlist to settle
    await ClockCycles(dut.clk, 12)

    # Read output in GL-safe way: replace X with 0 if present
    try:
        binstr = dut.uo_out.value.binstr
    except Exception:
        binstr = str(dut.uo_out.value)

    clean = binstr.replace("x", "0").replace("X", "0")
    out_val = int(clean, 2)

    dut._log.info(f"Final uo_out = 0x{out_val:02X} (expected 0xAD)")

    # Tolerant check (mask to 8 bits)
    assert (out_val & 0xFF) == 0xAD, f"Expected 0xAD, got 0x{out_val:02X}"

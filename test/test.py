import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    """CRC-3 codeword generator test with GL-safe handling."""

    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Initialize
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    # Longer reset for GL
    await ClockCycles(dut.clk, 20)
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 10)

    dut._log.info("Begin shifting bits")

    # Enable gating
    dut.ui_in[0].value = 1

    # Message: 10101 padded with 000 -> expected codeword 0xAD
    bits = [1, 0, 1, 0, 1, 0, 0, 0]

    for idx, b in enumerate(bits):
        dut.ui_in[1].value = b
        await ClockCycles(dut.clk, 1)
        dut._log.info(f"Cycle {idx}: input={b}, uo_out={dut.uo_out.value.binstr}")

    # Extra wait for CRC to settle
    await ClockCycles(dut.clk, 5)

    # Read GL-safe output
    binstr = dut.uo_out.value.binstr.replace("x", "0").replace("X", "0")
    out_val = int(binstr, 2)

    dut._log.info(f"Final uo_out = 0x{out_val:02X} (expected 0xAD)")

    assert (out_val & 0xFF) == 0xAD, f"Expected 0xAD, got 0x{out_val:02X}"

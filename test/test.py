import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ClockCycles

@cocotb.test()
async def crc_test(dut):
    """Test CRC module in TinyTapeout"""

    # Start clock
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Apply reset (longer for GL sim)
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)   # hold reset longer
    dut.rst_n.value = 1
    await ClockCycles(dut.clk, 5)    # wait extra cycles after release

    # Send 3-bit message (e.g., 0b101)
    msg = [1, 0, 1]
    dut._log.info("Sending message bits: %s", msg)
    for bit in msg:
        dut.ui_in.value = bit
        await RisingEdge(dut.clk)

    # Give time for CRC calculation
    await ClockCycles(dut.clk, 5)

    # Read output
    out_val = int(dut.uo_out.value)
    dut._log.info(f"uo_out = 0x{out_val:02X} (expected 0xAD)")

    # GL-safe check: mask unknowns if any
    assert (out_val & 0xFF) == 0xAD, f"Expected 0xAD, got 0x{out_val:02X}"

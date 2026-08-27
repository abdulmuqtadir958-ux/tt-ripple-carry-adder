import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_ripple_carry_adder(dut):
    dut._log.info("Start Ripple Carry Adder Test")

    dut.ena.value = 1
    dut.clk.value = 0
    dut.rst_n.value = 1
    dut.uio_in.value = 0

    test_cases = [
        (0, 0, 0, 0, 0),
        (5, 3, 0, 0, 8),   
        (15, 1, 0, 1, 0),   
        (7, 7, 1, 0, 15),   
        (15, 15, 1, 1, 15),
    ]

    for a, b, cin, exp_cout, exp_sum in test_cases:
        dut.ui_in.value = (b << 4) | a
        dut.uio_in.value = cin
        await Timer(10, units="ns")

        actual_sum = int(dut.uo_out.value) & 0xF
        actual_cout = (int(dut.uo_out.value) >> 4) & 0x1

        assert actual_sum == exp_sum, f"Failed A={a}, B={b}, Cin={cin} -> Sum: expected {exp_sum}, got {actual_sum}"
        assert actual_cout == exp_cout, f"Failed A={a}, B={b}, Cin={cin} -> Cout: expected {exp_cout}, got {actual_cout}"

    dut._log.info("All tests passed successfully!")

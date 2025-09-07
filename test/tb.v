`timescale 1ns/1ps
`default_nettype none

module tb_crc3;
    reg clk;
    reg rst_n;
    reg [7:0] ui_in;
    wire [7:0] uo_out;

    // DUT
    tt_um_crc3 dut (
        .ui_in(ui_in),
        .uo_out(uo_out),
        .uio_in(8'b0),
        .uio_out(),
        .uio_oe(),
        .ena(1'b1),
        .clk(clk),
        .rst_n(rst_n)
    );

    // 100 MHz
    initial clk = 1'b0;
    always #5 clk = ~clk;

    initial begin
        $dumpfile("tb.vcd");
        $dumpvars(0, tb_crc3);

        // Reset
        rst_n = 0; ui_in = 8'b0;
        repeat (5) @(posedge clk);
        rst_n = 1;

        // Enable shifting
        ui_in[0] = 1'b1;

        // Send message 10101 (MSB-first) then 3 padding zeros
        // Drive ui_in[1] just before posedge so DUT samples at posedge
        ui_in[1] = 1; @(posedge clk);
        ui_in[1] = 0; @(posedge clk);
        ui_in[1] = 1; @(posedge clk);
        ui_in[1] = 0; @(posedge clk);
        ui_in[1] = 1; @(posedge clk);
        ui_in[1] = 0; @(posedge clk); // padding
        ui_in[1] = 0; @(posedge clk); // padding
        ui_in[1] = 0; @(posedge clk); // padding

        // One more cycle to see the registered output
        @(posedge clk);

        // Disable
        ui_in[0] = 1'b0; @(posedge clk);

        $display("uo_out = 0x%02h (expected 0xAD)", uo_out);
        $finish;
    end
endmodule

`default_nettype wire

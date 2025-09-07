/* 
 * Copyright (c) 2024 BMSCE04
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_crc3 (
    input  wire [7:0] ui_in,    // ui_in[0]=enable, ui_in[1]=serial bit
    output wire [7:0] uo_out,   // 8-bit {msg[4:0], crc[2:0]} after 8 cycles; otherwise 0
    input  wire [7:0] uio_in,   // unused
    output wire [7:0] uio_out,  // unused
    output wire [7:0] uio_oe,   // unused
    input  wire       ena,      // platform enable
    input  wire       clk,      // clock (do NOT gate)
    input  wire       rst_n     // active-low reset
);

    // Active-high reset
    wire reset   = ~rst_n;

    // Inputs
    wire enable  = ui_in[0];
    wire data_in = ui_in[1];

    // Internal state
    reg  [4:0] msg_reg;    // shifts in 5 data bits (MSB-first)
    reg  [2:0] crc_reg;    // CRC-3 (poly x^3 + x + 1)
    reg  [3:0] bit_count;  // 0..8
    reg  [7:0] out_reg;    // registered output

    // Combinational next-state signals (no regs declared inside always)
    wire       shift_in = (bit_count < 4'd5) ? data_in : 1'b0;
    wire [4:0] msg_next_w = (bit_count < 4'd5) ? {msg_reg[3:0], data_in} : msg_reg;
    wire [2:0] crc_next_w = { (shift_in ^ crc_reg[2] ^ crc_reg[0]), crc_reg[2:1] };

    // Tie off IOs
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Lint-friendly consumption of unused inputs
    wire _unused_inputs;
    assign _unused_inputs = &{1'b0, ui_in[7:2], uio_in, 1'b0};

    // Drive outputs
    assign uo_out = out_reg;

    // Synchronous design, no gated clocks, no latches
    always @(posedge clk or posedge reset) begin
        if (reset) begin
            msg_reg   <= 5'b0;
            crc_reg   <= 3'b0;
            bit_count <= 4'd0;
            out_reg   <= 8'b0;
        end else if (ena) begin
            if (enable) begin
                // update shift registers
                msg_reg <= msg_next_w;
                crc_reg <= crc_next_w;

                // update bit counter (saturate at 8)
                if (bit_count < 4'd8)
                    bit_count <= bit_count + 1'b1;
                else
                    bit_count <= bit_count;

                // drive output after the 8th bit has been processed
                // When bit_count == 7 this will capture the new (msg_next_w, crc_next_w)
                if (bit_count >= 4'd7)
                    out_reg <= {msg_next_w, crc_next_w};
                else
                    out_reg <= 8'b0;
            end else begin
                // enable == 0 : hold state (no reset)
                msg_reg   <= msg_reg;
                crc_reg   <= crc_reg;
                bit_count <= bit_count;
                out_reg   <= out_reg;
            end
        end
        // if ena == 0 : do nothing (hold current state)
    end

endmodule

`default_nettype wire

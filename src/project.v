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

    // Tie off IOs
    assign uio_out = 8'b0;
    assign uio_oe  = 8'b0;

    // Lint-friendly consumption of unused inputs
    wire _unused_inputs;
    assign _unused_inputs = &{1'b0, ui_in[7:2], uio_in, 1'b0};

    // Drive outputs
    assign uo_out = out_reg;

    // Next-bit logic (outside always block)
    wire next_bit = (bit_count < 4'd5) ? data_in : 1'b0;

    // Synchronous design, no gated clocks, no latches
   always @(posedge clk or posedge reset) begin
    if (reset) begin
        msg_reg   <= 5'b0;
        crc_reg   <= 3'b0;
        bit_count <= 4'd0;
        out_reg   <= 8'b0;
    end else if (ena) begin
        if (enable) begin
            reg [4:0] msg_next;
            reg [2:0] crc_next;

            msg_next = (bit_count < 4'd5) ? {msg_reg[3:0], data_in} : msg_reg;
            crc_next = { next_bit ^ crc_reg[2] ^ crc_reg[0], crc_reg[2:1] };

            if (bit_count < 4'd8) begin
                msg_reg   <= msg_next;
                crc_reg   <= crc_next;
                bit_count <= bit_count + 1'b1;

                if (bit_count == 4'd7)
                    out_reg <= {msg_next, crc_next};
                else
                    out_reg <= 8'b0;
            end else begin
                // hold result while enable remains high
                out_reg <= {msg_reg, crc_reg};
            end
        end
        // if enable=0 → hold state, don’t reset
    end
end

endmodule

`default_nettype wire

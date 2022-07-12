#
# This file is part of LiteX-Boards.
#
# Copyright (c) 2019 Michael Betz <michibetz@gmail.com>
# Copyright (c) 2020 Fei Gao <feig@princeton.edu>
# Copyright (c) 2020 Florent Kermarrec <florent@enjoy-digital.fr>
# Copyright (c) 2022 Verneri Hirvonen <verneri.hirvonen@aalto.fi>
# SPDX-License-Identifier: BSD-2-Clause

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform, VivadoProgrammer

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("sysclk", 0, # 200MHz system clock
        Subsignal("p", Pins("H9"), IOStandard("LVDS")),
        Subsignal("n", Pins("G9"), IOStandard("LVDS")),
    ),
    ("usrclk", 0,
        Subsignal("p", Pins("AF14"), IOStandard("LVDS_25")),
        Subsignal("n", Pins("AG14"), IOStandard("LVDS_25")),
    ),
    ("user_sma_clock", 0,
        Subsignal("p", Pins("AD18"), IOStandard("LVDS_25")),
        Subsignal("n", Pins("AD19"), IOStandard("LVDS_25")),
    ),
    ("rec_clock_c", 0,
        Subsignal("p", Pins("AD20"), IOStandard("LVDS_25")),
        Subsignal("n", Pins("AE20"), IOStandard("LVDS_25")),
    ),
    ("si5324_int_alm_ls", 0, Pins("AJ25"), IOStandard("LVCMOS25")),
    ("si5324_rst_ls",     0, Pins("W23"),  IOStandard("LVCMOS25")),
    ("pl_cpu_reset", 0, Pins("A8"), IOStandard("LVCMOS15")),

    # Leds
    ("user_led", 0, Pins("A17"), IOStandard("LVCMOS15")), # GPIO_LED_0
    ("user_led", 1, Pins("W21"), IOStandard("LVCMOS25")), # GPIO_LED_RIGHT
    ("user_led", 2, Pins("G2"),  IOStandard("LVCMOS15")), # GPIO_LED_CENTER
    ("user_led", 3, Pins("Y21"), IOStandard("LVCMOS25")), # GPIO_LED_LEFT
    # user guide says that all of these are LVCMOS25
    #("user_led", 0, Pins("A17"), IOStandard("LVCMOS25")), # GPIO_LED_0
    #("user_led", 1, Pins("W21"), IOStandard("LVCMOS25")), # GPIO_LED_RIGHT
    #("user_led", 2, Pins("G2"),  IOStandard("LVCMOS25")), # GPIO_LED_CENTER
    #("user_led", 3, Pins("Y21"), IOStandard("LVCMOS25")), # GPIO_LED_LEFT

    # Buttons
    ("user_btn", 0, Pins("AK25"), IOStandard("LVCMOS25")), # GPIO_SW_LEFT
    ("user_btn", 1, Pins("K15"),  IOStandard("LVCMOS15")), # GPIO_SW_CENTER
    ("user_btn", 2, Pins("R27"),  IOStandard("LVCMOS25")), # GPIO_SW_RIGHT

    # Switches
    ("user_dip", 0, Pins("AB17"), IOStandard("LVCMOS25")), # GPIO_DIP_SW0
    ("user_dip", 1, Pins("AC16"), IOStandard("LVCMOS25")), # GPIO_DIP_SW1
    ("user_dip", 2, Pins("AC17"), IOStandard("LVCMOS25")), # GPIO_DIP_SW2
    ("user_dip", 3, Pins("AJ13"), IOStandard("LVCMOS25")), # GPIO_DIP_SW3

    # I2C
    ("i2c", 0,
        Subsignal("sda", Pins("AJ18")), # IIC_SDA_MAIN_LS
        Subsignal("scl", Pins("AJ14")), # IIC_SCL_MAIN_LS
        IOStandard("LVCMOS25")
    ),

    # DDR3 SDRAM (SODIMM)
    ("ddram", 0,
        Subsignal("a",       Pins(
            "E10 B9  E11 A9  D11 B6  F9  E8",
            "B10 J8  D6  B7  H12 A10 G11 C6"),
            IOStandard("SSTL15")),
        Subsignal("ba",      Pins("F8 H7 A7"), IOStandard("SSTL15")),
        Subsignal("ras_n",   Pins("H11"), IOStandard("SSTL15")),
        Subsignal("cas_n",   Pins("E7"), IOStandard("SSTL15")),
        Subsignal("we_n",    Pins("F7"), IOStandard("SSTL15")),
        Subsignal("cs_n",    Pins("J11"), IOStandard("SSTL15")),
        Subsignal("dm",      Pins("J3 F2 E1 C2"), IOStandard("SSTL15")),
        Subsignal("dq",      Pins(
            "L1 L2 K5 J4 K1 L3 J5 K6",
            "G6 H4 H6 H3 G1 H2 G5 G4",
            "E2 E3 D4 E5 F4 F3 D1 D3",
            "A2 B2 B4 B5 A3 B1 C1 C4"),
            IOStandard("SSTL15_T_DCI")), # Is the _T_DCI suffix required?
        Subsignal("dqs_p",   Pins("K3 J1 E6 A5"), IOStandard("DIFF_SSTL15")),
        Subsignal("dqs_n",   Pins("K2 H1 D5 A4"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_p",   Pins("G10"), IOStandard("DIFF_SSTL15")),
        Subsignal("clk_n",   Pins("F10"), IOStandard("DIFF_SSTL15")),
        Subsignal("cke",     Pins("D10"), IOStandard("SSTL15")),
        Subsignal("odt",     Pins("G7"), IOStandard("SSTL15")),
        Subsignal("reset_n", Pins("G17"), IOStandard("LVCMOS15")),
        Misc("SLEW=FAST"),
        Misc("VCCAUX_IO=HIGH"),
    ),
]



# Platform -----------------------------------------------------------------------------------------

class Platform(XilinxPlatform):
    default_clk_name   = "sysclk"
    default_clk_period = 1e9/200e6

    def __init__(self, toolchain="vivado"):
        XilinxPlatform.__init__(self, "xc7z045ffg900-2", _io, toolchain=toolchain)

    def create_programmer(self):
        return VivadoProgrammer()

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment)
        self.add_period_constraint(self.lookup_request("sysclk", loose=True), 1e9/200e6)
##################################################################################################################################
        #self.add_platform_command("set_property INTERNAL_VREF 0.84 [get_iobanks 64]")
        #self.add_platform_command("set_property INTERNAL_VREF 0.84 [get_iobanks 65]")
        #self.add_platform_command("set_property INTERNAL_VREF 0.84 [get_iobanks 66]")

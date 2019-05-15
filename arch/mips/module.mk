#
#  Openwrt Tools specification
#

TOOLS           = mipsel-openwrt-linux
PROCESSOR       = mipsel
OPENWRT_MIPSEL_CC_TOOLS = source
STAGING_DIR = /home/adam/Dokumenty/source/staging_dir
#BB_ARM_CC_DEPS  = bbArmCc-deps

#
# Paths
#m

TOOLS_ROOT      ?= $(STAGING_DIR)/toolchain-mipsel_24kc_gcc-7.3.0_musl
TOOLS_PATH	    ?= $(TOOLS_ROOT)/bin
TOOLS_LIB_PATH  ?= $(TOOLS_ROOT)/lib
TOOLS_INC       ?= $(TOOLS_ROOT)/include
#DEPS_PATH      ?= /usr/local/$(BB_ARM_CC_DEPS)

#ifeq (,$(wildcard $(TOOLS_PATH)))
#      $(info Beaglebone ARM cross compiler tools not found in $(TOOLS_PATH)/ directory)
#      $(info Download bbArmCc-tools.zip from ThingMagic website or Download gcc-linaro cross compiler toolchain)
#      $(info Unzip & copy to /usr/local/ directory as "bbArmCc-tools" in your linux-PC)
#endif

#ifeq (,$(wildcard $(DEPS_PATH)))
#      $(info Beaglebone ARM cross compiler dependecies not found in $(DEPS_PATH)/ directory)
#      $(info Download bbArmCc-deps.zip from ThingMagic website, unzip & copy /usr/local/ as "bbArmCc-deps" in your linux-PC)
#endif

#
# Tools 
#
CC	= $(TOOLS_PATH)/mipsel-openwrt-linux-gcc
C++     = $(TOOLS_PATH)/mipsel-openwrt-linux-g++
CiPP	= $(TOOLS_PATH)/mipsel-openwrt-linux-g++
OBJDUMP = $(TOOLS_PATH)/mipsel-openwrt-linux-objdump
ASM	= $(TOOLS_PATH)/mipsel-openwrt-linux-gcc
AR	= $(TOOLS_PATH)/mipsel-openwrt-linux-ar
LD      = $(TOOLS_PATH)/mipsel-openwrt-linux-ld

ifeq ($(BUILD), Debug)
STRIP ?= ls
else
STRIP = $(TOOLS_PATH)/mipsel-openwrt-linux-strip
endif

CFLAGS  += -DPC
#CFLAGS  += -I $(DEPS_PATH)/include

ETH_NAME ?= eth0

ifeq ($(BUILD), Debug)
CFLAGS          += -g
CDEFINES        += -DDEBUG
endif



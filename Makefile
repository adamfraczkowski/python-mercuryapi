APIZIP ?= mercuryapi-1.31.2.zip
APIVER ?= 1.31.2.40
PYTHON ?= $(shell { command -v python3 || command -v python; } 2>/dev/null)
STAGING_DIR ?= /home/adam/Dokumenty/source/staging_dir


TOOLS_ROOT      ?= $(STAGING_DIR)/toolchain-mipsel_24kc_gcc-7.3.0_musl
TOOLS_PATH	    ?= $(TOOLS_ROOT)/bin

MIPS_CC			?= $(TOOLS_PATH)/mipsel-openwrt-gcc
MIPS_CFLAGS		?= $(TOOLS_ROOT)/include

.PHONY: all mercuryapi install

all: mercuryapi	
ifeq ($(PLATFORM),MIPS)    
	CC=$(MIPS_CC)
	CFLAGS=$(MIPS_CFLAGS)
	export CC=$(CC)
	export CFLAGS=$(CFLAGS)
	$(PYTHON) setup.py build
else ifeq ($(PLATFORM),HOST)
	export CC=gcc
else     
	$(PYTHON) setup.py build
endif

install: mercuryapi
	$(PYTHON) setup.py install

mercuryapi: mercuryapi-$(APIVER)/.done
ifeq ($(PLATFORM),MIPS)	
	STAGING_DIR=$(STAGING_DIR) PLATFORM=MIPS SKIP_SAMPLES=TRUE make -C mercuryapi-$(APIVER)/c/src/api
else ifeq ($(PLATFORM),HOST)
	SKIP_SAMPLES=TRUE make -C mercuryapi-$(APIVER)/c/src/api
else
	make -C mercuryapi-$(APIVER)/c/src/api    
endif
	mkdir -p build/mercuryapi/include
	find mercuryapi-*/c/src/api -type f -name '*.h' ! -name '*_imp.h' | grep -v 'ltkc_win32' | xargs cp -t build/mercuryapi/include
	mkdir -p build/mercuryapi/lib
	find mercuryapi-*/c/src/api -type f -name '*.a' -or -name '*.so.1' | xargs cp -t build/mercuryapi/lib

mercuryapi-$(APIVER)/.done: $(APIZIP)
	unzip $(APIZIP)
	mkdir -p mercuryapi-$(APIVER)/c/src/arch/MIPS/openwrt
	cp arch/mips/module.mk mercuryapi-$(APIVER)/c/src/arch/MIPS/openwrt/
	patch -p0 -d mercuryapi-$(APIVER) < mercuryapi.patch
	touch mercuryapi-$(APIVER)/.done

$(APIZIP):
	wget https://www.jadaktech.com/wp-content/uploads/2018/11/$(APIZIP)

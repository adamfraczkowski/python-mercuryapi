APIZIP ?= mercuryapi-1.31.2.zip
APIVER ?= 1.31.2.40
PYTHON ?= $(shell { command -v python3 || command -v python; } 2>/dev/null)
STAGING_DIR ?= /home/adam/Dokumenty/source/staging_dir


.PHONY: all mercuryapi install

all: mercuryapi	
    ifeq ($(PLATFORM),MIPS)
    $(PYTHON) -c "import setuptools; execfile('setup-mips.py')" -x build
    else     
    $(PYTHON) setup.py build
    endif

install: mercuryapi
	$(PYTHON) setup.py install

mercuryapi: mercuryapi-$(APIVER)/.done
    ifeq ($(PLATFORM),MIPS)	
    STAGING_DIR=$(STAGING_DIR) PLATFORM=MIPS make -C mercuryapi-$(APIVER)/c/src/api
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

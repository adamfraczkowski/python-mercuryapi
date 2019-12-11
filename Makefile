APIZIP ?= mercuryapi-1.31.1.36-2.zip
APIVER ?= 1.31.1.36
PYTHON ?= $(shell { command -v python3 || command -v python; } 2>/dev/null)

# If you want to build to other architecture
ARCH ?=MIPS


.PHONY: all mercuryapi install

all: mercuryapi
	ifeq ($(ARCH),MIPS)
		$(PYTHON) setup.py build mips
	else
		$(PYTHON) setup.py build
	endif

install: mercuryapi
	#Instead of installing, build wheel package
	ifeq ($(ARCH),MIPS)
		$(PYTHON) setup.py bdist_wheel
	else
		$(PYTHON) setup.py install
	endif

mercuryapi: mercuryapi-$(APIVER)/.done
	ifeq ($(ARCH),MIPS)
		sh make_mercury_mips.sh $(APIVER)
	else
		make -C mercuryapi-$(APIVER)/c/src/api
	endif
	mkdir -p build/mercuryapi/include
	find mercuryapi-*/c/src/api -type f -name '*.h' ! -name '*_imp.h' ! -path '*ltkc_win32*' -exec cp {} build/mercuryapi/include/ \;

	mkdir -p build/mercuryapi/lib
	find mercuryapi-*/c/src/api -type f \( -name '*.a' -or -name '*.so.1' \) -exec cp {} build/mercuryapi/lib/ \;

mercuryapi-$(APIVER)/.done: $(APIZIP)
	unzip $(APIZIP)
	patch -p0 -d mercuryapi-$(APIVER) < mercuryapi.patch
	ifeq ($(ARCH),MIPS)
		patch -p0 -d mercuryapi-$(APIVER) < mercuryapi_mips.patch
	endif
	touch mercuryapi-$(APIVER)/.done

$(APIZIP):
	curl https://www.jadaktech.com/wp-content/uploads/2019/10/$(APIZIP) -o $(APIZIP)
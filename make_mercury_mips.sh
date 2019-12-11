APIVER = $1

export STAGING_DIR="/source/staging_dir"
export TOOLCHAIN_DIR="$STAGING_DIR/toolchain-mipsel_24kc_gcc-7.3.0_musl"
export CC="$TOOLCHAIN_DIR/bin/mipsel-openwrt-linux-gcc"
export STRIP="$TOOLCHAIN_DIR/bin/mipsel-openwrt-linux-strip"
export LDSHARED="$TOOLCHAIN_DIR/bin/mipsel-openwrt-linux-gcc -shared"
export TMR_ENABLE_SERIAL_READER_ONLY=1
make -C mercuryapi-$(APIVER)/c/src/api
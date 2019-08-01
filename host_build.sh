#REPLACE MAKEFILE_mercury in mercuryapi/c/src/api 
TMR_ENABLE_SERIAL_READER_ONLY=1 SKIP_SAMPLES=TRUE PLATFORM=HOST python3 setup.py bdist_wheel
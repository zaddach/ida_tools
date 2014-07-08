ida_tools
=========

Tools for IDA Pro
- qt_resource_extractor.py - A script that can extract QT resources from a binary. Currently works only for the LIFX lamp 1.3 firmware update, as offsets are hardcoded.
  Do ```exec(open('qt_resource_extractor.py').read()); dump_all_resources('/tmp/resources')``` to dump all resources from the current idb database into __/tmp/resources__.

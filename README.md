ida_tools
=========

Tools for IDA Pro
- qt_resource_extractor.py - A script that can extract QT resources from a binary. Currently works only for the LIFX lamp [1.3 MacOs firmware update](http://updates.lifx.co/1_3/20140627/LIFX%20Bulb%20Update%201.3.dmg), as offsets are hardcoded.
Load the executable (LIFX Bulb Update 1.3.app/Contents/MacOS/LIFX Bulb Update 1.3) into IDA Pro and then do ```exec(open('qt_resource_extractor.py').read()); dump_all_resources('/tmp/resources')``` to dump all resources from the current idb database into __/tmp/resources__.

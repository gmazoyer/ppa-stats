PPA Statistics
==============

Show statistics for a given PPA.

Requirements
------------

  * launchpadlib --> https://help.launchpad.net/API/launchpadlib
  * texttable    --> https://pypi.python.org/pypi/texttable/ (optional)

What is it?
-----------

This code is based on the one made by Sam Hewitt.

http://snwh.org/blog/2013-08-15-for-the-obsessive-data-hog-logging-your-launchpad-ppa

It was modified to:

  * Use the standard output of the shell instead of logging everything in a
    file.
  * Be more flexible when adding Ubuntu versions and architectures.
  * Use beautiful ASCII art tables.
  * Be more easy to maintain.
  * Anything more?

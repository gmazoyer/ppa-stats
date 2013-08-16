#!/usr/bin/python
#
# Authors:
#   Sam Hewitt <hewittsamuel@gmail.com>
#   Guillaume Mazoyer <gmazoyer@gravitons.in>
#

import sys, os
import time, datetime
from texttable import Texttable
from launchpadlib.launchpad import Launchpad

# For reference: "ppa:ownername/archivename" or
# "https://launchpad.net/~ownername/+archive/archive-name"

# Name of the owner of the ppa you would like the stats for.
PPAOWNER = 'java-gnome'
# Name of the PPA you would like the stats for.
PPANAME = 'ppa'
# System CPU architecture you would like the stats for.
ARCHS = [ 'i386', 'amd64' ]
# Versions of Ubuntu to check.
VERSIONS = [ 'precise', 'quantal', 'raring' ]

# Login into Launchpad Anoymously
lp_login = Launchpad.login_anonymously('ppastats', 'edge',
    "~/.launchpadlib/cache/", version='devel')
# PPA owner
owner = lp_login.people[PPAOWNER]
# PPA name
archive = owner.getPPAByName(name=PPANAME)

# Base URL to Launchpad API
base_url = 'https://api.launchpad.net/devel/ubuntu/'

# Print heading
print 'Download stats for ' + PPAOWNER + ' PPA'  
print '----------------------------------------------'

# For each version
for version in VERSIONS:
    print ''
    print 'Packages for ' + version

    result = [ [ 'Package', 'Version', 'Arch', 'Count' ] ]

    # For each architecture
    for arch in ARCHS:
        url_to_check = base_url + version + '/' + arch

        for individual_archive in archive.getPublishedBinaries(
            status='Published',distro_arch_series=url_to_check):
            # Get download count
            count = individual_archive.getDownloadCount()

            result.append(
                [
                    individual_archive.binary_package_name,
                    individual_archive.binary_package_version,
                    arch,
                    str(individual_archive.getDownloadCount())
                ]
            )

    # Show the result in a beautiful table
    table = Texttable()
    table.set_cols_dtype([ 't', 't', 't', 'i' ])
    table.set_cols_align([ 'l', 'r', 'r', 'r' ])
    table.add_rows(result)
    print table.draw()

#!/usr/bin/python
#
# Authors:
#   Sam Hewitt <hewittsamuel@gmail.com>
#   Guillaume Mazoyer <gmazoyer@gravitons.in>
#

import getopt
import sys
from launchpadlib.launchpad import Launchpad

# Define if we can use ASCII art tables
use_table = True
try:
    from texttable import Texttable
except:
    use_table = False

# For reference: "ppa:ownername/archivename" or
# "https://launchpad.net/~ownername/+archive/archive-name"

# System CPU architecture you would like the stats for.
ARCHS = ['i386', 'amd64']
# Versions of Ubuntu to check.
VERSIONS = ['precise', 'quantal', 'raring']


def process_ppa_stats(ppa_owner, ppa_name):
    # Login into Launchpad Anoymously
    lp_login = Launchpad.login_anonymously('ppastats', 'edge',
                                           "~/.launchpadlib/cache/",
                                           version='devel')
    # PPA owner
    owner = lp_login.people[ppa_owner]
    # PPA name
    archive = owner.getPPAByName(name=ppa_name)

    # Base URL to Launchpad API
    base_url = 'https://api.launchpad.net/devel/ubuntu/{}/{}'

    # Print heading
    header = 'Download stats for ' + ppa_owner + ' PPA'
    print header
    print '-' * len(header)

    # For each version
    for version in VERSIONS:
        print ''
        print 'Packages for ' + version

        result = [['Package', 'Version', 'Arch', 'Count']]

        # For each architecture
        for arch in ARCHS:
            url_to_check = base_url.format(version, arch)

            for individual_archive in archive.getPublishedBinaries(
                    status='Published', distro_arch_series=url_to_check):

                result.append(
                    [
                        individual_archive.binary_package_name,
                        individual_archive.binary_package_version,
                        arch,
                        str(individual_archive.getDownloadCount())
                    ]
                )

        if not use_table:
            # Simple terminal output
            for value in result:
                print value[0] + "\t" + value[1] + "\t" + value[2] + "\t" + \
                    value[3]
        else:
            # Show the result in a beautiful table
            table = Texttable()

            table.set_cols_dtype(['t', 't', 't', 'i'])
            table.set_cols_align(['l', 'r', 'r', 'r'])
            table.add_rows(result)

            print table.draw()


def usage():
    print "Usage: " + sys.argv[0] + " [OPTION]..."
    print ""
    print "  -h, --help \t display this help message"
    print "  -p, --ppa  \t specify the PPA to use with the following"
    print "             \t   format ppa:owner/name"
    print ""
    print "Exit status:"
    print " 0  if OK,"
    print " 1  if minor problems (e.g., cannot access PPA),"
    print " 2  if serious trouble (e.g., cannot access command-line argument)."
    print ""
    print "Report ppa-stats bugs to:"
    print "    <https://github.com/respawner/ppa-stats/issues>"
    print "ppa-stats home page: <https://github.com/respawner/ppa-stats>"


def main(argv):
    ppa_owner = "java-gnome"
    ppa_name = "ppa"

    try:
        # Parse the arguments given via the CLI
        opts, args = getopt.getopt(argv, "hp:", ["help", "ppa="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    # Handle arguments
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--ppa"):
            split = arg.split("/")
            ppa_owner = split[0].split(":")[1]
            ppa_name = split[1]

    # Process the stats
    process_ppa_stats(ppa_owner, ppa_name)

if __name__ == "__main__":
    main(sys.argv[1:])

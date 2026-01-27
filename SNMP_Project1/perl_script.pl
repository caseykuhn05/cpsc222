#!/usr/bin/perl
use strict;
use warnings;

# check auth logs for sudo sessions
my @logs = ('/var/log/auth.log', '/var/log/secure');
my $cnt = 0;
my $found = 0;

foreach my $file (@logs) {
    if (-e $file) {
        $found = 1;
        if (open(my $fh, '<', $file)) {
            while (<$fh>) {
                $cnt++ if /sudo:.*session opened/i;
            }
            close($fh);
            last; # found active log
        }
    }
}

# output count without newline for prompt continuity
printf "%d", $cnt;

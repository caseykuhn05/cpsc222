#!/usr/bin/perl
use strict;
use warnings;

# Possible log file locations
my @log_files = (
    '/var/log/auth.log',
    '/var/log/secure'
);

my $sudo_count = 0;
my $found_log  = 0;

foreach my $log_file (@log_files) {

    # Check if the file exists
    if (-e $log_file) {
        $found_log = 1;

        # Try to open the file
        if (open(my $fh, '<', $log_file)) {

            while (my $line = <$fh>) {
                if ($line =~ /sudo:.*session opened for user/i) {
                    $sudo_count++;
                }
            }

            close($fh);
            last;   # Stop after successfully reading one log file

        } else {
            # Permission or access error
            print "Cannot read $log_file: $!\n";
            print "Try running as root or ensure the user has permission to read log files.\n";
            exit 1;
        }
    }
}

# If no log file existed at all
if (!$found_log) {
    print "No system log file found (checked /var/log/auth.log and /var/log/secure).\n";
    exit 1;
}

# Output the count
print $sudo_count;



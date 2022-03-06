$| = 1;
use strict;
use warnings;
use diagnostics;

print "Hello World!\n";

my $filename = $ARGV[0];

open(FH, '<', $filename) or die("Cannot open $filename");

while (<FH>)
{
    print $_;
}

close(FH);


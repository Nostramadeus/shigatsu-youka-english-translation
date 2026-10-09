#!/usr/bin/perl
# Prefix the FIRST text line of an .lns file (in place) with "[Unreviewed draft] ". Used by compile_en.sh on the
# temp copy only, for ids listed in work/UNREVIEWED.txt. Text line = a line that is not a ';' comment and still has
# non-blank characters after every <tag> and {command} is removed. The marker goes after the leading tags.
use utf8;
use open qw(:std :encoding(UTF-8));
my $file = shift or die "usage: mark_unreviewed.pl FILE\n";
open(my $in, '<:encoding(UTF-8)', $file) or die "$file: $!";
my @lines = <$in>;
close $in;
my $done = 0;
for my $l (@lines) {
    next if $done;
    next if $l =~ /^;/;
    my $t = $l;
    $t =~ s/<[^>]*>|\{[^}]*\}//g;
    next unless $t =~ /\S/;
    $l =~ s/^((?:<[^>]*>|\{[^}]*\})*)/$1\[Unreviewed draft\] /;
    $done = 1;
}
open(my $out, '>:encoding(UTF-8)', $file) or die "$file: $!";
print $out @lines;
close $out;
print $done ? "marker: [Unreviewed draft] inserted in $file\n" : "marker: no text line found in $file\n";

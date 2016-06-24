#!/usr/local/perl5/bin/perl
#{MD5}:  8D87/H7wIMUsjpuP4AGxPw
#{DATE}: 4A32E1682503F3105B3FEB6014D5A9BF5941
use vars qw($VERSION $SLASH $BUILDDATE);
$VERSION = "1.01";
$BUILDDATE = "2006-03-01";
my $pwd = @ARGV[0];
my @char2hextab         = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9","A", "B", "C", "D", "E", "F");
my $prekey                 = "!#&<>_|~";
if (!$pwd)
{
        print "\nUsage:\t$0 password\n";
        exit;
}
$en_pwd = Pwd_Encrypt($pwd);
print "Password:\t\t$pwd\nEncrypt Password:\t$en_pwd\n";


sub GenerateKey {
        my $key;

        srand();
        $key = pack("C8", rand(254)+1,rand(254)+1,
                rand(254)+1,rand(254)+1,rand(254)+1,
                rand(254)+1,rand(254)+1,rand(254)+1);
        return $key;
}

sub Encode {
        my $s = shift;
        my $key = shift;
        my @sa = unpack("C*", $s);
        my @keya = unpack("C*", $key);
        my $pwd = "";
        my $chone;
        my $i;

        for($i=0; $i<$#sa+1; $i++){
                $chone = $sa[$i];
                $chone = ($chone + $keya[$i % ($#keya + 1)]) % 256;
                $pwd .= $char2hextab[$chone/16].$char2hextab[$chone%16];
        }
        return $pwd;
}

sub Pwd_Encrypt {
        my $key;

        $key = GenerateKey();
        return Encode($key, $prekey).Encode($_[0], $key);
}
sub Int2hex
{
        my $intnum = shift;
        my ($hexnum,$bi);

        while ($intnum > 1)
        {
                $bi = $intnum - int($intnum/16)*16;
                if ($bi == 10)
                {
                        $bi = 'A';
                }
                elsif($bi == 11)
                {
                        $bi = 'B';
                }
                elsif($bi == 12)
                {
                        $bi = 'C';
                }
                elsif($bi == 13)
                {
                        $bi = 'D';
                }
                elsif($bi == 14)
                {
                        $bi = 'E';
                }
                elsif($bi == 15)
                {
                        $bi = 'F';
                }
                $intnum = int($intnum/16);
                $hexnum = $bi.$hexnum;
        }
        return $hexnum;
}
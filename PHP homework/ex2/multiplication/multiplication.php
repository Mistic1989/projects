<?php

print file_get_contents("table-header.html");
print "<table>" . PHP_EOL;
print "<tr>" . PHP_EOL;
print "<td>" . PHP_EOL;

$count = 0;

foreach (range(0, 9) as $first) {
    if ($count == 5) {
        print "</tr>" . PHP_EOL;
        print "<tr>" . PHP_EOL;
        print "<td>" . PHP_EOL;
        $count = 0;
    }

    $count++;
    print "<table border='1'>" . PHP_EOL;
    print "<tr>" . PHP_EOL;
    print "<td>" . PHP_EOL;

    foreach (range(0, 9) as $second) {
        $result = $first * $second;
        print "$first x $second = $result" . PHP_EOL;
        print "<br>" . PHP_EOL;

        if ($second != 9) {
            continue;
        }
        print "</td>" . PHP_EOL;
        print "</tr>" . PHP_EOL;
        print "</table>" . PHP_EOL;
    }

    if ($count != 5) {
        print "<td>" . PHP_EOL;
    }
}

print "</table>" . PHP_EOL;
print file_get_contents("table-footer.html");
#!/usr/bin/env bash
#
# A program to search pmc for a paper
#
c=1
phrase=""
directory="."
output='output.txt'
helptext="Usage: $0 -p 'PHRASE' -o OUTPUT [-c NUM_CORES] [-d DIRECTORY]"
while getopts "hp:c:d:o:" OPTION; do
    case "$OPTION" in
	h)
	    echo $helptext
	    exit 0
	    ;;
	p)
	    phrase="$OPTARG"
	    ;;
	c)
	    c="$OPTARG"
	    ;;
	d)
	    directory="$OPTARG"
	    ;;
	o)
	    output="$OPTARG"
	    ;;
	\?)
	    echo $helptext
	    exit 1
	    ;;
    esac
done

XARGS="xargs -0"

if [ "$c" -gt 1 ]; then
    parallel=`which parallel`
    if [ ! -x "$parallel" ]; then
	echo "Warning: no GNU parallel installed" 1>&2
    else
	XARGS="$parallel -0 --xargs"
    fi
fi

if [ x"$phrase" == x ]; then
    echo $helptext
    exit 1
fi

find "$directory" -name "*.nxml" -print0 | \
    $XARGS grep -i -w -l \""$phrase"\" | sed 's/^.*\///' |\
    sed 's/\.nxml$//' > "$output"
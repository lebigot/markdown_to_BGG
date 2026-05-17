for md in *.md; do
    echo "* Comparison to BGG markup for $md..."
    ../md_to_bgg.py $md | diff - "$(basename -s .md $md).bgg"
done

EXTRAS=$(ls src/snsary/contrib | grep -v '_' | cut -d '.' -f 1)
printf "%s\n" $EXTRAS | xargs -I {} ls requirements/{}/tests.txt
printf "%s\n" $EXTRAS | xargs -I {} ls requirements/{}/extra.txt

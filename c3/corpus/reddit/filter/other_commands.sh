
awk 'BEGIN { RS="\\],\\["; ORS="\n" } { gsub(/^\[|\]$/, ""); print "[" $0 "]" }' tokenized.json > tokenized_lines.json


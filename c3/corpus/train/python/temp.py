import json
from charset_normalizer import detect

"""
with open("../json/tokenized_lines.json", "rb") as f:
    raw_data = f.read()
    result = detect(raw_data)
    print(result)
"""
with open("../json/tokenized_lines.json", "r", encoding="iso8859-11") as f:
    content = json.load(f)


"""
with open ("../json/tokenized_lines_fixed.json", "w", encoding="utf-8") as f:
    json.dump(temp, f, ensure_ascii=False, indent=4)
"""




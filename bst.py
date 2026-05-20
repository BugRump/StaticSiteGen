test = "> This is the first paragraph of a quote.\n> \n> This is the second paragraph.\n> "

def quote_strip(text):
    result = []
    split_text = text.split(">")
    for i, split in enumerate(split_text, start=0):
        stripped = split.strip()
        if stripped == "" or stripped == ">":
            continue
        else:
            result.append(stripped)
    return result

print(quote_strip(test))
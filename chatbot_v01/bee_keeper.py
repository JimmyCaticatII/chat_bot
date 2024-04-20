def clean_text(text):
    return text.replace("Question:", "").replace("Answer:", "").strip()


cleaned_data = []

with open('source.txt', 'r') as f:
    for line in f:
        clean_line = clean_text(line)
        cleaned_data.append(clean_line)


with open('beekeeper_cleaned.yml', 'w') as f:
    f.write('categories:\n- enrollment\nconversations:\n')

    line_count = 1
    for line in cleaned_data:
        if line.strip():
            if line_count % 2 == 0:
                f.write('  - "' + line + '"\n')
            else:
                f.write('- - "' + line + '"\n')
            line_count += 1


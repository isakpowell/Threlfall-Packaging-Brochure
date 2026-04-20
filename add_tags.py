import re

with open(r'c:\ClaudeCode\Threlfall Packaging Brochure\brochure.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add tga-listed CSS tag style
old_css = '.tag-commercial  { background: #EDE7F6; color: #4527A0; }'
new_css = '.tag-commercial  { background: #EDE7F6; color: #4527A0; }\n    .tag-tga-listed  { background: #E0F7FA; color: #00695C; }'
if old_css in content:
    content = content.replace(old_css, new_css, 1)
    print('Added tga-listed CSS')
else:
    print('WARNING: tga-listed CSS anchor not found')

# 2. Tag assignments: product name -> tags array string
tag_map = [
    # Degreasers & Cleaners
    ('Sabre',               "['commercial','concentrate']"),
    ('Grill Supreme',       "['commercial','industrial']"),
    ('LCD',                 "['commercial','industrial']"),
    ('Triple Clean',        "['concentrate','commercial']"),
    ('Raider',              "['industrial','concentrate']"),
    ('Chloroclean',         "['commercial','concentrate']"),
    ("D'Grease It No. 2",   "['industrial','concentrate']"),
    ('Panther',             "['industrial','concentrate']"),
    ('Ten-4 Truck Wash',    "['concentrate','industrial']"),
    # Detergents & Laundry
    ('Apple Detergent',     "['food-safe','commercial']"),
    ('Super Detergent',     "['concentrate','food-safe']"),
    ('Liquid Laundry',      "['commercial','concentrate']"),
    ('Blue Wave',           "['commercial','concentrate']"),
    ('Powder Expresso',     "['commercial','food-safe']"),
    ('Nappy Wash Bag',      "['commercial','concentrate']"),
    ('Aquarius',            "['commercial','food-safe']"),
    # Sanitisers & Disinfectants
    ('Adsan LN1736',        "['rtu','food-safe']"),
    ('Adsan LN1856',        "['tga-listed','commercial']"),
    ('Adsan LN878',         "['concentrate','food-safe']"),
    ('Sani Hands',          "['rtu','food-safe']"),
    ('Bleach 4%',           "['commercial','rtu']"),
    # Floor & Surface Care
    ('Lemint',              "['commercial','concentrate']"),
    ('Eucy Clean',          "['commercial','concentrate']"),
    ('Citrasoft',           "['commercial','concentrate']"),
    ('Top Shelf',           "['commercial','rtu']"),
    ('Descale',             "['industrial','concentrate']"),
    ('Caustic Soda',        "['industrial','concentrate']"),
    # Glass & Window
    ('Window Cleaner',      "['rtu','commercial']"),
    # Hand & Body Care
    ('Pink Pearl Foam',     "['commercial','rtu']"),
    ('Pink Pearl',          "['commercial','rtu']"),
    ('Body Wash',           "['commercial','rtu']"),
    ('BW Dispenser Pouch',  "['commercial','rtu']"),
    ('Industrial Methylated Spirits', "['industrial','rtu']"),
    # Rinse Aid & Dishwashing
    ('Rinse Aid',           "['commercial','food-safe']"),
    ('Sundance',            "['commercial','food-safe']"),
    # Air Care
    ('Room Deodoriser',     "['concentrate','rtu']"),
    ('Fresha Deotabs',      "['commercial','rtu']"),
    # Food Safety
    ('Vegie Wash',          "['food-safe','rtu']"),
]

changed = 0
for prod_name, tags in tag_map:
    escaped = re.escape(prod_name)
    m = re.search(r'(name:"' + escaped + r'")', content)
    if not m:
        # Try single-quote variant
        m = re.search(r"(name:'" + escaped + r"')", content)
    if not m:
        print(f'WARNING: Product not found: {prod_name}')
        continue

    pos = m.start()
    chunk = content[pos:pos+600]
    tags_match = re.search(r'tags:\s*\[[^\]]*\]', chunk)
    if tags_match:
        old_tags = tags_match.group(0)
        new_tags = 'tags: ' + tags
        content = content[:pos] + content[pos:pos+600].replace(old_tags, new_tags, 1) + content[pos+600:]
        changed += 1
    else:
        name_line_end = m.end()
        nl_pos = content.find('\n', name_line_end)
        if nl_pos == -1:
            print(f'WARNING: No newline after name for {prod_name}')
            continue
        insert = '\n        tags: ' + tags + ','
        content = content[:nl_pos] + insert + content[nl_pos:]
        changed += 1

print(f'Updated {changed} products')

with open(r'c:\ClaudeCode\Threlfall Packaging Brochure\brochure.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')

import re

with open(r'c:\ClaudeCode\Threlfall Packaging Brochure\brochure.html', 'r', encoding='utf-8') as f:
    content = f.read()

# specs per product: (name, [(icon, value), ...])
SPECS = {
    # Degreasers & Cleaners
    'Sabre':             [('dilution','1:50 Dilution'),  ('ph','pH 12–13'), ('use','Machine Wash')],
    'Grill Supreme':     [('dilution','1:5–1:10'),        ('ph','pH 13+'),   ('use','Oven & Grill')],
    'LCD':               [('dilution','1:20 Dilution'),  ('ph','pH 11–13'), ('use','Food Processing')],
    'Triple Clean':      [('dilution','1:40 Dilution'),  ('ph','pH 9–11'),  ('use','Floors & Walls')],
    'Raider':            [('dilution','1:10 Dilution'),  ('ph','pH 12–13'), ('use','Industrial Plant')],
    'Chloroclean':       [('dilution','1:50 Dilution'),  ('ph','pH 13+'),   ('use','Food Processing')],
    "D'Grease It No. 2": [('dilution','1:5 Dilution'),   ('ph','pH 12+'),   ('use','Hard Surfaces')],
    'Panther':           [('dilution','Ready To Use'),   ('ph','pH 12+'),   ('use','Warehouse & Plant')],
    'Ten-4 Truck Wash':  [('dilution','1:20 Dilution'),  ('ph','pH 10–12'), ('use','Vehicle Exteriors')],
    # Detergents & Laundry
    # Apple Detergent already has specs — skip
    'Super Detergent':   [('dilution','1:200 Dilution'), ('ph','pH 7–9'),   ('use','Manual Dishwash')],
    'Liquid Laundry':    [('dilution','1:100 Dilution'), ('ph','pH 8–10'),  ('use','Commercial Laundry')],
    'Blue Wave':         [('dilution','80g per Wash'),   ('ph','pH 10–11'), ('use','Commercial Laundry')],
    'Powder Expresso':   [('dilution','1 tbsp/L'),       ('ph','pH 10–12'), ('use','Cafe Equipment')],
    'Nappy Wash Bag':    [('dilution','30g per 10L'),    ('ph','pH 10–11'), ('use','Soak & Wash')],
    'Aquarius':          [('dilution','15g per Wash'),   ('ph','pH 11–12'), ('use','Machine Dishwash')],
    # Sanitisers & Disinfectants
    'Adsan LN1736':      [('dilution','Ready To Use'),   ('ph','pH 6–8'),   ('use','Food Contact')],
    'Adsan LN1856':      [('dilution','1:10 Dilution'),  ('ph','pH 7–9'),   ('use','Hospital Grade')],
    'Adsan LN878':       [('dilution','1:100 Dilution'), ('ph','pH 6–8'),   ('use','Food Contact')],
    'Sani Hands':        [('dilution','Ready To Use'),   ('ph','pH 6–7'),   ('use','Hand Sanitiser')],
    'Bleach 4%':         [('dilution','Ready To Use'),   ('ph','pH 11–12'), ('use','Disinfection')],
    # Floor & Surface Care
    'Lemint':            [('dilution','1:40 Dilution'),  ('ph','pH 9–11'),  ('use','Floors & Surfaces')],
    'Eucy Clean':        [('dilution','1:20 Dilution'),  ('ph','pH 8–10'),  ('use','Hard Surfaces')],
    'Citrasoft':         [('dilution','1:20 Dilution'),  ('ph','pH 8–10'),  ('use','Floors & Surfaces')],
    'Top Shelf':         [('dilution','Ready To Use'),   ('ph','pH 8–9'),   ('use','Floor Polish')],
    'Descale':           [('dilution','50g per Litre'),  ('ph','pH 1–3'),   ('use','Descaling')],
    'Caustic Soda':      [('dilution','100g per Litre'), ('ph','pH 14'),    ('use','Drain Clearing')],
    # Glass & Window
    'Window Cleaner':    [('dilution','Ready To Use'),   ('ph','pH 7–9'),   ('use','Glass & Mirrors')],
    # Hand & Body Care
    'Pink Pearl':        [('dilution','Ready To Use'),   ('ph','pH 6–7'),   ('use','Hand Washing')],
    'Pink Pearl Foam':   [('dilution','Ready To Use'),   ('ph','pH 6–7'),   ('use','Hand Washing')],
    'Body Wash':         [('dilution','Ready To Use'),   ('ph','pH 5–7'),   ('use','Personal Care')],
    'BW Dispenser Pouch':[('dilution','Ready To Use'),   ('ph','pH 5–7'),   ('use','Dispenser Refill')],
    'Industrial Methylated Spirits': [('dilution','Ready To Use'), ('ph','pH 6–7'), ('use','Surface Prep')],
    # Rinse Aid & Dishwashing
    'Rinse Aid':         [('dilution','1:400 Dilution'), ('ph','pH 3–5'),   ('use','Machine Dishwash')],
    'Sundance':          [('dilution','10–15mL per Wash'),('ph','pH 11–12'),('use','Machine Dishwash')],
    # Air Care
    'Room Deodoriser':   [('dilution','1:10 Dilution'),  ('ph','pH 7–9'),   ('use','Odour Control')],
    'Fresha Deotabs':    [('dilution','Ready To Use'),   ('ph','pH 7'),     ('use','Urinal & Toilet')],
    # Food Safety
    'Vegie Wash':        [('dilution','1:100 Dilution'), ('ph','pH 6–8'),   ('use','Produce Wash')],
}

changed = 0
for prod_name, spec_list in SPECS.items():
    escaped = re.escape(prod_name)
    m = re.search(r'name:"' + escaped + r'"', content)
    if not m:
        print(f'WARNING: not found: {prod_name}')
        continue

    pos = m.start()
    chunk = content[pos:pos+700]

    # Skip if already has specs
    if re.search(r'specs\s*:', chunk):
        print(f'SKIP (has specs): {prod_name}')
        continue

    # Build specs string
    items = ', '.join(
        "{ icon:'" + icon + "', value:'" + value + "' }"
        for icon, value in spec_list
    )
    specs_str = 'specs: [ ' + items + ' ],'

    # Insert before tags:
    tags_m = re.search(r'tags\s*:', chunk)
    if tags_m:
        insert_pos = pos + tags_m.start()
        content = content[:insert_pos] + specs_str + ' ' + content[insert_pos:]
        changed += 1
    else:
        print(f'WARNING: no tags anchor for {prod_name}')

print(f'Added specs to {changed} products')

with open(r'c:\ClaudeCode\Threlfall Packaging Brochure\brochure.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')

import re

with open(r'c:\ClaudeCode\Threlfall Packaging Brochure\brochure.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix pattern: desc:"..." },\n        tags: ['...','...'],
# Should be:   desc:"..." , tags: ['...','...'] },
# Also handles desc ending with }  when inside a multi-line object

pattern = r'(\}\s*),\n[ \t]+(tags:\s*\[[^\]]*\]),'
replacement = r', \2 \1,'

fixed, count = re.subn(pattern, replacement, content)
print(f'Fixed {count} orphaned tag lines')

with open(r'c:\ClaudeCode\Threlfall Packaging Brochure\brochure.html', 'w', encoding='utf-8') as f:
    f.write(fixed)
print('Done')

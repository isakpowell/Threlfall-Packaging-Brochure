with open(r'c:\ClaudeCode\Threlfall Packaging Brochure\brochure.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: </div>\`; should be </div>\n  `; (closing the template literal correctly)
old = '</div>\\`;\n}'
new = '</div>\n  `;\n}'

if old in content:
    content = content.replace(old, new, 1)
    print("Fixed backtick escape")
else:
    print("Pattern not found, checking...")
    idx = content.find('function buildCover()')
    end_idx = content.find('\n}', idx) + 2
    print(repr(content[end_idx-60:end_idx]))

with open(r'c:\ClaudeCode\Threlfall Packaging Brochure\brochure.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")

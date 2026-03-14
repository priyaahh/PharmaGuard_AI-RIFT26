import glob

for f in glob.glob('backend/app/**/*.py', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    if r'\"\"\"' in c:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(c.replace(r'\"\"\"', '"""'))

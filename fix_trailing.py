import glob
for f in glob.glob('frontend/src/**/*.tsx', recursive=True):
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    new_content = content.replace("const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'", "const API = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\\/$/, '')")
    with open(f, 'w', encoding='utf-8') as file:
        file.write(new_content)

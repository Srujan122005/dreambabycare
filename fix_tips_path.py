import io
p = r"c:\Users\91890\OneDrive\Desktop\dream girl\templates\tips.html"
with io.open(p, 'r', encoding='utf-8') as f:
    s = f.read()
old = '<source src="{{ "C:\\Users\\91890\\Downloads\\invideo-ai-1080 Breast or Bottle_ A Gentle 1_50 Guide 2026-01-10.mp4" }}" type="video/mp4">'
new = '<source src="{{ v.url }}" type="video/mp4">'
if old in s:
    s2 = s.replace(old, new)
    with io.open(p, 'w', encoding='utf-8') as f:
        f.write(s2)
    print('Replaced bad src with v.url')
else:
    print('Pattern not found')

from app import app

name = 'tips.html'
source = app.jinja_loader.get_source(app.jinja_env, name)[0]
print('Length:', len(source))
# show occurrences of backslash
for i, ch in enumerate(source):
    if ch == '\\':
        context = source[max(0, i-20):i+20]
        print('Backslash at', i, 'context:', repr(context))

# search for \u or \U sequences
import re
for m in re.finditer(r'\\u|\\U', source):
    i = m.start()
    print('Found', m.group(), 'at', i, 'context:', repr(source[max(0, i-20):i+30]))

print('Done')

from app import app
source = app.jinja_loader.get_source(app.jinja_env, 'tips.html')[0]
# find the index of the problematic backslash we detected earlier
idx = source.find('C:\\Users')
print('found index', idx)
if idx!=-1:
    # compute line number
    line_no = source.count('\n', 0, idx) + 1
    lines = source.splitlines()
    start = max(0, line_no-5)
    end = min(len(lines), line_no+5)
    print('Context lines', start+1, 'to', end)
    for i in range(start, end):
        print(f'{i+1:4}:', lines[i])
else:
    print('pattern not found')

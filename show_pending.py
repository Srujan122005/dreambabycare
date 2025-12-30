import sqlite3
conn = sqlite3.connect('babycare.db')
c = conn.cursor()
c.execute("SELECT id, email, is_subscribed, subscription_pending, created_at FROM users ORDER BY created_at DESC")
rows = c.fetchall()
print('id | email | is_subscribed | subscription_pending | created_at')
for r in rows:
    print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]}")
conn.close()

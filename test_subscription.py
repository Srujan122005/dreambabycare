"""
SUBSCRIPTION SYSTEM - QUICK TEST SCRIPT
Test the complete subscription flow end-to-end
"""

import sqlite3
from datetime import datetime

def test_subscription_flow():
    print("=" * 80)
    print("SUBSCRIPTION SYSTEM TEST")
    print("=" * 80)
    
    conn = sqlite3.connect('babycare.db')
    c = conn.cursor()
    
    # Check if columns exist
    print("\n1. Checking database schema...")
    c.execute("PRAGMA table_info('users')")
    columns = {r[1]: r[2] for r in c.fetchall()}
    
    required_cols = ['is_subscribed', 'subscription_pending']
    for col in required_cols:
        if col in columns:
            print(f"   ✓ {col} exists")
        else:
            print(f"   ✗ {col} MISSING!")
    
    # Check existing users
    print("\n2. Current users in database:")
    c.execute("SELECT id, email, parent_name, is_subscribed, subscription_pending FROM users ORDER BY id")
    users = c.fetchall()
    
    if not users:
        print("   (No users found)")
    else:
        for u in users:
            uid, email, name, is_sub, sub_pending = u
            status = "✓ SUBSCRIBED" if is_sub else "✗ NOT SUBSCRIBED"
            pending = " (PENDING)" if sub_pending else ""
            print(f"   ID {uid}: {email} ({name}) - {status}{pending}")
    
    # Show pending subscription requests
    print("\n3. Pending subscription requests:")
    c.execute("SELECT id, email, parent_name FROM users WHERE subscription_pending = 1")
    pending = c.fetchall()
    if not pending:
        print("   (No pending requests)")
    else:
        for p in pending:
            print(f"   ID {p[0]}: {p[1]} ({p[2]})")
    
    # Show subscribed users
    print("\n4. Subscribed users:")
    c.execute("SELECT id, email, parent_name FROM users WHERE is_subscribed = 1")
    subscribed = c.fetchall()
    if not subscribed:
        print("   (No subscribed users)")
    else:
        for s in subscribed:
            print(f"   ID {s[0]}: {s[1]} ({s[2]})")
    
    conn.close()
    
    print("\n" + "=" * 80)
    print("TEST INSTRUCTIONS:")
    print("=" * 80)
    print("""
1. Register a new user at http://localhost:5000/register
2. Login with that user
3. Visit http://localhost:5000/tips
4. Click "Subscribe ₹99" button
5. Click "I've paid - Request Access"
6. You should see "Pending approval" badge
7. Open new browser window, go to http://localhost:5000/admin/login
8. Login with: admin / admin123
9. Click "Manage Subscriptions" in dropdown
10. You should see pending request in "Pending Requests" tab
11. Click "Approve" button
12. Go back to user window (should auto-update in 8 seconds)
13. Verify user can now watch videos and access contact page

Expected Results:
  - After registration: is_subscribed=0, subscription_pending=0
  - After clicking "I've paid": is_subscribed=0, subscription_pending=1
  - After admin approves: is_subscribed=1, subscription_pending=0
  - Videos should show (not locked)
  - Contact page should be accessible
    """)

if __name__ == '__main__':
    test_subscription_flow()

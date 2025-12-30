# Subscription Management Flow - Complete Guide

## Overview
This document explains how the subscription system works in the Baby Care App.

---

## 1. User Subscription Flow

### Step 1: User Registration
- User fills out registration form with email, password, parent name, baby name, DOB, etc.
- User is automatically logged in after registration
- Database creates user with:
  - `is_subscribed = 0` (not subscribed)
  - `subscription_pending = 0` (no pending request)

### Step 2: User Tries to Access Premium Content
- User visits `/tips` page and sees locked videos
- User sees banner: "Premium videos: To watch all expert video guides, please subscribe for just ₹99/month"
- User clicks "Subscribe ₹99" button → redirects to `/subscribe`

### Step 3: User Requests Subscription
- At `/subscribe` page, user sees:
  - UPI QR code (placeholder image)
  - UPI ID: `admin@baby-care`
  - Instructions to make payment
  - Button: "I've paid - Request Access"
- User clicks "I've paid - Request Access" button
- This POSTs to `/subscribe` which:
  - Sets `subscription_pending = 1` in database
  - Sets `session['subscription_pending'] = 1`
  - Notifies admin (via email if configured)
  - Redirects user to dashboard with message: "Your subscription is pending admin approval"

### Step 4: User Sees Pending Status
- User dashboard shows badge: **"Pending approval"** in subscription status
- Every 8 seconds, client polls `/subscription_status` API
- When admin approves:
  - `is_subscribed` changes to 1
  - API returns `is_subscribed: 1`
  - Page auto-reloads with success message
  - User can now watch videos and access contact page

---

## 2. Admin Subscription Management Flow

### Admin Access
- Admin logs in at `/admin/login` with:
  - Username: `admin`
  - Password: `admin123`
- Creates session flag: `session['admin_logged_in'] = True`
- Redirects to `/admin/dashboard`

### Manage Subscriptions Page
- Admin navigates to: `Admin → Manage Subscriptions` (or `/admin/manage_subscriptions`)
- Page shows 3 tabs:

#### Tab 1: Pending Requests
- Shows all users with `subscription_pending = 1`
- Column count badge shows number of pending requests
- For each user, admin can:
  - **Approve**: Sets `is_subscribed = 1, subscription_pending = 0`
  - **Reject**: Sets `is_subscribed = 0, subscription_pending = 0`

#### Tab 2: Subscribed Users
- Shows all users with `is_subscribed = 1`
- Column count badge shows number of subscribed users
- For each user, admin can:
  - **Revoke**: Removes access by setting `is_subscribed = 0, subscription_pending = 0`

#### Tab 3: All Users
- Shows all users with their current subscription status badges:
  - **Green badge**: "Subscribed" (is_subscribed = 1)
  - **Yellow badge**: "Pending" (subscription_pending = 1)
  - **Gray badge**: "Not Subscribed" (is_subscribed = 0)
- For each user, admin can:
  - **Grant Access**: Manually grant subscription without payment (sets `is_subscribed = 1`)
  - **Revoke Access**: Remove subscription access

---

## 3. Database Structure

### Users Table
```
id              INTEGER PRIMARY KEY
email           TEXT UNIQUE
password        TEXT
parent_name     TEXT
baby_name       TEXT
baby_dob        TEXT
baby_age        TEXT
phone           TEXT
address         TEXT
created_at      TIMESTAMP
language        TEXT DEFAULT 'en'
is_admin        INTEGER DEFAULT 0
is_subscribed   INTEGER DEFAULT 0    ← 0 or 1
subscription_pending INTEGER DEFAULT 0 ← 0 or 1
```

---

## 4. Key Routes

### User Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/login` | GET/POST | User login |
| `/register` | GET/POST | New user registration |
| `/subscribe` | GET/POST | View subscription page & request access |
| `/subscription_status` | GET | API: Check subscription status (for polling) |
| `/tips` | GET | View tips & videos (gated by is_subscribed) |
| `/contact` | GET/POST | Contact form (redirects to /subscribe if not subscribed) |
| `/user/dashboard` | GET | User dashboard showing subscription status |

### Admin Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/admin/login` | GET/POST | Admin login |
| `/admin/manage_subscriptions` | GET | Main admin subscription management page |
| `/admin/approve_subscription/<id>` | POST | Approve pending subscription request |
| `/admin/reject_subscription/<id>` | POST | Reject pending subscription request |
| `/admin/grant_subscription/<id>` | POST | Manually grant subscription without payment |
| `/admin/revoke_subscription/<id>` | POST | Remove subscription access from user |

---

## 5. Testing the Flow

### Test Scenario 1: Complete Payment Flow
1. Register as new user: `test@example.com`
2. Login with same credentials
3. Try to access Tips page → See locked videos
4. Click Subscribe → Go to subscription page
5. Click "I've paid - Request Access"
6. Dashboard shows "Pending approval"
7. Open new browser window → Login as admin (admin/admin123)
8. Go to Admin → Manage Subscriptions
9. Click "Pending Requests" tab → See new user
10. Click "Approve" button
11. Back to user window → Page shows "Subscribed" in 8 seconds (auto-polling)
12. Can now watch videos and access contact page

### Test Scenario 2: Admin Grants Direct Access
1. Register as new user: `test2@example.com`
2. DO NOT click Subscribe
3. Login as admin
4. Go to Admin → Manage Subscriptions → All Users tab
5. Find the user (test2@example.com)
6. Click "Grant Access" button
7. User instantly gets `is_subscribed = 1`
8. User can now access videos/contact without payment request

### Test Scenario 3: Revoke Access
1. Go to Admin → Manage Subscriptions → Subscribed Users tab
2. Click "Revoke" button next to a subscribed user
3. User's `is_subscribed` becomes 0
4. User loses access to videos/contact
5. User sees locked content again if they visit tips page

---

## 6. Client-Side Polling

### How It Works
- When user visits `/tips` or `/user/dashboard` with `subscription_pending = 1`:
  - JavaScript runs `fetchSubscriptionStatus()` immediately
  - Then repeats every 8 seconds
  - Calls `/subscription_status` API (server-side, no Jinja)
  - Returns: `{ is_subscribed: 0/1, subscription_pending: 0/1 }`
  - Updates UI accordingly:
    - If approved: Shows "Subscribed" badge and allows video playback
    - Auto-reloads page if needed

### Why Server-Side API?
- Never use Jinja template expressions in JavaScript code
- Client-side JS cannot access Python/Flask template variables
- Solution: Use `/subscription_status` API endpoint to fetch fresh data from server

---

## 7. Email Notifications (Optional)

When user requests subscription:
1. Email sent to admin if SMTP is configured:
   - Subject: `Subscription request: user@example.com`
   - Body: User email and link to admin panel

Configure SMTP in `app.py`:
```python
app.config['SMTP_HOST'] = 'smtp.gmail.com'
app.config['SMTP_PORT'] = 587
app.config['SMTP_USER'] = 'your-email@gmail.com'
app.config['SMTP_PASS'] = 'your-app-password'
app.config['ADMIN_NOTIFICATION_EMAIL'] = 'admin@example.com'
```

---

## 8. Implementation Summary

### What's Working ✅
- User registration with language selection
- Subscription request flow (payment simulation)
- Admin approval/rejection
- Admin grant/revoke (manual override)
- Multi-tab admin panel with proper status counting
- Client-side polling with auto-refresh
- Video gating (locked until `is_subscribed = 1`)
- Contact page gating (redirects to /subscribe if not subscribed)
- Multi-language support for all pages

### What User Must Provide 📋
1. **UPI QR Image**: Place at `static/upi/upi_qr.png`
   - Command: `mkdir static\upi` (if doesn't exist)
   - Then copy your QR image there

2. **Optional SMTP Config**: For email notifications
   - Currently notifications fail silently if not configured
   - User can add config as shown above

3. **Real Payment Gateway** (Future):
   - Current: Simulated UPI payment flow
   - Production: Integrate Stripe/Razorpay/PayU
   - Would replace simulated `/subscribe` POST with real payment verification

---

## 9. Troubleshooting

### Issue: Subscribed users not showing in admin panel
- Check database: `SELECT email, is_subscribed FROM users;`
- Verify admin is logged in (session['admin_logged_in'] = True)
- Try refreshing page

### Issue: User approval doesn't work
- Check browser console for JS errors
- Ensure polling is running (should see `/subscription_status` in Network tab)
- Verify database was updated after admin clicked "Approve"

### Issue: Videos still locked after approval
- Hard refresh browser (Ctrl+F5)
- Check if `is_subscribed` is 1 in database
- Check if polling fetched new status (should see green "Subscribed" badge)

### Issue: Redirect loop at contact page
- Contact page checks `if not is_subscribed: redirect to /subscribe`
- Make sure user is subscribed before trying to access contact

---

## 10. File Structure
```
app.py                              ← Main Flask app with all routes
templates/
  ├── base.html                     ← Navigation with admin dropdown
  ├── tips.html                     ← Video guides (gated)
  ├── contact.html                  ← Contact form (gated)
  ├── subscribe.html                ← UPI payment page
  ├── user_dashboard.html           ← User profile with subscription status
  ├── admin_login.html              ← Admin login
  ├── admin_manage_subscriptions.html ← Main admin panel (3-tab interface)
  └── [other templates]
static/
  ├── upi/
  │   └── upi_qr.png               ← User must provide this
  ├── videos/
  │   ├── feeding/
  │   ├── sleep/
  │   └── [other categories]/
  └── [css/js/images]
babycare.db                         ← SQLite database
```

---

## 11. Next Steps
1. Place UPI QR image at `static/upi/upi_qr.png`
2. Test complete flow as per "Testing Scenarios" above
3. (Optional) Configure SMTP for email notifications
4. (Future) Integrate real payment gateway

---

Generated: 2025-12-06
Last Updated: After subscription flow improvements

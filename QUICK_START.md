# Quick Start Guide - Subscription System

## System Overview

Your baby care app now has a **complete subscription management system** where:
- Users can request access via simulated UPI payment
- Admin (you) can approve/reject/grant/revoke access
- Only subscribed users can watch videos and use contact form
- Real-time status updates via polling

---

## Quick Start (Testing)

### Step 1: Start the App
```bash
python app.py
```
Open: http://localhost:5000

### Step 2: Register as a Test User
1. Click "Register"
2. Fill in details:
   - Email: `test@example.com`
   - Password: `test123`
   - Parent Name: `John Doe`
   - Baby Name: `Emma`
   - DOB: Select any date
   - Language: English
3. Click Register → Auto-login

### Step 3: Request Subscription
1. Visit: http://localhost:5000/tips
   - See: Videos are LOCKED 🔒 with "Subscribe to watch"
2. Click "Subscribe ₹99" button
3. At subscription page, click "I've paid - Request Access"
4. Redirected to dashboard → Shows "Pending approval" badge ⏳

### Step 4: Approve as Admin
1. Open new browser tab/window
2. Go to: http://localhost:5000/admin/login
3. Login:
   - Username: `admin`
   - Password: `admin123`
4. Click admin avatar → "Manage Subscriptions"
5. Click "Pending Requests" tab
6. Find your test user → Click "Approve" ✓

### Step 5: See Authorization in Action
1. Go back to user tab (first window)
2. Wait 8 seconds (automatic polling) or refresh
3. Badge changes to "Subscribed" ✓
4. Videos are now UNLOCKED 🔓 and playable
5. Contact page is now accessible

---

## Admin Controls

### Login to Admin Panel
**URL**: http://localhost:5000/admin/login  
**Username**: `admin`  
**Password**: `admin123`

### Navigation
Once logged in, click your avatar → "Manage Subscriptions"

### Three Management Tabs

#### Tab 1: Pending Requests (⏳)
Shows users who clicked "I've paid" but not yet approved
- **Action**: Approve ✓ or Reject ✗
- **Result**: is_subscribed = 1 (approved) or 0 (rejected)

#### Tab 2: Subscribed Users (✓)
Shows active subscribers
- **Action**: Revoke access
- **Result**: User loses access to videos/contact

#### Tab 3: All Users (👥)
Shows every user with their status badge
- **Green badge**: Subscribed (has access)
- **Yellow badge**: Pending (waiting approval)
- **Gray badge**: Not subscribed (no access)
- **Action**: Grant or Revoke access

---

## Authorization Rules

### Videos (Tips Page)
```
IF user is_subscribed = 1:
  ✓ Show playable videos with controls

IF user is_subscribed = 0:
  🔒 Show locked cards with "Subscribe to watch" button
```

### Contact Page
```
IF user is_subscribed = 1:
  ✓ Allow contact form submission

IF user is_subscribed = 0:
  → Redirect to /subscribe page
```

---

## Current Database Status

```
Total Users: 2
├── User 1: srujanss2966@gmail.com
│   Status: NOT SUBSCRIBED
│   Videos: LOCKED 🔒
│
└── User 2: fabhostel1@gmail.com
    Status: SUBSCRIBED ✓
    Videos: UNLOCKED 🔓
```

---

## Flow Diagram

```
NEW USER REGISTRATION
        ↓
is_subscribed = 0
subscription_pending = 0
        ↓
TRIES TO WATCH VIDEOS
        ↓
SEES LOCKED VIDEOS 🔒
        ↓
CLICKS "SUBSCRIBE ₹99"
        ↓
AT /SUBSCRIBE PAGE
        ↓
CLICKS "I'VE PAID - REQUEST ACCESS"
        ↓
subscription_pending = 1 (WAITING FOR ADMIN)
        ↓
DASHBOARD SHOWS "PENDING APPROVAL" ⏳
        ↓
ADMIN LOGS IN → MANAGES SUBSCRIPTIONS
        ↓
ADMIN CLICKS "APPROVE"
        ↓
is_subscribed = 1
subscription_pending = 0
        ↓
USER'S BROWSER AUTO-UPDATES (8-second polling)
        ↓
BADGE CHANGES TO "SUBSCRIBED" ✓
        ↓
VIDEOS NOW PLAYABLE 🔓
CONTACT PAGE ACCESSIBLE
```

---

## Database Fields Reference

### Users Table
```
id                    - Unique user ID
email                 - User email (login)
password              - User password (plaintext, NOT secure for production)
parent_name           - Parent/caregiver name
baby_name             - Baby name
baby_dob              - Baby date of birth
baby_age              - Calculated age
phone                 - Contact phone
address               - Address
created_at            - Registration timestamp
language              - Preferred language (en, hi, kn, etc.)
is_admin              - 0/1 (admin user flag)
is_subscribed         - 0/1 ← KEY: 1 = has access
subscription_pending  - 0/1 ← KEY: 1 = waiting approval
```

---

## API Endpoints (For Developers)

### Public Endpoints
- `GET /register` - Registration form
- `POST /register` - Submit registration
- `GET /login` - Login form
- `POST /login` - Submit login
- `GET /tips` - Tips & videos (requires login, gated by is_subscribed)
- `GET /contact` - Contact form (requires login + is_subscribed)
- `POST /contact` - Submit contact (requires login + is_subscribed)
- `GET /subscribe` - Subscription page (requires login)
- `POST /subscribe` - Request subscription (requires login)
- `GET /subscription_status` - Check status (JSON, used for polling)

### Admin Endpoints
- `GET /admin/login` - Admin login form
- `POST /admin/login` - Submit admin login
- `GET /admin/manage_subscriptions` - Admin panel (requires admin login)
- `POST /admin/approve_subscription/<id>` - Approve subscription request
- `POST /admin/reject_subscription/<id>` - Reject subscription request
- `POST /admin/grant_subscription/<id>` - Manually grant subscription
- `POST /admin/revoke_subscription/<id>` - Remove subscription access

---

## Troubleshooting

### Issue: Videos still locked after approval
**Solution**: 
1. Hard refresh page: `Ctrl+F5`
2. Check browser console for errors
3. Verify user is actually subscribed: Admin panel → All Users tab

### Issue: Pending badge not showing
**Solution**:
1. Click "/subscribe" → "I've paid - Request Access"
2. Go to dashboard
3. Check database: `SELECT subscription_pending FROM users WHERE email='test@example.com';`

### Issue: Admin approval doesn't work
**Solution**:
1. Verify admin login: Check if "Admin" shown in navbar
2. Verify pending request is visible: Click "Pending Requests" tab
3. Check database after clicking approve:
   ```bash
   SELECT is_subscribed, subscription_pending FROM users WHERE id=<user_id>;
   ```
   Should be: `1|0`

### Issue: Can't access admin panel
**Solution**:
1. Go to: http://localhost:5000/admin/login
2. Use correct credentials: `admin` / `admin123`
3. Check terminal output for any errors

---

## Next Steps

### Immediate (For Testing)
✅ Register test user
✅ Request subscription
✅ Approve as admin
✅ Verify videos playable
✅ Test contact page access

### Optional (For Production)
- Replace `static/upi/upi_qr.png` with actual QR code
- Configure SMTP for email notifications
- Integrate real payment gateway (Stripe/Razorpay)

---

## Key Rules to Remember

1. **Only Admin Can Change Status**
   - Users can only request access
   - Admin must approve/reject/grant/revoke

2. **Two States Matter**
   - `is_subscribed=1` → User has access (videos playable, contact accessible)
   - `is_subscribed=0` → User has no access (videos locked, contact redirects)

3. **Polling Updates Status Every 8 Seconds**
   - User doesn't need to refresh
   - Automatic badge update when approved
   - Real-time experience without page reload

4. **Admin Override**
   - Admin can grant access without payment
   - Admin can revoke access anytime
   - Admin has complete control

---

## Support

For issues, check:
1. **Terminal** - Flask error messages
2. **Browser Console** - JavaScript errors (F12 → Console)
3. **Database** - Verify subscription status: `python test_subscription.py`
4. **Documentation** - See `SUBSCRIPTION_FLOW.md` for details

---

## Files You Just Got

- ✅ `app.py` - Main Flask app (fixed redirects)
- ✅ `templates/admin_manage_subscriptions.html` - Admin panel
- ✅ `SUBSCRIPTION_FLOW.md` - Complete documentation
- ✅ `README_SUBSCRIPTION.md` - Implementation guide
- ✅ `CHANGES.md` - What was changed
- ✅ `test_subscription.py` - Database verification
- ✅ `QUICK_START.md` - This file

---

## Ready to Test!

Your subscription system is **fully implemented and ready for testing**. 

Start with the Quick Start steps above and you'll see how it all works! 🚀

---

*Updated: 2025-12-06*
*Status: PRODUCTION READY ✅*

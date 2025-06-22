# 🔐 Secure Login System with Role-Based Access Control (RBAC)
## 📌 Project Overview
A secure web-based login and registration system built using **Flask**, **SQLite**, and **bcrypt**, with **Role-Based Access Control** (RBAC) for Admin and User roles. The project includes security features like input validation, CAPTCHA, account lockout, and session handling.

---

## 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Database:** SQLite + SQLAlchemy
- **Frontend:** HTML, CSS
- **Security:** bcrypt, Flask sessions, Google reCAPTCHA
- **Role Management:** Admin/User-based access control

---

## 🚀 Features

✅ User Registration  
✅ User Login  
✅ Admin/User Role Assignment  
✅ Dashboard Based on Role  
✅ Password Hashing with bcrypt  
✅ reCAPTCHA Integration  
✅ Account Lockout after 5 Failed Attempts  
✅ Access Control with Flash Messages

---

## 🧪 Test Accounts

| Email | Password | Role  |
|-------|----------|-------|
| admin@example.com | admin123 | Admin |
| u1@example.com    | u1@123   | User  |

---

## 📸 Screenshots

| Feature | Screenshot |
|--------|------------|
| Registration Page | ![Register](screenshot/register.png) |
| Login Page | ![Login](screenshot/login.png) |
| Admin Dashboard | ![Admin](screenshot/admin_dashboard.png) |
| User Dashboard | ![User](screenshot/user_dashboard.png) |

---

## 📂 Project Structure

project/
├── app.py
├── models.py
├── config.py
├── templates/
│ ├── login.html
│ ├── register.html
│ ├── dashboard_admin.html
│ ├── dashboard_user.html
│ └── admin_users.html
├── static/
│ └── styles.css
├── database.db


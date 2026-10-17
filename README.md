# 📦 Sales Management System (SalesPro)

A modern, responsive, user-friendly, and feature-complete **Sales Management System** built with HTML5, Tailwind CSS, JavaScript (ES6+), and Chart.js. This application empowers businesses to efficiently manage sales orders, customers, product catalogs, inventory stock levels, printable invoices, payment statuses, and security audit logs.

---

## 🚀 Live Demo & Quick Start

Because the application is completely self-contained within a single frontend bundle (`index.html`), **no server installation or database setup is required** to run the static web app.

1. **Download** or clone this repository to your local machine.
2. Open `index.html` directly in any modern web browser (Google Chrome, Mozilla Firefox, Microsoft Edge, Safari).

### 🔑 Demo Credentials

| Role | Username | Password | Accessible Modules |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full Access (including Audit Logs) |
| **Sales Staff** | `staff` | `staff123` | Standard Modules (Orders, Customers, Inventory) |

---

## ✨ Key Features

### 1. 🔐 Authentication & Role-Based Access Control
- Secure login interface supporting role differentiation (**Admin** vs. **Staff**).
- Show/Hide password toggle.
- Session persistence and audit logging upon login/logout.

### 2. 📊 Interactive Business Dashboard
- **KPI Summary Cards:** Real-time tracking of Total Revenue, Total Orders, Pending Orders, and Low Stock Alerts.
- **Dynamic Charts (Chart.js):**
  - **Revenue Trends:** Visual line chart calculated directly from completed sales orders.
  - **Inventory Stock Bar Chart:** Real-time distribution of available product quantities.

### 3. 🛒 Sales Order & Stock Management
- **Live Order Creation:** Select customers, products, quantities, and custom tax rates.
- **Automatic Inventory Deduction:** Stock levels automatically decrease upon order confirmation.
- **Stock Threshold Validation:** Prevents overselling by blocking orders that exceed available quantity.
- **Status Tracking:** Track orders through `Pending`, `Processing`, `Shipped`, `Delivered`, and `Cancelled`.

### 4. 📄 Invoice Generation & Export
- Automated generation of professional invoices for all sales orders.
- Itemized breakdowns showing subtotal, tax calculations, and final amounts.
- **Print Support:** One-click browser print integration tailored for hard-copy printing or saving as PDF.

### 5. 📦 Product & Inventory Catalog
- Expanded pre-seeded product list across Infrastructure, Hardware, Software, and Services.
- **Low-Stock Indicators:** Visual badges highlighting items falling below minimum threshold levels.

### 6. 👥 Customer Management & Payment Tracking
- Detailed directory storing customer contact details and addresses.
- Payment tracker recording payment methods, amounts, and statuses (`Pending`, `Paid`, `Partially Paid`, `Refunded`).

### 7. 📈 Sales Reports & CSV Export
- View sales metrics filtered across all transaction records.
- **CSV Export:** Download raw order history and transaction data directly to `.csv` for external analysis in Excel or Google Sheets.

### 8. 🛡️ Security Audit Logs
- Immutable activity record tracking user logins, order creations, and status modifications.

---

## 🛠️ Technology Stack

- **Structure:** HTML5
- **Styling:** Tailwind CSS (via CDN)
- **Interactivity:** JavaScript (ES6 Modules, Local State Management)
- **Data Visualization:** Chart.js
- **Iconography:** FontAwesome 6

---

## 📁 Recommended Project Folder Structure

If organizing into separate assets for production deployment:

```text
sales-management-system/
│
├── index.html            # Main HTML file (UI & View Containers)
├── css/
│   └── styles.css        # Custom CSS overrides and animations
├── js/
│   ├── app.js            # Core application state & navigation logic
│   ├── auth.js           # Authentication & permission handling
│   └── chart-config.js   # Chart.js initialization & data rendering
└── README.md             # Project documentation

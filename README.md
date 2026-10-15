Sales Management System (SalesOS)

A complete, modern, professional, user-friendly, and responsive Sales Management System website built to help businesses manage sales orders, customers, stock inventory, invoices, and analytical reports efficiently.

🌟 Key Features & Modules

Secure Authentication & Role-Based Access Control (RBAC):

Secure login & session management.

Role-based permissions separating Admin and Staff privileges.

Protected routes and automated audit logging.

Business Dashboard:

Real-time calculations of total revenue, orders, pending/completed fulfillments, and active clients.

Dynamic interactive charts powered by Chart.js.

Low-stock warnings and live activity audit trails.

Sales Order Management:

Create and track custom sales orders with automated tax, discount, and subtotal calculations.

Status tracking across Pending, Processing, Shipped, Delivered, and Cancelled.

Unique generated order numbers.

Invoice Management:

Generate, preview, and print invoices directly from confirmed orders.

Professional layout including business and client credentials, itemized lists, and payment status tracking.

Customer Management:

Add, view, edit, and deactivate customer records with validated emails and phone numbers.

Track total purchase history per client.

Product & Inventory Management:

Manage stock levels, minimum stock thresholds, and categories (Software, Hardware, Infrastructure, Services).

Automated inventory deduction upon completed sales and prevention of negative stock.

Sales Reports & Analytics:

Export summary metrics to CSV.

Date-range filtering and comprehensive revenue summaries.

🚀 Getting Started & Installation

Option 1: Running the Single-File Web Application (Frontend)

Download or save the index.html file to your local computer.

Open the file in any modern web browser (Chrome, Firefox, Safari, Edge).

Use the demo login credentials to sign in.

Option 2: Running the Python Streamlit Full Application

If you prefer the Python/SQLite implementation:

Ensure Python 3.8+ is installed on your machine.

Install the required dependencies:

pip install streamlit pandas plotly


Run the application:

streamlit run app.py


🔐 Default Demo Credentials

Role

Username

Password

Access Level

Admin

admin@salesos.com / admin

password123 / admin123

Full Access (Users, Security, Reports, Catalog)

Staff

staff@salesos.com / staff

password123 / staff123

Standard Access (Orders, Customers, Inventory)

🛠️ Technology Stack

Frontend: HTML5, Tailwind CSS, FontAwesome Icons, Chart.js / Plotly.

Backend & Logic: JavaScript (ES6+) or Python Streamlit / SQLite3.

Design System: Professional business theme featuring primary blue (#2563EB) and light gray (#F4F7FB) layouts.

📂 Project Structure

sales-management-system/
│
├── index.html         # Single-file production web application
├── app.py             # Python Streamlit full-stack implementation
└── README.md          # Project documentation and setup guide


🤝 Support & Contribution

Contributions, bug reports, and feature requests are welcome. Feel free to open an issue or submit a pull request.

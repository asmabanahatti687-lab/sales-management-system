import datetime
import sqlite3
from io import BytesIO
import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Sales Management System",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Professional Business Theme (#2563EB Blue & Light Gray)
st.markdown(
    """
    <style>
    .main { background-color: #F4F7FB; }
    .stMetric { background-color: #FFFFFF; padding: 15px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 5px solid #2563EB; }
    .card { background-color: #FFFFFF; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 20px; }
    h1, h2, h3 { color: #1E293B; }
    </style>
""",
    unsafe_allow_html=True,
)


# ==========================================
# DATABASE SETUP & INITIALIZATION
# ==========================================
def init_db():
  conn = sqlite3.connect("sales_system.db", check_same_thread=False)
  cursor = conn.cursor()

  # Users Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT,
            name TEXT
        )
    """)

  # Products Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE,
            name TEXT,
            category TEXT,
            price REAL,
            stock INTEGER,
            min_stock INTEGER
        )
    """)

  # Customers Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT
        )
    """)

  # Orders Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT UNIQUE,
            customer_name TEXT,
            order_date TEXT,
            status TEXT,
            subtotal REAL,
            tax REAL,
            discount REAL,
            total REAL
        )
    """)

  # Order Items Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT,
            product_name TEXT,
            quantity INTEGER,
            price REAL
        )
    """)

  # Payments Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_no TEXT,
            amount REAL,
            method TEXT,
            status TEXT,
            payment_date TEXT
        )
    """)

  # Audit Logs
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user TEXT,
            action TEXT
        )
    """)

  # Seed Default Data if empty
  cursor.execute("SELECT COUNT(*) FROM users")
  if cursor.fetchone()[0] == 0:
    cursor.execute(
        "INSERT INTO users (username, password, role, name) VALUES (?, ?,"
        " ?, ?)",
        ("admin", "admin123", "Admin", "System Administrator"),
    )
    cursor.execute(
        "INSERT INTO users (username, password, role, name) VALUES (?, ?,"
        " ?, ?)",
        ("staff", "staff123", "Staff", "Sales Associate"),
    )

  cursor.execute("SELECT COUNT(*) FROM products")
  if cursor.fetchone()[0] == 0:
    sample_products = [
        ("PRD-101", "Enterprise Cloud Server", "Infrastructure", 1200.00, 15, 5),
        ("PRD-102", "Secure VPN Router", "Hardware", 250.00, 40, 10),
        ("PRD-103", "Database Backup Suite", "Software", 450.00, 8, 5),
        ("PRD-104", "Wireless Access Point", "Hardware", 120.00, 25, 8),
        ("PRD-105", "IT Consulting (Hourly)", "Services", 150.00, 100, 20),
    ]
    cursor.executemany(
        "INSERT INTO products (code, name, category, price, stock, min_stock)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        sample_products,
    )

  cursor.execute("SELECT COUNT(*) FROM customers")
  if cursor.fetchone()[0] == 0:
    sample_customers = [
        (
            "Acme Corp",
            "contact@acme.com",
            "+1-555-0192",
            "123 Innovation Drive, Tech City",
        ),
        (
            "Globex Corporation",
            "info@globex.org",
            "+1-555-8391",
            "456 Industrial Pkwy, Metropolis",
        ),
        (
            "Stark Industries",
            "tony@stark.com",
            "+1-555-3821",
            "10880 Malibu Point, CA",
        ),
    ]
    cursor.executemany(
        "INSERT INTO customers (name, email, phone, address) VALUES (?, ?, ?,"
        " ?)",
        sample_customers,
    )

  conn.commit()
  return conn


conn = init_db()


def log_action(user, action):
  cursor = conn.cursor()
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  cursor.execute(
      "INSERT INTO audit_logs (timestamp, user, action) VALUES (?, ?, ?)",
      (timestamp, user, action),
  )
  conn.commit()


# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================
if "logged_in" not in st.session_state:
  st.session_state["logged_in"] = False
  st.session_state["user"] = None
  st.session_state["role"] = None
  st.session_state["name"] = None
        if submit:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, name FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user_record = cursor.fetchone()

        if user_record:
          st.session_state["logged_in"] = True
          st.session_state["user"] = username
          st.session_state["role"] = user_record[0]
          st.session_state["name"] = user_record[1]
          log_action(username, "User logged in successfully")
          st.success("Login successful! Redirecting...")
          st.rerun()
        else:
          st.error("Invalid username or password. Please try again.")

    with st.expander("ℹ️ Demo Credentials"):
      st.markdown(
          """
            - **Admin User:** `admin` / `admin123`
            - **Staff User:** `staff` / `staff123`
            """
      )


if not st.session_state["logged_in"]:
  login_page()
  st.stop()


# ==========================================
# SIDEBAR NAVIGATION & USER INFO
# ==========================================
st.sidebar.markdown(f"### Welcome, {st.session_state['name']}")
st.sidebar.caption(f"Role: **{st.session_state['role']}**")
st.sidebar.divider()

menu_options = [
    "Dashboard",
    "Sales Orders",
    "Create Order",
    "Invoice Management",
    "Customer Management",
    "Product & Inventory",
    "Sales Reports",
    "Payment Tracking",
]

if st.session_state["role"] == "Admin":
  menu_options.extend(["User Management", "Security Settings"])

menu_options.append("Logout")

selected_menu = st.sidebar.radio("Navigation", menu_options)

if selected_menu == "Logout":
  log_action(st.session_state["user"], "User logged out")
  st.session_state["logged_in"] = False
  st.session_state["user"] = None
  st.rerun()


# ==========================================
# 1. DASHBOARD
# ==========================================
if selected_menu == "Dashboard":
  st.title("📊 Business Dashboard")
  st.markdown("Overview of key sales metrics, orders, and inventory status.")

  # Fetch metrics
  df_orders = pd.read_sql("SELECT * FROM orders", conn)
  df_products = pd.read_sql("SELECT * FROM products", conn)
  df_customers = pd.read_sql("SELECT * FROM customers", conn)

  total_revenue = df_orders["total"].sum() if not df_orders.empty else 0.0
  total_orders = len(df_orders)
  pending_orders = (
      len(df_orders[df_orders["status"] == "Pending"])
      if not df_orders.empty
      else 0
  )
  completed_orders = (
      len(df_orders[df_orders["status"] == "Delivered"])
      if not df_orders.empty
      else 0
  )
  total_customers = len(df_customers)
  total_products = len(df_products)
  low_stock = len(df_products[df_products["stock"] <= df_products["min_stock"]])

  # Metric Cards
  c1, c2, c3, c4 = st.columns(4)
  c1.metric("Total Revenue", f"${total_revenue:,.2f}")
  c2.metric("Total Orders", total_orders)
  c3.metric("Pending Orders", pending_orders)
  c4.metric("Completed Orders", completed_orders)

  c5, c6, c7, c8 = st.columns(4)
  c5.metric("Total Customers", total_customers)
  c6.metric("Active Products", total_products)
  c7.metric("Low Stock Alerts", low_stock, delta_color="inverse")
  c8.metric(
      "System Status",
      "Operational",
      delta="Secure",
      delta_color="normal",
  )

  st.divider()

  # Charts
  col1, col2 = st.columns(2)
  with col1:
    st.subheader("📈 Revenue Trend")
    if not df_orders.empty:
      fig = px.line(
          df_orders,
          x="order_date",
          y="total",
          markers=True,
          title="Sales Revenue over Time",
          color_discrete_sequence=["#2563EB"],
      )
      st.plotly_chart(fig, use_container_width=True)
    else:
      st.info("No order data available for charts yet.")

  with col2:
    st.subheader("📦 Inventory Stock Levels")
    if not df_products.empty:
      fig2 = px.bar(
          df_products,
          x="name",
          y="stock",
          color="stock",
          title="Current Stock by Product",
          color_continuous_scale="Blues",
      )
      st.plotly_chart(fig2, use_container_width=True)
    else:
      st.info("No products available.")


# ==========================================
# 2.

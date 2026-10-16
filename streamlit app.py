import datetime
import sqlite3
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

  # Audit Logs Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user TEXT,
            action TEXT
        )
    """)

  # Seed Expanded Products Catalog if empty
  cursor.execute("SELECT COUNT(*) FROM products")
  if cursor.fetchone()[0] == 0:
    sample_products = [
        ("PRD-101", "Enterprise Cloud Server", "Infrastructure", 1200.00, 15, 5),
        ("PRD-102", "Secure VPN Router", "Hardware", 250.00, 40, 10),
        ("PRD-103", "Database Backup Suite", "Software", 450.00, 8, 5),
        ("PRD-104", "Wireless Access Point", "Hardware", 120.00, 25, 8),
        ("PRD-105", "IT Consulting (Hourly)", "Services", 150.00, 100, 20),
        ("PRD-106", "Cybersecurity Firewall", "Hardware", 850.00, 12, 4),
        ("PRD-107", "Project Management SaaS", "Software", 300.00, 50, 10),
        ("PRD-108", "Dedicated Storage Node", "Infrastructure", 1500.00, 6, 2),
    ]
    cursor.executemany(
        "INSERT INTO products (code, name, category, price, stock, min_stock)"
        " VALUES (?, ?, ?, ?, ?, ?)",
        sample_products,
    )

  # Seed Default Customers if empty
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
# SAFE SESSION STATE INITIALIZATION
# ==========================================
if "user" not in st.session_state:
  st.session_state["user"] = "admin"
if "role" not in st.session_state:
  st.session_state["role"] = "Admin"
if "name" not in st.session_state:
  st.session_state["name"] = "System Administrator"

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("### 📦 Sales Management System")
st.sidebar.caption(
    f"User: **{st.session_state['name']}** ({st.session_state['role']})"
)
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
    "Security Audit Logs",
]

selected_menu = st.sidebar.radio("Navigation", menu_options)


# ==========================================
# 1. DASHBOARD
# ==========================================
if selected_menu == "Dashboard":
  st.title("📊 Business Dashboard")
  st.markdown("Real-time metrics, order activities, and inventory status.")

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

  c1, c2, c3, c4 = st.columns(4)
  c1.metric("Total Revenue", f"${total_revenue:,.2f}")
  c2.metric("Total Orders", total_orders)
  c3.metric("Pending Orders", pending_orders)
  c4.metric("Delivered Orders", completed_orders)

  c5, c6, c7, c8 = st.columns(4)
  c5.metric("Total Customers", total_customers)
  c6.metric("Active Products", total_products)
  c7.metric("Low Stock Alerts", low_stock, delta_color="inverse")
  c8.metric("System Status", "Operational", delta="Secure")

  st.divider()

  col1, col2 = st.columns(2)
  with col1:
    st.subheader("📈 Revenue Trends")
    if not df_orders.empty:
      fig = px.line(
          df_orders,
          x="order_date",
          y="total",
          markers=True,
          color_discrete_sequence=["#2563EB"],
      )
      st.plotly_chart(fig, use_container_width=True)
    else:
      st.info("No order history available.")

  with col2:
    st.subheader("📦 Inventory Stock Levels")
    if not df_products.empty:
      fig2 = px.bar(
          df_products,
          x="name",
          y="stock",
          color="stock",
          color_continuous_scale="Blues",
      )
      st.plotly_chart(fig2, use_container_width=True)
    else:
      st.info("No products available.")


# ==========================================
# 2. SALES ORDERS
# ==========================================
elif selected_menu == "Sales Orders":
  st.title("📋 Sales Orders")
  st.markdown("Manage customer orders, track fulfillment status, and filter data.")

  df_orders = pd.read_sql("SELECT * FROM orders", conn)

  if not df_orders.empty:
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Pending", "Processing", "Shipped", "Delivered", "Cancelled"],
    )
    if status_filter != "All":
      df_orders = df_orders[df_orders["status"] == status_filter]

    st.dataframe(df_orders, use_container_width=True)

    st.subheader("Update Order Status")
    with st.form("update_order_form"):
      order_to_update = st.selectbox(
          "Select Order No", df_orders["order_no"].tolist()
      )
      new_status = st.selectbox(
          "New Status",
          ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"],
      )
      update_btn = st.form_submit_button("Update Status")

      if update_btn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE orders SET status = ? WHERE order_no = ?",
            (new_status, order_to_update),
        )
        conn.commit()
        log_action(
            st.session_state["user"],
            f"Updated order {order_to_update} status to {new_status}",
        )
        st.success(f"Order {order_to_update} updated successfully!")
        st.rerun()
  else:
    st.info("No sales orders recorded yet.")


# ==========================================
# 3. CREATE ORDER
# ==========================================
elif selected_menu == "Create Order":
  st.title("➕ Create New Sales Order")

  customers = pd.read_sql("SELECT * FROM customers", conn)
  products = pd.read_sql("SELECT * FROM products", conn)

  if customers.empty or products.empty:
    st.warning("Please add customers and products before creating an order.")
  else:
    with st.form("create_order_form"):
      customer_name = st.selectbox(
          "Select Customer", customers["name"].tolist()
      )
      selected_product = st.selectbox(
          "Select Product", products["name"].tolist()
      )
      quantity = st.number_input(
          "Quantity", min_value=1, value=1, step=1
      )
      discount = st.number_input(
          "Discount ($)", min_value=0.0, value=0.0, step=1.0
      )
      tax_rate = st.slider("Tax Rate (%)", 0.0, 20.0, 5.0)

      submit_order = st.form_submit_button("Confirm & Create Order")

      if submit_order:
        prod_row = products[products["name"] == selected_product].iloc[0]
        current_stock = prod_row["stock"]
        unit_price = prod_row["price"]

        if quantity > current_stock:
          st.error(
              f"Insufficient stock! Available quantity: {current_stock}"
          )
        else:
          subtotal = unit_price * quantity
          tax_amount = (subtotal - discount) * (tax_rate / 100)
          final_total = max(0.0, subtotal - discount + tax_amount)

          order_no = f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
          order_date = datetime.datetime.now().strftime("%Y-%m-%d")

          cursor = conn.cursor()
          cursor.execute(
              """
                        INSERT INTO orders (order_no, customer_name, order_date, status, subtotal, tax, discount, total)
                        VALUES (?, ?, ?, 'Pending', ?, ?, ?, ?)
                    """,
              (
                  order_no,
                  customer_name,
                  order_date,
                  subtotal,
                  tax_amount,
                  discount,
                  final_total,
              ),
          )

          cursor.execute(
              """
                        INSERT INTO order_items (order_no, product_name, quantity, price)
                        VALUES (?, ?, ?, ?)
                    """,
              (order_no, selected_product, quantity, unit_price),
          )

          new_stock = current_stock - quantity
          cursor.execute(
              "UPDATE products SET stock = ? WHERE name = ?",
              (new_stock, selected_product),
          )

          cursor.execute(
              """
                        INSERT INTO payments (order_no, amount, method, status, payment_date)
                        VALUES (?, ?, 'Credit Card', 'Pending', ?)
                    """,
              (order_no, final_total, order_date),
          )

          conn.commit()
          log_action(
              st.session_state["user"],
              f"Created new order {order_no} for {customer_name}",
          )
          st.success(
              f"Order {order_no} created successfully! Total: ${final_total:,.2f}"
          )


# ==========================================
# 4. INVOICE MANAGEMENT
# ==========================================
elif selected_menu == "Invoice Management":
  st.title("📄 Invoice Management")
  st.markdown("View and preview generated invoices for sales orders.")

  df_orders = pd.read_sql("SELECT * FROM orders", conn)

  if not df_orders.empty:
    selected_invoice = st.selectbox(
        "Select Order for Invoice", df_orders["order_no"].tolist()
    )
    order_info = df_orders[df_orders["order_no"] == selected_invoice].iloc[0]

    items = pd.read_sql(
        f"SELECT * FROM order_items WHERE order_no = '{selected_invoice}'", conn
    )

    st.markdown(
        f"""
        <div class="card">
            <h3>INVOICE #{order_info['order_no']}</h3>
            <p><b>Date:</b> {order_info['order_date']}</p>
            <p><b>Customer:</b> {order_info['customer_name']}</p>
            <p><b>Status:</b> {order_info['status']}</p>
            <hr>
            <h4>Order Items:</h4>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(items, use_container_width=True)

    st.markdown(
        f"""
            <hr>
            <p><b>Subtotal:</b> ${order_info['subtotal']:,.2f}</p>
            <p><b>Discount:</b> ${order_info['discount']:,.2f}</p>
            <p><b>Tax:</b> ${order_info['tax']:,.2f}</p>
            <h3><b>Final Amount:</b> ${order_info['total']:,.2f}</h3>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🖨️ Print / Export Invoice"):
      st.success(
          "Invoice ready for printing! Use your browser's print command (Ctrl+P"
          " / Cmd+P)."
      )
  else:
    st.info("No invoices available.")


# ==========================================
# 5. CUSTOMER MANAGEMENT
# ==========================================
elif selected_menu == "Customer Management":
  st.title("👥 Customer Management")

  tab1, tab2 = st.tabs(["View Customers", "Add Customer"])

  with tab1:
    df_customers = pd.read_sql("SELECT * FROM customers", conn)
    st.dataframe(df_customers, use_container_width=True)

  with tab2:
    with st.form("add_customer_form"):
      name = st.text_input("Customer/Company Name")
      email = st.text_input("Email Address")
      phone = st.text_input("Phone Number")
      address = st.text_area("Billing Address")
      submit_cust = st.form_submit_button("Save Customer")

      if submit_cust:
        if name and email:
          cursor = conn.cursor()
          cursor.execute(
              "INSERT INTO customers (name, email, phone, address) VALUES (?,"
              " ?, ?, ?)",
              (name, email, phone, address),
          )
          conn.commit()
          log_action(
              st.session_state["user"], f"Added new customer: {name}"
          )
          st.success("Customer added successfully!")
          st.rerun()
        else:
          st.error("Please fill in Name and Email.")


# ==========================================
# 6. PRODUCT & INVENTORY MANAGEMENT
# ==========================================
elif selected_menu == "Product & Inventory":
  st.title("📦 Product & Inventory Management")

  tab1, tab2 = st.tabs(["Inventory Catalog", "Add Product"])

  with tab1:
    df_products = pd.read_sql("SELECT * FROM products", conn)
    st.dataframe(df_products, use_container_width=True)

    low_stock_df = df_products[
        df_products["stock"] <= df_products["min_stock"]
    ]
    if not low_stock_df.empty:
      st.warning(
          "⚠️ Low stock alert for the following items:"
          f" {', '.join(low_stock_df['name'].tolist())}"
      )

  with tab2:
    with st.form("add_product_form"):
      code = st.text_input("Product Code (e.g., PRD-109)")
      name = st.text_input("Product Name")
      category = st.selectbox(
          "Category", ["Infrastructure", "Hardware", "Software", "Services"]
      )
      price = st.number_input("Selling Price ($)", min_value=0.0, value=100.0)
      stock = st.number_input(
          "Initial Stock Quantity", min_value=0, value=10, step=1
      )
      min_stock = st.number_input(
          "Minimum Stock Threshold", min_value=0, value=5, step=1
      )
      submit_prod = st.form_submit_button("Add Product")

      if submit_prod:
        if code and name:
          try:
            cursor = conn.cursor()
            cursor.execute(
                """
                            INSERT INTO products (code, name, category, price, stock, min_stock)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """,
                (code, name, category, price, stock, min_stock),
            )
            conn.commit()
            log_action(st.session_state["user"], f"Added product: {name}")
            st.success("Product added successfully!")
            st.rerun()
          except sqlite3.IntegrityError:
            st.error("Product code already exists.")
        else:
          st.error("Please fill in Product Code and Name.")


# ==========================================
# 7. SALES REPORTS
# ==========================================
elif selected_menu == "Sales Reports":
  st.title("📈 Sales Reports & Analytics")

  df_orders = pd.read_sql("SELECT * FROM orders", conn)

  if not df_orders.empty:
    total_revenue = df_orders["total"].sum()
    st.metric("Total Revenue", f"${total_revenue:,.2f}")

    col1, col2 = st.columns(2)
    with col1:
      fig = px.bar(
          df_orders,
          x="customer_name",
          y="total",
          color="customer_name",
          title="Sales by Customer",
      )
      st.plotly_chart(fig, use_container_width=True)

    with col2:
      fig2 = px.pie(
          df_orders,
          names="status",
          values="total",
          title="Revenue Share by Order Status",
      )
      st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📥 Export Reports")
    csv_data = df_orders.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Sales Report (CSV)",
        data=csv_data,
        file_name="sales_report.csv",
        mime="text/csv",
    )
  else:
    st.info("No data available for reports.")


# ==========================================
# 8. PAYMENT TRACKING
# ==========================================
elif selected_menu == "Payment Tracking":
  st.title("💳 Payment Tracking")

  df_payments = pd.read_sql("SELECT * FROM payments", conn)
  if not df_payments.empty:
    st.dataframe(df_payments, use_container_width=True)

    with st.form("update_payment"):
      payment_id = st.selectbox(
          "Select Payment Record ID", df_payments["id"].tolist()
      )
      new_pay_status = st.selectbox(
          "Payment Status", ["Pending", "Partially Paid", "Paid", "Refunded"]
      )
      pay_btn = st.form_submit_button("Update Payment Status")

      if pay_btn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE payments SET status = ? WHERE id = ?",
            (new_pay_status, payment_id),
        )
        conn.commit()
        log_action(
            st.session_state["user"],
            f"Updated payment ID {payment_id} to {new_pay_status}",
        )
        st.success("Payment status updated!")
        st.rerun()
  else:
    st.info("No payment records found.")


# ==========================================
# 9. SECURITY AUDIT LOGS
# ==========================================
elif selected_menu == "Security Audit Logs":
  st.title("🛡️ Security Audit Logs")
  df_logs = pd.read_sql(
      "SELECT * FROM audit_logs ORDER BY id DESC", conn
  )
  st.dataframe(df_logs, use_container_width=True)

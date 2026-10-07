import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

from ViewModels.database import create_table, create_action_table
from Models.foodmodel import FoodItem
from ViewModels.inventory import (
    calculate_status,
    add_food_item,
    get_all_items,
    get_items_by_name_or_category,
    get_item_by_id,
    update_food_item,
    delete_food_item,
    ExpiryStatus,
    save_item_actionstatus,
    get_item_actions,
    ActionStatus,
)
from ViewModels.validation import (
    validate_datetime,
    validate_quantity,
    validate_expiry_date,
)

create_table()
create_action_table()

st.set_page_config(
    page_title="FoodWise",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

COLORS = {
    "primary": "#10b981",
    "primary_dark": "#059669",
    "secondary": "#f59e0b",
    "danger": "#ef4444",
    "bg_light": "#f8fafc",
    "bg_card": "#ffffff",
    "text_primary": "#1e293b",
    "text_secondary": "#64748b",
}

st.markdown(
    f"""
    <style>
        * {{ font-family: 'Segoe UI', sans-serif; }}
        .stApp {{ background: linear-gradient(135deg, {COLORS['bg_light']} 0%, #eef2ff 100%); }}
        .block-container {{ padding-top: 1.5rem; padding-left: 2rem; padding-right: 2rem; max-width: 1400px; }}
        h1, h2, h3 {{ color: {COLORS['text_primary']}; font-weight: 700; }}
        .page-title {{ font-size: 32px; font-weight: 700; color: {COLORS['text_primary']}; margin-bottom: 0.2rem; }}
        .page-subtitle {{ font-size: 14px; color: {COLORS['text_secondary']}; margin-bottom: 1rem; }}
        .metric-card {{
            padding: 20px 18px; border-radius: 16px; color: white;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.18);
            margin-bottom: 1rem;
        }}
        .metric-card p {{ margin:0; }}
        .metric-card .value {{ font-size: 30px; font-weight: 700; margin-top: 8px; }}
        div.stButton > button {{
            width: 100%; border-radius: 12px; border: none;
            background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary_dark']} 100%);
            color: white; font-weight: 700; height: 48px; box-shadow: 0 8px 20px rgba(16, 185, 129, 0.15);
        }}
        div.stButton > button:hover {{
            transform: translateY(-1px); box-shadow: 0 12px 22px rgba(16, 185, 129, 0.22);
        }}
        .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > select {{
            border-radius: 10px !important; border: 1px solid #dbe3ef !important; padding: 10px 12px !important;
        }}
        .stDataFrame {{ border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.06); }}
        .card {{
            background: white; border: 1px solid #e2e8f0; border-radius: 14px; padding: 18px; box-shadow: 0 4px 14px rgba(0,0,0,0.05);
        }}
        .stAlert {{ border-radius: 12px; }}
    </style>
    """,
    unsafe_allow_html=True,
)

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"

nav_items = [
    ("🏠 Dashboard", "Dashboard"),
    ("➕ Add Food", "Add Food Item"),
    ("📦 Inventory", "View Inventory"),
    ("🔍 Search", "Search Item"),
    ("⏰ Expiry", "Expiry Monitor"),
    ("♻️ Waste", "Waste / Donation"),
    ("📊 Summary", "Inventory Summary"),
]

nav_cols = st.columns(len(nav_items))
for col, (label, menu_value) in zip(nav_cols, nav_items):
    with col:
        if st.button(label, use_container_width=True, key=f"nav_{menu_value}"):
            st.session_state.menu = menu_value

st.markdown("---")
menu = st.session_state.menu

# Helper function for status display

def get_status_label(expiry_date):
    status = calculate_status(expiry_date)
    if status == ExpiryStatus.AVAILABLE:
        return "🟢 Available"
    if status == ExpiryStatus.EXPIRING_SOON:
        return "🟠 Expiring Soon"
    return "🔴 Expired"

if menu == "Dashboard":
    items = get_all_items()
    total_items = len(items)
    total_quantity = sum(item[3] for item in items)
    available_count = 0
    expiring_soon_count = 0
    expired_count = 0
    waste_count = 0
    donation_count = 0

    for item in items:
        expiry_date = datetime.strptime(item[6], "%Y-%m-%d").date()
        status = calculate_status(expiry_date)

        if status == ExpiryStatus.AVAILABLE:
            available_count += 1
        elif status == ExpiryStatus.EXPIRING_SOON:
            expiring_soon_count += 1
        elif status == ExpiryStatus.EXPIRED:
            expired_count += 1

        for action in get_item_actions(item[1]):
            if action[1] == ActionStatus.WASTE.value:
                waste_count += 1
            elif action[1] == ActionStatus.DONATION.value:
                donation_count += 1

    st.markdown('<div class="page-title">👋 Welcome to FoodWise</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Manage your food inventory, track expiry dates, and reduce food waste.</div>', unsafe_allow_html=True)

    metrics = st.columns(4)
    with metrics[0]:
        st.markdown(f'<div class="metric-card"><p>📦 Food Items</p><p class="value">{total_items}</p></div>', unsafe_allow_html=True)
    with metrics[1]:
        st.markdown(f'<div class="metric-card"><p>⚖️ Total Quantity</p><p class="value">{total_quantity:g}</p></div>', unsafe_allow_html=True)
    with metrics[2]:
        st.markdown(f'<div class="metric-card"><p>🟢 Available</p><p class="value">{available_count}</p></div>', unsafe_allow_html=True)
    with metrics[3]:
        st.markdown(f'<div class="metric-card"><p>🟠 Expiring Soon</p><p class="value">{expiring_soon_count}</p></div>', unsafe_allow_html=True)

    st.write("")

    health_col, insight_col = st.columns([1.8, 1.2])

    with health_col:
        st.subheader("📊 Inventory Health")
        if total_items > 0:
            healthy_percentage = (available_count / total_items) * 100
            st.write(f"**{healthy_percentage:.0f}%** of your food inventory is currently available.")
            st.progress(min(healthy_percentage / 100, 1.0))
        else:
            st.info("Your inventory is empty. Add food items to get started.")

        st.write("")

        if total_items > 0:
            labels = ["Available", "Expiring Soon", "Expired"]
            values = [available_count, expiring_soon_count, expired_count]
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=["#10b981", "#f59e0b", "#ef4444"]))])
            fig.update_layout(height=340, margin=dict(l=10, r=10, t=20, b=20), paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

    with insight_col:
        st.subheader("💡 Quick Summary")
        st.markdown(
            f"""
            <div class="card">
                <p><strong>Available:</strong> {available_count}</p>
                <p><strong>Expiring Soon:</strong> {expiring_soon_count}</p>
                <p><strong>Expired:</strong> {expired_count}</p>
                <p><strong>Waste:</strong> {waste_count}</p>
                <p><strong>Donation:</strong> {donation_count}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        if expired_count > 0:
            st.error(f"🔴 {expired_count} item(s) have expired.")
        elif expiring_soon_count > 0:
            st.warning(f"🟠 {expiring_soon_count} item(s) are expiring soon.")
        else:
            st.success("✅ No urgent items found.")

    st.write("")

    impact_col1, impact_col2 = st.columns(2)
    with impact_col1:
        st.markdown(f"<div class='card'><h3>🎁 Donations</h3><h2>{donation_count}</h2></div>", unsafe_allow_html=True)
    with impact_col2:
        st.markdown(f"<div class='card'><h3>♻️ Waste</h3><h2>{waste_count}</h2></div>", unsafe_allow_html=True)

elif menu == "Add Food Item":
    st.markdown('<div class="page-title">➕ Add Food Item</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Add a new food item to your inventory</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        item_id = st.text_input("Item ID")
        name = st.text_input("Food Name")
        category = st.selectbox("Category", ["Dairy", "Vegetables", "Fruits", "Grains", "Meat", "Other"])
        quantity = st.number_input("Quantity", min_value=0.0, step=0.1)
    with col2:
        unit = st.selectbox("Unit", ["kg", "grams", "litres", "pieces"])
        purchase_date = st.date_input("Purchase Date")
        expiry_date = st.date_input("Expiry Date")

    if st.button("Add Food Item"):
        try:
            validate_quantity(quantity)
            validate_datetime(purchase_date.isoformat())
            validate_datetime(expiry_date.isoformat())
            validate_expiry_date(purchase_date, expiry_date)

            add_food_item(
                FoodItem(
                    id=item_id,
                    name=name,
                    category=category,
                    quantity=quantity,
                    unit=unit,
                    purchase_date=purchase_date,
                    expiry_date=expiry_date,
                )
            )
            st.success(f"Food item '{name}' added successfully!")
        except ValueError as e:
            st.error(str(e))

elif menu == "View Inventory":
    st.markdown('<div class="page-title">📦 Inventory</div>', unsafe_allow_html=True)
    items = get_all_items()
    if items:
        df = pd.DataFrame(items, columns=["ID", "Name", "Category", "Quantity", "Unit", "Purchase Date", "Expiry Date"])
        df["Status"] = df["Expiry Date"].apply(lambda x: get_status_label(datetime.strptime(x, "%Y-%m-%d").date()))
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No items in inventory.")

elif menu == "Search Item":
    st.markdown('<div class="page-title">🔍 Search Food</div>', unsafe_allow_html=True)
    search_text = st.text_input("Enter food name or category")
    if st.button("Search"):
        if search_text:
            results = get_items_by_name_or_category(search_text)
            if results:
                df = pd.DataFrame(results, columns=["ID", "Name", "Category", "Quantity", "Unit", "Purchase Date", "Expiry Date"])
                df["Status"] = df["Expiry Date"].apply(lambda x: get_status_label(datetime.strptime(x, "%Y-%m-%d").date()))
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.warning("No items found.")
        else:
            st.error("Please enter a search term.")

elif menu == "Expiry Monitor":
    st.markdown('<div class="page-title">⏰ Expiry Monitor</div>', unsafe_allow_html=True)
    items = get_all_items()

    expiring_soon = []
    expired = []
    available = []

    for item in items:
        expiry_date = datetime.strptime(item[6], "%Y-%m-%d").date()
        status = calculate_status(expiry_date)
        if status == ExpiryStatus.EXPIRING_SOON:
            expiring_soon.append(item)
        elif status == ExpiryStatus.EXPIRED:
            expired.append(item)
        else:
            available.append(item)

    tabs = st.tabs(["🟠 Expiring Soon", "🔴 Expired", "🟢 Available"])
    with tabs[0]:
        if expiring_soon:
            df = pd.DataFrame(expiring_soon, columns=["ID", "Name", "Category", "Quantity", "Unit", "Purchase Date", "Expiry Date"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.success("No expiring soon items.")

    with tabs[1]:
        if expired:
            df = pd.DataFrame(expired, columns=["ID", "Name", "Category", "Quantity", "Unit", "Purchase Date", "Expiry Date"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.success("No expired items.")

    with tabs[2]:
        if available:
            df = pd.DataFrame(available, columns=["ID", "Name", "Category", "Quantity", "Unit", "Purchase Date", "Expiry Date"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No available items.")

elif menu == "Waste / Donation":
    st.markdown('<div class="page-title">♻️ Waste / Donation</div>', unsafe_allow_html=True)
    items = get_all_items()
    if items:
        df = pd.DataFrame(items, columns=["ID", "Name", "Category", "Quantity", "Unit", "Purchase Date", "Expiry Date"])
        st.dataframe(df, use_container_width=True, hide_index=True)

        item_id = st.text_input("Enter Item ID")
        action = st.selectbox("Action", ["Mark as Waste", "Mark as Donation"])
        action_status = ActionStatus.WASTE if action == "Mark as Waste" else ActionStatus.DONATION

        if st.button("Submit"):
            if item_id:
                item = get_item_by_id(item_id)
                if not item:
                    st.error("Item not found.")
                else:
                    save_item_actionstatus(item[1], action_status, datetime.now().date())
                    st.success(f"Food item with ID '{item_id}' marked as '{action}'.")
            else:
                st.error("Please enter an Item ID.")
    else:
        st.warning("No items available in inventory.")

elif menu == "Inventory Summary":
    st.markdown('<div class="page-title">📊 Inventory Summary</div>', unsafe_allow_html=True)
    items = get_all_items()
    if items:
        total_items = len(items)
        total_quantity = sum(item[3] for item in items)
        category_counts = {}
        for item in items:
            category_counts[item[2]] = category_counts.get(item[2], 0) + 1

        metrics = st.columns(3)
        with metrics[0]:
            st.metric("Total Items", total_items)
        with metrics[1]:
            st.metric("Total Quantity", f"{total_quantity:g}")
        with metrics[2]:
            st.metric("Categories", len(category_counts))

        st.write("")
        st.subheader("Items by Category")
        fig = px.bar(x=list(category_counts.keys()), y=list(category_counts.values()), color=list(category_counts.values()))
        fig.update_layout(height=350, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Waste / Donation History")
        item_actions = []
        for item in items:
            actions = get_item_actions(item[1])
            item_actions.extend([(action[0], action[1], action[2]) for action in actions])
        if item_actions:
            df_actions = pd.DataFrame(item_actions, columns=["Item Name", "Action", "Action Date"])
            st.dataframe(df_actions, use_container_width=True, hide_index=True)
        else:
            st.info("No discard/donation history available.")
    else:
        st.info("No items available in inventory.")

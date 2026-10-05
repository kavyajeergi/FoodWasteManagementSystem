import pandas as pd
import streamlit as st

from ViewModels.database import create_table, create_action_table
from Models.foodmodel import FoodItem, ItemAction
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
from datetime import datetime

create_table()  # Ensure the database table is created when the app starts

create_action_table()

# --------------------------------------------------
# TOP NAVIGATION
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #F7F9F6;
    }

    /* Remove default top padding */
    .block-container {
        padding-top: 1rem;
    }

    /* App title */
    .app-title {
        font-size: 30px;
        font-weight: 700;
        color: #2E4D3A;
        margin-bottom: 2px;
    }

    .app-subtitle {
        color: #718076;
        font-size: 14px;
        margin-bottom: 18px;
    }

    /* Navigation buttons */
    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #DDE7DF;
        background-color: #FFFFFF;
        color: #405548;
        font-weight: 600;
        height: 45px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        background-color: #E8F3EA;
        border-color: #A8C7AF;
        color: #285438;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

col1, col2 = st.columns([2.5, 1])

with col1:
    st.markdown(
        """
        <div style="
            text-align:left;
            padding-top:10px;
        ">
        <div class="app-title">
            🍎 FoodWise
        </div>

        <div class="app-subtitle">
            Smart Food Inventory & Waste Management
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div style="
            text-align:right;
            padding-top:10px;
            color:#718076;
            font-size:14px;
        ">
            🌱 Reduce Waste • Save Food
        </div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# NAVIGATION
# --------------------------------------------------

nav1, nav2, nav3, nav4, nav5, nav6, nav7 = st.columns(7)

if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"


with nav1:
    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.menu = "Dashboard"

with nav2:
    if st.button("➕ Add Food", use_container_width=True):
        st.session_state.menu = "Add Food Item"

with nav3:
    if st.button("📦 Inventory", use_container_width=True):
        st.session_state.menu = "View Inventory"

with nav4:
    if st.button("🔍 Search", use_container_width=True):
        st.session_state.menu = "Search Item"

with nav5:
    if st.button("⏰ Expiry", use_container_width=True):
        st.session_state.menu = "Expiry Monitor"

with nav6:
    if st.button("♻️ Waste", use_container_width=True):
        st.session_state.menu = "Waste / Donation"

with nav7:
    if st.button("📊 Summary", use_container_width=True):
        st.session_state.menu = "Inventory Summary"


menu = st.session_state.menu

st.divider()

if menu == "Dashboard":
    st.header("🍎 Food Waste Management")

    items = get_all_items()

    # --------------------------------------------------
    # Calculate dashboard statistics
    # --------------------------------------------------

    total_items = len(items)
    total_quantity = 0

    available_count = 0
    expiring_soon_count = 0
    expired_count = 0

    waste_count = 0
    donation_count = 0

    for item in items:

        total_quantity += item[3]

        # Expiry status
        expiry_date = datetime.strptime(
            item[6], "%Y-%m-%d"
        ).date()

        status = calculate_status(expiry_date)

        if status == ExpiryStatus.AVAILABLE:
            available_count += 1

        elif status == ExpiryStatus.EXPIRING_SOON:
            expiring_soon_count += 1

        elif status == ExpiryStatus.EXPIRED:
            expired_count += 1

        # Waste / Donation history
        actions = get_item_actions(item[1])

        for action in actions:

            if action[1] == ActionStatus.WASTE.value:
                waste_count += 1

            elif action[1] == ActionStatus.DONATION.value:
                donation_count += 1

    # --------------------------------------------------
    # Welcome section
    # --------------------------------------------------

    st.markdown(
        """
        <div style="
            padding: 25px;
            border-radius: 18px;
            background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
            margin-bottom: 25px;
        ">

        <h2 style="margin-bottom:5px;">
            👋 Welcome to your Food Dashboard
        </h2>

        <p style="
            font-size:16px;
            color:#555;
            margin-bottom:0;
        ">
            Keep track of your food, reduce waste, and make the most
            of your inventory.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Main summary
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📦 Food Items",
            total_items
        )

    with col2:
        st.metric(
            "⚖️ Total Quantity",
            f"{total_quantity:g}"
        )

    with col3:
        st.metric(
            "🟢 Available",
            available_count
        )

    st.write("")

    # --------------------------------------------------
    # Inventory Health
    # --------------------------------------------------

    st.subheader("📊 Inventory Health")

    if total_items > 0:

        healthy_percentage = (
            available_count / total_items
        ) * 100

        st.write(
            f"**{healthy_percentage:.0f}%** of your food inventory "
            "is currently available."
        )

        st.progress(
            min(healthy_percentage / 100, 1.0)
        )

    else:

        st.info(
            "Your inventory is empty. Add some food items to get started."
        )

    st.write("")

    # --------------------------------------------------
    # Needs Attention
    # --------------------------------------------------

    st.subheader("⚠️ Needs Attention")

    attention_col1, attention_col2 = st.columns(2)

    with attention_col1:

        if expiring_soon_count > 0:

            st.warning(
                f"🟠 **{expiring_soon_count} item(s)** "
                "are expiring soon."
            )

        else:

            st.success(
                "✅ No food items are expiring soon."
            )

    with attention_col2:

        if expired_count > 0:

            st.error(
                f"🔴 **{expired_count} item(s)** "
                "have expired."
            )

        else:

            st.success(
                "✅ No expired food items."
            )

    st.write("")

    # --------------------------------------------------
    # Inventory status chart
    # --------------------------------------------------

    st.subheader("📈 Inventory Overview")

    chart_data = pd.DataFrame(
        {
            "Status": [
                "Available",
                "Expiring Soon",
                "Expired"
            ],
            "Items": [
                available_count,
                expiring_soon_count,
                expired_count
            ]
        }
    )

    st.bar_chart(
        chart_data.set_index("Status")
    )

    st.write("")

    # --------------------------------------------------
    # Waste & Donation
    # --------------------------------------------------

    st.subheader("♻️ Food Impact")

    impact_col1, impact_col2 = st.columns(2)

    with impact_col1:

        st.markdown(
            f"""
            <div style="
                padding:20px;
                border-radius:15px;
                background:#FFF8E1;
                border-left:6px solid #FFB300;
            ">

            <h3 style="margin:0;">
                🎁 {donation_count}
            </h3>

            <p style="margin:5px 0 0 0;">
                Food Donations
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    with impact_col2:

        st.markdown(
            f"""
            <div style="
                padding:20px;
                border-radius:15px;
                background:#FFEBEE;
                border-left:6px solid #E53935;
            ">

            <h3 style="margin:0;">
                ♻️ {waste_count}
            </h3>

            <p style="margin:5px 0 0 0;">
                Food Waste
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # --------------------------------------------------
    # Smart suggestion
    # --------------------------------------------------

    st.subheader("💡 Smart Suggestion")

    if expired_count > 0:

        st.error(
            "Some food items have already expired. "
            "Consider reviewing them in the Expiry Monitor."
        )

    elif expiring_soon_count > 0:

        st.warning(
            "Some food items are expiring soon. "
            "Consider consuming or donating them before they expire."
        )

    elif total_items == 0:

        st.info(
            "Start by adding your first food item."
        )

    else:

        st.success(
            "🎉 Great job! Your inventory is in good shape."
        )

st.write(f"You selected: {menu}")

if menu == "Add Food Item":
    st.header("➕ Add Food Item")

    item_id = st.text_input("Item ID")

    name = st.text_input("Food Name")

    category = st.selectbox(
        "Category", ["Dairy", "Vegetables", "Fruits", "Grains", "Meat", "Other"]
    )

    quantity = st.number_input("Quantity", min_value=0.0)

    unit = st.selectbox("Unit", ["kg", "grams", "litres", "pieces"])

    purchase_date = st.date_input("Purchase Date")

    expiry_date = st.date_input("Expiry Date")

    if st.button("Add Food Item"):
        try:
            # Validate inputs
            validate_quantity(quantity)
            validate_datetime(purchase_date.isoformat())
            validate_datetime(expiry_date.isoformat())
            validate_expiry_date(purchase_date, expiry_date)

            # Create a FoodItem instance
            new_item = FoodItem(
                id=item_id,
                name=name,
                category=category,
                quantity=quantity,
                unit=unit,
                purchase_date=purchase_date,
                expiry_date=expiry_date,
            )

            # Add the food item to the database
            add_food_item(new_item)

            st.success(f"Food item '{name}' added successfully!")

        except ValueError as e:
            st.error(str(e))


if menu == "View Inventory":
    st.header("📦 Food Inventory")

    items = get_all_items()

    df = pd.DataFrame(
        items,
        columns=[
            "ID",
            "Name",
            "Category",
            "Quantity",
            "Unit",
            "Purchase Date",
            "Expiry Date",
        ],
    )

    st.dataframe(df, use_container_width=True)

if menu == "Search Item":
    st.header("🔍 Search Food")

    search_text = st.text_input("Enter food name or category")

    if st.button("Search"):
        if search_text:
            results = get_items_by_name_or_category(search_text)

            if results:
                df_results = pd.DataFrame(
                    results,
                    columns=[
                        "ID",
                        "Name",
                        "Category",
                        "Quantity",
                        "Unit",
                        "Purchase Date",
                        "Expiry Date",
                    ],
                )

                st.dataframe(df_results, use_container_width=True)

            else:
                st.warning("No items found matching your search.")
        else:
            st.error("Please enter a search term.")

if menu == "Update Quantity":
    st.header("📈 Update Food Quantity")

    item_id = st.text_input("Enter Item ID to update")

    operation = st.selectbox("Operation", ["Increase", "Decrease"])

    amount = st.number_input("Amount to adjust", min_value=0.0)

    if st.button("Update Quantity"):
        if item_id and amount > 0:
            try:
                # Fetch current quantity from the database
                item = get_item_by_id(item_id)
                purchase_date = datetime.strptime(item[5], "%Y-%m-%d").date()

                expiry_date = datetime.strptime(item[6], "%Y-%m-%d").date()

                if not item:
                    st.error("Item not found.")
                else:
                    current_quantity = item[3]  # Assuming quantity is the 4th column

                    if operation == "Increase":
                        new_quantity = current_quantity + amount
                    else:  # Decrease
                        new_quantity = current_quantity - amount

                    if new_quantity < 0:
                        st.error("Quantity cannot be negative.")
                    else:
                        # Update the quantity in the database
                        update_food_item(
                            FoodItem(
                                id=item_id,
                                name=item[1],
                                category=item[2],
                                quantity=new_quantity,
                                unit=item[4],
                                purchase_date=purchase_date,
                                expiry_date=expiry_date,
                            )
                        )
                        st.success(
                            f"Quantity updated successfully. New quantity: {new_quantity}"
                        )
            except ValueError as e:
                st.error(str(e))

            except Exception as e:
                st.error(f"Database error: {e}")

if menu == "Remove Item":
    st.header("🗑️ Remove Food Item")

    item_id = st.text_input("Enter Item ID to remove")

    if st.button("Remove Item"):
        if item_id:
            try:
                # Fetch the item to ensure it exists
                item = get_item_by_id(item_id)
                if not item:
                    st.error("Item not found.")
                else:
                    # Remove the item from the database
                    delete_food_item(item_id)
                    st.success(f"Food item with ID '{item_id}' removed successfully.")
            except Exception as e:
                st.error(f"Database error: {e}")
        else:
            st.error("Please enter an Item ID.")

if menu == "Expiry Monitor":
    st.header("⏰ Expiry Monitor")

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

    if expiring_soon:
        st.subheader("Items Expiring Soon")
        df_expiring_soon = pd.DataFrame(
            expiring_soon,
            columns=[
                "ID",
                "Name",
                "Category",
                "Quantity",
                "Unit",
                "Purchase Date",
                "Expiry Date",
            ],
        )
        st.dataframe(df_expiring_soon, use_container_width=True)

    if expired:
        st.subheader("Expired Items")

        df_expired = pd.DataFrame(
            expired,
            columns=[
                "ID",
                "Name",
                "Category",
                "Quantity",
                "Unit",
                "Purchase Date",
                "Expiry Date",
            ],
        )
        st.dataframe(df_expired, use_container_width=True)

    if available:
        st.subheader("Available Items")

        df_available = pd.DataFrame(
            available,
            columns=[
                "ID",
                "Name",
                "Category",
                "Quantity",
                "Unit",
                "Purchase Date",
                "Expiry Date",
            ],
        )
        st.dataframe(df_available, use_container_width=True)

if menu == "Waste / Donation":
    st.header("♻️ Waste / Donation Management")

    items = get_all_items()

    if items:
        df = pd.DataFrame(
            items,
            columns=[
                "ID",
                "Name",
                "Category",
                "Quantity",
                "Unit",
                "Purchase Date",
                "Expiry Date",
            ],
        )

        st.dataframe(df, use_container_width=True)

        item_id = st.text_input("Enter Item ID to mark as Waste/Donation")

        action = st.selectbox("Action", ["Mark as Waste", "Mark as Donation"])

        if action == "Mark as Waste":
            action_status = ActionStatus.WASTE
        else:
            action_status = ActionStatus.DONATION

        if st.button("Submit"):
            if item_id:
                try:
                    # Fetch the item to ensure it exists
                    item = get_item_by_id(item_id)
                    if not item:
                        st.error("Item not found.")
                    else:
                        save_item_actionstatus(
                            item[1], action_status, datetime.now().date()
                        )
                        st.success(
                            f"Food item with ID '{item_id}' marked as '{action}'."
                        )
                except Exception as e:
                    st.error(f"Database error: {e}")
            else:
                st.error("Please enter an Item ID.")
    else:
        st.warning("No items available in the inventory.")

if menu == "Inventory Summary":
    st.header("📊 Inventory Summary")

    items = get_all_items()

    if items:
        df = pd.DataFrame(
            items,
            columns=[
                "ID",
                "Name",
                "Category",
                "Quantity",
                "Unit",
                "Purchase Date",
                "Expiry Date",
            ],
        )

        st.dataframe(df, use_container_width=True)

        # Summary statistics
        total_items = len(items)
        total_quantity = sum(
            item[3] for item in items
        )  # Assuming quantity is the 4th column

        st.subheader("Summary Statistics")
        st.write(f"Total Items: {total_items}")
        st.write(f"Total Quantity: {total_quantity}")
    else:
        st.warning("No items available in the inventory.")

    st.header("📊 Discard / Donation History")
    item_actions = []

    for item in items:
        actions = get_item_actions(item[1])  # Assuming name is the 2nd column
        item_actions.extend([(action[0], action[1], action[2]) for action in actions])

    if item_actions:
        df_actions = pd.DataFrame(
            item_actions,
            columns=["Item Name", "Action", "Action Date"],
        )
        st.dataframe(df_actions, use_container_width=True)
    else:
        st.warning("No discard/donation history available.")

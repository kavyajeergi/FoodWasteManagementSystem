import pandas as pd
import streamlit as st

from ViewModels.database import create_table
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

st.set_page_config(
    page_title="Food Waste Management System", page_icon="🍽️", layout="wide"
)

create_table()  # Ensure the database table is created when the app starts

st.title("🍎 Smart Food Waste Management System")

st.sidebar.title("Menu")

menu = st.sidebar.selectbox(
    "Choose an option",
    [
        "Dashboard",
        "Add Food Item",
        "View Inventory",
        "Search Item",
        "Update Quantity",
        "Remove Item",
        "Expiry Monitor",
        "Waste / Donation",
        "Inventory Summary",
    ],
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
                            item, action_status, datetime.now().date()
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

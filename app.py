import streamlit as st
from ViewModels.database import create_table
from ViewModels.validation import *
from Models.foodmodel import FoodItem
from ViewModels.inventory import *
import pandas as pd

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
                            return

                    # Update the quantity in the database
                    update_food_item(
                        FoodItem(
                            id=item_id,
                            name=item[1],
                            category=item[2],
                            quantity=new_quantity,
                            unit=item[4],
                            purchase_date=item[5],
                            expiry_date=item[6],
                        )
                    )

                    st.success(
                        f"Quantity updated successfully. New quantity: {new_quantity}"
                    )
            except ValueError as e:
                st.error(str(e))

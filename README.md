**Streamlit link: [https://foodwastemanagementsystem-gleykwdz2rnyrmu6m4nx9f.streamlit.app/#food-inventory](https://foodwastemanagementsystem-gleykwdz2rnyrmu6m4nx9f.streamlit.app/#food-inventory)**

# 🍎 Food Waste Management System

A simple and user-friendly **Food Waste Management System** built with **Python, Streamlit, and SQLite**.

The application helps users manage food inventory, monitor expiry dates, and track food items that are either **donated** or marked as **waste**. It also provides a colorful dashboard to give a quick overview of the food inventory and waste status.

---

## 📌 Project Overview

Food wastage is a common problem caused by poor inventory tracking and expired food items.

This application provides a simple solution to:

* Add and manage food items
* Track food quantity and expiry dates
* Monitor items that are expiring soon
* Identify expired food
* Mark food as waste or donation
* Search food items
* Update food quantities
* Remove food items
* View inventory statistics
* Track waste and donation history
* View everything through a dashboard

---

## ✨ Features

### 📊 Dashboard

The dashboard provides a quick overview of the inventory:

* 📦 Total Food Items
* ⚖️ Total Quantity
* 🟢 Available Items
* 🟠 Expiring Soon
* 🔴 Expired Items
* ♻️ Food Waste
* 🎁 Food Donations
* 📈 Inventory Status Chart
* 💡 Quick Summary and Alerts

---

### ➕ Add Food Item

Users can add food items with information such as:

* Item ID
* Food Name
* Category
* Quantity
* Unit
* Purchase Date
* Expiry Date

Example:

```text
ID: F001
Name: Milk
Category: Dairy
Quantity: 2
Unit: Litres
Purchase Date: 2026-10-01
Expiry Date: 2026-10-07
```

---

### 📦 View Inventory

Users can view all available food items in a table.

The inventory contains:

| Field         | Description              |
| ------------- | ------------------------ |
| ID            | Unique food item ID      |
| Name          | Food name                |
| Category      | Food category            |
| Quantity      | Available quantity       |
| Unit          | Kg, litres, pieces, etc. |
| Purchase Date | Date of purchase         |
| Expiry Date   | Expiration date          |

---

### 🔍 Search Food Items

Food items can be searched using:

* Food name
* Food category

For example:

```text
Search: Milk
```

or

```text
Search: Dairy
```

---

### ✏️ Update Quantity

Users can increase or decrease the quantity of an existing food item.

Example:

```text
Milk
Current Quantity: 5 litres

Operation: Decrease
Amount: 2

New Quantity: 3 litres
```

---

### 🗑️ Remove Food Item

Food items can be removed from the inventory using their unique Item ID.

---

### ⏰ Expiry Monitor

The application automatically calculates the status of food items based on the expiry date.

There are three statuses:

```text
🟢 AVAILABLE
🟠 EXPIRING SOON
🔴 EXPIRED
```

The application considers an item **Expiring Soon** when it has 3 days or less remaining.

---

### ♻️ Waste / Donation Management

Users can mark food items as:

```text
♻️ WASTE
🎁 DONATION
```

The application stores:

* Food item name
* Action
* Action date

Example:

```text
Milk → DONATION → 2026-10-05
Bread → WASTE → 2026-10-05
```

---

### 📈 Inventory Summary

The application provides a summary of:

* Total inventory
* Total quantity
* Waste history
* Donation history

This helps users understand how much food is being used, donated, or wasted.

---

# 🏗️ Project Architecture

The project follows a simple separation of responsibilities.

```text
FoodWasteManagementSystem
│
├── app.py
│
├── Models
│   └── foodmodel.py
│
├── ViewModels
│   ├── database.py
│   ├── inventory.py
│   └── validation.py
│
├── database
│   └── foodwaste.db
│
└── README.md
```

### `app.py`

Responsible for:

* Streamlit UI
* Navigation
* User input
* Displaying tables
* Dashboard
* Calling ViewModel functions

### `Models/foodmodel.py`

Contains data models such as:

```text
FoodItem
```

This represents a food item in the system.

### `ViewModels/inventory.py`

Contains business logic such as:

* Add food item
* Get inventory
* Search items
* Update quantity
* Delete item
* Calculate expiry status
* Save waste/donation actions
* Retrieve action history

### `ViewModels/database.py`

Responsible for:

* SQLite database connection
* Creating database tables
* Database configuration

### `ViewModels/validation.py`

Responsible for validating:

* Dates
* Quantity
* Expiry dates
* User input

---

# 🗄️ Database

The application uses **SQLite** as the database.

### Food Items Table

The main table stores:

```text
food_items
```

with fields such as:

```text
id
name
category
quantity
unit
purchase_date
expiry_date
```

### Item Actions Table

Waste and donation actions are stored in:

```text
item_actions
```

with:

```text
id
item_name
action
action_date
```

---

# 🛠️ Technologies Used

| Technology | Purpose                  |
| ---------- | ------------------------ |
| Python     | Application development  |
| Streamlit  | Web UI                   |
| SQLite     | Database                 |
| Pandas     | Data handling and tables |
| Git        | Version control          |
| VS Code    | Development environment  |

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone <your-github-repository-url>
```

Move into the project directory:

```bash
cd FoodWasteManagementSystem
```

---

## 2. Create a Virtual Environment

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install streamlit pandas
```

---

## 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser.

---

# 🖥️ Application Flow

```text
                ┌─────────────────────┐
                │       Dashboard     │
                └──────────┬──────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
     Add Food Item    View Inventory    Search Item
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Expiry Monitor  │
                  └────────┬────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
             Donation              Waste
                 │                   │
                 └─────────┬─────────┘
                           ▼
                  Inventory Summary
```

---

# 🎯 Future Enhancements

The project can be extended with:

* 🔐 User authentication
* 👥 Multiple users
* 📧 Expiry notifications
* 📱 Mobile application
* ☁️ Cloud database
* 📊 Advanced analytics
* 📈 Monthly waste reports
* 🎁 Donation organization management
* 🏷️ Barcode/QR code scanning
* 🤖 AI-based food waste prediction
* 📷 Food image recognition
* 📉 Waste reduction recommendations

---

# 💡 Future AI Enhancement

An AI-based recommendation system could predict which food items are likely to expire soon and recommend actions.

For example:

```text
⚠️ Milk expires in 2 days.

Recommendation:
Consider consuming or donating this item
before the expiry date to reduce food waste.
```

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/new-feature
```

3. Make your changes
4. Commit your changes

```bash
git commit -m "Add new feature"
```

5. Push the branch

```bash
git push origin feature/new-feature
```

6. Create a Pull Request

---

# 📄 License

This project is created for learning and demonstration purposes.

---

## 👩‍💻 Author

**Kavya Jeergi**

Food Waste Management System built using Python, Streamlit, and SQLite.

---

## ⭐ Project Goal

> **Reduce food waste by helping users track, manage, and take timely action on their food inventory.**

# 🍎 FoodWise

A modern, visually polished Food Waste Management System built with Python, Streamlit, SQLite, and Plotly.

The app helps users track food inventory, identify items nearing expiry, monitor waste and donations, and keep an overview of the full food lifecycle in a clean dashboard-based UI.

**Live app:** [https://foodwastemanagementsystem-gleykwdz2rnyrmu6m4nx9f.streamlit.app/#food-inventory](https://foodwastemanagementsystem-gleykwdz2rnyrmu6m4nx9f.streamlit.app/#food-inventory)

---

## Overview

Food waste is a growing problem caused by poor tracking, inaccurate stock levels, and missed expiry dates. FoodWise provides a simple and practical solution for:

- Managing food inventory
- Tracking quantities and expiry dates
- Detecting items that are expiring soon or already expired
- Marking items as waste or donation
- Searching records by item name or category
- Updating stock levels quickly
- Monitoring inventory trends through a dashboard

---

## New UI Experience

The application now uses a modern Streamlit layout with:

- A top navigation bar with quick access to all major actions
- Metric cards for important inventory insights
- Clean card-based UI styling
- Progress indicators and visual charts
- A dashboard-first workflow for everyday inventory monitoring
- Organized sections for:
  - Dashboard
  - Add Food Item
  - Update Quantity
  - Remove Item
  - Inventory
  - Search Item
  - Expiry Monitor
  - Waste / Donation
  - Inventory Summary

---

## Features

### Dashboard

The dashboard gives a quick overview of the current food inventory and operational health.

It includes:

- Total Food Items
- Total Quantity
- Available Items
- Expiring Soon
- Expired Items
- Waste records
- Donation records
- Inventory health chart
- Quick summary alerts

### Add Food Item

Users can add food items with:

- Item ID
- Food name
- Category
- Quantity
- Unit
- Purchase date
- Expiry date

Example:

```text
ID: F001
Name: Milk
Category: Dairy
Quantity: 2
Unit: litres
Purchase Date: 2026-10-01
Expiry Date: 2026-10-07
```

### Inventory View

The inventory section displays all items in a table with details such as:

- ID
- Name
- Category
- Quantity
- Unit
- Purchase Date
- Expiry Date
- Status

Items are automatically labeled as:

```text
🟢 Available
🟠 Expiring Soon
🔴 Expired
```

### Search Functionality

Users can search records by:

- Food name
- Food category

Example:

```text
Search: Milk
```

or

```text
Search: Dairy
```

### Update Quantity

The quantity can be updated for an existing food item.

### Remove Item

Items can be deleted from inventory using their unique item ID.

### Expiry Monitor

The app automatically calculates food status based on remaining days before expiry.

An item is marked as expiring soon when it has 3 days or fewer remaining.

The expiry monitor is organized into tabs:

- Expiring Soon
- Expired
- Available

### Waste / Donation Management

Users can mark any item as either:

- Waste
- Donation

These records are stored with:

- Item name
- Action type
- Action date

### Inventory Summary

The summary section provides insights into:

- Total inventory size
- Total quantity
- Item count by category
- Waste and donation history

---

## Project Structure

```text
FoodWasteManagementSystem
├── app.py
├── README.md
├── Models
│   └── foodmodel.py
├── ViewModels
│   ├── database.py
│   ├── inventory.py
│   └── validation.py
├── food_inventory.db
└── .streamlit/
```

### app.py

Main Streamlit application containing:

- UI layout and styling
- Navigation between sections
- Dashboard logic
- Inventory actions
- Charts and metrics

### Models/foodmodel.py

Contains data models used by the app, including `FoodItem`.

### ViewModels/inventory.py

Contains business logic for:

- Adding items
- Reading inventory
- Searching by name/category
- Updating quantities
- Deleting items
- Calculating expiry status
- Saving waste/donation actions
- Fetching action history

### ViewModels/database.py

Responsible for:

- SQLite database connection
- Table creation
- Data persistence

### ViewModels/validation.py

Validates:

- Dates
- Quantity values
- Expiry date rules
- User inputs

---

## Database

The app uses SQLite for local data storage.

### food_items table

Stores item-level information such as:

```text
id
name
category
quantity
unit
purchase_date
expiry_date
```

### item_actions table

Stores waste and donation actions:

```text
id
item_name
action
action_date
```

---

## Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- Git
- VS Code

---

## Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
```

Go into the project directory:

```bash
cd FoodWasteManagementSystem
```

### 2. Create a virtual environment

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install streamlit pandas plotly
```

### 4. Run the app

```bash
streamlit run app.py
```

The application will open in your browser.

---

## App Flow

```text
Dashboard
  ├── Add Food Item
  ├── Update Quantity
  ├── Remove Item
  ├── View Inventory
  ├── Search Item
  ├── Expiry Monitor
  ├── Waste / Donation
  └── Inventory Summary
```

---

## Future Enhancements

The app can be extended with:

- User authentication
- Multi-user support
- Email/notification alerts for expiring items
- Mobile app support
- Cloud database integration
- Advanced analytics and reporting
- Monthly waste insights
- Donation coordination features
- Barcode or QR code scanning
- AI-based expiry prediction
- Computer vision-based food recognition

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Make your changes
4. Commit your changes

```bash
git commit -m "Add new feature"
```

5. Push to your branch

```bash
git push origin feature/new-feature
```

6. Open a Pull Request

---

## License

This project is created for learning, demonstration, and practical inventory management use.

---

## Author

**Kavya Jeergi**

FoodWise is designed to help users reduce food waste by improving tracking, visibility, and action-taking around food inventory.

---

## Project Goal

> Reduce food waste by helping users track, monitor, and take timely action on their food inventory.

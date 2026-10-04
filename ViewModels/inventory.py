from datetime import date
from ViewModels.database import get_connection
from Models.foodmodel import FoodItem
from enum import Enum


class ExpiryStatus(str, Enum):
    EXPIRED = "EXPIRED"
    EXPIRING_SOON = "EXPIRING SOON"
    AVAILABLE = "AVAILABLE"


def calculate_status(expiry_date: date) -> str:
    today = date.today()
    days_remaining = (expiry_date - today).days

    if days_remaining < 0:
        return ExpiryStatus.EXPIRED

    elif days_remaining <= 3:
        return ExpiryStatus.EXPIRING_SOON

    else:
        return ExpiryStatus.AVAILABLE


def add_food_item(item: FoodItem):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO food_items (
                id,
                name,
                category,
                quantity,
                unit,
                purchase_date,
                expiry_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item.id,
                item.name,
                item.category,
                item.quantity,
                item.unit,
                item.purchase_date,
                item.expiry_date,
            ),
        )

        conn.commit()

    except Exception as e:
        print("DATABASE ERROR:", e)
        raise

    finally:
        conn.close()

def get_all_items():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            quantity,
            unit,
            purchase_date,
            expiry_date
        FROM food_items
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_items_by_name_or_category(search_term: str):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            category,
            quantity,
            unit,
            purchase_date,
            expiry_date
        FROM food_items
        WHERE name LIKE ? OR category LIKE ?
    """,
        (f"%{search_term}%", f"%{search_term}%"),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_item_by_id(item_id: str):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            category,
            quantity,
            unit,
            purchase_date,
            expiry_date
        FROM food_items
        WHERE id = ?
    """,
        (item_id,),
    )

    row = cursor.fetchone()

    conn.close()

    return row


def update_food_item(item: FoodItem):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    UPDATE food_items
    SET quantity = ?
    WHERE id = ?
    """,
        (item.quantity, item.id),
    )

    conn.commit()
    conn.close()

    return True


def delete_food_item(item_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
    DELETE FROM food_items
    WHERE id = ?
    """,
        (item_id,),
    )

    conn.commit()
    conn.close()

    return True


def save_item_actionstatus(item_name: str, action: str, action_date: date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO item_actions (item_name, action, action_date)
        VALUES (?, ?, ?)
        """,
        (item_name, action, action_date.isoformat()),
    )

    conn.commit()
    conn.close()


def get_item_actions(item_name: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT item_name, action, action_date
        FROM item_actions
        WHERE item_name = ?
        """,
        (item_name,),
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

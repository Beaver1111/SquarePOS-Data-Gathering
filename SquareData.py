import requests
import pandas as pd
import os
from datetime import datetime
from config import SQUARE_ACCESS_TOKEN, SQUARE_LOCATION_IDS, LOCAL_SAVE_DIR

def fetch_square_orders():
    """Fetch sales data from all Square locations"""
    all_orders = []
    
    for location_id in SQUARE_LOCATION_IDS:
        url = f"https://connect.squareup.com/v2/orders/search"
        headers = {
            "Square-Version": "2025-02-20",
            "Authorization": f"Bearer {SQUARE_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "location_ids": [location_id],
            "query": {}
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if "orders" in data:
                all_orders.extend(data["orders"])
            else:
                print(f"⚠️ No orders found for location {location_id}")
        else:
            print(f"❌ Failed to fetch data for location {location_id}: {response.json()}")

    return all_orders if all_orders else []  # Ensure it never returns None

def save_to_excel():
    """Save Square data to an Excel file"""
    orders = fetch_square_orders()

    if not orders:  # If orders is empty, avoid processing
        print("⚠️ No orders found. Skipping Excel export.")
        return
    
    orders_df = pd.DataFrame([{
        "location_id": order.get("location_id"),
        "id": order.get("id"),
        "created_at": order.get("created_at"),
        "state": order.get("state"),
        "total_money": order.get("total_money", {}).get("amount"),  
        "currency": order.get("total_money", {}).get("currency")
    } for order in orders])

    # Create filename with timestamp
    filename = f"square_data_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    filepath = os.path.join(LOCAL_SAVE_DIR, filename)

    orders_df.to_excel(filepath, index=False)
    print(f"✅ Data saved to {filepath}")

# Run the script
if __name__ == "__main__":
    save_to_excel()
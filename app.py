"""
StockWise — Smart Inventory and Reorder Management System
Main Streamlit Application Entrypoint
"""

import sys
from pathlib import Path

# Ensure workspace root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

# Streamlit Page Config
st.set_page_config(
    page_title="StockWise — Smart Inventory & Reorder Management",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize Database Schema & Default Configurations
from database.db import init_db, execute_one
init_db()

from ui.layout import apply_custom_styles
apply_custom_styles()

# Import UI Views
from ui.dashboard import render_dashboard_view
from ui.inventory import render_inventory_view
from ui.categories import render_categories_view
from ui.purchases import render_purchases_view
from ui.sales import render_sales_view
from ui.suppliers import render_suppliers_view
from ui.reorder import render_reorder_view
from ui.reports import render_reports_view
from ui.settings import render_settings_view
from services.reorder_service import get_low_stock_alerts
from services.demo_data import is_demo_data_loaded


def main():
    alerts = get_low_stock_alerts()
    alert_badge = f" ({len(alerts)})" if alerts else ""

    biz_row = execute_one("SELECT value FROM application_settings WHERE key = 'business_name';")
    store_name = biz_row["value"] if biz_row else "StockWise Retail"

    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 10px 0 20px 0; border-bottom: 1px solid #334155; margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="background: linear-gradient(135deg, #0d9488 0%, #0284c7 100%); width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 20px;">📦</div>
                    <div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">StockWise</div>
                        <div style="font-size: 0.72rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Smart Inventory System</div>
                    </div>
                </div>
                <div style="margin-top: 12px; font-size: 0.8rem; color: #38bdf8; font-weight: 500;">
                    📍 {store_name}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        nav_options = [
            "Overview",
            "Inventory",
            "Categories",
            "Stock In / Purchases",
            "Sales / Stock Out",
            "Suppliers",
            f"Reorder Recommendations{alert_badge}",
            "Reports and Analytics",
            "Settings",
        ]

        selected_nav = st.radio(
            "NAVIGATION MENU",
            nav_options,
            index=0,
            label_visibility="visible",
        )

        st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="padding: 12px; background-color: #1e293b; border-radius: 8px; font-size: 0.75rem; color: #94a3b8; border: 1px solid #334155;">
                <div style="font-weight: 600; color: #f1f5f9; margin-bottom: 4px;">System Health</div>
                <div>● Database: SQLite Local</div>
                <div>● Mode: Enterprise Offline</div>
                <div>● Version: 1.0.0 Pro</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    clean_selection = selected_nav.split(" (")[0].strip()

    prod_count_row = execute_one("SELECT COUNT(*) as cnt FROM products;")
    if prod_count_row and prod_count_row["cnt"] == 0 and not is_demo_data_loaded():
        st.info(
            "💡 **Welcome to StockWise!** Your inventory database is currently fresh and empty. "
            "To explore the system with realistic stationery shop inventory, historical purchases, "
            "and sales analytics, go to **Settings ➔ Demo Data Management** and click **Load Stationery Demo Data**."
        )

    if clean_selection == "Overview":
        render_dashboard_view()
    elif clean_selection == "Inventory":
        render_inventory_view()
    elif clean_selection == "Categories":
        render_categories_view()
    elif clean_selection == "Stock In / Purchases":
        render_purchases_view()
    elif clean_selection == "Sales / Stock Out":
        render_sales_view()
    elif clean_selection == "Suppliers":
        render_suppliers_view()
    elif clean_selection == "Reorder Recommendations":
        render_reorder_view()
    elif clean_selection == "Reports and Analytics":
        render_reports_view()
    elif clean_selection == "Settings":
        render_settings_view()


if __name__ == "__main__":
    main()

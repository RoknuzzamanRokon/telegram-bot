import MetaTrader5 as mt5
import os

# Initialize connection to MT5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

# The path where the screenshot will be saved (ensure this directory exists)
screenshot_path = os.path.join(os.getcwd(), "chart_screenshot.png")

# Parameters: symbol, timeframe, start_bar, chart_width_in_bars, chart_height_in_pixels
# Save screenshot
result = mt5.screenshot(
    symbol="EURUSD",
    timeframe=mt5.TIMEFRAME_D1,
    start_bar=0,
    chart_width_in_bars=100,
    chart_height_in_pixels=800,
    filename=screenshot_path
)

# Check if the screenshot was saved successfully
if result:
    print(f"Chart screenshot saved at: {screenshot_path}")
else:
    print("Failed to save chart screenshot")

# Shutdown MT5 connection
mt5.shutdown()


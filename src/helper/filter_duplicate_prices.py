import regex as re

import re

def filter_unique_prices(original_shipping_prices_list):
    filtered_prices = []
    i = 0

    while i < len(original_shipping_prices_list):
        current_price = original_shipping_prices_list[i]

        # Check if the current price is numeric using regex
        if re.match(r'^\d+\.\d+$', current_price):
            # Check if the next price is the same (i.e., a pair)
            if i + 1 < len(original_shipping_prices_list) and original_shipping_prices_list[i + 1] == current_price:
                # Add the price once if it's part of a pair
                filtered_prices.append(current_price)
                i += 2  # Skip the next one since it's a duplicate
            else:
                # If it's not part of a pair, just add it
                filtered_prices.append(current_price)
                i += 1
        else:
            # Handle non-numeric values directly
            filtered_prices.append(current_price)
            i += 1

    return filtered_prices
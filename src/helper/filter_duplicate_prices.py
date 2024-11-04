import regex as re

def filter_unique_prices(original_shipping_prices_list):
    filtered_prices = []
    last_price = None
    consecutive_count = 0

    for price in original_shipping_prices_list:
        if re.match(r'^\d+\.\d+$', price):  # Check if the price is numeric
            if price == last_price:  # If the current price is the same as the last one
                consecutive_count += 1  # Increment the count of this price
            else:
                # If the last price is set and was seen consecutively, add it based on the count
                if last_price is not None:
                    if consecutive_count % 2 == 1:  # Add the last price if the count is odd
                        filtered_prices.append(last_price)
                    elif consecutive_count == 2:  # If it's the second in the pair, add it too
                        filtered_prices.append(last_price)

                # Reset for the new price
                last_price = price  
                consecutive_count = 1  # Reset count for the new price
        else:
            # Handle non-numeric values
            if last_price is not None:
                if consecutive_count % 2 == 1:  # Add the last price if the count is odd
                    filtered_prices.append(last_price)
                elif consecutive_count == 2:  # If it's the second in the pair, add it too
                    filtered_prices.append(last_price)

            filtered_prices.append(price)
            last_price = None  # Reset last price since we encountered a non-numeric value
            consecutive_count = 0  # Reset consecutive count

    # Check last price after loop ends
    if last_price is not None:
        if consecutive_count % 2 == 1:  # Add the last price if the count is odd
            filtered_prices.append(last_price)
        elif consecutive_count == 2:  # If it's the second in the pair, add it too
            filtered_prices.append(last_price)

    return filtered_prices

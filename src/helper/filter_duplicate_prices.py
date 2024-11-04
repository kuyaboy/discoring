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
                consecutive_count = 1  # Reset count for new price
            
            # Calculate how many should be added based on consecutive pairs
            if consecutive_count % 2 == 1:  # Add only if we have an odd count
                filtered_prices.append(price)  # Add the price to the filtered list
            elif consecutive_count == 2:  # If it's the second in the pair, add it too
                filtered_prices.append(price)

            last_price = price  
        else:
            filtered_prices.append(price)
            last_price = None  # Reset last price since we encountered a non-numeric value
            consecutive_count = 0  # Reset consecutive count

    return filtered_prices
    
h = ['Unavailable in Philippines', 'Unavailable in Philippines', '14.00', '14.00', '40.00', '40.00', 'Unavailable in Philippines', 'Unavailable in Philippines', 'Unavailable in Philippines', '14.00', '14.00', 'Unavailable in Philippines']


filter_unique_prices(h)

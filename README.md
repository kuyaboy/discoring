# Discoring

This project serves as an automated monitoring tool for good sales on Discogs.com of desired records — so we don't have to spend all our free time scrolling through Discogs 😁

## Description

This project consists of several Python scripts designed to scrape data from the Discogs marketplace based on a user-defined configuration file (`.json`). The config specifies which records from your Discogs wantlist you want to track.

The scraper extracts and parses the following information for each listing:

- **Listing ID**
- **Release ID**
- **Record Name**
- **Artist Name**
- **Media Condition**
- **Sleeve Condition**
- **Currency** (the currency the item is listed in)
- **Item Price**
- **Seller Name**
- **Seller Rating**
- **Shipping Price**
- **Shipping Origin**
- **Date** (when the data was scraped)

To provide consistent pricing, the project integrates the [FXRatesAPI](https://fxratesapi.com/) to convert both the item price and shipping price into a desired currency.

After scraping and parsing, each record’s data is stored as a Python dictionary and saved to a JSON file. Finally, these records are inserted into a MongoDB collection, containing your tracked Discogs listings.

Each scraping cycle follows the same procedure. Listings that are already present in your MongoDB collection will **not** be re-inserted; instead, they will only be **updated** if the pricing has changed. Listings that exist in your MongoDB collection but are no longer available on the Discogs marketplace will be **deleted**.

You yourself define queries for *Item Price*, *Shipping Price*, *Media Condition*, and *Sleeve Condition* that a listing must meet. If a listing matches your query conditions, you will receive a notification on Telegram.

The project is designed to run anywhere with minimal installation. In fact, the only requirement is to have Docker installed on your local machine (see the **Prerequisites** section in *Getting Started*).

## Getting Started

### Prerequisites

- [Discogs Account](https://www.discogs.com/) & Wantlist with records to monitor
- [Docker](https://docs.docker.com/get-started/get-docker/)
- [MongoDB Collection](https://www.mongodb.com/)
- [Telegram-Bot](https://core.telegram.org/bots/api)
- [FXRatesAPI Account](https://fxratesapi.com/)

### Dependencies

This project requires the following Python libraries:

- `lxml==5.4.0`
- `pymongo==4.13.0`
- `pyvirtualdisplay==3.0`
- `python3-discogs-client==2.8`
- `python-dotenv==1.1.0`
- `requests==2.32.3`
- `regex==2024.11.6`
- `selenium==4.25.0`
- `webdriver-manager==4.0.2`

These dependencies are installed automatically during the Docker image build process from the `requirements.txt` file in the root directory.

### Installations

Download and install [Docker](https://docs.docker.com/get-started/get-docker/)

### Configurations

#### Environment Variables

Before running the program, ensure that a .env file is created in the root directory of the project. This file should contain the following environment variables:

```.env
DISCOGS_USER_TOKEN=
MONGODB_URI=
MONGODB_NAME=
MONGODB_COLLECTION_LISTINGS=
MONGODB_COLLECTION_MESSAGES=
DISCOGS_USERNAME=
DISCOGS_PASSWORD=
FXRATES_API_TOKEN=
TELEGRAM_API_TOKEN=
TELEGRAM_CHAT_ID=
TELEGRAM_CHAT_URL=
```

#### Records to track config

In the */src/config* directory, locate the file named wantlist_filter_config.json.

Replace the sample entries with the records from your wantlist that you want to monitor. Use the following JSON structure:

```json
[
    {
        "artist": "Artist Name",
        "title": "Record Title",
        "year": 2000,
        "format": "Vinyl" # or CD/Cassette etc.
    }
]
```

You can find the required information (artist, title, year, format) on the release page of the record you're interested in on Discogs.

‼️Make sure each entry accurately matches the release details to ensure the filtering works properly

#### MongoDB queries

In the */src/mongodb* directory, you will find a file named `queries.py`.
This file contains the query definition your MongoDB collection.

```python
def get_queries():
    return {
        # Replace 'your_query_name' with the name of your query (only for informative purpose)
        # Replace record_name, item_price_in_your_currency and shipping_price_in_your_currency with actual variables or values
        'your_query_name': create_query('record_name', item_price_in_your_currency, shipping_price_in_your_currency)
    }
```

‼️Make sure that `record_name` accurately matches the name on Discogs

### Executing program

#### Setup Instructions

Follow these steps to get started:

1. Clone Git Repository

    ```bash
    git clone https://github.com/kuyaboy/discoring.git
    ```

2. Build Docker Image

    ```bash
    docker build -t discoring .
    ```

3. Run Container

    ```bash
    docker run --name container-name -d discoring
    ```

## Found an issue?

If an error occurs you will also get a notification on Telegram. You can either fix it yourself and make a pull request or open an issue and I will try to fix it as soon as possible.

## License

This project is licensed under the MIT License - see the LICENSE file for details

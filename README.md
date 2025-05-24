# Discoring

This scraper serves as an automated monitoring tool for good sales on Discogs.com of desired records — so we don't have to spend all our free time scrolling through Discogs 😁

## Description

This scraper consists of several Python scripts designed to scrape data from the Discogs marketplace based on a user-defined configuration file (`.json`). The config specifies which records from your Discogs wantlist you want to track.

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

You yourself define queries for *Artist Name*, *Record Name*, *Item Price (for your currency)*, *Shipping Price (for your currency)*, *Media Condition*, *Sleeve Condition* and optionally the *Seller Rating* that a listing must meet. If a listing matches your query conditions, you will receive a notification on Telegram.

The scraper is designed to run anywhere with minimal installation. In fact, the only installation-requirement is Docker on your local machine (see the **Prerequisites** section in *Getting Started*).

## Getting Started

### Prerequisites

- [Discogs User Token](https://www.discogs.com/) & Wantlist with records to monitor
- [Docker](https://docs.docker.com/get-started/get-docker/)
- [FXRatesAPI Token](https://fxratesapi.com/)
- [MongoDB with collections](https://www.mongodb.com/)
- [Telegram API Token](https://core.telegram.org/bots/api)
- [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) is optional (on Windows use Git Bash Terminal **with LF line endings**)

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

Before running the scraper, ensure that a `.env` file is created in the root directory of the project. This file should contain the following environment variables:

```.env
CURRENCY=
DISCOGS_USERNAME=
DISCOGS_USER_TOKEN=
FXRATES_API_TOKEN=
TELEGRAM_API_TOKEN=
TELEGRAM_CHAT_ID=
TELEGRAM_CHAT_URL=
MONGODB_NAME=
MONGODB_URI=
MONGODB_COLLECTION_LISTINGS=
MONGODB_COLLECTION_MESSAGES=
```

ℹ️ `CURRENCY` refers to the abbreviation of your preferred currency (e.g., *usd* for US Dollars).

ℹ️ The `TELEGRAM_CHAT_URL` is built as followed:

```url
 https://api.telegram.org/<TELEGRAM_API_TOKEN>/sendMessage?chat_id=<TELEGRAM_CHAT_ID>&text=
```

#### Records to track config

To set up your monitoring list, do the following steps:

1. Navigate to the `/src/config` directory in your project and create a new file named `monitoring_list.json`.

2. Open the provided `monitoring_list_template.json` file and copy the sample entries into your newly created `monitoring_list.json` file.

3. Once copied, edit these entries to include only the records you want to monitor from your wantlist.

```json
[
  {
    "artist_name": "Artist Name",
    "record_name": "Example Record",
    "year": 1998,
    "format": "Vinyl (or other format type)"
  }
]
```

You can find the required information (artist, title, year, format) on the release page of the record you're interested in on Discogs.

‼️Make sure each entry accurately matches the release details to ensure the filtering works properly

#### MongoDB queries config

Also in the */src/config* directory, you will find a file named `queries_template.py`:

Follow the same steps as described in the ***Records to track config*** section, where you initially create a file named `queries.py` by copying the contents of the existing `queries_template.py`. Once the file is created, adjust the values for the following parameters:

- *Artist Name*, *Record Name*, *Item Price (for your currency)*, *Shipping Price (for your currency)*, *Media Condition*, *Sleeve Condition* and optionally the *Seller Rating*

### Executing program

#### Setup Instructions

Follow these steps to get started after you have all the necessary installations:

1. In the top-right corner of the repository page, click the “Fork” button.

2. Clone the forked Git Repository to your local machine

    ```bash
    git clone https://github.com/kuyaboy/discoring.git
    ```

3. Build Docker Image

    ```bash
    docker build -t discoring:latest .
    ```

4. Run Container (add or remove flags as needed)

    ```bash
    docker run -d --name <container-name> discoring:latest
    ```

## Found an issue?

If an error occurs while you're working with the project, you'll receive a notification on Telegram. Since you're working from a fork, you have two options:

1. Fix the issue yourself in your forked repository, then open a pull request with your changes.

2. Open an issue in the original repository describing the problem and the ERROR message, and I’ll look into fixing it as soon as possible.

Either approach helps improve the project 😁

## License

This project is licensed under the MIT License - see the LICENSE file for details

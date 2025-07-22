# Google Trends Data for TradingView (Pine Seeds)

This repository provides Google Trends data for use in TradingView through the Pine Seeds service.

## Overview

Pine Seeds allows you to import custom data series into TradingView using GitHub repositories as a backend. This repository contains Google Trends data that can be accessed in TradingView Pine Script.

## Available Data Series

### Search Terms
- `GOOGL_TRENDS_BITCOIN` - Bitcoin search interest
- `GOOGL_TRENDS_STOCK_MARKET` - Stock market search interest  
- `GOOGL_TRENDS_RECESSION` - Recession search interest
- `GOOGL_TRENDS_INFLATION` - Inflation search interest
- `GOOGL_TRENDS_CRYPTOCURRENCY` - Cryptocurrency search interest

## Usage in TradingView

1. Open TradingView Pine Script editor
2. Use the following format to access data:
```pinescript
//@version=5
indicator("Google Trends Analysis", overlay=false)

// Import Google Trends data
bitcoin_trends = request.seed("YOUR_GITHUB_USERNAME", "GOOGL_TRENDS_BITCOIN", "close")
recession_trends = request.seed("YOUR_GITHUB_USERNAME", "GOOGL_TRENDS_RECESSION", "close")

// Plot the data
plot(bitcoin_trends, title="Bitcoin Trends", color=color.orange)
plot(recession_trends, title="Recession Trends", color=color.red)
```

## Data Structure

Each CSV file contains:
- `time`: Unix timestamp (daily resolution)
- `close`: Google Trends interest score (0-100)

## Data Updates

- Data is automatically updated daily via GitHub Actions
- Limited to 5 updates per day as per Pine Seeds restrictions
- Historical data covers up to 6000 data points (approximately 16 years of daily data)

## Limitations

- Only daily timeframes (1D and above) are supported
- Data won't appear in TradingView symbol search
- Maximum 6000 data elements per series
- 5 updates per day limit

## Data Sources

Data is sourced from Google Trends API using automated scripts that fetch:
- Relative search interest (0-100 scale)
- Geographic scope: Worldwide
- Category: All categories
- Time range: Past 5 years (rolling window)

## Repository Structure

```
/
├── data/
│   ├── GOOGL_TRENDS_BITCOIN.csv
│   ├── GOOGL_TRENDS_STOCK_MARKET.csv
│   ├── GOOGL_TRENDS_RECESSION.csv
│   ├── GOOGL_TRENDS_INFLATION.csv
│   └── GOOGL_TRENDS_CRYPTOCURRENCY.csv
├── scripts/
│   ├── fetch_trends.py
│   └── validate_data.py
├── .github/
│   └── workflows/
│       └── update_data.yml
└── README.md
```

## Setup Instructions

1. Fork this repository
2. Enable GitHub Actions in your fork
3. Set up Google Trends API access (if using automated updates)
4. Use your GitHub username in Pine Script requests

## Contributing

Feel free to:
- Add new search terms
- Improve data collection scripts
- Report issues with data quality
- Suggest new features

## License

This project is open source and available under the MIT License. 
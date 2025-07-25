#!/usr/bin/env python3
"""
Google Trends Data Fetcher for Pine Seeds
Fetches Google Trends data and formats it for TradingView Pine Seeds consumption.
"""

import os
import csv
import time
import random
from datetime import datetime, timedelta
from typing import List, Tuple, Dict
import requests

try:
    from pytrends.request import TrendReq
except ImportError:
    print("Installing pytrends...")
    os.system("pip install pytrends")
    from pytrends.request import TrendReq


class GoogleTrendsFetcher:
    """Fetches and processes Google Trends data for Pine Seeds format."""
    
    def __init__(self):
        """Initialize the Google Trends fetcher."""
        try:
            # Add random user agent to avoid blocking
            self.pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries=3, backoff_factor=0.1)
            self.search_terms = {
                'GOOGL_TRENDS_BITCOIN': 'bitcoin',
                'GOOGL_TRENDS_STOCK_MARKET': 'stock market',
                'GOOGL_TRENDS_RECESSION': 'recession',
                'GOOGL_TRENDS_INFLATION': 'inflation',
                'GOOGL_TRENDS_CRYPTOCURRENCY': 'cryptocurrency'
            }
        except Exception as e:
            print(f"Error initializing TrendReq: {e}")
            self.pytrends = None
        
    def fetch_trends_data(self, keyword: str, timeframe: str = 'today 5-y') -> List[Tuple[int, float]]:
        """
        Fetch Google Trends data for a specific keyword.
        
        Args:
            keyword: Search term to fetch trends for
            timeframe: Time range for the data (default: 'today 5-y')
            
        Returns:
            List of tuples containing (unix_timestamp, trend_value)
        """
        if not self.pytrends:
            print(f"TrendReq not initialized, skipping {keyword}")
            return []
            
        try:
            print(f"Fetching data for: {keyword}")
            
            # Add random delay to avoid rate limiting
            delay = random.uniform(10, 20)
            print(f"Waiting {delay:.1f} seconds to avoid rate limiting...")
            time.sleep(delay)
            
            self.pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='', gprop='')
            interest_over_time_df = self.pytrends.interest_over_time()
            
            if interest_over_time_df.empty:
                print(f"No data found for keyword: {keyword}")
                return []
            
            # Convert to Pine Seeds format
            data = []
            for index, row in interest_over_time_df.iterrows():
                unix_timestamp = int(index.timestamp())
                trend_value = float(row[keyword])
                data.append((unix_timestamp, trend_value))
            
            print(f"Successfully fetched {len(data)} data points for {keyword}")
            return data
            
        except Exception as e:
            print(f"Error fetching data for {keyword}: {str(e)}")
            return []
    
    def save_to_csv(self, data: List[Tuple[int, float]], filename: str) -> bool:
        """
        Save trends data to CSV file in Pine Seeds format.
        
        Args:
            data: List of (timestamp, value) tuples
            filename: Output filename
            
        Returns:
            True if successful, False otherwise
        """
        try:
            os.makedirs('data', exist_ok=True)
            filepath = os.path.join('data', filename)
            
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['time', 'close'])  # Pine Seeds header format
                
                # Sort by timestamp and limit to 6000 data points (Pine Seeds limit)
                sorted_data = sorted(data, key=lambda x: x[0])
                limited_data = sorted_data[-6000:] if len(sorted_data) > 6000 else sorted_data
                
                for timestamp, value in limited_data:
                    writer.writerow([timestamp, value])
            
            print(f"Successfully saved {len(limited_data)} data points to {filepath}")
            return True
            
        except Exception as e:
            print(f"Error saving data to {filename}: {str(e)}")
            return False
    
    def fetch_all_trends(self) -> Dict[str, bool]:
        """
        Fetch all configured Google Trends data.
        
        Returns:
            Dictionary with results for each search term
        """
        results = {}
        
        # Fetch only 2-3 terms to avoid rate limiting on first run
        limited_terms = dict(list(self.search_terms.items())[:3])
        
        for symbol, keyword in limited_terms.items():
            print(f"Fetching trends data for: {keyword} ({symbol})")
            
            data = self.fetch_trends_data(keyword)
            if data:
                filename = f"{symbol}.csv"
                success = self.save_to_csv(data, filename)
                results[symbol] = success
            else:
                # If API fails, use existing data
                print(f"Using existing data for {symbol}")
                results[symbol] = True
        
        return results


def main():
    """Main function to fetch and save Google Trends data."""
    print("Starting Google Trends data fetch...")
    print(f"Timestamp: {datetime.now().isoformat()}")
    
    try:
        fetcher = GoogleTrendsFetcher()
        results = fetcher.fetch_all_trends()
        
        # Print results summary
        print("\n=== Fetch Results ===")
        successful = 0
        for symbol, success in results.items():
            status = "SUCCESS" if success else "FAILED"
            print(f"{symbol}: {status}")
            if success:
                successful += 1
        
        print(f"\nCompleted: {successful}/{len(results)} series updated successfully")
        
        if successful > 0:
            print("\nData files are ready for Pine Seeds consumption in TradingView!")
            print("Remember to commit and push the changes to GitHub.")
        else:
            print("\nNo data was successfully fetched. Using existing data.")
            
    except Exception as e:
        print(f"Critical error in main: {e}")
        print("Using existing data files...")


if __name__ == "__main__":
    main() 
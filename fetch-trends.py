from pytrends.request import TrendReq
import pandas as pd
import time
import os

# List of Indian region geocodes
in_region_geocodes = [
    'IN-AN', 'IN-AP', 'IN-AR', 'IN-AS', 'IN-BR', 'IN-CH', 'IN-CT', 'IN-DL', 'IN-DN', 'IN-GA',
    'IN-GJ', 'IN-HP', 'IN-HR', 'IN-JH', 'IN-JK', 'IN-KA', 'IN-KL', 'IN-LA', 'IN-LD', 'IN-MH',
    'IN-ML', 'IN-MN', 'IN-MP', 'IN-MZ', 'IN-NL', 'IN-OR', 'IN-PB', 'IN-PY', 'IN-RJ', 'IN-SK',
    'IN-TN', 'IN-TG', 'IN-TR', 'IN-UP', 'IN-UT', 'IN-WB'
]

def fetch_trends_data(keywords, regions, timeframe='2020-06-04 2024-06-04'):
    pytrends = TrendReq(hl='en-IN', tz=0)  # Use Indian locale and timezone
    all_data = pd.DataFrame()

    for region in regions:
        for keyword in keywords:
            try:
                pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=region, gprop='')
                interest_over_time_df = pytrends.interest_over_time()
                if not interest_over_time_df.empty:
                    interest_over_time_df = interest_over_time_df.drop(columns=['isPartial'])
                    interest_over_time_df['region'] = region
                    interest_over_time_df['keyword'] = keyword
                    all_data = pd.concat([all_data, interest_over_time_df])
                    print(f"Collected data for {keyword} in {region}")
                else:
                    print(f"No data for {keyword} in {region}.")
                time.sleep(60)  # Wait for 60 seconds to avoid hitting the rate limit
            except Exception as e:
                print(f"An error occurred for keyword {keyword} in {region}: {e}")
                time.sleep(60)  # Wait for 60 seconds before retrying with the next keyword

    if not all_data.empty:
        file_path = os.path.join('data', 'combined_trends_data_by_region_in.csv')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        all_data.to_csv(file_path, index=False)
        print(f"Saved combined data to {file_path}")
    else:
        print("No data collected for any keyword.")

if __name__ == "__main__":
    kw_list = [
        "smartphone", "laptop", "headphones", "tablet", "smartwatch",
    ]
    fetch_trends_data(kw_list, in_region_geocodes, timeframe='2020-06-04 2024-06-04')

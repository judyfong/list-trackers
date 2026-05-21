## Vibecoded using google.com
## csv file needs these headers
## YYYY-MM-DD, HH:MM GMT, X mins, workout or commute, exercises,
# csv file is currently called temp-ex.csv would be nice to import it from the
# command line
import csv
import re
from collections import defaultdict

# Dictionary to hold year -> {'total_minutes': 0, 'commute_minutes': 0, 'days': set()}
yearly_summary = defaultdict(lambda: {'total_minutes': 0.0, 'commute_minutes': 0.0, 'days': set()})

try:
    with open('temp-ex.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            clean_row = {k.strip(): (v.strip() if v else '') for k, v in row.items() if k is not None}
            
            date_str = clean_row.get('YYYY-MM-DD', '')
            mins_str = clean_row.get('X mins', '')
            activity_type = clean_row.get('workout or commute', '').lower()
            
            if date_str:
                year = date_str.split('-')[0] # Extracts "YYYY"
                
                numbers_only = re.findall(r'\d+\.?\d*', mins_str)
                mins = float(numbers_only[0]) if numbers_only else 0.0
                
                # Math Aggregation
                yearly_summary[year]['total_minutes'] += mins
                yearly_summary[year]['days'].add(date_str)
                
                # Track commute minutes separately for the percentage math
                if 'commute' in activity_type:
                    yearly_summary[year]['commute_minutes'] += mins

    # Print table headers
    print(f"\n{'Year':<8} | {'Total Mins':<12} | {'Active Days':<12} | {'Commute %':<10}")
    print("-" * 53)
    
    for year in sorted(yearly_summary.keys()):
        total_mins = yearly_summary[year]['total_minutes']
        commute_mins = yearly_summary[year]['commute_minutes']
        days_count = len(yearly_summary[year]['days'])
        
        # Calculate percentage (prevent division by zero error if total_mins is 0)
        commute_pct = (commute_mins / total_mins * 100) if total_mins > 0 else 0.0
        
        print(f"{year:<8} | {total_mins:<12,.1f} | {days_count:<12} | {commute_pct:>8.1f}%")
    print()

except FileNotFoundError:
    print("\nError: 'temp-ex.csv' file not found.")


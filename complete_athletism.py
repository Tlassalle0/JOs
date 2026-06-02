import pandas as pd
import os
import csv
import re

def complete_athletism_file():
    """
    Complete the athletism file by adding all non-winning athletics participants
    from the all_participations data.
    """
    
    # Read the current athletism file (contains only winners - top 3)
    print("Reading athletism.csv (current winners)...")
    athletism_df = pd.read_csv('raw_data/athletism.csv', on_bad_lines='skip')
    
    # Read the processed all_participations file (has gender column)
    print("Reading processed all_participations data...")
    participations_df = pd.read_csv('cleaned_data/all_participations.csv')
    
    # Filter for Athletics discipline only
    athletics_df = participations_df[participations_df['discipline'] == 'Athletics'].copy()
    print(f"Found {len(athletics_df)} athletics participations total")
    
    # Create a set of existing winners to exclude them
    # Use a more efficient approach with name+year+event combination
    winners_set = set()
    for _, row in athletism_df.iterrows():
        # Create a unique identifier for each winner
        name_val = str(row['Name']).upper() if pd.notna(row['Name']) else ''
        event_val = str(row['Event']).upper() if pd.notna(row['Event']) else ''
        identifier = f"{name_val}|{row['Year']}|{event_val}"
        winners_set.add(identifier)
    
    print(f"Found {len(winners_set)} unique winners in athletism.csv")
    
    # Filter out winners from athletics data more efficiently
    # First, filter out medal winners from athletics data
    athletics_non_medalists = athletics_df[
        (athletics_df['medal'].isna()) | 
        (~athletics_df['medal'].isin(['Gold', 'Silver', 'Bronze']))
    ].copy()
    
    print(f"Found {len(athletics_non_medalists)} athletics participants without medals")
    
    # Now filter out those who are already in the winners list
    non_winners = []
    for _, row in athletics_non_medalists.iterrows():
        # Create event name matching the athletism.csv format
        event_name = row['event_name']
        event_clean = str(event_name).strip()
        
        # Handle NaN year
        year_val = int(row['year']) if pd.notna(row['year']) else 0
        
        # Create identifier to check against winners
        identifier = f"{str(row['as']).upper()}|{year_val}|{event_clean.upper()}"
        
        # Check if this is already in winners
        is_winner = identifier in winners_set
        if not is_winner:
            non_winners.append({
                'Gender': 'M' if row['gender'] in ['Men', 'Boys'] else 'W' if row['gender'] in ['Women', 'Girls'] else 'M',
                'Event': event_clean,
                'Location': get_olympic_location(year_val),
                'Year': year_val,
                'Medal': 'None',  # No medal for non-winners
                'Name': row['as'],
                'Nationality': row['noc'],  # Add NOC as Nationality
                'NOC': row['noc'],  # NOC column right after Nationality
                'Result': ''  # No result for non-winners
            })
    
    non_winners_df = pd.DataFrame(non_winners)
    print(f"Found {len(non_winners_df)} non-winning athletics participants")
    
    # Combine winners and non-winners
    # First, add NOC column to existing athletism data if it doesn't exist
    if 'NOC' not in athletism_df.columns:
        athletism_df['NOC'] = athletism_df['Nationality']  # Use Nationality as NOC
    
    # Ensure medal column has proper values for existing data
    athletism_df['Medal'] = athletism_df['Medal'].fillna('None')
    
    # Clean event names to remove commas that cause quoting issues and clean up extra spaces
    athletism_df['Event'] = athletism_df['Event'].str.replace(',', ' ', regex=False).str.replace('  ', ' ', regex=False)
    non_winners_df['Event'] = non_winners_df['Event'].str.replace(',', ' ', regex=False).str.replace('  ', ' ', regex=False)
    
    # Fix number formatting: replace "1 500" with "1500", "3 000" with "3000", etc.
    athletism_df['Event'] = athletism_df['Event'].str.replace(r'(\d)\s+(\d)', r'\1\2', regex=True)
    non_winners_df['Event'] = non_winners_df['Event'].str.replace(r'(\d)\s+(\d)', r'\1\2', regex=True)
    
    # Normalize event names: convert distances to standard meters format
    def normalize_event_name(event):
        if pd.isna(event):
            return event
        event_str = str(event)
        
        # Convert distances like "1500M" to "1500 metres"
        event_str = re.sub(r'(\d+)M\b', r'\1 metres', event_str)
        
        # Convert kilometers to meters
        event_str = re.sub(r'(\d+)\s*kilometre[s]?\b', lambda m: f"{int(m.group(1)) * 1000} metres", event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'(\d+)\s*km\b', lambda m: f"{int(m.group(1)) * 1000} metres", event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'(\d+)\s*Km\b', lambda m: f"{int(m.group(1)) * 1000} metres", event_str, flags=re.IGNORECASE)
        
        # Convert miles to standard track equivalents
        event_str = re.sub(r'\b1\s*mile[s]?\b', '1500 metres', event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'\b2\s*mile[s]?\b', '3000 metres', event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'\b3\s*mile[s]?\b', '5000 metres', event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'\b5\s*mile[s]?\b', '8000 metres', event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'\b10\s*mile[s]?\b', '16000 metres', event_str, flags=re.IGNORECASE)
        
        # Convert yards to meters
        event_str = re.sub(r'\b60\s*yard[s]?\b', '55 metres', event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'\b100\s*yard[s]?\b', '100 metres', event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'\b120\s*yard[s]?\b', '110 metres', event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'\b220\s*yard[s]?\b', '200 metres', event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'\b440\s*yard[s]?\b', '400 metres', event_str, flags=re.IGNORECASE)
        event_str = re.sub(r'\b880\s*yard[s]?\b', '800 metres', event_str, flags=re.IGNORECASE)
        
        # Fix specific steeplechase conversion: 2590 metres should be 2500 metres
        event_str = re.sub(r'\b2590\s*metres\s*Steeplechase\b', '2500 metres Steeplechase', event_str, flags=re.IGNORECASE)
        
        # Remove gender suffixes since gender is in separate column
        event_str = re.sub(r'\s+(Men|Women|Mixed|Boys|Girls)\s*$', '', event_str, flags=re.IGNORECASE)
        
        # Clean up extra spaces
        event_str = re.sub(r'\s+', ' ', event_str).strip()
        return event_str
    
    athletism_df['Event'] = athletism_df['Event'].apply(normalize_event_name)
    non_winners_df['Event'] = non_winners_df['Event'].apply(normalize_event_name)
    
    # Reorder columns to match desired format: Gender,Event,Location,Year,Medal,Name,Nationality,NOC,Result
    athletism_df = athletism_df[['Gender', 'Event', 'Location', 'Year', 'Medal', 'Name', 'Nationality', 'NOC', 'Result']]
    non_winners_df = non_winners_df[['Gender', 'Event', 'Location', 'Year', 'Medal', 'Name', 'Nationality', 'NOC', 'Result']]
    
    combined_df = pd.concat([athletism_df, non_winners_df], ignore_index=True)
    
    # Filter to only athletics events (exclude other sports)
    athletics_keywords = [
        'metres', 'mile', 'yard', 'Relay', 'Hurdles', 'Steeplechase', 'Jump', 'Throw', 
        'Shot Put', 'Discus', 'Hammer', 'Javelin', 'Pole Vault', 'High Jump', 'Long Jump',
        'Triple Jump', 'Marathon', 'Race Walk', 'Cross-Country', 'Decathlon', 'Heptathlon',
        'Pentathlon', 'Team All-Around', 'Individual All-Around'
    ]
    
    def is_athletics_event(event):
        if pd.isna(event):
            return False
        event_str = str(event).lower()
        return any(keyword.lower() in event_str for keyword in athletics_keywords)
    
    combined_df = combined_df[combined_df['Event'].apply(is_athletics_event)]
    
    # Sort by Year, Event, and Medal (winners first)
    combined_df['medal_sort'] = combined_df['Medal'].map({'G': 1, 'S': 2, 'B': 3, '': 4}).fillna(4)
    combined_df = combined_df.sort_values(['Year', 'Event', 'medal_sort'])
    combined_df = combined_df.drop('medal_sort', axis=1)
    
    # Save the completed file without quotes around event names
    output_file = 'cleaned_data/athletism_completed.csv'
    combined_df.to_csv(output_file, index=False, quoting=csv.QUOTE_NONE, escapechar='\\')
    
    print(f"\nCompleted athletism file saved to: {output_file}")
    print(f"Total participants: {len(combined_df)}")
    print(f"Original winners: {len(athletism_df)}")
    print(f"Added non-winners: {len(non_winners_df)}")
    
    # Show sample of the data
    print("\nSample of completed data:")
    print(combined_df.head(15))
    
    # Show some statistics
    print(f"\nStatistics:")
    print(f"Years covered: {combined_df['Year'].min()} - {combined_df['Year'].max()}")
    print(f"Unique events: {combined_df['Event'].nunique()}")
    print(f"Unique athletes: {combined_df['Name'].nunique()}")
    print(f"Medal distribution:")
    print(combined_df['Medal'].value_counts())
    
    return combined_df

def get_olympic_location(year):
    """
    Get the Olympic host location for a given year.
    """
    locations = {
        1896: 'Athens',
        1900: 'Paris',
        1904: 'St Louis',
        1908: 'London',
        1912: 'Stockholm',
        1920: 'Antwerp',
        1924: 'Paris',
        1928: 'Amsterdam',
        1932: 'Los Angeles',
        1936: 'Berlin',
        1948: 'London',
        1952: 'Helsinki',
        1956: 'Melbourne / Stockholm',
        1960: 'Rome',
        1964: 'Tokyo',
        1968: 'Mexico',
        1972: 'Munich',
        1976: 'Montreal',
        1980: 'Moscow',
        1984: 'Los Angeles',
        1988: 'Seoul',
        1992: 'Barcelona',
        1996: 'Atlanta',
        2000: 'Sydney',
        2004: 'Athens',
        2008: 'Beijing',
        2012: 'London',
        2016: 'Rio',
        2020: 'Tokyo'
    }
    return locations.get(year, 'Unknown')

if __name__ == "__main__":
    completed_df = complete_athletism_file()

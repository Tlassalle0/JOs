import pandas as pd
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def list_all_events():
    """
    List all unique events from the athletism completed file
    """
    # Read the completed athletism file
    print("Reading athletism_completed.csv...")
    df = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', '2-cleaned_data', 'athletism_completed.csv'), on_bad_lines='skip')
    
    # Get unique events
    unique_events = df['Event'].unique()
    
    # Sort events alphabetically
    sorted_events = sorted(unique_events)
    
    print(f"\nTotal unique events: {len(sorted_events)}")
    print("=" * 50)
    
    # Print each event with count
    for event in sorted_events:
        count = len(df[df['Event'] == event])
        print(f"{event:<40} ({count} participants)")
    
    # Show some statistics
    print(f"\nStatistics:")
    print(f"Total participants: {len(df)}")
    print(f"Years covered: {df['Year'].min()} - {df['Year'].max()}")
    print(f"Gender distribution:")
    gender_counts = df['Gender'].value_counts()
    for gender, count in gender_counts.items():
        print(f"  {gender}: {count}")

if __name__ == "__main__":
    list_all_events()

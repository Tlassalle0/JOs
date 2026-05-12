import pandas as pd

def list_all_events():
    """
    List all unique events from the athletism completed file
    """
    # Read the completed athletism file
    print("Reading athletism_completed.csv...")
    df = pd.read_csv('cleaned_data/athletism_completed.csv', on_bad_lines='skip')
    
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
    
    # Also save to a text file for easy reference
    with open('athletics_events_list.txt', 'w', encoding='utf-8') as f:
        f.write(f"Athletics Events List\n")
        f.write(f"Total unique events: {len(sorted_events)}\n")
        f.write("=" * 50 + "\n\n")
        
        for event in sorted_events:
            count = len(df[df['Event'] == event])
            f.write(f"{event:<40} ({count} participants)\n")
    
    print(f"\nEvents list also saved to: athletics_events_list.txt")
    
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

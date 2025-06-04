import pandas as pd
import numpy as np

DATA_FILE = "donor_data.csv"
SUMMARY_FILE = "donor_summary.csv"
DONATION_GAP_DAYS = 90

# Initialize donors DataFrame with explicit dtypes to avoid FutureWarning
donors = pd.DataFrame({
    'Name': pd.Series(dtype='str'),
    'Blood Group': pd.Series(dtype='str'),
    'Donation Date': pd.Series(dtype='str'),
    'Volume (ml)': pd.Series(dtype='float')
})

# Try to load existing data if available
try:
    donors = pd.read_csv(DATA_FILE, dtype={
        'Name': str,
        'Blood Group': str,
        'Donation Date': str,
        'Volume (ml)': float
    })
except FileNotFoundError:
    pass

def get_today_str():
    return str(pd.Timestamp.today().date())

def date_diff_days(date1, date2):
    arr1 = pd.to_datetime(date1)
    arr2 = pd.to_datetime(date2)
    return (arr1 - arr2).days

def mark_eligibility():
    if donors.empty:
        return pd.DataFrame()
    today = get_today_str()
    donors['Donation Date'] = donors['Donation Date'].astype(str)
    last_donation = donors.groupby('Name')['Donation Date'].max().reset_index()
    last_donation['Days Since Last'] = last_donation['Donation Date'].apply(lambda d: date_diff_days(today, d))
    last_donation['Eligibility'] = np.where(
        last_donation['Days Since Last'] >= DONATION_GAP_DAYS, "Eligible", "Not Eligible"
    )
    blood_groups = donors.groupby('Name')['Blood Group'].first().reset_index()
    last_donation = last_donation.merge(blood_groups, on='Name', how='left')
    return last_donation

def not_eligible_message(days_since_last):
    days_left = DONATION_GAP_DAYS - days_since_last
    if days_left > 0:
        return f"You are not eligible to donate blood. Please wait at least {days_left} more day(s)."
    else:
        return ""

def is_user_eligible(name):
    elig_df = mark_eligibility()
    if elig_df is None or elig_df.empty:
        return True, ""
    matches = elig_df[elig_df['Name'].str.lower() == name.lower()]
    if matches.empty:
        return True, ""
    donor = matches.to_dict('records')[0]
    if donor['Eligibility'] == "Not Eligible":
        return False, not_eligible_message(donor['Days Since Last'])
    return True, ""

def get_existing_blood_group(name):
    matches = donors[donors['Name'].str.lower() == name.lower()]
    if not matches.empty:
        donor = matches.to_dict('records')[0]
        return donor['Blood Group']
    return None

def add_donor():
    name = input("Enter donor's name: ").strip().title()
    is_eligible, msg = is_user_eligible(name)
    if not is_eligible:
        print(msg)
        return
    existing_bg = get_existing_blood_group(name)
    if existing_bg:
        blood_group = existing_bg
        print(f"Blood group for {name} found as {blood_group}.")
    else:
        blood_group = input("Enter blood group (e.g., A+, O-): ").strip().upper()
    date_input = input("Enter donation date (YYYY-MM-DD) [leave blank for today]: ").strip()
    volume = float(input("Enter donation volume in ml: ").strip())
    donation_date = date_input if date_input else get_today_str()
    global donors
    new_row = {
        "Name": name,
        "Blood Group": blood_group,
        "Donation Date": donation_date,
        "Volume (ml)": volume
    }
    donors = pd.concat([donors, pd.DataFrame([new_row])], ignore_index=True)
    print(f"Donation by {name} logged successfully.")

def show_eligibility():
    elig = mark_eligibility()
    if elig is not None and not elig.empty:
        print("\nEligibility Status based on 90-day rule")
        print(f"{'Name':25}    {'Blood Group':15}    {'Last Donation':>16}    {'Days Since':>14}    {'Eligibility':>12}")
        for _, row in elig.sort_values(by='Donation Date', ascending=False).iterrows():
            print(f"{row['Name']:25}    {row['Blood Group']:15}    {row['Donation Date']:>16}    {int(row['Days Since Last']):>14}    {row['Eligibility']:>12}")
        print()

def show_summary():
    if donors.empty:
        print("No donation records found.")
        return
    summary = donors.groupby('Name').agg({
        'Blood Group': 'first',
        'Volume (ml)': 'sum',
        'Donation Date': ['count', 'max']
    })
    summary.columns = ['Blood Group', 'Total Volume (ml)', 'Donation Count', 'Last Donation']
    summary = summary.reset_index()
    today = get_today_str()
    summary['Days Since Last Donation'] = summary['Last Donation'].apply(lambda d: date_diff_days(today, d))
    summary = summary.sort_values(by='Last Donation', ascending=False)
    print("\nDonor Summary")
    print(f"{'Name':25}    {'Blood Group':15}    {'Total(ml)':>12}    {'Count':>8}    {'Last Donation':>16}    {'Days Since':>14}")
    for _, row in summary.iterrows():
        print(f"{row['Name']:25}    {row['Blood Group']:15}    {int(row['Total Volume (ml)']):>12}    {int(row['Donation Count']):>8}    {row['Last Donation']:>16}    {int(row['Days Since Last Donation']):>14}")
    print()

def export_csv():
    donors.to_csv(DATA_FILE, index=False)
    if not donors.empty:
        summary = donors.groupby('Name').agg({
            'Blood Group': 'first',
            'Volume (ml)': 'sum',
            'Donation Date': ['count', 'max']
        })
        summary.columns = ['Blood Group', 'Total Volume (ml)', 'Donation Count', 'Last Donation']
        summary = summary.reset_index()
        today = get_today_str()
        summary['Days Since Last Donation'] = summary['Last Donation'].apply(lambda d: date_diff_days(today, d))
        summary.to_csv(SUMMARY_FILE, index=False)
    print("All records and summaries exported to CSV files.")

def main():
    while True:
        print("\n=== Blood Donation Log System ===")
        print("1. Add new donor donation")
        print("2. Check eligibility of donors")
        print("3. Show donor summary")
        print("4. Export data to CSV")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            add_donor()
        elif choice == '2':
            show_eligibility()
        elif choice == '3':
            show_summary()
        elif choice == '4':
            export_csv()
        elif choice == '5':
            export_csv()
            print("Thank you for using the Blood Donation Log System.")
            break
        else:
            print("Invalid choice. Please try again.")

main()
# Blood Donation Log System

A comprehensive management system for tracking blood donations, donor eligibility, and donation statistics.

## Description

This Blood Donation Log System is a command-line Python application designed to help blood donation centers track donors, donations, and eligibility. The system maintains records of donors, their blood groups, donation dates, and volumes, while automatically calculating eligibility based on the standard 90-day rule.

## Features

- **Donor Management**: Add and track blood donors with relevant information
- **Blood Group Tracking**: Automatically remembers returning donors' blood groups
- **Eligibility Calculation**: Enforces the 90-day rule between donations
- **Summary Statistics**: View aggregated data about donors and donations
- **Data Export**: Export records and summaries to CSV files for backup or analysis
- **User-Friendly Interface**: Simple command-line interface for all operations

## Installation

```bash
# Clone the repository
git clone https://github.com/ThekingGST/Blood-Donation-Log-System.git

# Navigate to the project directory
cd Blood-Donation-Log-System

```

## Usage

```bash
# Run the main program
python main.py
```

### Main Functions

The system includes several key functions:

1. **Add Donor** - Record a new blood donation with donor details
2. **Show Eligibility** - Display which donors are eligible to donate based on the 90-day rule
3. **Show Summary** - View comprehensive statistics about all donors
4. **Export Data** - Save all records to CSV files

## Data Structure

The system tracks the following information for each donation:

- **Name**: Donor's full name
- **Blood Group**: Donor's blood type (e.g., A+, O-, B+)
- **Donation Date**: Date when donation occurred
- **Volume**: Amount of blood donated in milliliters
- **Days Since Last Donation**: Calculated field for eligibility checking

## Dependencies

- Python 3.6+
- pandas: For data manipulation and analysis

## Author

Created by ThekingGST

---

*This project was developed as a personal project assigned by my club.*

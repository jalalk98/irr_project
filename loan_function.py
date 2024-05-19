from dateutil.relativedelta import relativedelta
import numpy_financial as npf
import pandas as pd
from datetime import datetime

with open("input.txt", "r") as file:
    for line in file:
        key, value = line.strip().split("=")
        key = key.strip()
        value = value.strip()
        if key == "valuation_date":
            valuation_date = datetime.strptime(value, "%Y-%m-%d").date()
        elif key == "grade":
            grade = value
        elif key == "issue_date":
            issue_date = datetime.strptime(value, "%Y-%m-%d").date()
        elif key == "term":
            term = float(value)
        elif key == "coupon_rate":
            coupon_rate = float(value)
        elif key == "invested":
            invested = float(value)
        elif key == "os_balance":
            os_balance = float(value)
        elif key == "recovery_rate":
            recovery_rate = float(value)
        elif key == "purchase_premium":
            purchase_premium = float(value)
        elif key == "service_fee":
            service_fee = float(value)
        elif key == "earnout_fee":
            earnout_fee = float(value)
        elif key == "default_multiplier":
            default_multiplier = float(value)
        elif key == "prepay_multiplier":
            prepay_multiplier = float(value)
        elif key == "product_pos":
            product_pos = int(value)


def calculate_playdate(row):
    if row['Months'] == 1:
        return issue_date # type: ignore
    else:
        return issue_date + relativedelta(months=int(row['Months'] - 1)) # type: ignore

def calculate_scheduled_principal(month):
    if month == 1:
        return 0
    else:
        return npf.ppmt(coupon_rate/12, month-1, term, -invested)

def calculate_scheduled_interest(month, scheduled_principal):
    if month == 1:
        return 0
    else:
        payment = npf.pmt(coupon_rate/12, term, -invested)
        return payment - scheduled_principal

previous_balance = invested
def calculate_scheduled_balance(month, df):
    global previous_balance
    if month == 1:
        previous_balance = invested
        return invested
    else:
        scheduled_principal = df.loc[month-1, 'Scheduled_Principal']
        sch_balance = previous_balance - scheduled_principal
        previous_balance = sch_balance
        return sch_balance

def calculate_prepay(row, df_prepay):
    if row['Months'] == 1:
        return 0
    else:
        term_col = str(term).split(".",1)[0] + 'M'
        prepay_str = df_prepay.loc[row['Months']-2, term_col].replace('%', '')  # Remove quotes and '%' symbol
        prepay_float = float(prepay_str) * 100  # Convert to float and multiply by 100
        return prepay_float

def calculate_default_rate(row, df_charge):
    month = row['Months']
    value = df_charge.iloc[month - 1, product_pos]
    if isinstance(value, str) and '%' in value:
        value = value.replace('%', '')
        return float(value) * 100  # Convert to float and handle as percentage
    return value  # Return as is if it's not a string with '%'
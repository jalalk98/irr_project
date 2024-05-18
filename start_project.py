import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import numpy_financial as npf

file_path = 'Loan IRR Calc Model.xlsx'
sheet_name1 = 'Prepay'
sheet_name2 = "Charged Off"

df_prepay = pd.read_excel(file_path,sheet_name=sheet_name1, header = 1) # second row as header
df_prepay = df_prepay.applymap(lambda x: f'{x:.17f}%' if isinstance(x, float) else x)

df_charge = pd.read_excel(file_path,sheet_name=sheet_name2)
df_charge = df_charge.applymap(lambda x: f'{x:.17f}%' if isinstance(x, float) else x)

pd.options.display.float_format = '{:.2f}'.format
# pd.options.display.float_format = '{:.12f}%'.format

valuation_date = datetime(2017, 12, 31)
grade = "C4" 
issue_date = datetime(2015, 8, 24)
term = 36
coupon_rate = 0.28
invested = 7500
os_balance = 3228.61
recovery_rate = 0.08
purchase_premium = 0.0514
service_fee = 0.025
earnout_fee = 0.025
default_multiplier = 1
prepay_multiplier = 1
product_pos = 66

previous_balance = invested
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


def calculate_scheduled_balance(month):
    global previous_balance
    if month == 1:
        previous_balance = invested
        return invested
    else:
        scheduled_principal = df.loc[month-1, 'Scheduled_Principal']
        sch_balance = previous_balance - scheduled_principal
        previous_balance = sch_balance
        return sch_balance

def calculate_prepay(row):
    if row['Months'] == 1:
        return 0
    else:
        term_col = str(term) + 'M'
        prepay_str = df_prepay.loc[row['Months']-2, term_col].replace('%', '')  # Remove quotes and '%' symbol
        prepay_float = float(prepay_str) * 100  # Convert to float and multiply by 100
        return prepay_float

def calculate_default_rate(row):
    month = row['Months']
    value = df_charge.iloc[month - 1, product_pos]
    if isinstance(value, str) and '%' in value:
        value = value.replace('%', '')
        return float(value) * 100  # Convert to float and handle as percentage
    return value  # Return as is if it's not a string with '%'

df = pd.DataFrame({'Months': range(1, 38)})
df['Payment_Count'] = df['Months'].apply(lambda x: 0 if x == 1 else x - 1)
df['Playdate'] = df.apply(calculate_playdate, axis=1)
df['Scheduled_Principal'] = df['Months'].apply(calculate_scheduled_principal)
df['Scheduled_Interest'] = df.apply(lambda row: calculate_scheduled_interest(row['Months'], row['Scheduled_Principal']), axis=1)
df['Scheduled_Balance'] = df['Months'].apply(calculate_scheduled_balance)
df['Prepay'] = df.apply(calculate_prepay, axis=1)
df['Default_Rate'] = df.apply(calculate_default_rate, axis=1)



print(df)

import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from 

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


df = pd.DataFrame({'Months': range(1, 38)})
df['Payment_Count'] = df['Months'].apply(lambda x: 0 if x == 1 else x - 1)
df['Playdate'] = df.apply(calculate_playdate, axis=1)
df['Scheduled_Principal'] = df['Months'].apply(calculate_scheduled_principal)


print(df)

import pandas as pd
import numpy_financial as npf

file_path = 'D:\\User\\Downloads\\Loan IRR Calc Model.xlsx'
sheet_name = 'IRR Calculation'

df = pd.read_excel(file_path,sheet_name=sheet_name)

cash_flows = df['Total_CF'].to_list()

irr = npf.irr(cash_flows)*12

print(f"The Internal Rate of Return (IRR) is: {irr:.2%}")
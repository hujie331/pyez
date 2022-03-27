import pandas as pd

read_file=pd.read_excel(r'inventory_sjca_spare.xlsx')
read_file.to_csv(r'inventory_sjca_spare.csv', index=None,header=True)
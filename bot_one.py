import pandas as pd 
import	numpy as np
import MetaTrader5 as mt5 
import functions as fc 
import time
from func_meta import extrair_base, comprar_mercado, vender_mercado, total_ordens


#comprar_mercado('EURUSD', 2.5)
#total = total_ordens()
#print(total+5)
#time.sleep(40)
#vender_mercado('EURUSD', 2.5)

data = extrair_base('PETR4', 'D1', 1000)
data
import re
import warnings
warnings.filterwarnings(action='ignore')
from glob import glob
from tqdm import tqdm
from datetime import datetime
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm
from mplfinance.original_flavor import candlestick2_ohlc


font_path = 'C:/Windows/Fonts/H2HDRM.TTF'
fontprop = fm.FontProperties(fname=font_path, size=18)


kospi = pd.read_csv('data/kospi_info.csv', index_col=False)
kosdaq = pd.read_csv('data/kosdaq_info.csv', index_col=False)

kospi_code = list(kospi['code'])
kosdaq_code = list(kosdaq['code'])

kospi_name = list(kospi['name'])
kosdaq_name = list(kosdaq['name'])


def save_price(code_list, count):
    for code in tqdm(code_list, total=len(code_list)):
        rate = []
        code = re.sub('[^0-9]+', '', code)
        url = f'https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe=day&count={str(count)}&requestType=0'
        url = requests.get(url)
        soup = BeautifulSoup(url.content, 'html.parser')

        item_list = soup.find_all('item')
        data = []
        for item in item_list:
            item_info = item.get('data').split('|')
            if '0' in item_info:
                stop_price = item_info[4]
                for i in range(1,5):
                    item_info[i] = stop_price
            data.append(item_info)
        dataframe = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'], data=data)
        for i in range(len(dataframe)):
            if i == 0:
                rate.append(0)
            else:
                rate.append(int(dataframe['close'][i])/int(dataframe['close'][i-1]) - 1)
        dataframe['rate'] = rate
        dataframe['dir'] = [1 if r >= 0 else 0 for r in rate]
        dataframe.to_csv(f'sample/A{code}.csv', index=False)


save_price(kospi_code, 800)
save_price(kosdaq_code, 800)
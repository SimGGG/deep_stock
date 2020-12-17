import re
from datetime import datetime
from tqdm import tqdm
from mplfinance.original_flavor import candlestick2_ohlc
import warnings; warnings.filterwarnings("ignore")
from glob import glob

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker
from mplfinance.original_flavor import candlestick2_ohlc

### description ###
# drw_ : Entire plot of candle and volume
# draw_candle : plot of candle
# draw_volume : plot of volume


# set font for plot title
font_path = 'C:/Windows/Fonts/H2HDRM.TTF' # custom fonts path
fontprop = fm.FontProperties(fname=font_path, size=18)

# Load corp. info
kospi = pd.read_csv('data/kospi_info.csv', index_col=False)
kosdaq = pd.read_csv('data/kosdaq_info.csv', index_col=False)

kospi_code = list(kospi['code'])
kosdaq_code = list(kosdaq['code'])

kospi_name = list(kospi['name'])
kosdaq_name = list(kosdaq['name'])


code_name_dic = {}
for c1, c2, n1, n2 in zip(kospi_code, kosdaq_code, kospi_name, kosdaq_name):
    code_name_dic[c1] = n1
    code_name_dic[c2] = n2



def draw_(data, code, name):
    fig = plt.figure(figsize=(10,10))
    gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])
    ax = []
    ax.append(plt.subplot(gs[0]))
    ax.append(plt.subplot(gs[1], sharex=ax[0]))
    ax[0].get_xaxis().set_visible(False)
    index = data.index.astype('str') # 캔들스틱 x축이 str로 들어감

    # 지수 이동평균선 데이터 구하기
    data['MA5'] = data['close'].rolling(5).mean()
    data['MA20'] = data['close'].rolling(20).mean()
    data['MA60'] = data['close'].rolling(60).mean()
    data['MA120'] = data['close'].rolling(120).mean()

    # 이동평균선 그리기
    ax[0].plot(index, data['MA5'], label='MA5', linewidth=1.0, color = 'tab:red')
    ax[0].plot(index, data['MA20'], label='MA20', linewidth=2.0, color = 'darkorange')
    ax[0].plot(index, data['MA60'], label='MA60', linewidth=1.0, color = 'darkgreen')
    ax[0].plot(index, data['MA120'], label='MA120', linewidth=1.0, color = 'black')

    # X축 티커 숫자 30개로 제한
    ax[0].xaxis.set_major_locator(ticker.MaxNLocator(30))

    # 그래프 title과 축 이름 지정
    ax[0].set_title(f'{name}', fontsize=22, fontproperties=fontprop)
    ax[0].set_xlabel('Date')
    plt.xticks(rotation=45, size=5)

    # 캔들차트 그리기
    x = np.arange(len(data.index))
    candlestick2_ohlc(ax[0], data['open'], data['high'],
                      data['low'], data['close'],
                      width=0.6, colorup='tab:red', colordown='mediumblue')
    ax[0].legend()

    # 거래량 그래프 그리기
    ax[1].bar(x, data.volume, color='k', width=0.6, align='center')
    plt.tight_layout()

    # hide plot outline
    fig.patch.set_visible(False)
    ax[0].axis('off')
    ax[1].axis('off')
    plt.savefig(f'./sample_candle_250_1x1/{code}.jpg', dpi=200)
    plt.grid()
    plt.show()
    plt.close()


def draw_candle(data, code, name):
    fig = plt.figure(figsize=(10,10))
    ax = fig.add_subplot(111)


    index = data.index.astype('str')  # 캔들스틱 x축이 str로 들어감
    x = np.arange(len(data.index))

    # 그래프 title과 축 이름 지정
    ax.set_title(f'{name}', fontsize=22, fontproperties=fontprop)
    ax.set_xlabel('Date')
    plt.xticks(rotation=45, size=5)

    candlestick2_ohlc(ax, data['open'], data['high'],
                      data['low'], data['close'],
                      width=0.6, colorup='tab:red', colordown='mediumblue')
    plt.tight_layout()
    ax.axis('on') # if hide plot axis, replace to off
    fig.patch.set_visible(False)
    plt.savefig(f'./{code}.jpg', dpi=200)
    # plt.grid()
    # plt.show()


def draw_volume(data, code, name):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)
    index = data.index.astype('str')  # 캔들스틱 x축이 str로 들어감
    x = np.arange(len(data.index))

    # 그래프 title과 축 이름 지정
    ax.set_title(f'{name}', fontsize=22, fontproperties=fontprop)
    ax.set_xlabel('Date')
    plt.xticks(rotation=45, size=5)

    ax.bar(x, data.volume, color='k', width=0.6, align='center')
    ax.axis('on') # if hide plot axis, replace to off
    plt.tight_layout()
    fig.patch.set_visible(False)
    plt.savefig(f'./{code}.jpg', dpi=200)
    # plt.grid()
    # plt.show()





sample_list = glob('./sample/*.csv') # Crawled data path
window_start = -100 # start date of window
window_end = -1 # end date of window

for sample in tqdm(sample_list):
    code = re.findall('[A-Z0-9]+', sample)[0]
    name = code_name_dic[code]
    data = pd.read_csv(sample, index_col=False)
    data.index = list(map(lambda x: datetime.strptime(str(x), '%Y%m%d').date(), data['date']))
    data.drop(columns=['date'], inplace=True)

    draw_(data.iloc[window_start:window_end, :], code, name)
    draw_candle(data.iloc[window_start:window_end, :], code, name)
    draw_volume(data.iloc[window_start:window_end, :], code, name)


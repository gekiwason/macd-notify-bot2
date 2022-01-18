import ccxt
import os
import time
import datetime
import talib as ta
import pandas as pd
import requests
from pprint import pprint
import json
from linebot import (LineBotApi, WebhookHandler)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage)
from linebot.exceptions import (LineBotApiError, InvalidSignatureError)
from dotenv import load_dotenv

load_dotenv('.env') 
binance = ccxt.binance()

# line送信用token,api
line_notify_id = os.getenv('LINE_NOTIFY_ID')
line_notify_token = os.getenv('LINE_NOTIFY_TOKEN')

df = "NaN"
cycle = 0
golden_cross_symbol_list = ["\nBinance_MACD_GC一覧"]
dead_cross_symbol_list = ["\nMACD_DC一覧"]

# 時間軸設定(単位は時間)
TIME_MARGIN = 1


def read_crypt_pricedata():
    try:
        # CSV読み込み
        df = pd.read_csv('BinanceAllCryptPriceData.csv', index_col=0)
    except:
        print("BinanceAllCryptPriceData.csvが見つかりませんでした", flush=True)

    return df


def get_all_crypt_pricedata():
    try:
        AllCryptPriceData = binance.fetchTickers()
        current_price_df = pd.DataFrame(AllCryptPriceData)

        # closeのみ抽出
        current_price_df = pd.DataFrame(current_price_df.loc["close"])

        # 行列反転
        current_price_df = current_price_df.T
    except:
        print("Binanceから価格情報を取得できませんでした", flush=True)

    return current_price_df


def add_current_price(df, current_price_df):
    # 今日の日付で行追加
    try:
        # 日時取得
        d_today = datetime.datetime.now()
        df.loc[d_today] = "NaN"
    except:
        print("日時情報を取得できませんでした", flush=True)

    symbolList = current_price_df.columns
    for symbol in symbolList:
        if symbol in df.columns:
            # csvに該当シンボルがある
            df.loc[d_today, symbol] = current_price_df.loc["close", symbol]
        else:
            # csvに該当シンボルが無い（新規上場）
            df[symbol] = "NaN"
            df.loc[d_today, symbol] = current_price_df.loc["close", symbol]

    return df


def write_crypt_pricedata(df):
    try:
        # CSV読み込み
        df.to_csv("BinanceAllCryptPriceData.csv")
    except:
        print("BinanceAllCryptPriceData.csvに書き込めませんでした", flush=True)


def cal_tech_incicator(df):
    golden_cross_symbol_list = ["MACD_GC一覧"]
    dead_cross_symbol_list = ["\n", "\nMACD_DC一覧"]
    golden_cross_count = 0
    dead_cross_count = 0

    symbolList = current_price_df.columns
    for symbol in symbolList:
        # macd計算
        close = df[symbol]
        macd, macdsignal, macdhist = ta.MACD(close, fastperiod=6, slowperiod=19, signalperiod=9)

        try:
            if macd.iloc[-1] < 0 and macdsignal.iloc[-1] < 0:

                if macdhist.iloc[-2] < 0 and macdhist.iloc[-1] > 0:
                    golden_cross_symbol_list.append("\n" + symbol)
                    golden_cross_count += 1

            elif macd.iloc[-1] > 0 and macdsignal.iloc[-1] > 0:

                if macdhist.iloc[-2] > 0 and macdhist.iloc[-1] < 0:
                    dead_cross_symbol_list.append("\n" + symbol)
                    dead_cross_count += 1

        except:
            print("macdの計算に失敗しました", flush=True)

    golden_cross_symbol_list.insert(1, "\nGC数:" + str(golden_cross_count))
    dead_cross_symbol_list.insert(2, "\nDC数:" + str(dead_cross_count))

    return golden_cross_symbol_list, dead_cross_symbol_list


def send_line(golden_cross_symbol_list, dead_cross_symbol_list, cycle):
   try:
        if cycle != 1:
            message = golden_cross_symbol_list + dead_cross_symbol_list

        else:
            message = "Binance_全銘柄MACD_GC_DC通知プログラムを起動しました"

        message = "".join(message)
        line_bot_api = LineBotApi(channel_access_token=line_notify_token)
        line_bot_api.push_message(line_notify_id, TextSendMessage(text=message))

   except:
        print("ラインを送信できませんでした", flush=True)


print("Binance_全銘柄MACCDゴールデンクロス通知プログラムを起動しました", flush=True)
while True:
    cycle += 1
    print(cycle, "回目の価格取得です", flush=True)

    if os.path.exists('BinanceAllCryptPriceData.csv'):
        df = read_crypt_pricedata()
        current_price_df = get_all_crypt_pricedata()
        df = add_current_price(df, current_price_df)
        golden_cross_symbol_list, dead_cross_symbol_list = cal_tech_incicator(df)
        write_crypt_pricedata(df)
        send_line(golden_cross_symbol_list, dead_cross_symbol_list, cycle)

    else:
        # 初回起動時用
        df = get_all_crypt_pricedata()
        df.drop('close', axis=0)
        df.set_axis([datetime.datetime.now()], axis=0, inplace=True)
        write_crypt_pricedata(df)
        send_line(golden_cross_symbol_list, dead_cross_symbol_list, cycle)

    time.sleep(TIME_MARGIN * 3600)

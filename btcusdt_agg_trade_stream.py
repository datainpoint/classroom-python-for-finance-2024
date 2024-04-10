import sqlite3
import asyncio
from websockets import connect
import json
import aiosqlite

conn = sqlite3.connect("agg_trade.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS btcusdt;")
create_table_statement = """
CREATE TABLE btcusdt (
    id UNSIGNED BIG INT PRIMARY KEY,
    trade_time UNSIGNED BIG INT,
    price float,
    quantity float
)
"""
cursor.execute(create_table_statement)
cursor.execute("CREATE INDEX idx_trade_time ON btcusdt(trade_time);")
conn.commit()
conn.close()

async def insert_data_into_db(url):
    async with connect(url) as websocket:
        data_dicts = []
        while True:
            data_str = await websocket.recv()
            data_dict = json.loads(data_str)
            data_to_append = (data_dict["a"], data_dict["T"], data_dict["p"], data_dict["q"])
            data_dicts.append(data_to_append)
            print(data_dict)
            if len(data_dicts) > 10:
                print("Inserting into DB...")
                async with aiosqlite.connect("agg_trade.db") as db:
                    await db.executemany("""INSERT INTO btcusdt (id, trade_time, price, quantity) VALUES (?, ?, ?, ?)""", data_dicts)
                    await db.commit()
                data_dicts = []
                
url = "wss://fstream.binance.com/ws/btcusdt@aggTrade"
asyncio.run(insert_data_into_db(url))
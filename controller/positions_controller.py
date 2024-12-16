from contextlib import closing

import pymysql
from pymysql.cursors import DictCursor

from config import db_config


class PositionsController:
    def __init__(self):
        self.conn = pymysql.connect(**db_config, cursorclass=DictCursor)
        self.create_positions_table()

    def create_positions_table(self):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS idx_positions (
                                idx_position_id INT AUTO_INCREMENT PRIMARY KEY,
                                zerodha_instrument_token INT,
                                index_name VARCHAR(255),
                                exchange VARCHAR(255),
                                direction INT,
                                position_entry_time DATETIME,
                                position_entry_price FLOAT,
                                position_exit_time DATETIME,
                                position_exit_price FLOAT,
                                exit_reason VARCHAR(255),
                                profit FLOAT
                            )
                        ''')
            cursor.execute('''CREATE TABLE IF NOT EXISTS opt_positions (
                                opt_position_id INT AUTO_INCREMENT PRIMARY KEY,
                                idx_position_id INT,
                                zerodha_instrument_token INT,
                                zerodha_trading_symbol VARCHAR(255),
                                zerodha_name VARCHAR(255),
                                zerodha_exchange VARCHAR(255),
                                alice_token VARCHAR(255),
                                alice_trading_symbol VARCHAR(255),
                                alice_name VARCHAR(255),
                                alice_exchange VARCHAR(255),
                                index_name VARCHAR(255),
                                direction INT,
                                position_type INT COMMENT 
                                '1 = OPT BUY\r\n2 = OPT SELL',
                                position_entry_time DATETIME,
                                position_entry_price FLOAT,
                                position_exit_time DATETIME,
                                position_exit_price FLOAT,
                                exit_reason VARCHAR(255),
                                profit FLOAT,
                                lot_size INT,
                                expiry DATE
                            )
                    ''')
            self.conn.commit()

    def get_index_positions(self, status):
        with closing(self.conn.cursor()) as cursor:
            if status == "active":
                cursor.execute('''
                    SELECT * FROM idx_positions 
                    WHERE position_exit_time IS NULL 
                      AND DATE(position_entry_time) = CURRENT_DATE
                    ORDER BY position_entry_time DESC
                ''')
            elif status == "closed":
                cursor.execute('''
                    SELECT * FROM idx_positions 
                    WHERE position_exit_time IS NOT NULL 
                      AND DATE(position_entry_time) = CURRENT_DATE
                    ORDER BY position_entry_time DESC
                ''')
            return cursor.fetchall()

    def get_option_positions(self, position_type, status):
        with closing(self.conn.cursor()) as cursor:
            if status == "active":
                cursor.execute('''
                    SELECT * FROM opt_positions 
                    WHERE position_type = %s 
                      AND position_exit_time IS NULL 
                      AND DATE(position_entry_time) = CURRENT_DATE
                    ORDER BY position_entry_time DESC
                ''', (position_type,))
            elif status == "closed":
                cursor.execute('''
                    SELECT * FROM opt_positions 
                    WHERE position_type = %s 
                      AND position_exit_time IS NOT NULL 
                      AND DATE(position_entry_time) = CURRENT_DATE
                    ORDER BY position_entry_time DESC
                ''', (position_type,))
            return cursor.fetchall()

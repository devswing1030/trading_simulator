class Snapshot:
    def __init__(self, symbol):
        self.symbol = symbol
        self.name = ''
        self.bid_px = ''
        self.bid_qty = ''
        self.ask_px = ''
        self.ask_qty = ''
        self.last_px = ''
        self.volume = ''
        self.close_px = ''
        self.market_status = ''
        self.timestamp = ''

    def __str__(self):
        return f"symbol: {self.symbol}, name: {self.name}, " \
               f"bid_px: {self.bid_px}, bid_qty: {self.bid_qty}, " \
               f"ask_px: {self.ask_px}, ask_qty: {self.ask_qty}, " \
               f"last_px: {self.last_px}, volume: {self.volume}, close_px: {self.close_px}, market_status: {self.market_status}" \
               f"timestamp: {self.timestamp}"

    @staticmethod
    def create_table(conn):
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS nasdaq_snapshot
                     (symbol text, name text, bid_px text, bid_qty text, ask_px text, ask_qty text, last_px text, 
                     volume text, close_px text, market_status text, timestamp text, PRIMARY KEY (symbol))
                     ''')
        conn.commit()

    def update_or_insert(self, conn):
        c = conn.cursor()
        c.execute('SELECT * FROM nasdaq_snapshot WHERE symbol=?', (self.symbol,))
        if c.fetchone():
            c.execute('''UPDATE nasdaq_snapshot SET name=?, bid_px=?, bid_qty=?, ask_px=?, ask_qty=?, last_px=?, volume=?, 
                        close_px=?, market_status=?, timestamp=? WHERE symbol=?''',
                      (self.name, self.bid_px, self.bid_qty, self.ask_px, self.ask_qty, self.last_px, self.volume,
                       self.close_px, self.market_status, self.timestamp, self.symbol))
        else:
            c.execute('''INSERT INTO nasdaq_snapshot (symbol, name, bid_px, bid_qty, ask_px, ask_qty, last_px, volume, close_px, market_status, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (self.symbol, self.name, self.bid_px, self.bid_qty, self.ask_px, self.ask_qty, self.last_px, self.volume, self.close_px, self.market_status, self.timestamp))
        conn.commit()

import psycopg2
import os

DB_URL = os.environ.get("DB_URL")
print(f"📍 CURRENT DB_URL IN USE = {DB_URL}")

def connect_db():
    try:
        conn = psycopg2.connect(DB_URL)
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None

def create_table():
    conn = connect_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    chat_id BIGINT NOT NULL,
                    name TEXT NOT NULL,
                    username TEXT,
                    contact TEXT,
                    email TEXT,
                    is_member BOOLEAN DEFAULT FALSE,
                    language TEXT DEFAULT 'en',
                    affcode TEXT,
                    usage_count INTEGER DEFAULT 0,
                    last_used_date DATE DEFAULT CURRENT_DATE,
                    is_premium BOOLEAN DEFAULT FALSE,
                    mt5_broker TEXT,
                    mt5_login TEXT,
                    mt5_password TEXT,
                    risk_type TEXT,
                    risk_value TEXT,
                    metaapi_account_id TEXT,
                    is_copy_subscribed BOOLEAN DEFAULT FALSE,
                    is_mt5_valid BOOLEAN DEFAULT FALSE
                );
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Table created or updated successfully.")
        except Exception as e:
            print("❌ Error creating/updating table:", e)

if __name__ == "__main__":
    create_table()

import psycopg2
import logging

def create_accounts(conn):
    with conn.cursor() as cur:
        cur.execute(
            "CREATE TABLE IF NOT EXISTS washerWorld.Room (RoomID INT PRIMARY KEY NOT NULL, RoomName STRING);"
        )
        #cur.execute("INSERT INTO washerWorld.Room (RoomID, RoomName) VALUES (2, 'Elingson')")
        cur.execute("SELECT * FROM washerworld.Room")
        from_balance = cur.fetchall()
        print(from_balance)
        logging.debug("create_accounts(): status message: %s", cur.statusmessage)
    conn.commit()


if __name__ == '__main__':
    password_thing = input("Enter password:")
    conn = psycopg2.connect(
        database='defaultdb',
        user='cameron',
        password=password_thing,
        sslmode='verify-full',
        port=26257,
        host='free-tier11.gcp-us-east1.cockroachlabs.cloud',
        options='--cluster=stung-whale-219'
    )
    create_accounts(conn)


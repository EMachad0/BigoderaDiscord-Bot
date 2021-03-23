from notebooks.DB import conn


def insert(*args):
    cur = conn.cursor()
    cur.execute(f"INSERT INTO users (discord_user, handle) VALUES {args} ON CONFLICT (discord_user) DO UPDATE SET handle='{args[1]}'")
    conn.commit()


def select():
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users")
    return cur.fetchall()


def clear():
    cur = conn.cursor()
    cur.execute(f"DELETE FROM users")
    conn.commit()


if __name__ == "__main__":
    clear()

from notebooks.DB import conn


def insert(*args):
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO users (discord_user, handle) VALUES {args} ON CONFLICT (discord_user) DO UPDATE SET handle='{args[1]}'")
    conn.commit()


def select_all():
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users")
    return cur.fetchall()


def select(discord_user):
    cur = conn.cursor()
    cur.execute(f"SELECT handle FROM users WHERE discord_user='{discord_user}'")
    return cur.fetchall()[0][0]


def clear():
    cur = conn.cursor()
    cur.execute(f"DELETE FROM users")
    conn.commit()


if __name__ == "__main__":
    select("jnk#9477")

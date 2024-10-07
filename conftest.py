import pytest
import mysql.connector

@pytest.fixture
def connect():
     con = mysql.connector.connect(user="root", host="127.0.0.1", password="")
     return con

@pytest.fixture
def set_up_db(connect):
    curs = connect.cursor()
    
    try:
        curs.execute("CREATE DATABASE IF NOT EXISTS TestSupportData")
        curs.execute("USE TestSupportData")

        create_tbl = """CREATE TABLE IF NOT EXISTS API_DATA(
        userId INT,
        id INT,
        title Varchar(100),
        body Varchar(200)
        )"""

        curs.execute(create_tbl)

        api_data = [
             (
                 1,
                 1,
                "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
                "quia et suscipit\nsuscipi"
            ),
            (
                 1,
                 2,
                "qui est esse",
                "est rerum tempore vitae\nsequi"
            ),
            (
                1,
                3,
                "ea molestias quasi exercitationem repellat qui ipsa sit aut",
                "et iusto sed quo iure\nvoluptatem"
            )
        ]

        inser_query = 'INSERT INTO API_DATA (userId, id, title, body) VALUES (%s, %s, %s, %s)'
        curs.executemany(inser_query, api_data)
        connect.commit()

    except mysql.connector.Error as err:
        print("Error ", err.msg)
    
    finally:
        curs.close()
        connect.close()
    
@pytest.fixture
def select_data(connect):
        try:
            with connect.cursor() as curs:
                curs.execute("USE TestSupportData")
                select_query = "SELECT * from API_DATA"
                curs.execute(select_query)
                data = curs.fetchall()
                return data
            
        except mysql.connector.Error as e:
            raise RuntimeError(f"Database error: {e}")
        
        except Exception as e:
            raise RuntimeError(f"An error occurred: {e}")
    

@pytest.fixture
def tear_db_down(connect):
    curs = connect.cursor()
    drop_tbl = "DROP TABLE API_DATA"

    try:
        curs.execute("USE TestSupportData")

        curs.execute(drop_tbl)
        
        drop_db = "DROP DATABASE TestSupportData"
        curs.execute(drop_db)
        connect.commit()

    except mysql.connector.Error as err:
        print("Deleting database failed with", err.msg)

    finally:
        curs.close()
        connect.close()


    
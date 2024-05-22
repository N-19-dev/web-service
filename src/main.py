from sqlalchemy import TextClause, create_engine, text
import random
from faker import Faker
from datetime import datetime
from flask import Flask, jsonify


app = Flask(__name__)

db_string = "postgresql://root:root@localhost:5432/postgres"

engine = create_engine(db_string)

create_user_table_sql = text("""
CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    age INTEGER,
    email VARCHAR(255) UNIQUE NOT NULL,
    job VARCHAR(255)    
)
""")

create_application_table_sql = text("""
CREATE TABLE IF NOT EXISTS Application (
    id SERIAL PRIMARY KEY,
    appname VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    lastconnection TIMESTAMP,
    user_id INTEGER REFERENCES Users(id)
)
""")


def run_sql(query: TextClause):
    with engine.connect() as connection:
        trans = connection.begin() 
        connection.execute(query) 
        trans.commit() 

def run_sql_with_results(query: TextClause):
    with engine.connect() as connection:
        trans = connection.begin()   
        result = connection.execute(query) 
        trans.commit()
        return result


fake= Faker()


def populate_table():
    for i in range (100):
        firstname= fake.first_name()
        lastname=fake.last_name()
        age= random.randrange(18,90)
        email=fake.email()
        job=fake.job().replace("'", "")
        insert_statement = text(f"""
        INSERT INTO Users (firstname, lastname, age, email, job) 
        VALUES ('{firstname}', '{lastname}', '{age}', '{email}', '{job}')
        RETURNING id
        """)
        # Récupérer l'id
        user_id = run_sql_with_results(insert_statement).scalar()
        print(user_id)

        apps = ['Facebook', 'Twitter', 'Instagram', 'LinkedIn', 'Snapchat']
        num_apps = random.randint(1,5)

        for i in range(num_apps):
            username = fake.user_name()
            lastconnection = datetime.now()
            app_name = random.choice(apps)
            sql_insert_app =text( f"""
            INSERT INTO Application (appname, username, lastconnection, user_id)
            VALUES ('{app_name}', '{username}', '{lastconnection}', '{user_id}')
                """)
            run_sql(sql_insert_app)



@app.route("/users", methods=["GET"])
def get_users():
    users = run_sql_with_results(text("SELECT * FROM users"))
    data = []
    for user in users:
        data.append({
            'id': user[0],
            'firstname': user[1],
            'lastname': user[2],
            'age': user[3],
            'email': user[4],  
            'job': user[5],   
        })
    return jsonify(data)

if __name__ =='__main__':
    run_sql(create_user_table_sql)
    run_sql(create_application_table_sql)
    populate_table()
    app.run(host="0.0.0.0", port=8081)
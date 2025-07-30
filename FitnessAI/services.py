import pymysql
from decouple import config

class Dataoperations:

    def __init__(self):
        self.host = config('DB_HOST')
        self.port = int(config('DB_PORT'))
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.database = config('DB_NAME')

    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            ssl={"ssl": True}
        )

    def add_profile(self, name, age, gender, height_cm, weight, bmi, food, step):
        flag = False
        con = self.get_connection()
        curs = con.cursor()
        curs.execute("""
            INSERT INTO fitness_profile 
            (person_name, age, gender, height_cm, weight_kg, bmi, food_type, steps_per_day, recorded_on)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURDATE())
        """, (name, age, gender, height_cm, weight, bmi, food, step))
        con.commit()
        con.close()
        flag = True
        return flag

    def list_of_users(self):
        con = self.get_connection()
        curs = con.cursor()
        curs.execute("SELECT profile_id, person_name FROM fitness_profile")
        data = curs.fetchall()
        con.close()
        return data

    def get_profile_by_id(self, profile_id):
        con = self.get_connection()
        curs = con.cursor()
        curs.execute("""
            SELECT person_name, age, gender, height_cm, weight_kg, bmi, food_type, steps_per_day 
            FROM fitness_profile 
            WHERE profile_id = %s
        """, (profile_id,))
        row = curs.fetchone()
        con.close()
        return row

    def update_profile(self, name, age, gender, height_cm, weight_kg, bmi, food_type, steps_per_day):
        con = self.get_connection()
        curs = con.cursor()
        sql = """
            UPDATE fitness_profile 
            SET age=%s, gender=%s, height_cm=%s, weight_kg=%s, bmi=%s, food_type=%s, steps_per_day=%s, recorded_on=CURDATE()
            WHERE person_name=%s
        """
        curs.execute(sql, (age, gender, height_cm, weight_kg, bmi, food_type, steps_per_day, name))
        con.commit()
        updated = curs.rowcount > 0
        con.close()
        return updated

    def delete_profile(self, profile_id):
        con = self.get_connection()
        curs = con.cursor()
        curs.execute("DELETE FROM fitness_profile WHERE profile_id = %s", (profile_id,))
        flag = curs.rowcount > 0
        con.commit()
        con.close()
        return flag

    def report(self):
        con = self.get_connection()
        curs = con.cursor()
        curs.execute("""
            SELECT profile_id, person_name, age, gender, height_cm, weight_kg, bmi, recorded_on 
            FROM fitness_profile
        """)
        row = curs.fetchall()
        con.close()
        return row

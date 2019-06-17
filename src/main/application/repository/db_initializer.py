from random import randint

from mysql import connector

from src.main.application.config.db_config import mysql
from src.main.application.utils.random_date import getRandomDate
from src.main.application.utils.random_hour import getRandomTime, getDuration

mydb=mysql.connect()

#     host="localhost",
#
#     port="3306",
#
#     user="root",
#
#     passwd="",
#
#     db="recfacedb"
#
# )

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE recfacedb")
mycursor.execute("CREATE DATABASE recfacedb")

mycursor.execute("USE recfacedb")

#user table - id,name,passwd
mycursor.execute("CREATE TABLE `user` ("
  "`user_id` bigint(20) NOT NULL AUTO_INCREMENT,"
  "`user_name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,"
  "`user_password` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,"
  "PRIMARY KEY (`user_id`)"
  ") ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
)

#create admin user
mycursor.execute("INSERT INTO user(user_id,user_name,user_password) VALUES (0,'admin','admin')")

#person table - id,name,email,age,sex,picture data
mycursor.execute("CREATE TABLE `person` ("
  "`person_id` bigint(20) NOT NULL AUTO_INCREMENT,"
  "`person_name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,"
  "`person_email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,"
  "`person_age` bigint(20) DEFAULT NULL,"
  "`person_sex` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,"
  "`person_picture_data` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,"
  "PRIMARY KEY (`person_id`)"
  ") ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
)

#attendance table - id,person,data,in,out,duration
mycursor.execute("CREATE TABLE `attendance` ("
  "`attendance_id` bigint(20) NOT NULL AUTO_INCREMENT,"
  "`attendance_date` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,"
  "`attendance_in` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,"
  "`attendance_out` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,"
  "`attendance_duration` bigint(20) DEFAULT NULL,"
  "PRIMARY KEY (`attendance_id`)"
  ") ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
)

#log table - id,person,attendance
mycursor.execute("CREATE TABLE `log` ("
  "`log_id` bigint(20) NOT NULL AUTO_INCREMENT,"
  "`log_person` bigint(20) NOT NULL ,"
  "`log_attendance` bigint(20) NOT NULL ,"
  "PRIMARY KEY (`log_id`),"
  "FOREIGN KEY(`log_person`) REFERENCES person(`person_id`),"
  "FOREIGN KEY(`log_attendance`) REFERENCES attendance(`attendance_id`)"      
  ") ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
)

#user_person table - id,user_id,person_id
mycursor.execute("CREATE TABLE `user_person` ("
  "`id` bigint(20) NOT NULL AUTO_INCREMENT,"
  "`user_id` bigint(20) NOT NULL ,"
  "`person_id` bigint(20) NOT NULL ,"
  "PRIMARY KEY (`id`),"
  "FOREIGN KEY(`user_id`) REFERENCES user(`user_id`),"
  "FOREIGN KEY(`person_id`) REFERENCES person(`person_id`) "
  ") ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;"
)

persons=["ana","alex","andrei","maria","elena","bogdan","radu","andreia","marius"]
ages=[20,23,27,30,21,24,33,22,25]
sexes=["female","male","male","female","female","male","male","male","male"]

insert_stmt_person = (
  "INSERT INTO person (person_id, person_name, person_email, person_age, person_sex) "
  "VALUES (%s, %s, %s, %s, %s)"
)

insert_stmt_attendance = (
  "INSERT INTO attendance (attendance_id, attendance_date, attendance_in, attendance_out, attendance_duration) "
  "VALUES (%s, %s, %s, %s, %s)"
)

insert_stmt_log = (
  "INSERT INTO log (log_person, log_attendance) "
  "VALUES (%s, %s)"
)

insert_stmt_user=(
    "INSERT INTO user(user_id,user_name,user_password)"
    "VALUES (%s, %s, %s)"
)

insert_stmt_user_person = (
  "INSERT INTO user_person (user_id, person_id) "
  "VALUES (%s, %s)"
)

for i in range (1, 1000):
    data_person = (i, persons[i % len(persons)], persons[i % len(persons)]+"@email.ex", ages[i%len(ages)], sexes[i%len(sexes)])
    mycursor.execute(insert_stmt_person,data_person)

    start=getRandomTime()
    end=getRandomTime()
    if(start>end):
        start,end=end,start

    data_attendance = (i, getRandomDate(), start, end, getDuration(start,end))
    mycursor.execute(insert_stmt_attendance, data_attendance)

for i in range (1, 1000):
    data_log=(randint(1,999),randint(1,999))
    mycursor.execute(insert_stmt_log, data_log)

for i in range(3,len(persons)):
    data_user=(i,persons[i],persons[i])
    mycursor.execute(insert_stmt_user,data_user)
    data_user_person=(i,i)
    mycursor.execute(insert_stmt_user_person,data_user_person)


mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db)

mydb.commit()

mycursor.close()
mydb.close()
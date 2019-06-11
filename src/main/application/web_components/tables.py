from flask_table import Table, Col, LinkCol

class Results(Table):
    classes = ['table','table-hover']
    person_id = Col('Id_Person',show=False)
    person_name = Col('Name')
    person_email = Col('Email')
    person_age = Col('Age')
    person_sex = Col('Sex')
    log_id = Col('Id_Log',show=False)
    log_person = Col('Person', show=False)
    log_attendance = Col('Attendance', show=False)
    attendance_id = Col('Id_Attendance',show=False)
    attendance_date = Col('Date')
    attendance_in = Col('In')
    attendance_out = Col('Out',show=False)
    attendance_duration = Col('Duration',show=False)

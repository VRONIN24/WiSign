from fastapi import FastAPI, Request
import uvicorn
import requests
import mysql.connector
from datetime import datetime
import server_config

class WiSign_Server:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.login_database()
        self.app = FastAPI()
        self.app.add_api_route("/data", self.get_data, methods=["POST"])

    async def get_data(self, request: Request):
        data = await request.json()
        print("received: " + str(data))
        if(data[0] == "Register"):
            response = self.register(data)
        elif(data[0] == "Login"):
            response = self.login(data)
        elif(data[0] == "classroom_details_request"):
            response = self.get_classroom_data(data[1])
        elif(data[0] == "Attendance"):
            response = self.attendance_submit(data)
        elif(data[0] == "student_info"):
            response = self.get_student_info(data)
        elif(data[0] == "teacher_filter_data" or data[0] == "apply_teacher_filter" or data[0] == "teacher_update_data"):
            print("-----------------matched: " + str(data[0]))
            response = self.handle_teacher_ui(data)
        elif(data[0] == "admin_admin_info" or data[0] == "admin_delete" or data[0] == "admin_edit" or data[0] == "admin_update" or data[0] == "admin_dept_filter" or data[0] == "admin_teacher_info" or data[0] == "admin_student_filter" or data[0] == "admin_student_info"):
            response = self.handle_admin_ui(data)
        #print("\n---------------" + str(data[0]) + "----------\n")
        #print("\n---------------" + str(data[1]) + "----------\n")
        #print("\n---------------" + str(data[2]) + "----------\n")
        return [response]                                                                   #**every data is sent back as a list.

    def login_database(self):
        self.connection = mysql.connector.connect(host=server_config.DATABASE_IP, user=server_config.DATABASE_USERNAME, password=server_config.DATABASE_PASSWORD, database="classroom_server", port=server_config.DATABASE_PORT, autocommit=True)
        if(self.connection.is_connected()):
            print("[+]logged in")
        self.cursor = self.connection.cursor()

    def login(self, data):                                                                  #**every teacher's name must start with t, student's name with s, and admin's name with a
        if data[1][0] == "t":  
            query = "SELECT * FROM teacher WHERE id=%s AND password=%s;"
            self.cursor.execute(query, (data[1], data[2]))
            row = list(self.cursor.fetchone())
            if not row:
                return False
            else:
                row.insert(0, "teacher")
                row.pop()
                return row
        elif data[1][0] == "a":
            query = "SELECT * FROM admin WHERE id=%s AND password=%s;"
            self.cursor.execute(query, (data[1], data[2]))
            row = list(self.cursor.fetchone())
            if not row:
                return False
            else:
                row.insert(0, "admin")
                row.pop()
                return row  #**the return row contains a list like [<user_type>, <id>, <name>, <email>, <mac>, <intake>, <section>, <department>]
        elif data[1][0] == "s":
            query = "SELECT * FROM student WHERE id=%s AND password=%s;"
            self.cursor.execute(query, (data[1], data[2]))
            row = list(self.cursor.fetchone())
            if not row:
                return False;
            else:
                row.insert(0, "student")
                row.pop()
                return row  #**the return row contains a list like [<user_type>, <id>, <name>, <email>, <mac>, <intake>, <section>, <department>]

    #***dynamically registering to the database based on the registration profile type.
    def register(self, data):
        print(data)
        print("-------------------------------")
        if data[1] == "Student":
            query = "INSERT INTO student (id, name, mac, intake, section, department, password) VALUES (%s, %s, %s, %s, %s, %s, %s);"
            self.cursor.execute(query, (data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
            self.connection.commit()
        elif data[1] == "Teacher":
            query = "INSERT INTO teacher (id, name, mac, department, email, password) VALUES (%s, %s, %s, %s, %s, %s);"
            self.cursor.execute(query, (data[2], data[3], data[4], data[5], data[6], data[7]))
            self.connection.commit()
        elif data[1] == "Assign Teacher":
            query = "INSERT INTO assigned_teacher (id, course_id, section, intake) VALUES (%s, %s, %s, %s);"
            self.cursor.execute(query, (data[2], data[3], data[4], data[5]))
            self.connection.commit()
            print("i ran----------------------------")
        elif data[1] == "Course":
            query = "INSERT INTO course (course_id, course_name) VALUES (%s, %s)"
            self.cursor.execute(query, (data[2], data[3]))
            self.connection.commit()
        elif data[1] == "Classroom":
            query = "INSERT INTO classroom (room_id, period_no, department, section, intake, saturday, sunday, monday, tuesday, wednesday, thursday, friday) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            self.cursor.execute(query, (data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13]),)
            self.connection.commit()
        elif data[1] == "Admin":
            query = "INSERT INTO admin (id, password) VALUES (%s, %s);"
            self.cursor.execute(query, (data[2], data[3]))
            self.connection.commit()
        elif data[1] == "Period":
            query = "DELETE FROM period;"
            self.cursor.execute(query)
            self.connection.commit()
            for period in data:
                if not (period == data[0] or period == data[1]):
                    query = "INSERT INTO period (number, start_time, end_time) VALUES (%s, %s, %s)"
                    self.cursor.execute(query, (period[0], period[1], period[2]))
                    self.connection.commit()
        return "Registration successful!" 

    def get_student_info(self, data):
        student_id = data[2]
        print(student_id)
        query = "SELECT state, present_ping, total_ping, percentage, date, course_id FROM attendance WHERE id=%s ORDER BY course_id;"
        self.cursor.execute(query, (student_id,))
        row = list(self.cursor.fetchall())
        query1 = "SELECT course_id, SUM(CASE WHEN state = 'present' THEN 1 ELSE 0 END) AS present_count, COUNT(state) AS total_count, (SUM(CASE WHEN state = 'present' THEN 1 ELSE 0 END) / COUNT(state) * 100) AS present_percentage FROM attendance WHERE id = %s GROUP BY course_id ORDER BY course_id;"
        self.cursor.execute(query1, (student_id,))
        row1 = list(self.cursor.fetchall())
        if not row:
            return [False]
        if not row1:
            row1 = ["No Course record found"]
        row.append(row1)
        return row

    def attendance_submit(self, details):
        total_ping = details[1][0]
        period_no = details[1][1]
        print("PERIOD: " + period_no + "\nPING: " + str(total_ping))
        for student in details[2:]:
            st_id = student[0]
            name = student[1]
            mac = student[2]
            intake = student[3]
            section = student[4]
            course_id = student[5]
            department = student[6]
            present_ping = student[7]
            try:
                percentage = int((int(present_ping)/int(total_ping)) * 100)
            except ZeroDivisionError:
                percentage = 0
            if(percentage > 70):
                state = "present"
            else:
                state = "absent"
            current_date = str(datetime.now().date())
            query = "INSERT INTO attendance (id, name, mac, intake, section, department, present_ping, total_ping, percentage, state, date, period_no, course_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cursor.execute(query, (st_id, name, mac, intake, section, department, present_ping, total_ping, str(percentage), state, current_date, period_no, course_id))
            self.connection.commit()
        return "submitted"

    def get_classroom_data(self, room_id):
        period_no = self.find_period_no()
        print(period_no)
        if not period_no:
            return [False, "no periods at the current hour"]
        else:
            current_day = datetime.now().strftime("%A").lower()
            query = "SELECT intake, section, " + str(current_day) + " FROM classroom WHERE period_no=%s AND room_id=%s"
            self.cursor.execute(query, (period_no, room_id,))
            response = self.cursor.fetchall()
            print(response)
            intake = response[0][0]
            section = response[0][1]
            course_id = response[0][2]
            data_list = [[intake, section, course_id]]
            query1 = "SELECT id, name, email, mac FROM student WHERE intake=%s AND section=%s"
            self.cursor.execute(query1, (intake, section,))
            response1 = self.cursor.fetchall()
            for row in response1:
                data_list.append(list(row))
            query2 = "SELECT teacher_id FROM assigned_teacher WHERE intake=%s AND section=%s AND course_id=%s"
            self.cursor.execute(query2, (intake, section, course_id))
            response2 = self.cursor.fetchone()
            teacher_id = response2[0]
            query3 = "SELECT id, name, mac, department, email FROM teacher WHERE id=%s"
            self.cursor.execute(query3, (teacher_id,))
            response3 = self.cursor.fetchone()
            data_list.insert(0, list(response3))
            print("printing rows of data_list: ")
            data_list[0].append(str(period_no))
            for row in data_list:
                print(row)
            return data_list

    def find_period_no(self):
        current_time = datetime.now().time()
        query = "SELECT * FROM period"
        self.cursor.execute(query)
        response = self.cursor.fetchall()
        print(response)
        for row in response:
            start_time = row[1]
            end_time = row[2]
            start = datetime.strptime(start_time, "%H:%M").time()
            end = datetime.strptime(end_time, "%H:%M").time()
            print(current_time)
            print(start_time)
            if(start <= current_time):
                in_range = start <= current_time <= end
                print("start: " + str(start) + " <= current: " + str(current_time) + " <= end: " + str(end))
            else:
                in_range = current_time >= start and current_time <= end

            if in_range:
                return row[0]
        return False

    def handle_teacher_ui(self, data):
        if data[0] == "teacher_filter_data":
            query = "SELECT DISTINCT intake, section, course_id FROM assigned_teacher WHERE teacher_id=%s;"
            self.cursor.execute(query, (data[1],))
            row = list(self.cursor.fetchall())
            query = """SELECT DISTINCT T2.date 
                FROM assigned_teacher AS T1
                JOIN attendance AS T2 ON 
                    T1.intake = T2.intake AND 
                    T1.section = T2.section AND 
                    T1.course_id = T2.course_id
                WHERE T1.teacher_id = %s
                ORDER BY T2.date;"""
            self.cursor.execute(query, (data[1],))
            row1 = list(self.cursor.fetchall())
            date_list = []
            for date in row1:
                date_list.append(date[0])
            print("**printing row: ")
            print(row)
            print("**printing row1: ")
            print(row1)
            return [row, date_list]
        elif data[0] == "apply_teacher_filter":
            query = "SELECT DISTINCT state, id, name, present_ping, total_ping, percentage FROM attendance WHERE intake=%s AND section=%s AND course_id=%s AND date=%s ORDER BY id;"
            self.cursor.execute(query, (data[1], data[2], data[3], data[4]))
            response = list(self.cursor.fetchall())
            #print("each student response: " + str(response))
            result = []
            for student in response:
                query1 = "SELECT (SUM(CASE WHEN state = 'present' THEN 1 ELSE 0 END) / COUNT(state) * 100) AS present_percentage FROM attendance WHERE id = %s AND course_id = %s;"
                self.cursor.execute(query1, (student[1], data[3],))
                course_percentage = list(self.cursor.fetchone())
                student_list = list(student)
                student_list.append(str(int(course_percentage[0])))
                result.append(student_list)
            return result
        elif data[0] == "teacher_update_data":
            intake = data[1][0]
            section = data[1][1]
            course_id = data[1][2]
            date = data[1][3]
            for user_data in data[2]:
                query = "UPDATE attendance SET state=%s WHERE intake=%s AND section=%s AND course_id=%s AND date=%s AND id=%s;"
                self.cursor.execute(query, (user_data[0], intake, section, course_id, date, user_data[1]))
                self.connection.commit()
            return "updated"
            #date_list = 

    def handle_admin_ui(self, data):
        if data[0] == "admin_admin_info":
            response_data_list = []
            query = "SELECT id FROM admin;"
            self.cursor.execute(query)
            response = self.cursor.fetchall()
            for item in response:
                response_data_list.append(item[0])
            print(response_data_list)
            return response_data_list
        elif data[0] == "admin_delete":
            if data[1][0] == "a":
                table = "admin"
            if data[1][0] == "t":
                table = "teacher"
            if data[1][0] == "s":
                table = "student"
            query = f"DELETE FROM {table} WHERE id=%s";
            self.cursor.execute(query, (data[1],))
            self.connection.commit()
            return "deleted"
        elif data[0] == "admin_edit":
            print(data)
            table = ""
            if data[1][0] == "a":
                table = "admin"
            elif data[1][0] == "s":
                table = "student"
            elif data[1][0] == "t":
                table = "teacher"
            query = f"SELECT * FROM {table} WHERE id=%s"
            #query1 = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='classroom_server' AND TABLE_NAME=%s"
            self.cursor.execute(query, (data[1],))
            result = self.cursor.fetchall()
            result = list(result[0])
            #self.cursor.execute(query1, (table,))
            #result1 = self.cursor.fetchall()
            ##column_names = [col[0] for col in result1]
            result_list = [result]#, column_names]
            print(("result_list: " + str(result_list)))
            return result_list
        elif data[0] == "admin_update":
            print(data)
            query = ""
            if data[1][0] == "a":
                table = "admin"
                query = "UPDATE admin SET id=%s, password=%s WHERE id=%s"
            elif data[1][0] == "s":
                table = "student"
                query = "UPDATE student SET id=%s, name=%s, email=%s, mac=%s, intake=%s, section=%s, department=%s, password=%s WHERE id=%s"
            elif data[1][0] == "t":
                table = "teacher"
                query = "UPDATE teacher SET id=%s, name=%s, mac=%s, department=%s, email=%s, password=%s WHERE id=%s"
            #query = f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA='classroom_server' AND TABLE_NAME=%s;"
            #self.cursor.execute(query, (table,))
            #result = self.cursor.fetchall()
            #columns = [col[0] for col in result]
            params = data[2] + [data[1]]
            #column_list = self.cursor.execute("")
            #set_clause = ", ".join([f"{col}=%s" for col in columns])
            #query = f"UPDATE {table} SET {set_clause} WHERE id=%s"
            self.cursor.execute(query, params)
            print("query: " + str(query))
            return "got it"
        elif data[0] == "admin_dept_filter":
            query = "SELECT DISTINCT department FROM teacher;"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            departments = [col[0] for col in result]
            print(departments)
            return departments
        elif data[0] == "admin_teacher_info":
            query = "SELECT * FROM teacher WHERE department=%s;"
            self.cursor.execute(query, (data[1],))
            response = self.cursor.fetchall()
            return response
        elif data[0] == "admin_student_filter":
            query = "SELECT DISTINCT department, intake, section FROM student ORDER BY intake, section;"
            self.cursor.execute(query)
            response = self.cursor.fetchall()
            print(response)
            return response
        elif data[0] == "admin_student_info":
            print(data)
            query = "SELECT * FROM student WHERE department=%s AND intake=%s AND section=%s"
            self.cursor.execute(query, (data[1], data[2], data[3],))
            response = self.cursor.fetchall()
            return response

server = WiSign_Server()
if __name__ == "__main__":
    #server = WiSign_Server()

    uvicorn.run(server.app, host="0.0.0.0", port=5000, reload=False)


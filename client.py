import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QCheckBox, QVBoxLayout, QComboBox, QScrollArea, QHBoxLayout, QSpacerItem, QSizePolicy, QFrame
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QPalette, QBrush
import requests
import platform
import os
import json
from ap_scanner import AP_Scanner
from client_config import SERVER_IP, SERVER_PORT

class GUI:
	def __init__(self):
		#***preparing the main window for the GUI
		self.window = QWidget()
		self.window.setWindowTitle("WiSign")
		self.main_layout = QVBoxLayout()
		self.ap_status = 0
		self.container_widget = QWidget()
		self.container_widget.setLayout(self.main_layout)
		'''self.container_widget.setStyleSheet("""
			QWidget {
				background-image: url("background.png");
				background-repeat: no-repeat;
				background-position: center;
			}
		""")'''

		scroll_area = QScrollArea()
		scroll_area.setWidgetResizable(True)
		scroll_area.setWidget(self.container_widget)
		#self.window.setLayout(self.main_layout)
		self.window_layout = QVBoxLayout()
		self.window.setLayout(self.window_layout)
		self.window_layout.addWidget(scroll_area)

		#self.login_page()
		#***declaring the necessary attributes
		self.form_container_layout = ""				#**required to access the registration form layout from update_form function
		self.form_dropdown = "" 					#**contains the option for form registration drop down menu, required to access the list from update_form function
		self.input_number_of_periods = ""           #**needed for dynamic period registration based on number of periods
		self.user_input = ""						#**username input for login, required to access in authenticate function
		self.password_input = ""                    #**password input for login, required to access in authenticate function
		self.registration_data_object = []			#**a list to hold all the object according to the chosen registration form
		self.history = [self.selection_page]							#**keeps history for the back button
		#self.maximized = True						#**
		#self.client_id = ""						#**
		self.login_response = "" 							#set to 'student' if student logged in, 'teacher' for teacher, "admin" for admin
		self.classroom_info = []
		self.refresh_classroom_timer = QTimer()
		self.ap_scanner = AP_Scanner()
		self.student_details = []
		self.total_pings = 0
		self.period_no = 0

	def login_page(self):
		self.clear_layout()
		container = QWidget()
		container_layout = QVBoxLayout()
		container.setLayout(container_layout)
		container_layout.setSpacing(10)     
		container_layout.setAlignment(Qt.AlignCenter)
		container_layout.setContentsMargins(30, 30, 50, 50)

		logo_label = QLabel()
		pixmap = QPixmap("wisign_logo.png")
		pixmap = pixmap.scaled(280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		logo_label.setPixmap(pixmap)

		login_button = QPushButton("Login")
		login_button.clicked.connect(self.authenticate)
		login_button.setFixedWidth(150)
		login_button.setFixedHeight(50)

		input_style = """
		    QLineEdit {
		    	font-size: 15pt;
		    	padding: 8px;
		    	padding-left: 8px;
		    }
			"""
		self.user_id_input = QLineEdit()
		self.user_id_input.setPlaceholderText("user ID")
		self.user_id_input.setFixedWidth(270)
		self.user_id_input.setFixedHeight(60)
		self.user_id_input.setAlignment(Qt.AlignLeft)
		self.user_id_input.setStyleSheet(input_style)
		self.user_id_input.returnPressed.connect(lambda: QTimer.singleShot(0, login_button.click))

		self.password_input = QLineEdit()
		self.password_input.setPlaceholderText("password")
		self.password_input.setEchoMode(QLineEdit.Password)
		self.password_input.setFixedWidth(270)
		self.password_input.setFixedHeight(60)
		self.password_input.setAlignment(Qt.AlignLeft)
		self.password_input.setStyleSheet(input_style)
		self.password_input.returnPressed.connect(lambda: QTimer.singleShot(0, login_button.click))

		label_style = """
    		font-size: 15pt;
    		padding: 5px;
			"""
		id_label = QLabel("User ID")
		id_label.setStyleSheet(label_style)
		password_label = QLabel("Password")
		password_label.setStyleSheet(label_style)

		container_layout.addWidget(logo_label)
		container_layout.addWidget(id_label)
		container_layout.addWidget(self.user_id_input)
		container_layout.addWidget(password_label)
		container_layout.addWidget(self.password_input)
		container_layout.addWidget(login_button)

		self.main_layout.addWidget(container, alignment=Qt.AlignCenter)

	def authenticate(self):
		user_id = self.user_id_input.text()
		password = self.password_input.text()
		self.login_response = self.client_server_comm(["Login", user_id, password])		#**sends the user_id and password to the backend for verification. all teacher's user_id must start with t, admin's name with a, and students name with s
		#print(response)
		print("this is response: " + str(self.login_response))#############################
		if self.login_response[0] == False:
			self.user_id_input.clear()
			self.password_input.clear()
			self.user_id_input.setPlaceholderText("Wrong credentials")
		elif self.login_response[0][0] == "admin":
			self.enter_page(self.admin_page)
			#self.login_as = response
		elif self.login_response[0][0] == "teacher":
			self.enter_page(self.teacher_page)
			#self.login_as = response
		elif self.login_response[0][0] == "student":
			self.enter_page(self.student_page)
			#self.login_as = response
		else:
			self.user_id_input.clear()
			self.password_input.clear()
			self.user_id_input.setPlaceholderText("Wrong credentials")
			#self.password_input.setPlaceholderText("Try again")

	#***provides with the drop down menu option and calls the "update_form" function to dynamically update the form based on chosen profile to register
	def registration_page(self):
		self.clear_layout()

		form_container = QWidget()
		self.form_container_layout = QVBoxLayout()
		form_container.setLayout(self.form_container_layout)
		self.form_container_layout.setSpacing(10)
		self.form_container_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
		self.form_container_layout.setContentsMargins(30, 90, 50, 5)
		form_container.setStyleSheet("""
			QLineEdit{
				max-width: 300px;
				min-width: 300px;
				max-height:50px;
				min-height:50px;
			}
		""")

		drop_down_label = QLabel("Register")
		self.form_container_layout.addWidget(drop_down_label)

		self.form_dropdown = QComboBox()
		self.form_dropdown.addItems(["Student", "Teacher", "Assign Teacher", "Course", "Classroom", "Period", "Admin"])
		self.form_dropdown.currentIndexChanged.connect(self.update_form)
		self.form_container_layout.addWidget(self.form_dropdown)
		self.main_layout.addWidget(form_container)
		self.update_form()

	def update_form(self, notification=None, selection=None):				#**parameters notification holds if any notification needs to be displayed such as "Registration successful" to indicate success of any previous registration if there was any. parameter selection indicates the selection form to display by default or on function call.
		if not selection:													#**if no form was given to select, then the last used form is selected or the first form in the list is selected to display by default 
			selection = self.form_dropdown.currentText()

		for i in reversed(range(2, self.form_container_layout.count())):	#**clearing up widgets except the drop down menu and the registration label
			widget = self.form_container_layout.itemAt(i).widget()
			if widget is not None:
				widget.setParent(None)

		if selection == "Student":
			input_id = QLineEdit()
			input_id.setPlaceholderText("ID")
			input_name = QLineEdit()
			input_name.setPlaceholderText("Name")
			input_MAC = QLineEdit()
			input_MAC.setPlaceholderText("MAC")
			input_intake = QLineEdit()
			input_intake.setPlaceholderText("Intake")
			input_section = QLineEdit()
			input_section.setPlaceholderText("Section")
			input_department = QLineEdit()
			input_department.setPlaceholderText("Department")
			input_password = QLineEdit()
			input_password.setPlaceholderText("Password")
			self.form_container_layout.addWidget(input_id)
			self.form_container_layout.addWidget(input_name)
			self.form_container_layout.addWidget(input_MAC)
			self.form_container_layout.addWidget(input_intake)
			self.form_container_layout.addWidget(input_section)
			self.form_container_layout.addWidget(input_department)
			self.form_container_layout.addWidget(input_password)
			self.registration_data_object.clear()
			self.registration_data_object.extend(["Register", "Student", input_id, input_name, input_MAC, input_intake, input_section, input_department, input_password])
		elif selection == "Teacher":
			input_id = QLineEdit()
			input_id.setPlaceholderText("ID")
			input_name = QLineEdit()
			input_name.setPlaceholderText("Name")
			input_course = QLineEdit()
			input_course.setPlaceholderText("MAC")
			input_email = QLineEdit()
			input_email.setPlaceholderText("Department")
			input_MAC = QLineEdit()
			input_MAC.setPlaceholderText("Email")
			input_password = QLineEdit()
			input_password.setPlaceholderText("Password")
			self.form_container_layout.addWidget(input_id)
			self.form_container_layout.addWidget(input_name)
			self.form_container_layout.addWidget(input_course)
			self.form_container_layout.addWidget(input_email)
			self.form_container_layout.addWidget(input_MAC)
			self.form_container_layout.addWidget(input_password)
			self.registration_data_object.clear()
			self.registration_data_object.extend(["Register", "Teacher", input_id, input_name, input_course, input_email, input_MAC, input_password])
		elif selection == "Assign Teacher":
			input_teacher_id = QLineEdit()
			input_teacher_id.setPlaceholderText("Teacher ID")
			input_course_id = QLineEdit()
			input_course_id.setPlaceholderText("Course ID")
			input_section = QLineEdit()
			input_section.setPlaceholderText("Section")
			input_intake = QLineEdit()
			input_intake.setPlaceholderText("Intake")
			self.form_container_layout.addWidget(input_teacher_id)
			self.form_container_layout.addWidget(input_course_id)
			self.form_container_layout.addWidget(input_section)
			self.form_container_layout.addWidget(input_intake)
			self.registration_data_object.clear()
			self.registration_data_object.extend(["Register", "Assign Teacher", input_teacher_id, input_course_id, input_section, input_intake])
		elif selection == "Classroom":
			input_room_id = QLineEdit()
			input_room_id.setPlaceholderText("Room ID")
			input_period = QLineEdit()
			input_period.setPlaceholderText("Period no.")
			input_department = QLineEdit()
			input_department.setPlaceholderText("Department")
			input_section = QLineEdit()
			input_section.setPlaceholderText("Section")
			input_intake = QLineEdit()
			input_intake.setPlaceholderText("Intake")
			input_sat = QLineEdit()
			input_sat.setPlaceholderText("Saturday")
			input_sun = QLineEdit()
			input_sun.setPlaceholderText("Sunday")
			input_mon = QLineEdit()
			input_mon.setPlaceholderText("Monday")
			input_tue = QLineEdit()
			input_tue.setPlaceholderText("Tuesday")
			input_wed = QLineEdit()
			input_wed.setPlaceholderText("Wednesday")
			input_thurs = QLineEdit()
			input_thurs.setPlaceholderText("Thursday")
			input_fri = QLineEdit()
			input_fri.setPlaceholderText("Friday")
			self.form_container_layout.addWidget(input_room_id)
			self.form_container_layout.addWidget(input_period)
			self.form_container_layout.addWidget(input_department)
			self.form_container_layout.addWidget(input_section)
			self.form_container_layout.addWidget(input_intake)
			self.form_container_layout.addWidget(input_sat)
			self.form_container_layout.addWidget(input_sun)
			self.form_container_layout.addWidget(input_mon)
			self.form_container_layout.addWidget(input_tue)
			self.form_container_layout.addWidget(input_wed)
			self.form_container_layout.addWidget(input_thurs)
			self.form_container_layout.addWidget(input_fri)
			self.registration_data_object.clear()
			self.registration_data_object.extend(["Register", "Classroom", input_room_id, input_period, input_department, input_section, input_intake, input_sat,
				input_sun, input_mon, input_tue, input_wed, input_thurs, input_fri])
		elif selection == "Course":
			input_course_id = QLineEdit()
			input_course_id.setPlaceholderText("Course ID")
			input_course_name = QLineEdit()
			input_course_name.setPlaceholderText("Course Name")
			self.form_container_layout.addWidget(input_course_id)
			self.form_container_layout.addWidget(input_course_name)
			self.registration_data_object.clear()
			self.registration_data_object.extend(["Register", "Course", input_course_id, input_course_name])
		elif selection == "Admin":
			input_admin_id = QLineEdit()
			input_admin_id.setPlaceholderText("Admin ID")
			input_admin_password = QLineEdit()
			input_admin_password.setPlaceholderText("Admin password")
			self.form_container_layout.addWidget(input_admin_id)
			self.form_container_layout.addWidget(input_admin_password)
			self.registration_data_object.clear()
			self.registration_data_object.extend(["Register", "Admin", input_admin_id, input_admin_password])
		elif selection == "Period":											#**if the chosen option is period then provide them with how many periods and then based on that dynamically register that many periods by calling "create_periods" on button press.
			self.input_number_of_periods = QLineEdit()
			self.input_number_of_periods.setPlaceholderText("Enter the number of total periods a day")
			self.input_number_of_periods.returnPressed.connect(self.create_periods)
			self.form_container_layout.addWidget(self.input_number_of_periods)
		if selection and selection != "Period":   							#**creates the button for every form except period registration form since for period registration, the submit button is created by "create_period" function after creation of the form by it.
			register_button = QPushButton("Register")
			register_button.clicked.connect(self.submit_registration)
			register_button.setFixedWidth(250)
			register_button.setFixedHeight(50)
			self.form_container_layout.addWidget(register_button)
		if notification and isinstance(notification, list):					#**checks if there is any notification, if there is so, then shows it. for example "Registration successful"
			notification_label = QLabel(str(notification[0]))
			notification_label.setStyleSheet("color: #00ffcc; font-weight: bold;")
			self.form_container_layout.addWidget(notification_label)

	#***submits the registration data to the backend
	def submit_registration(self):
		data_list = []
		for data in self.registration_data_object:
			if isinstance(data, str):
				data_list.append(data)
			elif isinstance(data, list):
				if(self.registration_data_object[1] == "Period"):
					period_data = []
					for period_detail in data:
						if isinstance(period_detail, str):
							period_data.append(period_detail)
						else:
							period_data.append(period_detail.text())
				data_list.append(period_data)
			else:
				data_list.append(data.text())
		response = self.client_server_comm(data_list)
		self.update_form(response, self.registration_data_object[1])

	#***creates form for periods based on the number of periods chosen to register
	def create_periods(self):
		for i in reversed(range(2, self.form_container_layout.count())):
			widget = self.form_container_layout.itemAt(i).widget()
			if widget is not None:
				widget.setParent(None)
		period = int(self.input_number_of_periods.text())
		self.registration_data_object.clear()
		self.registration_data_object.extend(["Register", "Period"])
		for i in range(1, period+1):
			input_period_no = QLabel("Period no " + str(i))
			input_start_time = QLineEdit()
			input_start_time.setPlaceholderText("Start time")
			input_end_time = QLineEdit()
			input_end_time.setPlaceholderText("End time")
			self.form_container_layout.addWidget(input_period_no)
			self.form_container_layout.addWidget(input_start_time)
			self.form_container_layout.addWidget(input_end_time)
			self.registration_data_object.append([str(i), input_start_time, input_end_time])
		register_button = QPushButton("Register")
		register_button.clicked.connect(self.submit_registration)
		register_button.setFixedWidth(250)
		register_button.setFixedHeight(50)
		self.form_container_layout.addWidget(register_button)

	def check_os(self):
		os_name = platform.system()
		if os_name == "Linux":
			return True
		else:
			return False

	#***the page to view information regarding the registered classroom
	def classroom_page(self):
		#self.clear_layout()
		#updates = []
		#classroom_details = self.client_server_comm()
		#classroom_details.
		#student_state_list = []

		container = QWidget()
		container_layout = QVBoxLayout()
		container.setLayout(container_layout)
		container_layout.setSpacing(1)
		container_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
		container.setStyleSheet("font-size: 18px; color: #00ffcc;")
		container_layout.setContentsMargins(30, 30, 30, 30)

		h_container_layout = QHBoxLayout()
		h_container_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

		v_container1_layout = QVBoxLayout()
		v_container1_layout.setAlignment(Qt.AlignLeft)

		v_container2_layout = QVBoxLayout()
		v_container2_layout.setAlignment(Qt.AlignCenter)

		os_check = self.check_os()
		if(os_check == False):
			self.error_page("Classroom mode requires a Linux system.")
		else:
			if(os.path.exists("classroom_config")):

				self.loading_page(classroom_page=True)
				QApplication.processEvents()

				classroom_info = self.read_write_config_file()
				room_id = classroom_info[0]

				if self.ap_status == 0:
					print("classroom_info: " + str(classroom_info))
					print("classroom_info[3]: " + str(classroom_info[3]))
					self.ap_status = 1
					network_interface = classroom_info[1]
					ap_interface = classroom_info[2]
					blocked_domain = classroom_info[3]
					ap_name = classroom_info[4]
					ap_password = classroom_info[5]
					self.ap_scanner.network_interface = network_interface
					self.ap_scanner.ap_interface = ap_interface
					print("blocked_domain: " + str(blocked_domain))
					self.ap_scanner.blocked_domain.extend(blocked_domain)
					self.ap_scanner.ap_name = ap_name
					self.ap_scanner.ap_password = ap_password
					print("ap_started-----------------------------------------------------------------")
					self.ap_scanner.start_ap()

				classroom_details_request = ["classroom_details_request", str(room_id)]
				response = self.client_server_comm(classroom_details_request)
				print(response)

				if(response[0][0] != False):
					classroom_id_label = QLabel("Classroom ID: " + room_id)
					intake_sec_label = QLabel("Intake: " + response[0][1][0] + "/" + response[0][1][1])
					total_number_label = QLabel("Total Number of Students: " + str(len(response[0])-2))
					present_label = QLabel("Present: -")
					course_id_label = QLabel("Course ID: " + response[0][1][2])
					department_label = QLabel("Department: " + response[0][0][3])
					period_no = response[0][0][-1]

					v_container1_layout.addWidget(classroom_id_label)
					v_container1_layout.addWidget(intake_sec_label)
					v_container1_layout.addWidget(total_number_label)
					
					v_container2_layout.addWidget(course_id_label)
					v_container2_layout.addWidget(department_label)
					v_container2_layout.addWidget(present_label)

					h_container_layout.addLayout(v_container1_layout)
					h_container_layout.addSpacing(50)
					h_container_layout.addLayout(v_container2_layout)

					teacher_label = QLabel("ID: " + response[0][0][0] + " | Name: " + response[0][0][1] + " | Email: " + response[0][0][4])

					std_scroll_area = QScrollArea()
					std_scroll_area.setWidgetResizable(True)
					std_widget = QWidget()
					std_layout = QVBoxLayout()
					std_layout.setAlignment(Qt.AlignTop)
					std_widget.setLayout(std_layout)

					scan_report = self.ap_scanner.monitor_client()
					scan_report = list(set(scan_report))
					scan_report.insert(0, "FF:FF:FF:FF:FF:FF")
					scan_report.insert(1, "22:4q:as:33:44:66")########################################################################################################
					print("report: " + str(scan_report))

					if(period_no != self.period_no):
						#send data to backend
						if self.period_no != 0:
							self.student_details.insert(0, [str(self.total_pings), self.period_no])
							self.student_details.insert(0, "Attendance")  #["Attendance", total_pings, id, name, mac, intake, section, department, present_ping]
							self.client_server_comm(self.student_details)
						self.period_no = period_no
						self.student_details.clear()
						self.total_pings = 0
						for student in response[0][2:]:
							self.student_details.append([student[0], student[1], student[3], response[0][1][0], response[0][1][1], response[0][1][2], response[0][0][3], 0]) #[id, name, mac, intake, section, department, ping]
						print("details: " + str(self.student_details))

					self.total_pings = self.total_pings + 1
					count = 0
					for student in self.student_details:
						for client in scan_report:
							print("comparing: '" + str(student[2].lower() + "'=='" + str(client.lower()) + "'"))
							print("report: " + str(scan_report))
							state = "Absent"
							if student[2].lower() == client.lower():
								print("[+]Matched")
								state = "Present"
								count = count + 1
								student[7] = student[7] + 1
							else:
								print("[+]Dismatched")
								state = "Absent"
						print(str(student[0]) + " is getting " + str(state))
						std_label = QLabel("ID: " + student[0] + " | Name: " + student[1] + " | " + str(state) + " | Present pings: " + str(student[7]) + " | Total pings: " + str(self.total_pings))
						std_label.setWordWrap(True)
						std_label.setStyleSheet("font-size: 14px; padding: 5px; border: 1px solid #00ffcc; margin-bottom: 5px;")
						std_layout.addWidget(std_label)
					present_label.setText("Present: " + str(count))

					#std_label = QLabel("ID: " + student[0] + " | Name: " + student[1])
					#student.append(std_label)
					#student_state_list.append(std_label, student[2], student[3])
					
					std_scroll_area.setWidget(std_widget)
					std_scroll_area.setFixedHeight(700)

					container_layout.addLayout(h_container_layout)
					container_layout.addWidget(teacher_label)
					container_layout.addWidget(std_scroll_area)
				else:
					no_class_label = QLabel("No classes at the moment")
					container_layout.addWidget(no_class_label)
					if(self.total_pings != 0):
						self.student_details.insert(0, [str(self.total_pings), self.period_no])
						self.student_details.insert(0, "Attendance")  #["Attendance", total_pings, id, name, mac, intake, section, department, present_ping]
						self.client_server_comm(self.student_details)
						self.period_no = 0
						self.student_details.clear()
						self.total_pings = 0

				self.clear_layout(classroom_page=True)
				self.main_layout.addWidget(container)

				def refresh_classroom_page():
					self.classroom_page()

				#self.refresh_classroom_timer.timeout.connect(refresh_classroom_page)--------------#
				#self.refresh_classroom_timer.start(60000)										   #commented these lines for testing
																								   #
				#self.refresh_classroom_timer.stop()-----------------------------------------------
				
				# Disconnect any previously connected slots to avoid multiple triggers
				try:
					self.refresh_classroom_timer.timeout.disconnect()
				except TypeError:
					# No previous connections, ignore
					pass
				# Connect the refresh function once
				self.refresh_classroom_timer.timeout.connect(self.classroom_page)
				# Start the timer
				self.refresh_classroom_timer.start(60000)

			else:
				self.error_page("Please ask an admin to setup the classroom first")

	#***the page to take the classroom_id 
	def setup_page(self):
		self.clear_layout()
		container = QWidget()
		container_layout = QVBoxLayout()
		container.setLayout(container_layout)
		container_layout.setAlignment(Qt.AlignTop|Qt.AlignCenter)
		container_layout.setContentsMargins(30, 30, 50, 50)
		container_layout.setSpacing(20)

		room_id_label = QLabel("Room ID:")
		input_room_id = QLineEdit()
		input_room_id.setPlaceholderText("Room ID")
		input_room_id.setFixedHeight(70)
		input_room_id.setFixedWidth(340)

		network_interface_label = QLabel("Network Interface: ")
		network_interface_input = QLineEdit()
		network_interface_input.setPlaceholderText("Network Interface name")
		network_interface_input.setFixedHeight(70)
		network_interface_input.setFixedWidth(340)

		ap_interface_label = QLabel("AP interface: ")
		ap_interface_input = QLineEdit()
		ap_interface_input.setPlaceholderText("AP Interface")
		ap_interface_input.setFixedHeight(70)
		ap_interface_input.setFixedWidth(340)

		ap_name_label = QLabel("SSID: ")
		ap_name_input = QLineEdit()
		ap_name_input.setPlaceholderText("AP name")
		ap_name_input.setFixedHeight(70)
		ap_name_input.setFixedWidth(340)

		ap_password_label = QLabel("Password: ")
		ap_password_input = QLineEdit()
		ap_password_input.setPlaceholderText("Password")
		ap_password_input.setFixedHeight(70)
		ap_password_input.setFixedWidth(340)

		blocked_domains_label = QLabel("Domains to block (comma separated): ")
		blocked_domains_input = QLineEdit()
		blocked_domains_input.setPlaceholderText("example: facebook.com, youtube.com, chatgpt.com")
		blocked_domains_input.setFixedHeight(70)
		blocked_domains_input.setFixedWidth(340)

		submission_state_label = QLabel("")		
		def submit_classroom_id():               #function inside function, this function handles the notification of successfully submitting the room id once submit button is clicked. it is connected to the button
			room_id = self.classroom_info[0].text().strip()
			network_interface = self.classroom_info[1].text().strip()
			ap_interface = self.classroom_info[2].text().strip()
			print("self.classroom_info[3].text() = " + str(self.classroom_info[3].text().strip()))###########
			#blocked_domains = self.classroom_info[3].text().strip().split(", ")
			blocked_domains = [domain.strip() for domain in self.classroom_info[3].text().strip().split(",")]
			ap_name = self.classroom_info[4].text().strip()
			ap_password = self.classroom_info[5].text().strip()
			classroom_data_list = [room_id, network_interface, ap_interface, blocked_domains, ap_name, ap_password]
			if room_id:
				self.read_write_config_file(classroom_data_list)
				submission_state_label.setText("Room ID " + str(room_id) + " has been registered for this system")
			else:
				submission_state_label.setText("Please complete the form first!")	
		submit_button = QPushButton("Submit")
		submit_button.setStyleSheet("font-size:18pt;")
		self.classroom_info.clear()
		self.classroom_info.extend([input_room_id, network_interface_input, ap_interface_input, blocked_domains_input, ap_name_input, ap_password_input])
		submit_button.clicked.connect(submit_classroom_id)

		container_layout.addWidget(room_id_label)
		container_layout.addWidget(input_room_id)
		container_layout.addWidget(network_interface_label)
		container_layout.addWidget(network_interface_input)
		container_layout.addWidget(ap_interface_label)
		container_layout.addWidget(ap_interface_input)
		container_layout.addWidget(ap_name_label)
		container_layout.addWidget(ap_name_input)
		container_layout.addWidget(ap_password_label)
		container_layout.addWidget(ap_password_input)
		container_layout.addWidget(blocked_domains_label)
		container_layout.addWidget(blocked_domains_input)
		container_layout.addWidget(submit_button)
		container_layout.addWidget(submission_state_label)

		self.main_layout.addWidget(container)

	def error_page(self, error_message):
		self.clear_layout()
		container = QWidget()
		container_layout = QVBoxLayout()
		container.setLayout(container_layout)
		container_layout.setAlignment(Qt.AlignCenter)
		container_layout.setContentsMargins(30, 30, 50, 50)

		label = QLabel("Error: " + str(error_message))
		label.setStyleSheet("color: #00FFCC; font-size:18pt;")
		container_layout.addWidget(label)

		self.main_layout.addWidget(container)

	#***to read and write on the classroom_config file, containing classroom configuration
	def read_write_config_file(self, data=None):    
		if data:
			with open("classroom_config", "w") as file:
				json.dump(data, file)
			return ["configuration saved successfully"]
		else:
			with open("classroom_config", "r") as file:
				room_id = json.load(file)
			file.close()
			return room_id

	#***clears layout, preparing the window to be used by other pages.
	def clear_layout(self, classroom_page=False):
		if self.refresh_classroom_timer.isActive():
			self.refresh_classroom_timer.stop()

		for i in reversed(range(self.main_layout.count())):
			widget = self.main_layout.itemAt(i).widget()
			if widget is not None:
				widget.setParent(None)

	#***handles communication with backend server
	def client_server_comm(self, data):
		url = "http://" + SERVER_IP + ":" + SERVER_PORT + "/data"
		#url = "http://100.91.122.81:5000/data"
		print("\n\n" + str(data) + "\n\n")
		response = requests.post(url, json=data)
		responded_data = response.json()
		return responded_data

	#***the page to select the mode of the application, classroom or user
	def selection_page(self):
		self.clear_layout()
		container = QWidget()
		container_layout = QVBoxLayout()
		container.setLayout(container_layout)
		container_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter) 
		container_layout.setContentsMargins(30, 30, 50, 50)
		container_layout.setSpacing(20) 

		logo_label = QLabel()
		pixmap = QPixmap("wisign_logo.png")
		pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		logo_label.setPixmap(pixmap)
		logo_label.setAlignment(Qt.AlignCenter)

		container_layout.addWidget(logo_label)
		container_layout.addSpacing(20) 

		label = QLabel("Welcome to WiSign!")
		label.setStyleSheet("font-size:18pt;")

		classroom_button = QPushButton("Classroom")
		classroom_button.setStyleSheet("font-size:18pt;")
		classroom_button.clicked.connect(lambda: self.enter_page(self.classroom_page))
		classroom_button.setFixedHeight(70)
		classroom_button.setFixedWidth(340)

		user_button = QPushButton("User Login")
		user_button.setStyleSheet("font-size:18pt;")
		user_button.clicked.connect(lambda: self.enter_page(self.login_page))
		user_button.setFixedHeight(70)
		user_button.setFixedWidth(340)

		container_layout.addWidget(label)
		container_layout.addSpacing(10)  
		container_layout.addWidget(classroom_button)
		container_layout.addWidget(user_button)

		self.main_layout.addWidget(container, alignment=Qt.AlignTop | Qt.AlignHCenter)

	def student_page(self):
		self.clear_layout()
		response = self.client_server_comm(["student_info"] + (self.login_response[0]))
		if response[0][0] == False:
			no_data_label = QLabel("<span style='font-size: 20px; color: #00FFCC; font-family: Arial;'>No data found regarding this user</span>")
			no_data_label.setAlignment(Qt.AlignCenter)
			self.main_layout.addWidget(no_data_label)
		else:
			container = QWidget()
			container_layout = QHBoxLayout()
			container.setLayout(container_layout)
			#container_layout.setAlignment(Qt.AlignTop)

			student_info_widget = QWidget()
			student_info_layout = QVBoxLayout(student_info_widget)
			student_info_widget.setStyleSheet(
					"""
				QLabel {
					background-color: #292929;
					color: white;
					font-size: 18pt;
					font-weight: bold;
					font-family: Arial;
					/*border: 4px solid #00FFCC;*/
					padding: 8px 10px; 
					/*border-bottom: 2px solid #CCCCCC;*/
				}
			""")
			student_info_layout.setSpacing(20)
			student_info_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
			name_label = QLabel(f"<div style='font-size: 16px;'><b><span style='color: #00FFCC;'>Name: </span><span style='color: white';>{self.login_response[0][2]}</span></b></div>")
			name_label.setWordWrap(True)
			id_label = QLabel(f"<div style='font-size: 16px;'><b><span style='color: #00FFCC;'>ID: </span><span style='color: white';>{self.login_response[0][1]}</span></b></div>")
			email_label = QLabel(f"<div style='font-size: 16px;'><b><span style='color: #00FFCC;'>Email: </span><span style='color: white';>{self.login_response[0][3]}</span></b></div>")
			mac_label = QLabel(f"<div style='font-size: 16px;'><b><span style='color: #00FFCC;'>MAC: </span><span style='color: white';>{self.login_response[0][4]}</span></b></div>")
			intake_label = QLabel(f"<div style='font-size: 16px;'><b><span style='color: #00FFCC;'>Intake: </span><span style='color: white';>{self.login_response[0][5]}</span></b></div>")
			section_label = QLabel(f"<div style='font-size: 16px;'><b><span style='color: #00FFCC;'>Section: </span><span style='color: white';>{self.login_response[0][6]}</span></b></div>")
			department_label = QLabel(f"<div style='font-size: 16px;'><b><span style='color: #00FFCC;'>Department: </span><span style='color: white';>{self.login_response[0][7]}</span></b></div>")


			student_info_layout.addWidget(name_label)
			student_info_layout.addWidget(id_label)
			student_info_layout.addWidget(email_label)
			student_info_layout.addWidget(mac_label)
			student_info_layout.addWidget(intake_label)
			student_info_layout.addWidget(section_label)
			student_info_layout.addWidget(department_label)

			student_attendance_widget = QWidget()
			student_attendance_layout = QVBoxLayout(student_attendance_widget)
			student_attendance_layout.setAlignment(Qt.AlignTop)
			#student_attendance_layout.addStretch(1)
			student_attendance_scroll = QScrollArea()
			student_attendance_scroll.setWidgetResizable(True)
			student_attendance_scroll.setStyleSheet(
				"""
				QScrollArea { 
					border: 2px solid #00FFCC; 
					padding: 10px; 
					background-color: #2F2F2F;
				}
				""")
			present_count = 0
			for day in response[0][:-1]:
				print("day: " + str(day))
				status = day[0].upper()
				if(status == "ABSENT"):
					bg_colour = "#663333"
				else:
					bg_colour = "#335555"
					present_count = present_count + 1
				attendance_label_text = f"""
					<div style='color: white; padding: 0px;'>
						<span style='font-size: 18px; font-weight: bold;'>{status}</span> 
						<span style='font-size: 14px; color: #00FFCC; margin-left: 20px;'>Course ID: {day[5]}</span>
						<span style='float: right; font-size: 18px; font-weight: bold; color: yellow;'>{day[3]}%</span>
					</div>
					<div style='font-size: 12px; color: #AAAAAA;'>
						Date: {day[4]} | Present: {day[1]} min / Total: {day[2]} min
					</div>
					"""
				attendance_label = QLabel(attendance_label_text)
				attendance_label.setWordWrap(True)
				attendance_label.setStyleSheet("border: 1px solid #00FFCC; padding: 5px; font-size: 15px; font-family: Arial; margin-bottom: 10px; background-color: " + str(bg_colour) + ";")
				student_attendance_layout.addWidget(attendance_label)
			separator = QFrame()
			separator.setFrameShape(QFrame.HLine)
			separator.setFrameShadow(QFrame.Sunken)
			separator.setFixedWidth(335)
			separator.setStyleSheet("border-top: 7px solid #00FFCC;")
			student_info_layout.addWidget(separator)
			total_days = len(response[0])
			percentage = int((present_count/total_days) * 100)
			total_label = QLabel(f"<div style='font-size: 16px;'><b><span style='color: #00FFCC;'>Total Classes: </span><span style='color: white';>{total_days}</span></b></div>")
			present_label = QLabel(f"<div style='font-size: 16px;'><b><span style='color: #00FFCC;'>Total Presents: </span><span style='color: white';>{present_count}</span></b></div>")
			percentage_label = QLabel(f"<div style='font-size: 16px;'><b><span style='color: #00FFCC;'>Present Percentage: </span><span style='color: white';>{percentage}%</span></b></div>")
			course_label = QLabel("<div style='font-size: 16px;'>Present <span style='color: #00FFCC;'><b>|</b></span> Total Class <span style='color: #00FFCC;'><b>|</b></span> Percentage</b>")
			student_info_layout.addWidget(course_label)
			for course in response[0][-1]:
				course_label = QLabel(f"<div style='font-size: 16px;'><span style='color: #00FFCC;'>{course[0]}: </span>  {course[1]} <span style='color: #00FFCC;'>|</span> {course[2]} <span style='color: #00FFCC;'>|</span> {int(course[3])}%</div>")
				student_info_layout.addWidget(course_label)

			separator1 = QFrame()
			separator1.setFrameShape(QFrame.HLine)
			separator1.setFrameShadow(QFrame.Sunken)
			separator1.setFixedWidth(350)
			separator1.setStyleSheet("border-top: 3px solid #00FFCC;")
			student_info_layout.addWidget(separator1)
			student_info_layout.addWidget(total_label)
			student_info_layout.addWidget(present_label)
			student_info_layout.addWidget(percentage_label)
			student_info_layout.addStretch(1)

			student_info_scroll = QScrollArea()
			student_info_scroll.setWidgetResizable(True)
			student_info_scroll.setWidget(student_info_widget)

			student_attendance_scroll.setWidget(student_attendance_widget)
			container_layout.addWidget(student_info_scroll, 2)
			container_layout.addWidget(student_attendance_scroll, 8)

			self.main_layout.addWidget(container)

	def teacher_page(self):
		self.clear_layout()
		intake_list = ["Select Intake"]
		section_list = ["Select Section"]
		course_list = ["Select Courses"]
		date_list = ["Select Date"]
		filter_data_list = self.client_server_comm(["teacher_filter_data", self.login_response[0][1]])
		print(filter_data_list[0])
		for filter_data in filter_data_list[0][0]:
			print(filter_data)
			if filter_data[0] not in intake_list:
				intake_list.append(filter_data[0])
			if filter_data[1] not in section_list:
				section_list.append(filter_data[1])
			if filter_data[2] not in course_list:
				course_list.append(filter_data[2])
		for date_data in filter_data_list[0][1]:
			print(date_data)
			date_list.append(date_data)

		container = QWidget()
		container_layout = QHBoxLayout(container)

		teacher_info_widget = QWidget()
		teacher_info_layout = QVBoxLayout(teacher_info_widget)
		teacher_info_scroll = QScrollArea()
		teacher_info_scroll.setWidgetResizable(True)
		teacher_info_scroll.setWidget(teacher_info_widget)

		teacher_label = QLabel("Teacher")
		teacher_name_label = QLabel("Name: " + self.login_response[0][2])
		teacher_id_label = QLabel("ID: " + self.login_response[0][1])
		teacher_MAC_label = QLabel("MAC: " + self.login_response[0][3])
		teacher_department_label = QLabel("Department: " + self.login_response[0][4])
		teacher_email_label = QLabel("Email: " + self.login_response[0][5])
		teacher_label.setStyleSheet("""
			QLabel {
				background-color: #292929;
				color: white;
				font-size: 18pt;
				font-weight: bold;
				font-family: Arial;
				border: 4px solid #00FFCC;
				padding: 8px 10px; 
				border-bottom: 2px solid #CCCCCC;
			}
		""")
		info_label_style = """
			QLabel {
				background-color: #292929;
				color: white;
				font-size: 13pt;
				font-family: Arial;
				padding: 15px 20px;
				border-bottom: 1px solid #CCCCCC;
			}
		"""
		teacher_name_label.setStyleSheet(info_label_style)
		teacher_name_label.setWordWrap(True)
		teacher_id_label.setStyleSheet(info_label_style)
		teacher_MAC_label.setStyleSheet(info_label_style)
		teacher_department_label.setStyleSheet(info_label_style)
		teacher_department_label.setWordWrap(True)
		teacher_email_label.setStyleSheet(info_label_style)
		teacher_email_label.setWordWrap(True)
		teacher_info_layout.addWidget(teacher_label)
		teacher_info_layout.addWidget(teacher_name_label)
		teacher_info_layout.addWidget(teacher_id_label)
		teacher_info_layout.addWidget(teacher_MAC_label)
		teacher_info_layout.addWidget(teacher_department_label)
		teacher_info_layout.addWidget(teacher_email_label)
		spacer_label = QLabel("")
		teacher_info_layout.addWidget(spacer_label)
		course_head_label = QLabel("Current Courses")
		course_head_label.setStyleSheet(
			"""
				QLabel {
					background-color: #292929;
					color: white;
					font-size: 18pt;
					font-weight: bold;
					font-family: Arial;
					border: 4px solid #00FFCC;
					padding: 8px 10px; /* More padding for a title */
					border-bottom: 2px solid #CCCCCC; /* Thicker gray line for the main separator */
				}
			"""
			)
		teacher_info_layout.addWidget(course_head_label)
		for course in course_list[1:]:
			course_label = QLabel(str(course))
			course_label.setStyleSheet(info_label_style)
			teacher_info_layout.addWidget(course_label)
		teacher_info_layout.addStretch(1)

		sub_vbox_widget = QWidget()
		sub_vbox_layout = QVBoxLayout(sub_vbox_widget)

		teacher_filter_widget = QWidget()
		teacher_filter_layout = QHBoxLayout(teacher_filter_widget)

		self.teacher_student_widget = QWidget()
		self.teacher_student_layout = QVBoxLayout(self.teacher_student_widget)
		teacher_student_scroll = QScrollArea()
		teacher_student_scroll.setWidgetResizable(True)
		teacher_student_scroll.setWidget(self.teacher_student_widget)
		teacher_student_scroll.setStyleSheet(				
			"""
			QScrollArea { 
				border: 2px solid #00FFCC; 
				padding: 10px; 
				background-color: #2F2F2F;
			}
			""")

		filter_style = """
			QComboBox {
					min-width: 120px; 
					padding: 5px;
					font-size: 14px;
					font-family: Arial;
					font-weight: bold;
					color: white; 
					background-color: #292929;  
				}
				QComboBox QAbstractItemView {
					font-size: 14px;
					background-color: #3F3F3F;
					color: white;
					selection-background-color: #3F3F3F; 
				}
			"""
		intake_filter = QComboBox()
		intake_filter.setStyleSheet(filter_style)
		for intake in intake_list:
			intake_filter.addItem(intake)	
		teacher_filter_layout.addWidget(intake_filter, 3)

		section_filter = QComboBox()
		section_filter.setStyleSheet(filter_style)
		for section in section_list:
			section_filter.addItem(section)
		teacher_filter_layout.addWidget(section_filter, 3)

		course_filter = QComboBox()
		course_filter.setStyleSheet(filter_style)
		for course in course_list:
			course_filter.addItem(course)
		teacher_filter_layout.addWidget(course_filter, 3)

		date_filter = QComboBox()
		date_filter.setStyleSheet(filter_style)
		for date in date_list:
			date_filter.addItem(date)
		teacher_filter_layout.addWidget(date_filter, 3)

		filter_button = QPushButton("Filter")
		filter_button.setStyleSheet(
			"""
			QPushButton {
				min-width: 40px;
				min-height: 20px;
				background-color: #3F3F3F; 
				color: white;           
				border: 1px solid #00FFCC;
				padding: 5px 15px;
				font-size: 14px;
				font-weight: bold;
			}
			QPushButton:hover {
				background-color: #292929;
			}
			""")
		student_info_list = []
		current_section_data = [0, 0, 0, 0]
		student_update_list = []
		self.update_notification_label = QLabel("<span style='font-weight: bold;'>•</span> Updated successfully! Please re-apply the Filter to view updated page.") #**it is defined here because applied_filter function needs to access it to hide it when filter is applied
		self.update_notification_label.setStyleSheet("color: #00FFCC; font-size: 18px;")
		self.update_notification_label.setVisible(False) #**hiding it initially. will only be visible at update_present() function
		def clear_layout_widgets(layout):
			if layout is not None:
				while layout.count():
					item = layout.takeAt(0)
					widget = item.widget()
					if widget is not None:
						widget.setParent(None)
						widget.deleteLater()
		def apply_filter():
			self.update_notification_label.setVisible(False)
			current_section_data[0] = intake_filter.currentText()
			current_section_data[1] = section_filter.currentText()
			current_section_data[2] = course_filter.currentText()
			current_section_data[3] = date_filter.currentText()
			response = self.client_server_comm(["apply_teacher_filter", current_section_data[0], current_section_data[1], current_section_data[2], current_section_data[3]])
			nonlocal student_info_list
			student_info_list = response[0]
			print("**response: " + str(response))
			clear_layout_widgets(self.teacher_student_layout)
			index_count = 0
			for student in response[0]:
				student_widget = QFrame()
				student_widget.setFrameShape(QFrame.StyledPanel)
				student_widget.setStyleSheet("background-color: #551111; border-radius: 6px; padding: 8px;")
				student_row = QHBoxLayout(student_widget)
				state = False
				if student[0] == "present":
					state = True
				row_info = f"""
					<div style='color: white; padding: 2px;'>
						<span style='font-size: 16px; font-weight: bold;'>ID: {student[1]}</span>
						<span style='font-size: 12px; color: #00FFCC; margin-left: 10px;'>Name: {student[2]}</span>
						<span style='float: right; font-size: 16px; font-weight: bold; color: yellow;'>Course Presence: {student[6]}%</span>
					</div>
					<div style='font-size: 12px; color: #AAAAAA;'>
						Present: {student[3]} min | Total: {student[4]} min | Day present: {student[5]}%
					</div>
				"""
				info_label = QLabel(row_info)
				info_label.setWordWrap(True)
				check_box = QCheckBox("Present")
				check_box.setChecked(state)
				if state:
						student_widget.setStyleSheet("background-color: #335555; border-radius: 6px; padding: 8px;")
				else:
						student_widget.setStyleSheet("background-color: #663333; border-radius: 6px; padding: 8px;")
				def update_checkbox_data(checkbox_state, widget=student_widget, box_student=student, index=index_count):
					if checkbox_state:
						widget.setStyleSheet("background-color: #335555; border-radius: 6px; padding: 8px;")
						box_student[0] = "present"
					else:
						widget.setStyleSheet("background-color: #663333; border-radius: 6px; padding: 8px;")
						box_student[0] = "absent"
					if index not in student_update_list:
						student_update_list.append(index)
					else:
						student_update_list.remove(index)
					print(box_student)

				check_box.stateChanged.connect(update_checkbox_data)

				student_row.addWidget(info_label)
				student_row.addWidget(check_box)

				self.teacher_student_layout.addWidget(student_widget)
				index_count = index_count + 1
			self.teacher_student_layout.addStretch(1)
			
		filter_button.clicked.connect(apply_filter)
		teacher_filter_layout.addWidget(filter_button, 1)

		def update_present():
			print(student_info_list)
			updated_data = ["teacher_update_data", current_section_data]
			updated_data.append([])
			for index in student_update_list:
				updated_data[2].append(student_info_list[index])
			student_update_list.clear()
			if(len(updated_data[2]) > 0):
				response = self.client_server_comm(updated_data)
				self.update_notification_label.setText("<span style='font-weight: bold;'>•</span> Updated successfully! Please re-apply the Filter to view the updated page")
				self.update_notification_label.setVisible(True)
			else:
				self.update_notification_label.setText("<span style='font-weight: bold;'>•</span> No changes were made")
				self.update_notification_label.setVisible(True)

		button_style = """
			QPushButton {
				min-width: 40px;
				min-height: 20px;
				background-color: #3F3F3F; 
				color: white;
				border: 1px solid #00FFCC;
				padding: 5px 15px;
				font-size: 14px;
				font-weight: bold;
				font-family: Arial;
			}
			QPushButton:hover {
				background-color: #292929;
			}
			"""
		update_button = QPushButton("Update")
		update_button.setMaximumWidth(120)
		update_button.setStyleSheet(button_style)
		update_button.clicked.connect(update_present)
		sub_vbox_layout.addWidget(teacher_filter_widget, alignment=Qt.AlignTop)
		sub_vbox_layout.addWidget(teacher_student_scroll)

		configure_page_button = QPushButton("Configure AP")
		configure_page_button.setStyleSheet(button_style)
		configure_page_button.clicked.connect(lambda: self.enter_page(self.setup_page))

		notify_button_widget = QWidget()
		notify_button_layout = QHBoxLayout(notify_button_widget)
		notify_button_layout.addWidget(update_button, alignment=Qt.AlignLeft)
		notify_button_layout.addWidget(self.update_notification_label, alignment=Qt.AlignLeft)
		sub_vbox_layout.addWidget(notify_button_widget)#, alignment=Qt.AlignRight)
		#sub_vbox_layout.addWidget(self.update_notification_label, alignment=Qt.AlignLeft)
		sub_vbox_layout.addWidget(configure_page_button, alignment=Qt.AlignLeft)

		container_layout.addWidget(teacher_info_scroll, 2)
		container_layout.addWidget(sub_vbox_widget, 8)

		self.main_layout.addWidget(container)

	def admin_page(self):
		self.clear_layout()
		def clear_button_widgets(layout):
		    if layout is None:
		        return
		    try:
		        count = layout.count()
		    except RuntimeError:
		        return
		    while count > 0:
		        item = layout.takeAt(0)
		        if item.widget():
		            item.widget().deleteLater()
		        elif item.layout():
		            clear_button_widgets(item.layout())
		        count -= 1
		container_widget = QWidget()
		container_layout = QHBoxLayout(container_widget)

		filter_widget = QWidget()
		self.filter_layout = QHBoxLayout(filter_widget)
		info_widget = QWidget()
		self.info_layout = QVBoxLayout(info_widget)
		info_scroll = QScrollArea()
		info_scroll.setWidgetResizable(True)
		info_scroll.setWidget(info_widget)
		info_scroll.setStyleSheet(
		    """
		    QScrollArea {
		        border: 2px solid #00FFCC;
		        padding: 10px;
		    }
		    """
		)
		admin_info_widget = QWidget()
		admin_info_layout = QVBoxLayout(admin_info_widget)
		admin_info_scroll = QScrollArea()
		admin_info_scroll.setWidgetResizable(True)
		admin_info_scroll.setWidget(admin_info_widget)

		sub_vbox_widget = QWidget()
		sub_vbox_layout = QVBoxLayout(sub_vbox_widget)

		result_widget = QWidget()
		result_widget = QVBoxLayout(result_widget)

		admin_label = QLabel("Admin")
		admin_label.setStyleSheet(
			"""
			QLabel {
				background-color: #292929;
				color: white;
				font-size: 18pt;
				font-weight: bold;
				font-family: Arial;
				border: 4px solid #00FFCC;
				padding: 8px 10px; /* More padding for a title */
				border-bottom: 2px solid #CCCCCC;
			}
		""")
		admin_id = QLabel("ID: " + self.login_response[0][1])
		admin_id.setStyleSheet(
			"""
			QLabel {
				background-color: #292929;
				color: white;
				font-size: 14pt;
				font-weight: bold;
				font-family: Arial;
				/*border: 4px solid #00FFCC;*/
				padding: 8px 10px;
				border-bottom: 2px solid #CCCCCC;
			}
		""")
		#spacer_label = QLabel("\n\n")
		button_style = """
			QPushButton {
				width: 40px;
				height: 40px;
				background-color: #3F3F3F; 
				color: white;           
				border: 1px solid #00FFCC;
				padding: 5px 15px;
				font-size: 18px;
				font-weight: bold;
				font-family: Arial;
			}
			QPushButton:hover {
				background-color: #292929;
			}
			"""
		combobox_style = """
			QComboBox {
					min-width: 120px; 
					padding: 5px;
					font-size: 14px;
					font-family: Arial;
					font-weight: bold;
					color: white; 
					background-color: #292929;  
				}
				QComboBox QAbstractItemView {
					font-size: 14px;
					background-color: #3F3F3F;
					color: white;
					selection-background-color: #3F3F3F; 
				}
			"""
		def admin_edit(user):
			clear_button_widgets(self.info_layout)
			if isinstance(user, list):
				user = user[0]
			response = self.client_server_comm(["admin_edit", user])
			response[0].append([])
			if response[0][0][0][0] == "t":
				response[0][1] = ["ID", "NAME", "MAC", "DEPARTMENT", "EMAIL", "NEW PASSWORD"]
			elif response[0][0][0][0] == "s":
				response[0][1] = ["ID", "NAME", "EMAIL", "INTAKE", "MAC", "SECTION", "DEPARTMENT", "NEW PASSWORD"]
			elif response[0][0][0][0] == "a":
				response[0][1] = ["ID", "NEW PASSWORD"]
			print("STUDENT EDIT: " + str(response))
			index_count = 0
			update_button = QPushButton("Update")
			update_button.setStyleSheet(
				"""
			QPushButton {
				background-color: #3F3F3F; 
				color: white;           
				border: 1px solid #00FFCC;
				padding: 5px 15px;
				font-size: 18px;
				font-weight: bold;
				font-family: Arial;
			}
			QPushButton:hover {
				background-color: #292929;
			}
			"""
				)
			self.info_layout.addWidget(update_button, alignment=Qt.AlignRight)
			edit_object_list = []
			print("compared: " + str(response))
			for data in response[0][0]:
				print(data)
				#if response[0][1][index_count] == "password":
				#	label = QLabel("NEW PASSWORD")	
				#else:
				label = QLabel(response[0][1][index_count].upper())
				label.setStyleSheet(
					"""
					QLabel {
						background-color: #292929;
						color: #00FFCC;
						font-size: 18pt;
						font-weight: bold;
						font-family: Arial;
						padding: 8px 10px; 
						border-bottom: 2px solid #CCCCCC; 
					}""")
				if response[0][1][index_count].upper() == "NEW PASSWORD":
					edit = QLineEdit()
				else:
					edit = QLineEdit(data)
				edit.setStyleSheet(
				"""
					QLineEdit{
						/*max-width: 300px;*/
						min-width: 300px;
						max-height:50px;
						min-height:50px;
						font-size: 14px;
					}
				""")
				spacer = QLabel("")
				edit_object_list.append(edit)
				def admin_update():
					data_list = []
					for edit_obj in edit_object_list:
						data_list.append(edit_obj.text())
					print("data list: " + str(data_list))
					print("user: " + str(user))
					response = self.client_server_comm(["admin_update", user, data_list])
					print(response)
				update_button.clicked.connect(admin_update)
				self.info_layout.addWidget(label)
				self.info_layout.addWidget(edit)
				self.info_layout.addWidget(spacer)
				index_count = index_count + 1
			self.info_layout.addStretch(1)
		def admin_delete(user, btn, btn1):
			if isinstance(user, list):
				user = user[0]
			print("***USER: " + str(user))
			print("request to delete: " + str(user))
			response = self.client_server_comm(["admin_delete", user])
			btn.setStyleSheet("""
			    QPushButton {
			        font-size: 14px;
			        font-weight: bold;
			        padding: 8px 15px;
			        border: 2px solid red;
			    }
			    QPushButton:hover {
				background-color: #292929;
				}
			""")
			btn.setText("Deleted")
			btn1.hide()
		def button_row_add(data, label_list, label_style=None):
			clear_button_widgets(self.info_layout)
			if(label_style==None):
				label_style="""
					QLabel {
						color: white;
						font-size: 15pt;
						font-weight: bold;
						font-family: "Courier New", "Consolas", monospace;
						padding: 5px 7px; 
					}"""				
			button_style = """
			    QPushButton {
			        font-size: 14px;
			        font-weight: bold;
			        padding: 8px 15px;
			    }
			    QPushButton:hover {
				background-color: #292929;
				}
			"""
			index_count = 0
			for row in data:
				print("DATA: " + str(data))
				row_widget = QWidget()
				row_layout = QHBoxLayout(row_widget)
				row_widget.setStyleSheet("""
					QWidget {
						background-color: #292929;
						color: white;
						font-family: Arial;
						padding: 8px 10px; 
					}""")
				row_info_label = QLabel(str(label_list[index_count]))
				row_info_label.setStyleSheet(label_style)
				index_count = index_count + 1
				edit_button = QPushButton("Edit")
				edit_button.setStyleSheet(button_style)
				edit_button.clicked.connect(lambda checked=False, user=row: admin_edit(user))
				delete_button = QPushButton("Delete")
				delete_button.setStyleSheet(button_style)
				delete_button.clicked.connect(lambda checked=False, user=row, btn=delete_button, btn1=edit_button: admin_delete(user, btn, btn1))

				row_layout.addWidget(row_info_label)
				row_layout.addStretch(1)
				row_layout.addWidget(edit_button)
				row_layout.addWidget(delete_button)

				self.info_layout.addWidget(row_widget)
			self.info_layout.addStretch(1)
		def register_button_function():
			self.enter_page(self.registration_page)
		register_button = QPushButton("Register")
		register_button.setStyleSheet(button_style)
		register_button.clicked.connect(register_button_function)
		def admin_button_function():
			clear_button_widgets(self.filter_layout)
			clear_button_widgets(self.info_layout)
			response = self.client_server_comm(["admin_admin_info"])
			print("short: " + str(response[0]))
			user_list = response[0].copy()
			index_count = 0
			for user_id in response[0]:
				response[0][index_count] = "ID: " + response[0][index_count]
				index_count = index_count + 1
			button_row_add(user_list, response[0])
			print("Admin info: " + str(response))
		def get_admin_teacher_info():
			clear_button_widgets(self.info_layout)
			department = self.department_filter.currentText()
			response = self.client_server_comm(["admin_teacher_info", department])
			label_list = []
			for teacher in response[0]:
				teacher.pop()
				label_list.append(str(teacher).replace("'", "").replace(", ", " | ").replace("[", "").replace("]", ""))
			button_row_add(response[0], label_list)
			print("admin teacher info: " + str(response))
		def teacher_button_function():
			clear_button_widgets(self.filter_layout)
			clear_button_widgets(self.info_layout)
			self.department_filter = QComboBox()
			self.department_filter.setStyleSheet(combobox_style)
			department_list = self.client_server_comm(["admin_dept_filter"])
			print("DEPARTMENT: " + str(department_list))
			for department in department_list[0]:
				self.department_filter.addItem(department)
			search_button = QPushButton("Search")
			search_button.setStyleSheet("""
			QPushButton {
				background-color: #3F3F3F; 
				color: white;           
				border: 1px solid #00FFCC;
				padding: 5px 15px;
				font-size: 18px;
				font-weight: bold;
				font-family: Arial;
			}
			QPushButton:hover {
				background-color: #292929;
			}
			""")
			search_button.clicked.connect(get_admin_teacher_info)
			self.filter_layout.addWidget(self.department_filter)
			self.filter_layout.addStretch(1)
			self.filter_layout.addWidget(search_button)
		def get_admin_student_info():
			department = self.admin_student_obj_list[0].currentText()
			intake = self.admin_student_obj_list[1].currentText()
			section = self.admin_student_obj_list[2].currentText()
			response = self.client_server_comm(["admin_student_info", department, intake, section])
			label_list = []
			for data in response[0]:
				label_list.append(str(data).replace("'", "").replace("[", "").replace("]", "").replace(", ", " | "))
			print("label_list: " + str(label_list))
			print("user_list : " + str(response[0]))
			button_row_add(response[0], label_list)
		def student_button_function():
			clear_button_widgets(self.filter_layout)
			clear_button_widgets(self.info_layout)
			response = self.client_server_comm(["admin_student_filter"])
			print(response)
			department_items = []
			intake_items = []
			section_items = []
			for data in response[0]:
				if data[0] not in department_items:
					department_items.append(data[0])
				if data[1] not in intake_items:
					intake_items.append(data[1])
				if data[2] not in section_items:
					section_items.append(data[2])
			department_items.sort()
			intake_items.sort()
			section_items.sort(key=int)
			department_filter = QComboBox()
			department_filter.setStyleSheet(combobox_style)
			department_filter.addItem("Select Department")
			department_filter.addItems(department_items)
			intake_filter = QComboBox()
			intake_filter.setStyleSheet(combobox_style)
			intake_filter.addItem("Select Intake")
			intake_filter.addItems(intake_items)
			section_filter = QComboBox()
			section_filter.setStyleSheet(combobox_style)
			section_filter.addItem("Select Section")
			section_filter.addItems(section_items)
			self.admin_student_obj_list = [department_filter, intake_filter, section_filter]
			search_button = QPushButton("Search")
			search_button.setStyleSheet("""
			QPushButton {
				background-color: #3F3F3F; 
				color: white;           
				border: 1px solid #00FFCC;
				padding: 5px 15px;
				font-size: 18px;
				font-weight: bold;
				font-family: Arial;
			}
			QPushButton:hover {
				background-color: #292929;
			}
			""")
			search_button.clicked.connect(get_admin_student_info)
			self.filter_layout.addWidget(department_filter)
			self.filter_layout.addWidget(intake_filter)
			self.filter_layout.addWidget(section_filter)
			self.filter_layout.addStretch(1)
			self.filter_layout.addWidget(search_button)

		admin_button = QPushButton("Admin")
		admin_button.setStyleSheet(button_style)
		admin_button.clicked.connect(admin_button_function)
		teacher_button = QPushButton("Teacher")
		teacher_button.setStyleSheet(button_style)
		teacher_button.clicked.connect(teacher_button_function)
		student_button = QPushButton("Student")
		student_button.setStyleSheet(button_style)
		student_button.clicked.connect(student_button_function)

		admin_info_layout.addWidget(admin_label)
		admin_info_layout.addWidget(admin_id)
		admin_info_layout.addStretch(1)
		#admin_info_layout.addWidget(spacer_label)
		logo_label = QLabel()
		pixmap = QPixmap("wisign_logo.png")
		pixmap = pixmap.scaled(270, 270, Qt.KeepAspectRatio, Qt.SmoothTransformation)
		logo_label.setPixmap(pixmap)
		logo_label.setAlignment(Qt.AlignCenter)
		logo_label.setStyleSheet("padding: 20px;")
		admin_info_layout.addWidget(logo_label)
		admin_info_layout.addStretch(1)
		admin_info_layout.addWidget(register_button)#, alignment=Qt.AlignBottom)
		admin_info_layout.addWidget(admin_button)
		admin_info_layout.addWidget(teacher_button)
		admin_info_layout.addWidget(student_button)

		sub_vbox_layout.addWidget(filter_widget)
		sub_vbox_layout.addWidget(info_scroll)

		container_layout.addWidget(admin_info_scroll, 2)
		container_layout.addWidget(sub_vbox_widget, 8)

		self.main_layout.addWidget(container_widget)

	def loading_page(self, classroom_page=False):
		if classroom_page==False:
			self.clear_layout()
		else:
			self.clear_layout(classroom_page=True)
		container = QWidget()
		container_layout = QVBoxLayout()
		container.setLayout(container_layout)
		container_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter) 
		container_layout.setContentsMargins(30, 30, 50, 50)
		container_layout.setSpacing(20) 
		label = QLabel("Loading...")
		label.setStyleSheet("font-size:30pt;")
		container_layout.addWidget(label)

		self.main_layout.addWidget(container, alignment=Qt.AlignTop | Qt.AlignHCenter)	

	def enter_page(self, current_page):
		self.history.append(current_page)
		current_page()

	def go_back(self):
		if(len(self.history) > 1):
			self.history.pop()
		self.history[-1]()

	#***the function to run the application with
	def run(self):
		self.window.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
		self.title_bar = QWidget()
		title_bar_layout = QHBoxLayout()
		title_bar_layout.setContentsMargins(0, 0, 0, 0)
		self.title_bar.setLayout(title_bar_layout)

		back_button = QPushButton("Back")
		back_button.clicked.connect(self.go_back)
		back_button.setFixedSize(50, 30)
		title_bar_layout.addWidget(back_button)

		#title_bar_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

		logo_label = QLabel()
		pixmap = QPixmap('wisign_logo.png')
		pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio ,Qt.SmoothTransformation)
		logo_label.setPixmap(pixmap)
		title_bar_layout.addWidget(logo_label)

		title_bar_layout.addItem(QSpacerItem(400, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

		minimize_button = QPushButton("-")
		minimize_button.setFixedSize(30, 30)
		minimize_button.clicked.connect(self.window.showMinimized)
		title_bar_layout.addWidget(minimize_button)

		close_button = QPushButton("X")
		close_button.setFixedSize(30, 30)
		close_button.clicked.connect(self.window.close)
		title_bar_layout.addWidget(close_button)

		self.window_layout.insertWidget(0, self.title_bar)

		self.window.setStyleSheet("""
			QWidget{
				background-color: #3D3A3A;
				color: #FFFFFF;
			}
			QLineEdit{
				background-color: #424242;
				color: #FFFFFF;
				border: #00ffcc;
				padding-left: 10px;
				padding-right: 5px;
			}
			QPushButton{
				background-color: #333333;
				color: #FFFFFF;
				border: 1px solid #00ffcc;
				padding: 5px;
			}
			""")
		self.window.showMaximized()
		#self.registration_page()
		#self.login_page()
		#self.classroom_page()
		self.selection_page()
		#self.teacher_page()
		#self.setup_page()
		#print("exitinggggggggggg")
		sys.exit(app.exec_())							#when app.exec() exits (the application) it returns a 0, which then makes sure that sys.exit() exits the program cleanly


if __name__ == "__main__":
	os.environ["XDG_RUNTIME_DIR"] = f"/run/user/{os.getpid()}"
	app = QApplication(sys.argv)
	test = GUI()
	test.run()
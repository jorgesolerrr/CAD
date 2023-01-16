import os
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.list import OneLineIconListItem, OneLineListItem, MDList
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton,MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast
from kivy.properties import ObjectProperty, StringProperty, ColorProperty
from kivy.lang import Builder
from kivy.metrics import dp
from os import getcwd
from cad_backend import CAD
from .kivy_files.tools import clickableTextField 

Current_CAD: CAD = None
widgets_path = getcwd() + "\\cad_frontend\\kivy_files\\"



class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class Login(Screen):
    course = ObjectProperty()
    token = ObjectProperty()

    def Submit(self):
        if self.course.text == "" or self.token.text == "":
            self.show_log_exceptions("A required field is missing")
            return False
        try:
            global Current_CAD
            Current_CAD = CAD("http://localhost/webservice/rest/server.php", self.token.text, self.course.text)

            return True
        except Exception as e:
            self.show_log_exceptions(str(e))
            self.token.text = ""
            return False

    def show_log_exceptions(self, text: str):
        self.dialog = MDDialog(
            title="Login Error",
            text=text,
            size_hint=(0.5, 1),
            buttons=[MDFlatButton(text="OK", on_release=self.close_dialog)],
        )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()


class Dashboard(Screen):
    pass


class ContentNavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class Exam(Screen):
    data_period = ObjectProperty()
    date_picker = ObjectProperty()
    exam_box = ObjectProperty()
    exam_table = None
    show_button = None
    dates = None    
    def on_save_dates(self, instance, value, date_range):
        '''
        Events called when the "OK" dialog box button is clicked.

        :type instance: <kivymd.uix.picker.MDDatePicker object>;
        :param value: selected date;
        :type value: <class 'datetime.date'>;
        :param date_range: list of 'datetime.date' objects in the selected range;
        :type date_range: <class 'list'>;
        '''
        if len(self.dates) == 0:
            self.dates.append(str(value))
            self.exam_table.add_row((str(value), ()))
        else:
            try:
                i = self.dates.index(str(value))
                toast("this date already taken")
                return
            except:
                self.dates.append(str(value))
                self.exam_table.add_row((str(value), ()))

        print(str(value))

    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
        self.date_dialog.dismiss()

    def show_date_picker(self):
        if not self.dates:
            self.dates = []
        if not self.exam_table:
            self.exam_table = MDDataTable(
                use_pagination = True,
                pos_hint = {'center_x': 0.5},
                size_hint_y = 0.6,
                column_data = [
                    ("Date", dp(30)),
                    ("Courses to exam", dp(40))
                ]
            )
            self.exam_box.add_widget(self.exam_table)
        if not self.show_button:
            self.show_button = MDRaisedButton(
                text = "Show Calendar",
                pos_hint = {'center_x': 0.5,'center_y': 0.2},
                on_release = self.show_calendar
            )
            self.exam_box.add_widget(self.show_button)
        self.exam_box
        self.date_dialog = MDDatePicker()
        self.date_dialog.bind(on_save=self.on_save_dates, on_cancel=self.on_cancel)
        self.date_dialog.open()

    def show_calendar(self, event):
        if self.data_period.text == "":
            toast("Enter correct period")
            return
        try:
            response = Current_CAD.GetExamCalendar(self.dates, self.data_period.text)
        except Exception as e:
            toast(str(e))
            return
        new_row_data = [(key,str(tuple(response[key]))) for key in response.keys()]
        self.exam_table.row_data = new_row_data


class Students(Screen):
    data_students = ObjectProperty()
    buttton_panel = ObjectProperty()
    search_course = ObjectProperty()
    search_fullname = ObjectProperty()
    check_fullname = ObjectProperty()
    drop = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.courses_menu = None
        self.rows_data = []
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path
        )
    def get_next_courses(self):
        try:
            next_courses = Current_CAD.GetCADStudents.GetNextCoursesToEnroll(self.search_fullname.text)
        except KeyError:
            toast("This student is not in CAD")
            return
        except Exception as e:
            toast(str(e))
            return
        self.search_course.text = ""
        self.approveButton.disabled = True
        self.get_approved_coursesButton.disabled = False
        self.enrollButton.disabled = False
        courses_data = [(next_courses[key]["period"], key, next_courses[key]["name"]) for key in next_courses.keys()]

        self.students_table.column_data =[("period", dp(18)), ("shortname", dp(25)),("name", dp(30)) ]
        self.students_table.row_data = courses_data
    
    def open_file_manager(self):
        self.file_manager.show(os.path.expanduser("\\"))  # output manager to the screen
        self.manager_open = True
    
    def select_path(self, path: str):
        self.exit_manager()
        result = Current_CAD.EnrollStudentsInCAD(path)
        print(result)
        
    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def approve(self, event):
        students = self.students_table.get_row_checks()
        approves = []
        for st in students:
            approves.append(st[2])
        try:    
            response = Current_CAD.ApproveStudent(approves, self.search_course.text)
        except Exception as e :
            toast(str(e))
        toast(response)
    
    def enroll(self, event):
        courses = self.students_table.get_row_checks()
        student = self.search_fullname.text
        for cs in courses:
            try:
                Current_CAD.EnrollStudentInCourse(student, cs[1])
            except Exception as e:
                toast(str(e))
        toast("success")

    def get_approved_courses(self, event):
        items = MDList()
        approved = Current_CAD.GetCADStudents.GetApprovedCourses(self.search_fullname.text)
        for course in approved:
            items.add_widget(OneLineListItem(text = course))
        dialog = MDDialog(
                title = "Approved Courses",
                type="custom",
                content_cls = items
            )        
        dialog.open() 

    def load_table(self):
        boxL = MDBoxLayout(
            orientation = "vertical",
            pos_hint  = {'center_x': 0.3,'center_y': 0.8},
            size_hint_x = 0.6,
            spacing ="24dp"
        )
        self.students_table = MDDataTable(
            use_pagination = True,
            check = True,
            column_data = [
                ("No./period", dp(30)),
                ("Username/course", dp(30)),
                ("Fullname", dp(30)),
            ],
            row_data = self.rows_data  
        )
        
        self.button_boxL= MDBoxLayout(
            orientation = "horizontal",
            size_hint_y = 0.1,
            spacing ="24dp"
        )
        self.approveButton = MDRaisedButton(
            text = "Approve",
            disabled = True,
            on_release = self.approve,
        )
        self.enrollButton = MDRaisedButton(
            text = "Enroll",
            disabled = True,
            on_release = self.enroll
        )
        self.get_approved_coursesButton = MDRaisedButton(
            text = "Show approved courses",
            disabled = True,
            on_release = self.get_approved_courses
        )
        
        self.button_boxL.add_widget(self.approveButton)
        self.button_boxL.add_widget(self.enrollButton)
        self.button_boxL.add_widget(self.get_approved_coursesButton)
        self.students_table.bind(on_check_press=self.on_check_press)
        boxL.add_widget(self.students_table)
        boxL.add_widget(self.button_boxL)
        self.data_students.add_widget(boxL)
    

    def on_check_press(self, instance_table, current_row):
        '''Called when a table row is clicked.'''

        print(instance_table, current_row)



    def createDrop(self):
        if self.courses_menu is None:
            courses = Current_CAD.courses if not Current_CAD == None else {}
            menuCoursesList = [
                {
                    "viewclass": "IconListItem",
                    "icon": "school",
                    "width": dp(100),
                    "height": dp(56),
                    "text": f"{key}-" + courses[key]["name"],
                    "on_release": lambda x=f"{key}": self.set_item(x),
                }
                for key in courses.keys()
            ]
            self.courses_menu = MDDropdownMenu(
                caller=self.drop,
                items=menuCoursesList,
                width_mult=4,
            )

    def dropCourses(self):
        self.courses_menu.open()

    def set_item(self, shortname):
        self.approveButton.disabled = False
        self.enrollButton.disabled = True
        self.get_approved_coursesButton.disabled = True
        self.search_fullname.text = ""
        self.search_course.text = shortname
        self.FillTable_SearchByCourse(shortname)
        self.courses_menu.dismiss()
        
    
    def FillTable_SearchByCourse(self, text : str):
        students = (
            Current_CAD.GetStudentsFromCourse(text)
        )
        students_data = [
            (i, students[i]["username"], students[i]["fullname"])
            for i in range(len(students))
        ]
        self.students_table.update_row_data(self.students_table, students_data) 

    def on_enter(self, *args):
        # student_clickableTextField = Builder.load_string(clickableTextField)
        # self.buttton_panel.add_widget(student_clickableTextField)
        self.load_table()

    


    

        


# class ClickableTextFieldRound(MDRelativeLayout):
#     drop = ObjectProperty()
#     text = StringProperty()
#     hint_text = StringProperty()

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.courses_menu = None
#         self.currentCourse = self.text

    


sm = ScreenManager()
sm.add_widget(Login(name="login"))
sm.add_widget(Dashboard(name="dashboard"))


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        cours_page = Builder.load_file(widgets_path + "exam_page.kv")
        dash_page = Builder.load_file(widgets_path + "dashboard_page.kv")
        stud_page = Builder.load_file(widgets_path + "students_page.kv")
        self.login_page = Builder.load_file(widgets_path + "login_page.kv")

        return self.login_page

    def logout(self, obj):
        self.root.current = "login"
        self.root.transition.direction = "right"

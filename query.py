import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

year = "2022"
url = "https://www.unibz.it/en/timetable/?sourceId=unibz&department=370&degree=13756&fromDate=2022-09-26&toDate=2022-12-31&page="
pages = 9

MonthsCSV = {
    'Jan': '01',
    'Feb': '02',
    'Mar': '03',
    'Apr': '04',
    'May': '05',
    'Jun': '06',
    'Jul': '07',
    'Aug': '08',
    'Sep': '09',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}


class Course:
    def __init__(self, day, room, time, name, teacher="", type=""):
        self.day = day
        self.room = room
        self.time = time
        self.name = name
        self.teacher = teacher
        self.type = type

    def print(self):
        print("----------------------------------")
        print("{} || {} || {} || {}".format(
            self.day, self.room, self.time, self.type))
        print(self.name)
        if (self.teacher != ""):
            print(self.teacher)

    def GetStartTime(self):
        return self.time.split(" - ")[0]

    def GetEndTime(self):
        return self.time.split(" - ")[1]

    def FormatDescriptionForCSV(self):
        if (self.teacher != ""):
            return "{} | {}".format(self.type, self.teacher)
        else:
            return self.type

    def FormatNameForCSV(self):
        nameforcsv = self.name.replace(",", "⸒")
        return nameforcsv

    def FormatDateForCSV(self):
        daymonth = self.day.split(", ")[1]
        day = daymonth.split((" "))[0]
        monthhr = daymonth.split((" "))[1]
        month = MonthsCSV[monthhr]
        return "{}/{}/{}".format(month, day, year)

    def FormatTimeForCSV(time):
        hour = int(time[0:2])
        if (hour > 12):
            return "{}:{} PM".format(f'{(hour-12):02}', time[3:])
        else:
            return "{} AM".format(time)

    def FormatCSV(self):
        return "{},{},{},{},{},{}\n".format(self.FormatNameForCSV(), self.FormatDateForCSV(), Course.FormatTimeForCSV(self.GetStartTime()), Course.FormatTimeForCSV(self.GetEndTime()), self.FormatDescriptionForCSV(), self.room)

    def WriteHeaderToCSV(f):
        f.write("Subject,Start Date,Start Time,End Time,Description,Location\n")

    def WriteToCsv(self, f):
        f.write(self.FormatCSV())


def GetDaysFromPage(driver):
    days = driver.find_elements(By.TAG_NAME, "article")
    return days


def GetDateFromDay(day):
    date = day.find_element(By.CLASS_NAME, "u-h4")
    return date.text


def GetCoursesOnDay(day):
    courses = day.find_elements(By.CLASS_NAME, "t-scitec")
    return courses


def GetRoomFromCourse(course):
    room = course.find_element(
        By.CSS_SELECTOR, "p[class='u-push-btm-quarter u-tt-caps u-fs-sm u-c-theme u-fw-bold']")
    return room.text


def GetTimeFromCourse(course):
    timeandtype = course.find_element(
        By.CSS_SELECTOR, "p[class='u-push-btm-none u-tt-caps u-fs-sm u-fw-bold']").text
    time = timeandtype.split(" · ")[0]
    return time


def GetTypeFromCourse(course):
    timeandtype = course.find_element(
        By.CSS_SELECTOR, "p[class='u-push-btm-none u-tt-caps u-fs-sm u-fw-bold']").text
    type = timeandtype.split(" · ")[1]
    return type


def GetTeacherFromCourse(course):
    teacher = course.find_element(
        By.CSS_SELECTOR, "p[class='u-push-btm-none u-tt-caps u-ls-1 u-fs-sm u-fw-normal']").text
    return teacher


def GetNameFromCourse(course):
    name = course.find_element(
        By.CSS_SELECTOR, "h3[class='u-h5 u-push-btm-1']").text
    return name


def GetAllCourses(url, pages):
    cnt = 0
    c = []
    driver = webdriver.Firefox()

    for i in range(1, pages+1):
        urlpage = url.replace("page=", "page={}".format(i))

        driver.get(urlpage)

        days = GetDaysFromPage(driver)
        for day in days:
            date = GetDateFromDay(day)
            courses = GetCoursesOnDay(day)
            for course in courses:
                room = GetRoomFromCourse(course)
                time = GetTimeFromCourse(course)
                type = GetTypeFromCourse(course)
                teacher = GetTeacherFromCourse(course)
                name = GetNameFromCourse(course)
                c.append(Course(day=date, room=room, time=time,
                                name=name, teacher=teacher, type=type))
    return c


c = GetAllCourses(
    url, pages)

f = open("courses.csv", mode="+w")

Course.WriteHeaderToCSV(f)

for course in c:
    course.WriteToCsv(f)

f.close()

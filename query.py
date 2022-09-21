
from unittest import TestCase
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By


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


pages = 9
url = "https://www.unibz.it/en/timetable/?sourceId=unibz&department=370&degree=13756&fromDate=2022-09-26&toDate=2022-12-31&page="
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
            c[cnt].print()
            cnt = cnt+1

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
from datetime import timedelta, date
from time import sleep
from random import randrange


def iterate_dates_range(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


def scrap_day(driver, date, station, wait_time=10):
    driver.get(f'https://www.wunderground.com/history/daily/{station}/date/{date.strftime("%Y-%m-%d")}')

    WebDriverWait(driver, wait_time).until(ec.presence_of_element_located((By.CLASS_NAME, "mat-row.ng-star-inserted")))
    sleep(randrange(1, 5))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all("tr", class_="mat-row ng-star-inserted")
    day = []

    for row in rows:
        cols = row.find_all("td")

        measure = {
            'date': date,
            'time': cols[0].find("span", class_="ng-star-inserted").text.strip(),
            'temperature': cols[1].find("span", class_="wu-value wu-value-to").text.strip(),
            'dew_point': cols[2].find("span", class_="wu-value wu-value-to").text.strip(),
            'humidity': cols[3].find("span", class_="wu-value wu-value-to").text.strip(),
            'wind_cardinal': cols[4].find("span", class_="ng-star-inserted").text.strip(),
            'wind_speed': cols[5].find("span", class_="wu-value wu-value-to").text.strip(),
            'wind_gust': cols[6].find("span", class_="wu-value wu-value-to").text.strip(),
            'pressure': cols[7].find("span", class_="wu-value wu-value-to").text.strip(),
            'precipitation_rate': cols[8].find("span", class_="wu-value wu-value-to").text.strip(),
            'condition': cols[9].find("span", class_="ng-star-inserted").text.strip()

        }
        day.append(measure)

    return day


if __name__ == "__main__":

    start_date = date(2019, 1, 1)
    end_date = date(2020, 1, 1)
    station = "LEVC"  # weatherunderground station code
    wait_time = 30
    driver = webdriver.Firefox()

    for loop_date in iterate_dates_range(start_date=start_date, end_date=end_date):
        scraped_day = scrap_day(driver=driver, date=loop_date, station=station, wait_time=wait_time)
        for time in scraped_day:
            print(time)  # Your sink

    driver.close()

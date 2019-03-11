# Little program to take a light novel from wuxiaworld.com and well... steal it for me! ;]

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time
import os
import textwrap
import re

# website = str(input("Which Book would you like to steal to today? https://www. "))
# testing with specific book for now
website = "wuxiaworld.com/novel/against-the-gods"

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)
print("Opening Firefox")
start = webdriver.Firefox(profile)
start.install_addon('C:\\Users\\Sati\\PycharmProjects\\SecondScript\\ublock_origin-1.18.4-an+fx.xpi')
print("Going to the website")
start.get("https://www." + website)


def book_data():
    book_title = start.find_element_by_css_selector('.p-15 > h4:nth-child(1)').text
    book_translator = start.find_element_by_css_selector('.dl-horizontal > dd:nth-child(2)').text
    chapters = start.find_elements_by_class_name("chapter-item")
    total_chapters = len(chapters)

    print(book_title + "\nTranslated by: " + book_translator)
    print("Total Chapters:" + str(total_chapters))


def make_book():
    book_title = start.find_element_by_css_selector('.p-15 > h4:nth-child(1)').text

    if os.path.isdir(book_title) is False:
        os.makedirs(book_title, 0o777)
        print("Making a new directory")
        os.chdir(book_title)
        print(os.getcwd())
    else:
        print("Directory :" + book_title + ", already exists and will be used")
        os.chdir(book_title)
        print(os.getcwd())


def next_chapter():
    try:
        start.find_element_by_css_selector('.top-bar-area > ul:nth-child(1) > li:nth-child(3) > a:nth-child(1)').click()
        print("This is the next chapter!")

    except NoSuchElementException:
        print("Looks like there's no chapters left!")
        return False

    except WebDriverException:
        print("page load error")
        start.refresh()
        return True

    return True


def chapter_thief():
    start.find_element_by_class_name("chapter-item").click()
    chapter_number = 0
    while next_chapter() is True and chapter_number < 10:
        if chapter_number == 0:
            start.back()
        chapter_title = start.find_element_by_css_selector('div.caption > div:nth-child(3) > h4:nth-child(2)').text
        chapter_title = re.sub(':|\\?| ', '_', chapter_title)
        print(chapter_title)

        print("Taking the chapter")
        chapter_text = start.find_element_by_class_name("fr-view").text
        print("Copying the chapter")
        chapter = open(chapter_title + ".txt", "w+", encoding="utf-8")
        try:
            chapter.write(textwrap.fill(chapter_text, 100))
            time.sleep(5)
        finally:
            chapter.close()
            chapter_number = chapter_number + 1
        print("Finished Chapter " + str(chapter_number))


def chapter_order():
    if os.path.isfile('Prologue.txt') is True:
        os.rename('Prologue.txt', 'Chapter_0_Prologue')
    elif os.path.isfile('prologue.txt') is True:
        os.rename('prologue.txt', 'Chapter_0_Prologue')
    else:
        return


if __name__ == '__main__':
    book_data()
    make_book()
    chapter_thief()
    chapter_order()


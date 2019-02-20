# Little program to take a light novel from wuxiaworld and well... steal it for me! ;]

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import os
import textwrap
import re

# website = str(input("Which Book would you like to steal to today? https:// "))

# testing with BTTH novel for now
website = "wuxiaworld.com/novel/battle-through-the-heavens"

print("Opening Firefox")
start = webdriver.Firefox()
print("Going to the website")
start.get("https://" + website)
start.stop_client()  # Because wuxiaworld has annoying ads that keep reloading


def chapter_exists(chapter_number):
    try:
        start.find_element_by_partial_link_text("Chapter " + str(chapter_number))
    except NoSuchElementException:
        print("The Book is completed/up to date.")
        return False
    return True


def make_book():
    book_title = start.find_element_by_css_selector('.p-15 > h4:nth-child(1)')

    if os.path.isdir(book_title.text) is False:
        os.makedirs(book_title.text, 0o777)
        print("Making a new directory")
        os.chdir(book_title.text)
        print(os.getcwd())
    else:
        print("Directory :" + book_title.text + ", already exists and will be used")
        os.chdir(book_title.text)
        print(os.getcwd())


def chapter_thief():
    chapter_number = 1
    while chapter_exists(chapter_number) is True:
        chapter_title = start.find_element_by_partial_link_text("Chapter " + str(chapter_number)).text
        chapter_title = re.sub(':|\\?| ', '_', chapter_title)
        print(chapter_title)

        print("Going to chapter " + str(chapter_number))
        start.find_element_by_partial_link_text("Chapter " + str(chapter_number)).click()

        print("Taking a chapter")
        chapter_text = start.find_element_by_class_name("fr-view").text

        print("Copying chapter")
        chapter = open((chapter_title + ".txt"), "w+", encoding="utf-8")
        try:
            chapter.write(textwrap.fill(chapter_text, 100))
        finally:
            chapter.close()
        print("Finished Chapter " + str(chapter_number))

        chapter_number = chapter_number + 1
        start.back()


if __name__ == "__main__":
    make_book()
    chapter_thief()

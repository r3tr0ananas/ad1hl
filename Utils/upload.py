from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple

import undetected_chromedriver as uc
from .config import Config
from .Constant import Constant
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import logging
from time import sleep
import platform
import random
from pathlib import Path
import os

logging.basicConfig()

__all__ = ("AD1HLUP", )

class AD1HLUP:
    def __init__(self) -> None:
        self.config = Config(Path(os.getcwd(), "config.json"))
        self.driver = uc.Chrome(user_data_dir=self.config.user_data)
        self.constant = Constant()
        self.wait_time = random.randint(1,2)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
    
    def __clear(self, field):
        field.click()
        sleep(self.wait_time)
        if platform.platform() == "Darwin":
            field.send_keys(Keys.COMMAND + 'a')
        else:
            field.send_keys(Keys.CONTROL + 'a')
        sleep(self.wait_time)
        field.send_keys(Keys.BACKSPACE)

    def __field(self, field, string):
        self.__clear(field)
        sleep(self.wait_time)

        field.send_keys(string)

    def __get_video_id(self) -> str | None:
        video_id = None
        try:
            video_url_container = self.driver.find_element(By.XPATH, self.constant.VIDEO_URL_CONTAINER)
            video_url_element = video_url_container.find_element(By.XPATH, self.constant.VIDEO_URL_ELEMENT)
            video_id = video_url_element.get_attribute(self.constant.HREF).split('/')[-1]
        except:
            self.logger.warning(self.constant.VIDEO_NOT_FOUND_ERROR)
            pass
        return video_id

    def upload(self, file: str, title: str, description: str) -> Tuple[bool, str | None]:
        self.driver.get(self.constant.YOUTUBE_UPLOAD_URL)

        WebDriverWait(self.driver, timeout=25).until(EC.presence_of_element_located((By.XPATH, self.constant.INPUT_FILE_VIDEO)))

        self.driver.find_element(By.XPATH, self.constant.INPUT_FILE_VIDEO).send_keys(str(file))

        self.logger.debug("Video send: {}".format(str(file)))

        upload_container = None

        while upload_container is None:
            sleep(self.wait_time)
            upload_container = self.driver.find_element(By.XPATH, self.constant.UPLOADING_STATUS_CONTAINER)

        WebDriverWait(self.driver, timeout=25).until(EC.element_to_be_clickable((By.ID, self.constant.TEXTBOX_ID)))

        title_field, description_field = self.driver.find_elements(By.ID, self.constant.TEXTBOX_ID)

        self.__field(title_field, title)
        self.__field(description_field, description)

        self.driver.find_element(By.ID, self.constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {}'.format(self.constant.NEXT_BUTTON))

        sleep(self.wait_time)

        self.driver.find_element(By.ID, self.constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {}'.format(self.constant.NEXT_BUTTON))

        sleep(self.wait_time)

        self.driver.find_element(By.ID, self.constant.NEXT_BUTTON).click()
        self.logger.debug('Clicked {}'.format(self.constant.NEXT_BUTTON))

        video_id = self.__get_video_id()

        last_process = None

        upload_container = self.driver.find_element(By.XPATH, self.constant.UPLOADING_STATUS_CONTAINER)

        done = False

        while done is False:
            uploading_progress = upload_container.text # Wird hochgeladen 91&nbsp;% ... Noch 30 Sekunden

            if not uploading_progress.__contains__("Wird hochgeladen"):
                done = True
                break

            print(uploading_progress)

            prozent = uploading_progress.split(" ")[2]

            if prozent == last_process:
                self.logger.info('Upload: {}%'.format(prozent))

            sleep(self.wait_time * 5)
            try:
                upload_container = self.driver.find_element(By.XPATH, self.constant.UPLOADING_STATUS_CONTAINER)
            except:
                upload_container = None

            last_process = prozent

        done_button = self.driver.find_element(By.ID, self.constant.DONE_BUTTON)

        if done_button.get_attribute('aria-disabled') == 'true':
            error_message = self.driver.find_element(By.XPATH, self.constant.ERROR_CONTAINER).text
            self.logger.error(error_message)
            return (False, None)

        done_button.click()
        self.logger.info(
            "Published the video with video_id = {}".format(video_id))
        sleep(self.wait_time)
        self.driver.quit()
        return (True, video_id)
    
    
from ig_page import IGPage
from google_drive import DriveAPI
from selenium.common.exceptions import NoSuchElementException
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from google_sheets import SheetsAPI


sheets = SheetsAPI()
response = sheets.read_sheet()
sheet_rows = response["values"]
print(sheet_rows)


igpage = IGPage()
igpage.login()

for row in sheet_rows[1:]:
    folder_id = row[1]
    influencer_acc = row[2]
    igpage.get_page(influencer_acc)
    try:
        igpage.download_story(influencer_acc, folder_id)
        igpage.close_story()
    except NoSuchElementException:
        pass
    # except PermissionError:
    #     pass







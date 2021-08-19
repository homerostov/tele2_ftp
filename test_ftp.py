from ftplib import FTP
import pytest
import allure
import time
from pathlib import Path

def get_speed(size, time):
    return int(size / 1024 /time)


ftp = FTP('speedtest.tele2.net')
ftp.login()
# files_list = ftp.nlst()[:-1]
files_list = ('100KB.zip', '10MB.zip', '1KB.zip', '1MB.zip', '20MB.zip', '2MB.zip', '3MB.zip',  '50MB.zip', '512KB.zip', '5MB.zip')

@allure.title('Вход на сервер')
def test_login():
    pytest.ftp = FTP('speedtest.tele2.net')
    allure.attach(pytest.ftp.login(), 'Ответ')

@allure.title('Печать списка в файл')
def test_dir_files_list():
    allure.attach(pytest.ftp.retrlines('LIST'), 'Ответ')

@pytest.mark.parametrize('file_name', files_list)
@allure.title('Загрузка файла {file_name}')
def test_speed_download(file_name):
    start_time = time.time()
    with open(file_name, 'wb') as fp:
         ftp.retrbinary('RETR ' + file_name, fp.write)
    fin_time =  time.time() - start_time
    file_size = int(ftp.sendcmd('SIZE '+ file_name)[4:])
    allure.attach('size = ' + str(int(file_size)/1024) + 'kb\n' +
                  'time = ' + str(round(fin_time,3)) + 'secs',
                  'speed: ' + str(get_speed(file_size, fin_time)) + 'kb/sec')

@pytest.mark.parametrize('file_name', files_list)
@allure.title('Выгрузка файла {file_name}')
def test_speed_upload(file_name):
    pytest.ftp.cwd('upload')
    start_time = time.time()
    with open(file_name, 'rb') as file:
        pytest.ftp.storbinary('STOR ' + file_name, file)
    fin_time =  time.time() - start_time
    file_size = int(Path(file_name).stat().st_size)
    allure.attach('size = ' + str(int(file_size)/1024) + 'kb\n' +
                  'time = ' + str(round(fin_time,3)) + 'secs',
                  'speed: ' + str(get_speed(file_size, fin_time)) + ' kb/sec')
    pytest.ftp.cwd('/')


import io
import re
from collections import Counter
import statistics
import os
import gzip

def read_logs(logs):
    if os.path.splitext(logs)[1] == '.gz':
        with gzip.open(logs) as zip_log:
            with io.TextIOWrapper(zip_log, encoding='utf-8') as unzip_log:
                logs = unzip_log.read()
    else:
        with open(logs, 'r') as file:
            logs = file.read()
    return logs

def main():
    folder = {"LOG": "./IT_logs"}
    #Фильтрация и сортировка
    filter_p = {'URL': r'\"[A-Z]+ ([^\s]+)', 'REQUEST_TIME': r'.* (\d+\.\d+)'}
    name_logs = sorted(os.listdir(folder.get("LOG")))
    log_name = name_logs[-1]
    log_path = f'{folder.get("LOG")}\{log_name}'
    all = 0
    url_clear = re.findall(filter_p['URL'], read_logs(log_path))
    request_time_clear = re.findall(filter_p['REQUEST_TIME'], read_logs(log_path))
    number_of_urls = Counter(url_clear)
    report = []
    if not name_logs:
        return print('LOGS were not found!')
    if not request_time_clear:
        print("REQUEST_TIME were not found!")
        for key, value in number_of_urls.items():
            all += value
        for key, value in number_of_urls.items():
            report.append(f"URL - {key} - {value} - {round((value / all) * 100)}% - !not found!")
        for i in range(len(report)):
            print(report[i])
        print("Can't calculate median without REQUEST_TIME")
    else:
        for key, value in number_of_urls.items():
            all += value
        j = 0
        for key, value in number_of_urls.items():
            if not request_time_clear[j]:
                report.append(f"URL - {key} - {value} - {round((value / all) * 100)}% - not found")
                j += 1
            else:
                report.append(f"URL - {key} - {value} - {round((value / all) * 100)}% - {request_time_clear[j]}")
                j += 1
        for i in range(len(report)):
            print(report[i])
        print('Median - ' + str(statistics.median(map(float, request_time_clear))))

if __name__ == '__main__':
    main()
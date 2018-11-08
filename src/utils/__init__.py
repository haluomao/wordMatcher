from src.zhtools.langconv import *
import csv


def convent_to_simplified(sentence):
    """
    Convert traditional sentence to simplified.
    :param sentence:
    :return:
    """
    return Converter('zh-hans').convert(sentence)


def read_csv(file_path):
    csv_data = csv.reader(open(file_path))
    for row in csv_data:
        # print(row[0])
        pass

if __name__ == '__main__':
    print(convent_to_simplified('憂郁的臺灣烏龜'))

import datetime
import argparse
from dataclasses import dataclass


@dataclass
class Driver:
    Abbreviation: str
    Name: str
    Company: str
    start_time: datetime
    end_time: datetime

    @property
    def result_time(self):
        return self.end_time - self.start_time


def file_process(file_name):
    data_dict = {}
    try:
        with open(file_name, "r") as data_file:
            for item in data_file.readlines():
                item = item.rstrip()
                if item != '':
                    data_dict[item[:3]] = datetime.datetime.strptime(
                        item[3:], '%Y-%m-%d_%H:%M:%S.%f')
    except IOError:
        print(f"There is no file named {file_name}")

    return data_dict


def load_data(data_folder):
    list_of_names = []
    whole_list = []

    start_dict = file_process(data_folder + "/start.log")
    end_dict = file_process(data_folder + "/end.log")

    try:
        with open(data_folder + "/abbreviations.txt", "r") as abbr_file:
            for item in abbr_file.readlines():
                item = item.rstrip()
                list_of_names.append(item.split('_'))
    except IOError:
        print(f"There is no such file")

    for abbreviation, driver_name, company_name in list_of_names:

        driver = Driver(abbreviation, driver_name, company_name,
                        start_dict[abbreviation], end_dict[abbreviation])
        whole_list.append(driver)

    return whole_list


def build_report(whole_list):
    ''' This function return the dictionary with drivers with their driving statistics

        Parameters:
        start_dict, end_dict, list_of_names

        Returns:
        dictionary with drivers statistics

    '''
    fail_list = []
    drivers_list = []

    for driver in whole_list:

        if driver.start_time < driver.end_time:
            drivers_list.append(driver)
        elif driver.start_time > driver.end_time:
            fail_list.append(driver)

    drivers_list.sort(key=lambda x: x.result_time)

    return drivers_list, fail_list


def print_report(data_folder, desc=False):
    ''' This function prints the report with drivers statistics

        Parameters:
        data_folder, desc=False)

        Returns:
        prints the report

    '''

    whole_list = load_data(data_folder)
    drivers_list, fail_list = build_report(whole_list)

    print_list = []
    max_name_chars = 0
    max_comp_chars = 0

    for item in whole_list:
        max_name_chars = max(max_name_chars, len(item.Name))
        max_comp_chars = max(max_comp_chars, len(item.Company))

    for i, item in enumerate(drivers_list, start=1):

        print_string = f"{i:2}.{item.Name:{max_name_chars}} | {item.Company:{max_comp_chars}} | {item.result_time}"

        print_list.append(print_string)

    string_div = "-" * len(print_string)
    print_list.append(string_div)

    if desc:
        print_list = reversed(print_list)
   
    for item in print_list:
        print(item)

    print("possible errors in data:")
    print(string_div)
    for item in fail_list:
        print(
            f"{item.Name:{max_name_chars}} | {item.Company:{max_comp_chars}} | {item.result_time}")


def main(test_list):

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--files",
        help="type folder with files",
        type=str, required=True)

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--asc', action='store_const', const='asc', dest='sort')
    group.add_argument(
        '--desc',
        action='store_const',
        const='desc',
        dest='sort')

    parser.add_argument(
        "--driver",
        help="driver statictics",
        type=str)

    args = parser.parse_args(test_list)

    if args.files and not args.driver:
        print_report(args.files, desc=(args.sort == 'desc'))

    elif args.files and args.driver:
        whole_list = load_data(args.files)
        for item in whole_list:
            if args.driver == item.Name:
                print(
                    f"Abbreviation: {item.Abbreviation}  Name: {item.Name}  Company: {item.Company} \nStart time: {item.start_time}  End time: {item.end_time}")

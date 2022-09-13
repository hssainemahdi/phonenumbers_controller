import csv
import phonenumbers

from phonenumbers.phonenumberutil import NumberParseException


def export_bad_numbers(fields: list, numbers: list):
    with open("./phonenumbers_status.csv", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(fields)
        csv_writer.writerows(numbers)


def get_number_validity(number: str, region=None) -> bool:
    try:
        if isinstance(number, list):
            parsed_number = phonenumbers.parse(number[0], region)
        else:
            parsed_number = phonenumbers.parse(number, region)
    except IndexError as err:
        return False, False
    is_possible = phonenumbers.is_possible_number(parsed_number)
    is_valid = phonenumbers.is_valid_number(parsed_number)
    return is_possible, is_valid


def get_all_numbers():
    all_numbers = []
    with open(
        "./query.20220907.173437.csv", newline="", encoding="utf-8", errors="replace"
    ) as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        for number in csv_reader:
            all_numbers.append(number)
    return all_numbers


def parse_numbers(numbers: list) -> None:
    fields = ["number", "is_possible", "is_valid", "is_bad_formatted/contain unauthorised caracter", "Reason"]
    bad_numbers = []
    bad_formatted_numbers = []
    for number in numbers:
        try:
            if "+" in number:
                is_possible, is_valid = get_number_validity(number, region=None)
            else:
                # Here we consider if phone number is not in format +49649564528
                # then it must be a french number
                is_possible, is_valid = get_number_validity(number, region="FR")
        except NumberParseException as err:
            bad_formatted_numbers.append(number)
            row = [f"{number}", "False", "False", "Yes", f"{err}"]
            bad_numbers.append(row)
        if not is_possible or not is_valid:
            if number:
                row = [f"{number}", f"{is_possible}", f"{is_valid}"]
                bad_numbers.append(row)
    export_bad_numbers(fields, bad_numbers)


if __name__ == "__main__":
    all_numbers = get_all_numbers()
    parse_numbers(all_numbers)

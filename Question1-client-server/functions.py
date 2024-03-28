from datetime import datetime


def is_alpha_string(s):
    for char in s:
        if not char.isalpha() and char != ' ':
            return False
    return True


def is_phone_number(s):
    return all(c.isdigit() or c == '-' for c in s)

# private function to check if a string represents a valid date
def is_valid_date(date_str):
    try:
        if not date_str:
            return True
        datetime.strptime(date_str, '%Y-%m-%d')
        input_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.now().date()
        return input_date <= today
    except ValueError:
        print(date_str)
        return False

# private function to check if a string represents a valid date and if it is greater than a other date
def is_date_greater_or_equal(new_date, earlier_date):
    try:
        if not new_date:
            return True
        after_date = datetime.strptime(new_date, '%Y-%m-%d').date()
        before_date = datetime.strptime(earlier_date, '%Y-%m-%d').date()
        return after_date >= before_date
    except ValueError:
        return False

# This function validates the details the server got from the user
def validate_input_data(first_name,last_name,city,street,number,date_of_birth,telephone,\
                                     mobile_phone,vaccine_dates,vaccine_manufacturers,\
                                     positive_result_date, recovery_date,id="11111111"):
    errors = []
    if not id.isdigit() or len(str(id)) <= 7 or len(str(id)) > 9:
        errors.append('ID must be a number with more than 7 digits and less then 10')

    for field in [first_name,last_name, city, street]:
        if not is_alpha_string(field) or len(field) <= 1:
            errors.append(f'A name or an address must be a sequence of letters (without numbers) that is greater than 1')

    if not number or not number.isdigit() or int(number) == 0:
        errors.append('Number must be a non-zero number')

    if not date_of_birth or not is_valid_date(date_of_birth):
        errors.append('DateOfBirth must be a valid date')

    for field in [telephone, mobile_phone]:
        if not is_phone_number(field):
            errors.append('Telephone and MobilePhone must be a sequence of only digits and \'-\'')

    for vaccine_date in vaccine_dates:
        if vaccine_date and (vaccine_date != '' and not is_date_greater_or_equal(vaccine_date,date_of_birth)):
            errors.append(f'VaccineDate must be NONE or a valid date greater then birth date.')

    for manufacturer in vaccine_manufacturers:
        if manufacturer!='' and manufacturer not in [None, 'Moderna', 'Pfizer', 'AstraZeneca', 'Gamalia']:
            errors.append(f'VaccineManufacturer must be NONE or Moderna, Pfizer, AstraZeneca, or Gamalia')

    if sum(1 for element in vaccine_dates if element == '') != sum(1 for element in vaccine_manufacturers if element == ''):
        errors.append("Each vaccine must include a manufacturer's name")

    if positive_result_date and not is_date_greater_or_equal(positive_result_date,date_of_birth):
        errors.append('PositiveResultDate must be NONE or a valid date greater then birth date.')

    if recovery_date and (not is_date_greater_or_equal(positive_result_date,date_of_birth) or \
            (not positive_result_date or not is_date_greater_or_equal(recovery_date,positive_result_date))):
        errors.append('RecoveryDate must be NONE or a date greater than PositiveResultDate')

    return errors
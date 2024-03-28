from flask import Flask, request, jsonify, send_from_directory, render_template
import sqlite3
from flask_cors import CORS
from functions import validate_input_data


app = Flask(__name__)
CORS(app)

DB_NAME = 'mydatabase.db'
@app.route('/')
def home():
    return render_template('index.html')


# private function to execute SQL queries
def execute_query(query, params=()):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")
    finally:
        conn.close()


# creates a new member with personal and corona details
@app.route('/members', methods=['POST'])
def create_member():
    try:
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()

        #gets the data of the client
        data = request.get_json()
        id = data.get('ID')
        first_name = data.get('FirstName')
        last_name = data.get('LastName')
        city = data.get('City')
        street = data.get('Street')
        number = data.get('Number')
        date_of_birth = data.get('DateOfBirth')
        telephone = data.get('Telephone')
        mobile_phone = data.get('MobilePhone')
        vaccine_dates = data.get('VaccineDates', [])
        vaccine_manufacturers = data.get('VaccineManufacturers', [])
        positive_result_date = data.get('PositiveResultDate')
        recovery_date = data.get('RecoveryDate')

        # checks the validity of the details
        errors = validate_input_data(first_name,last_name,city,street,number,date_of_birth,telephone,\
                                     mobile_phone,vaccine_dates,vaccine_manufacturers,\
                                     positive_result_date, recovery_date,id)
        if len(errors) != 0:
            return jsonify({'errors: ': errors}), 400

        cursor.execute('''INSERT INTO PersonalInformation (ID, FirstName, LastName, City, Street, Number,
                        DateOfBirth, Telephone, MobilePhone)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (id, first_name, last_name, city, street, number,
                       date_of_birth, telephone, mobile_phone))

        # if at least one of the Corona details fields is not empty
        if any(vaccine_dates) or any(vaccine_manufacturers) or positive_result_date or recovery_date:
            cursor.execute('''INSERT INTO CoronaDetails (ID, VaccineDate1, VaccineDate2, VaccineDate3, VaccineDate4,
                                                                  VaccineManufacturer1, VaccineManufacturer2, VaccineManufacturer3,
                                                                  VaccineManufacturer4, PositiveResultDate, RecoveryDate)
                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (id, vaccine_dates[0] if vaccine_dates[0] else None,
                            vaccine_dates[1] if vaccine_dates[1] else None,
                            vaccine_dates[2] if vaccine_dates[2] else None,
                            vaccine_dates[3] if vaccine_dates[3] else None,
                            vaccine_manufacturers[0] if vaccine_manufacturers[0] else None,
                            vaccine_manufacturers[1] if vaccine_manufacturers[1] else None,
                            vaccine_manufacturers[2] if vaccine_manufacturers[2] else None,
                            vaccine_manufacturers[3] if vaccine_manufacturers[3] else None,
                            positive_result_date if positive_result_date else None,
                            recovery_date if recovery_date else None))

        conn.commit()
        return jsonify({'message': 'Member created successfully'}), 201
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


# gets the details of a given member
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT PersonalInformation.*, VaccineDate1, VaccineDate2, VaccineDate3, VaccineDate4,
                                                                  VaccineManufacturer1, VaccineManufacturer2, VaccineManufacturer3,
                                                                  VaccineManufacturer4, PositiveResultDate, RecoveryDate
                          FROM PersonalInformation
                          LEFT JOIN CoronaDetails ON PersonalInformation.ID = CoronaDetails.ID
                          WHERE PersonalInformation.ID = ?''', (id,))

        member_data = cursor.fetchone()

        if member_data:
            #if the data exist, puts it in a dictionary to send a json answer
            member_dict = {
                'ID': member_data[0],
                'FirstName': member_data[1],
                'LastName': member_data[2],
                'City': member_data[3],
                'Street': member_data[4],
                'Number': member_data[5],
                'DateOfBirth': member_data[6],
                'Telephone': member_data[7],
                'MobilePhone': member_data[8],
                'VaccineDate1': member_data[9],
                'VaccineDate2': member_data[10],
                'VaccineDate3': member_data[11],
                'VaccineDate4': member_data[12],
                'VaccineManufacturer1': member_data[13],
                'VaccineManufacturer2': member_data[14],
                'VaccineManufacturer3': member_data[15],
                'VaccineManufacturer4': member_data[16],
                'PositiveResultDate': member_data[17],
                'RecoveryDate': member_data[18]
            }
            return jsonify(member_dict), 200
        else:
            return jsonify({'error': 'Member not found'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


# get the id and name of all members
@app.route('/members', methods=['GET'])
def get_members():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''SELECT ID, FirstName,LastName FROM PersonalInformation''')
    members = cursor.fetchall()
    conn.close()

    members_list = []
    for member in members:
        member_dict = {
            'ID': member[0],
            'FirstName': member[1],
            'LastName': member[2]
        }
        members_list.append(member_dict)

    return jsonify(members_list), 200

# Update a given member's details
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        #geting the details of the client
        data = request.get_json()
        iD = data.get('ID')
        first_name = data.get('FirstName')
        last_name = data.get('LastName')
        city = data.get('City')
        street = data.get('Street')
        number = data.get('Number')
        date_of_birth = data.get('DateOfBirth')
        telephone = data.get('Telephone')
        mobile_phone = data.get('MobilePhone')
        vaccine_dates = data.get('VaccineDates', [])
        vaccine_manufacturers = data.get('VaccineManufacturers', [])
        positive_result_date = data.get('PositiveResultDate')
        recovery_date = data.get('RecoveryDate')

        # Checking if the details are valid
        errors = validate_input_data(first_name, last_name, city, street, number, date_of_birth, telephone, \
                                     mobile_phone, vaccine_dates, vaccine_manufacturers, \
                                     positive_result_date, recovery_date)
        if errors:
            print(errors)
            return jsonify({'errors: ': errors}), 400

        cursor.execute('''UPDATE PersonalInformation
                             SET FirstName = ?, LastName = ?, City = ?, Street = ?, Number = ?,
                                 DateOfBirth = ?, Telephone = ?, MobilePhone = ?
                             WHERE ID = ?''',
                      (first_name, last_name, city, street, number,
                       date_of_birth, telephone, mobile_phone, id))
        conn.commit()

        # if at least one of the Corona details fields is not empty:
        if any(vaccine_dates) or any(vaccine_manufacturers) or positive_result_date or recovery_date:
            cursor.execute('''SELECT ID FROM CoronaDetails WHERE ID = ?''', (id,))
            result = cursor.fetchone()
            # The reason why a check is required here whether the ID already exists when updating the CoronaDetails table is:
            # because when updating the details, the client can update information about the corona,
            # but if so far, no details about the corona have been entered for this member,
            # he does not have a line in the table, so a line needs to be added
            if result:
                cursor.execute('''UPDATE CoronaDetails
                                    SET VaccineDate1=?, VaccineDate2=?, VaccineDate3=?, 
                                    VaccineDate4=?, VaccineManufacturer1=?, VaccineManufacturer2=?, 
                                    VaccineManufacturer3=?, VaccineManufacturer4=?, PositiveResultDate=?, 
                                    RecoveryDate=? 
                                    WHERE ID = ?''',
                                (vaccine_dates[0] if vaccine_dates[0] else None,
                                vaccine_dates[1] if vaccine_dates[1] else None,
                                vaccine_dates[2] if vaccine_dates[2] else None,
                                vaccine_dates[3] if vaccine_dates[3] else None,
                                vaccine_manufacturers[0] if vaccine_manufacturers[0] else None,
                                vaccine_manufacturers[1] if vaccine_manufacturers[1] else None,
                                vaccine_manufacturers[2] if vaccine_manufacturers[2] else None,
                                vaccine_manufacturers[3] if vaccine_manufacturers[3] else None,
                                positive_result_date if positive_result_date else None,
                                recovery_date if recovery_date else None, id))

                conn.commit()
            else:
                cursor.execute('''INSERT INTO CoronaDetails (ID, VaccineDate1, VaccineDate2, VaccineDate3, VaccineDate4,
                                                                                  VaccineManufacturer1, VaccineManufacturer2, VaccineManufacturer3,
                                                                                  VaccineManufacturer4, PositiveResultDate, RecoveryDate)
                                                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                               (id, vaccine_dates[0] if vaccine_dates[0] else None,
                                vaccine_dates[1] if vaccine_dates[1] else None,
                                vaccine_dates[2] if vaccine_dates[2] else None,
                                vaccine_dates[3] if vaccine_dates[3] else None,
                                vaccine_manufacturers[0] if vaccine_manufacturers[0] else None,
                                vaccine_manufacturers[1] if vaccine_manufacturers[1] else None,
                                vaccine_manufacturers[2] if vaccine_manufacturers[2] else None,
                                vaccine_manufacturers[3] if vaccine_manufacturers[3] else None,
                                positive_result_date if positive_result_date else None,
                                recovery_date if recovery_date else None))

                conn.commit()

        return jsonify({'message': 'Member updated successfully'}), 200
    except Exception as e:
        print(f'error: {str(e)}')
        return jsonify({'error': str(e)}), 500


# Delete a given member
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()

        # checking for existing before we delete
        cursor.execute('''SELECT ID FROM PersonalInformation WHERE ID = ?''', (id,))
        result = cursor.fetchone()

        if not result:
            return jsonify({'error': 'Member not found'}), 404

        cursor.execute('''DELETE FROM PersonalInformation WHERE ID = ?''', (id,))
        conn.commit()
        return jsonify({'message': 'Member deleted successfully'}), 200

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
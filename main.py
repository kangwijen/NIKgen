import json
import random

def generate_random():
    '''
        Generate random NIKs
    '''
    with open('data/province.json', 'r') as f:
        provinces = json.load(f)

    with open('data/regency.json', 'r') as f:
        kabupaten = json.load(f)

    with open('data/subdistrict.json', 'r') as f:
        subdistricts = json.load(f)

    print("Generate Random NIKs")
    print("Enter the number of NIKs to generate")
    n = input("Number of NIKs: ")

    while not n.isdigit():
        print("Invalid input. Please enter a valid number.")
        n = input("Number of NIKs: ")

    n = int(n)

    def search_regency(province_code):
        regency_group = [regency for regency_group in kabupaten for regency in regency_group if regency['kode_dagri'].startswith(province_code)]
        return regency_group[random.randint(0, len(regency_group) - 1)]

    def search_subdistrict(province_code, regency_code):
        subdistrict_group = [subdistrict for subdistrict_group in subdistricts for subdistrict in subdistrict_group if subdistrict['kode_dagri'].startswith(province_code + "." + regency_code)]
        return subdistrict_group[random.randint(0, len(subdistrict_group) - 1)]

    for _ in range(n):
        province = provinces[random.randint(0, len(provinces) - 1)]
        regency = search_regency(province['kode_dagri'])
        subdistrict = search_subdistrict(province['kode_dagri'], regency['kode_dagri'][-2:])
        birth_date = str(random.randint(1, 31)).zfill(2)
        birth_month = str(random.randint(1, 12)).zfill(2)
        birth_year = str(random.randint(0, 99)).zfill(2)
        gender = random.choice(['M', 'F'])

        if gender == 'F':
            birth_date = str(int(birth_date) + 40).zfill(2)

        special_code = str(random.randint(0, 9999)).zfill(4)

        nik = province['kode_dagri'] + regency['kode_dagri'][-2:] + subdistrict['kode_dagri'][-2:] + birth_date + birth_month + birth_year + special_code
        print("Province:", province['nama_dagri'])
        print("Regency:", regency['nama_dagri'])
        print("Subdistrict:", subdistrict['nama_dagri'])
        print("Birth Date:", birth_date if gender == 'M' else str(int(birth_date) - 40).zfill(2))
        print("Birth Month:", birth_month)
        print("Birth Year:", birth_year)
        print("Gender:", gender)
        print("NIK: " + nik)
    
def generate_specific():
    '''
        Generate a specific NIK
    '''
    province_code = ""
    regency_code = ""
    subdistrict_code = ""
    birth_date = ""
    birth_month = ""
    birth_year = ""
    gender = ""
    special_code = ""

    print("Enter the following details to generate a specific NIK")

    with open('data/province.json', 'r') as f:
        provinces = json.load(f)

    def search_province(input_str):
        if input_str.isdigit():
            if input_str in [province['kode_dagri'] for province in provinces]:
                return [province for province in provinces if province['kode_dagri'] == input_str][0]
        else: 
            input_str_lower = input_str.lower() 
            matches = [province for province in provinces if input_str_lower in province['nama_dagri'].lower()]
            if matches:
                return matches
        return None

    user_input = input("Enter Province Code or Name: ")
    provinces_found = search_province(user_input)

    while provinces_found is None:
        print("No matching province found. Please try again.")
        user_input = input("Enter Province Code or Name: ")
        provinces_found = search_province(user_input)

    if isinstance(provinces_found, list):
        print("Multiple provinces match the input:")
        for index, province in enumerate(provinces_found, start=1):
            print(f"{index}. Code: {province['kode_dagri']}, Name: {province['nama_dagri']}")
        choice = input("Please enter the number corresponding to the correct province: ")
        while not choice.isdigit() or int(choice) not in range(1, len(provinces_found) + 1):
            print("Invalid input. Please enter a valid number.")
            choice = input("Please enter the number corresponding to the correct province: ")
        selected_province = provinces_found[int(choice) - 1]
        print("Province:", selected_province['nama_dagri'])
    else:
        selected_province = provinces_found
        print("Province:", provinces_found['nama_dagri'])

    with open('data/regency.json', 'r') as f:
        kabupaten = json.load(f)

    def search_regency(province_code, input_str):
        if input_str.isdigit():
            search_code = province_code + "." + input_str
            matches = [regency for regency_group in kabupaten for regency in regency_group if regency['kode_dagri'].startswith(search_code)]
            if matches:
                return matches
        else:  
            input_str_lower = input_str.lower() 
            matches = [regency for regency_group in kabupaten for regency in regency_group if input_str_lower in regency['nama_dagri'].lower() and regency['kode_dagri'].startswith(province_code)]
            if matches:
                return matches
        return None

    user_input = input("Enter Regency Code or Name: ")
    province_code = selected_province['kode_dagri']
    regencies_found = search_regency(province_code, user_input)

    while regencies_found is None:
        print("No matching regency found. Please try again.")
        user_input = input("Enter Regency Code or Name: ")
        regencies_found = search_regency(province_code, user_input)

    if isinstance(regencies_found, list):
        print("Multiple regencies match the input:")
        for index, regency in enumerate(regencies_found, start=1):
            print(f"{index}. Code: {regency['kode_dagri'][-2:]}, Name: {regency['nama_dagri']}")
        choice = input("Please enter the number corresponding to the correct regency: ")
        while not choice.isdigit() or int(choice) not in range(1, len(regencies_found) + 1):
            print("Invalid input. Please enter a valid number.")
            choice = input("Please enter the number corresponding to the correct regency: ")
        selected_regency = regencies_found[int(choice) - 1]
        print("Regency:", selected_regency['nama_dagri'])
    else:
        selected_regency = regencies_found
        print("Regency:", selected_regency['nama_dagri'])

    with open('data/subdistrict.json', 'r') as f:
        subdistricts = json.load(f)

    def search_subdistrict(province_code, regency_code, input_str):
        if input_str.isdigit():
            search_code = province_code + "." + regency_code + "." + input_str
            matches = [subdistrict for subdistrict_group in subdistricts for subdistrict in subdistrict_group if subdistrict['kode_dagri'].startswith(search_code)]
            if matches:
                return matches
        else:  
            input_str_lower = input_str.lower() 
            matches = [subdistrict for subdistrict_group in subdistricts for subdistrict in subdistrict_group if input_str_lower in subdistrict['nama_dagri'].lower() and subdistrict['kode_dagri'].startswith(province_code + "." + regency_code)]
            if matches:
                return matches
        return None

    user_input = input("Enter Subdistrict Code or Name: ")
    province_code = selected_province['kode_dagri']
    regency_code = selected_regency['kode_dagri'][-2:]
    subdistricts_found = search_subdistrict(province_code, regency_code, user_input)

    while subdistricts_found is None:
        print("No matching subdistrict found. Please try again.")
        user_input = input("Enter Subdistrict Code or Name: ")
        subdistricts_found = search_subdistrict(province_code, regency_code, user_input)

    if isinstance(subdistricts_found, list):
        print("Multiple subdistricts match the input:")
        for index, subdistrict in enumerate(subdistricts_found, start=1):
            print(f"{index}. Code: {subdistrict['kode_dagri'][-2:]}, Name: {subdistrict['nama_dagri']}")
        choice = input("Please enter the number corresponding to the correct subdistrict: ")
        while not choice.isdigit() or int(choice) not in range(1, len(subdistricts_found) + 1):
            print("Invalid input. Please enter a valid number.")
            choice = input("Please enter the number corresponding to the correct subdistrict: ")
        selected_subdistrict = subdistricts_found[int(choice) - 1]
        print("Subdistrict:", selected_subdistrict['nama_dagri'])
    else:
        selected_subdistrict = subdistricts_found
        print("Subdistrict:", selected_subdistrict['nama_dagri'])

    subdistrict_code = selected_subdistrict['kode_dagri'][-2:]

    while True:
        birth_date = input("Birth Date: ")
        if birth_date.isdigit():
            birth_date = int(birth_date)
            if 1 <= birth_date <= 31:
                birth_date = str(birth_date).zfill(2)
                break
            else:
                print("Invalid input. Birth date must be between 1 and 31.")
        else:
            print("Invalid input. Please enter a valid number.")

    while True:
        birth_month = input("Birth Month: ")
        if birth_month.isdigit():
            birth_month = int(birth_month)
            if 1 <= birth_month <= 12:
                birth_month = str(birth_month).zfill(2)
                break
            else:
                print("Invalid input. Birth month must be between 1 and 12.")
        else:
            print("Invalid input. Please enter a valid number.")

    while True:
        birth_year = input("Birth Year: ")
        if birth_year.isdigit():
            birth_year = int(birth_year)
            if len(str(birth_year)) == 4:
                birth_year = str(birth_year)[-2:]

            if 0 <= int(birth_year) <= 99:
                birth_year = str(birth_year).zfill(2)
                break
            else:
                print("Invalid input. Birth year must be between 0 and 99.")
        else:
            print("Invalid input. Please enter a valid number.")

    while True:
        gender = input("Gender (Male/Female or M/F): ")
        if gender.lower() in ['male', 'm', 'female', 'f']:
            if gender.lower() in ['female', 'f']:
                birth_date = str(int(birth_date) + 40).zfill(2)
            break
        else:
            print("Invalid input. Please enter Male/Female or M/F.")
    
    while True:
        special_code = input("Special Code (4 digits): ")
        if special_code.isdigit() and len(special_code) == 4:
            break
        else:
            print("Invalid input. Special code must be 4 digits.")

    nik = province_code + regency_code + subdistrict_code + birth_date + birth_month + birth_year + special_code
    print("NIK: " + nik + "\n")


def main():
    while True:
        print("Welcome to NIK Generator")
        print("1. Generate Specific NIK")
        print("2. Generate Random NIK")
        print("Type 'exit' to exit the program")
        choice = input("Choose: ")

        if choice == "1":
            generate_specific()
        elif choice == "2":
            generate_random()
        elif choice == "exit":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
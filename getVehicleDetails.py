
def get_vehicle_type(text):
    v_type = None

    # if text is a string
    if text.isalpha():
        print(text)
        text = text.upper()
        to_array = list(text)

        # cars
        print(to_array)
        if to_array[0] == 'C' or to_array[0] == 'K':
            v_type = 'Car'
            return v_type
        # Bike
        elif to_array[0] == 'M' or to_array[0] == 'T' or to_array[0] == 'U' or to_array[0] == 'V' or to_array[0] == 'W' or to_array[0] == 'X' or to_array[0] == 'B':
            v_type = 'Bike'
            return v_type
        # Bus
        elif to_array[0] == 'N' or to_array[0] == 'J':
            v_type = 'Bus'
            return v_type
        # Lorry
        elif to_array[0] == 'L' or to_array[0] == 'D':
            v_type = 'Lorry'
            return v_type
        # Threewheel
        elif to_array[0] == 'Q' or to_array[0] == 'Y' or to_array[0] == 'A':
            v_type = 'Threewheel'
            return v_type
        # Dual purpose vehicle
        elif to_array[0] == 'P':
            v_type = 'Dual Purpose Vehicle'
            return v_type
        # Tractor
        elif to_array[0] == 'R':
            v_type = 'Tractor'
            return v_type
        # Land master
        elif to_array[0] == 'S':
            v_type = 'Land master'
            return v_type
        else:
            v_type = 'Vehicle class cannot be detected'
            return v_type


# return province on call
def get_province(text):
    text = text.upper()
    provinces = {'SP': 'Southern Province',
                 'WP': 'Western Province',
                 'EP': 'Eastern Province',
                 'NP': 'Nothern Province',
                 'NW': 'North Western Province',
                 'SG': 'Sabaragamuwa Province',
                 'CP': 'Central Province',
                 'NC': 'North Central Province',
                 'UW': 'Uwa Province',
                 }

    if text in provinces.keys():
        return provinces[text]

    else:
        return 'Province cannot detected'


def vehicle_related(text):
    to_array = list(text)
    print(to_array)

    if to_array[0] == 'ය':
        return 'Army'
    elif to_array[0] == 'න':
        return 'Navy'
    elif to_array[0] == 'ග':
        return 'Air Force'
    elif to_array[0].isdigit():
        return categorized_by_number(text.split('SRI')[0])
    else:
        return 'Cannot detected'

# return vehicle category using number


def categorized_by_number(text):
    num = int(text)

    if (num > 1 and 21 > num) or (num > 300 and 303 > num):
        return 'Petrol Vehilce'
    elif num == 20:
        return 'Petrol Van'
    elif (num > 21 and 30 > num) or (num > 60 and 63 > num) or (num > 40 and 48 > num) or (num > 67 and 68 > num) or (num > 226 and 227 > num):
        return 'Heavy Diesel Vehicle'
    elif (num > 31 and 32 > num) or (num > 64 and 65 > num) or (num > 50 and 59 > num) or (num > 250 and 254 > num):
        return 'Light Diesel Vehicle'
    elif(num > 80 and 160 > num):
        return 'Motor Bike'
    elif(num > 200 and 207 > num):
        return 'Threwheel'
    elif(num > 60 and 63 > num):
        return 'Diesel Bus'
    elif(num > 67 and 83 > num) or (num > 40 and 48 > num):
        return 'Diesel Lorry'
    else:
        return 'Cannot detected'


def extract_text_eng_n_num(text):
    # text = '30-2234'
    text = text.replace(' ', '')
    text = text.replace('-', '')
    text = text.replace('+', '')

    pro_code = None
    v_model = None
    if text[0].isalpha():
        if len(text) == 9:
            pro_code = text[:2]
            v_model = text[2:5]

        if len(text) == 8:
            pro_code = text[:2]
            v_model = text[2:4]

    else:
        text = text.replace('-', '')
        text = text.replace(' ', '')

        if len(text) == 7:

            v_model = text[0:3]

        if len(text) == 6:

            v_model = text[0:2]

    return pro_code, v_model


def extract_text_si(text):

    text = text.replace(' ', '')
    text = text.replace('-', '')
    text = text.replace('+', '')

    number_plate = None
    v_model = None
    print(text)
    if text[0].isdigit():
        if len(text) == 8:
            v_model = text[:3]
            number_plate = text[:3] + ' SRI ' + text[4:]
        if len(text) == 7:
            v_model = text[:2]
            number_plate = text[:2] + ' SRI ' + text[3:]
        if len(text) == 6:
            v_model = text[:1]
            number_plate = text[:1] + ' SRI ' + text[2:]
    else:
        number_plate = text

    return number_plate, v_model

import regex 
import sys

# Normalization dictionary
Normalization_dict = {"inch": (2.54, "centimeter"),
    "foot": (0.3048, "meter"),
    "mile": (1.609344, "kilometer"),
    "ounce": (28.349523125, "gram"),
    "pound": (0.45359237, "kilogram"),
    "square foot": (0.092903, "square meter"),
    "square mile": (2.58999, "square kilometer"),
    "cup": (0.236588, "liter"),
    "quart": (0.946353, "liter"),
    "gallon": (3.785411784, "liter"),

    # default values (to be overwritten in initialization):
    "EUR": (1.137, "USD"),  # Euro 
    "CNY": (0.137, "USD"),  # Chinese yuan
    "GBP": (1.327, "USD")}  # British pound sterling

# Abbreviations
Abbrev_dict = {"USD": "$", "EUR": "€", "CNY": "¥", "GBP": "£", 
    "foot": "ft", "square foot": "sq ft",
    "square mile": "sq mi",
    "kilogram": "kg",
    "square meter": "m²", "square kilometer": "km²"}

Currency_symbol_to_abbrev = {
    '$': 'USD',
    "€": 'EUR',
    "¥": "CNY",
    "£": "GBP"
}

# Irregular plurals
Irregular_dict = {"foot": "feet", 
                  "square foot": "square feet"}
# Currency codes
Currency_dict = {"USD", "EUR", "CNY", "GBP"}

# Currency symbols (they precede the quantity)
Currency_symbols = {"$", "€", "¥", "£"}

def int_or_float(num: int | float | str) -> int | float | None:
    """converts strings to int or float as appropriate"""
    if isinstance(num, (int, float)):
        return num
    elif regex.match(r'-?\d+$', num):
        return int(num)
    elif regex.match(r'-?\d+\.\d+$', num):
        return float(num)
    else:
        return None

#Create Class QuantNorm 
class QuantNorm():
    def __init__(self, number, unit,currency_update={}):
        number = int_or_float(number)
        if number is not None:
            self.og_number = number
            self.og_unit = unit
        if currency_update:
            for currency,value in currency_update.items():
                Normalization_dict[currency] = value

    def __str__(self):
        return self.normalize_quant_s()
    
    def round(self,number):
        if isinstance(number, float):
            number = round(number,2)
            return number
        else:
            return number
    
    #If the input unit is plural then convert it to singular form
    def singular(self, unit):
        unit = unit.lower()
        #if the unit is currency then no conversion is needed
        if unit.upper() in Currency_dict:
            return unit.upper()
        #if unit is irregular plural 
        if unit in Irregular_dict.values():
            for singular, plural in Irregular_dict.items():
                if unit == plural:
                    return singular
        # If unit ends with 'es', then strip the 'es' and check if it's in the dictionary
        elif unit.endswith('es'):
            singlular_unit = unit[:-2]
            if singlular_unit in Normalization_dict:
                return singlular_unit
        
        #if unit ends with just 's', then strip the 's' and return if it's in the dictionary
        elif unit.endswith('s'):
            singlular_unit = unit[:-1]
            if singlular_unit in Normalization_dict:
                return singlular_unit
            
        else:
            return unit

    #Convert a unit from singular form into the plural form 
    def plural(self,unit):
        unit = unit.lower()
        #if the unit is currency then no conversion is needed
        if unit.upper() in Currency_dict or unit.upper() in Currency_symbols:
            return unit.upper()
        
        #Check if the unit has an irregular spelling, if so then return the plural version
        if unit in Irregular_dict:
            for singular,plural in Irregular_dict.items():
                if unit == singular:
                    return plural
        
        #If the unit ends in [sh, ch, s, x] then add 'es; to the end to make it plural
        elif unit[-2:] in ['sh','ch'] or unit[-1] in ['s','x']:
            plural = unit + 'es'
            return plural
        
        #If none of the above then add 's' to create the plural
        else:
            plural = unit + 's'
            return plural

    def normalize_quant(self):
        singular_unit = self.singular(self.og_unit)

        if singular_unit in Normalization_dict:
            factor, new_unit_singular = Normalization_dict[singular_unit]
            converted_number = self.round(factor * self.og_number)     
            return (converted_number,new_unit_singular)
        
        else:
            return (self.og_number,singular_unit)
    
    def normalize_quant_s(self):
        converted_value, unit_singular = self.normalize_quant()

        #If the unit does not = 1, then use the plural form of the unit
        if converted_value != 1:
            unit_output = self.plural(unit_singular)

            #Return the currency symbol followed by the number value
            if unit_singular in Currency_dict:
                return f'{Abbrev_dict[unit_singular]} {converted_value}'
            
            return f'{converted_value} {unit_output}'
        else:
            return f'{converted_value} {unit_singular}'

#Only run this if this file is run directly and not imported
if __name__ == "__main__":
    #Initialize lists and arguments
    arguments = sys.argv[1:]
    #Check length of arguments and  
    if len(arguments) == 2:
        number = arguments[0]
        unit = arguments[1]
    elif len(arguments) == 3:
        number = arguments[0]
        unit = f'{arguments[1]} {arguments[2]}'

    conversion = QuantNorm(number,unit,currency_update={})
    print(conversion)
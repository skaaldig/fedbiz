import re


def remove_special(text):
    return re.sub('[^A-Za-z0-9]+', '_', text).strip('_').lower()


def format_ja_codes(code):
    ja_code = re.findall(r'[^-]*-[^-]', str(code))
    return re.sub('[^A-Za-z0-9]+', '_', str(ja_code)).strip('_').lower()


def format_class_codes(code):
    class_code = re.findall(r'(\d+)', str(code))
    if not class_code:
        return re.findall(r'[A-Z]{1,2}\W', str(code))[0].strip(' ')
    return class_code[0]


def format_naics_code(code):
    naics_code = re.findall(r'\d{6}', str(code))
    if not naics_code:
        return re.findall(r'\d{3}', str(code))[0]
    return naics_code[0]


def format_fair_codes(code):
    code = re.sub('-+', ' ', str(code))
    class_code = re.findall(r'^((?:\S+\s+){2}\S+).*', str(code))
    if class_code:
        return re.sub('[^A-Za-z0-9]+', '_', str(class_code)).strip('_').lower()

    else:
        return remove_special(code)

import re

regex = re.compile(r'(.+):(.+)')
regex_composer_name = re.compile(r'(.+?)\(')
composer_key = 'Composer'
composition_key = 'Composition Year'
year_regex = re.compile(r'.*([0-9]{4}).*')
century_regex = re.compile(r'.*([0-9]{2})th.*')



f = open('scorelib.txt', 'r')
data = {}
composer_pieces = {}
century_pieces = {}
for line in f:
    if line.strip() is "":
        data = {}
        continue
    match = regex.match(line)

    if not match:
        continue
    key = match.group(1).strip()
    value = match.group(2).strip()


    if key == composer_key and value:
        match_name = regex_composer_name.match(value)
        if match_name:
            value = match_name.group(1).strip()
        if not composer_pieces.get(value):
            composer_pieces[value] = 1
        else:
            composer_pieces[value] += 1
    elif key == composition_key and value:
        century = None
        year_match = year_regex.match(value)
        if year_match:
            century = year_match.group(1)
            century = int(century[:2]) + 1
        else:
            century_match = century_regex.match(value)
            if century_match:
                century = century_match.group(1)

        if century:
            if not century_pieces.get(str(century)):
                century_pieces[str(century)] = 1
            else:
                century_pieces[str(century)] += 1

    data[key] = value

sorted_composer_pieces = sorted(composer_pieces,
                                key=composer_pieces.get,
                                reverse=True)
sorted_century_pieces = sorted(century_pieces,
                               key=century_pieces.get,
                               reverse=True)

for sorted_c_p in sorted_composer_pieces[:5]:
    print("{0}: {1}".format(sorted_c_p, composer_pieces[sorted_c_p]))
for sorted_c_p in sorted_century_pieces[:5]:
    print("{0}th Century: {1}".format(sorted_c_p, century_pieces[sorted_c_p]))



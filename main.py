import csv
import re


def beauty_phone(persona):
    pattern = r"(\+7|8)?\s*\(?(\d{3})\)?(-|\s)*(\d{3})(-|\s)*(\d{2})(-|\s)*(\d{2})"
    pattern_c = re.compile(pattern)
    persona[5] = pattern_c.sub(r"+7(\2)\4-\6-\8", persona[5])
    if len(persona[5]) > 16:
        pattern = r"(\+7\(\d{3}\)\d{3}-\d{2}-\d{2})\s*\(?(\w*.)\s*(\d{4})\)?"
        pattern_c = re.compile(pattern)
        persona[5] = pattern_c.sub(r"\1 \2\3", persona[5])


def beauty_name(persona):
    stic_persona = persona[0] + ' ' + persona[1] + ' ' + persona[2]
    stic_persona = re.sub(' +', ' ', stic_persona).rstrip().lstrip()
    stic_persona = stic_persona.split(' ')
    for i in range(0, 3):
        if i < len(stic_persona):
            persona[i] = stic_persona[i]


def make_good(contacts_list):
    for idx, persona in enumerate(contacts_list):
        beauty_name(persona)
        beauty_phone(persona)
        contacts_list[idx] = persona


def remove_dub(contacts_list):
    contacts_list_res = []
    for persona in contacts_list:
        if len(contacts_list_res) < 1:
            contacts_list_res.append(persona)
        else:
            match_flag = 0
            for persona_res in contacts_list_res:
                if persona_res[0] == persona[0] and persona_res[1] == persona[1]:
                    match_flag = 1
                    for i in range(2, 7):
                        if persona_res[i] != persona[i]:
                            persona_res[i] = persona_res[i] + persona[i]
            if match_flag == 0:
                contacts_list_res.append(persona)
    return contacts_list_res


with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

make_good(contacts_list)
contacts_list_res = remove_dub(contacts_list)

with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list_res)

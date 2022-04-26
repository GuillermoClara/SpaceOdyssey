
def parse_settings():
    """
    Parses data from file into settings dictionary
    """
    for line in settings_file.readlines():
        splitted = line.split(':')
        setting = splitted[0].strip()
        value = splitted[1].strip()
        settings_dict.update([(setting, value)])


def parse_language():
    """
    Reads translations from current selected language
    """
    lang_file = open('lang/'+settings_dict.get('language').lower()+'.txt', 'r')
    language_dict.clear()
    for sentence in lang_file.readlines():
        splitted = sentence.split(':')
        key = splitted[0].strip()
        value = splitted[1].strip()
        language_dict.update([(key, value)])


def parse_scores():
    """
    Loads nonvolatile user data into a dictionary
    """
    scores_file = open('assets/player/data.txt', 'r')
    scores_dict.clear()
    for line in scores_file.readlines():
        splitted = line.split(':')
        key = splitted[0].strip()
        value = int(splitted[1].strip())
        scores_dict.update([(key, value)])


def save_scores():
    """
    Saves player scores into file system
    """
    file = open('assets/player/data.txt', 'w')
    for key, value in scores_dict.items():
        file.write(key+': '+str(value)+'\n')
    file.close()


def save_settings():
    """
    Saves settings from RAM (dictionary) into file system
    """
    file = open('assets/player/settings.txt', 'w')
    for key, value in settings_dict.items():
        file.write(key+': '+value+'\n')
    file.close()


settings_file = open('assets/player/settings.txt', 'r')
settings_dict = dict()
language_dict = dict()
scores_dict = dict()





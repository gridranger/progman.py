from enum import Enum


class Tags(Enum):
    ACCESSORIES = "Accessories"
    CREATIVITY = "Creativity"
    DEVELOPMENT = "Development"
    GAMES = "Games"
    HIDDEN = "Hidden"
    INTERNET = "Internet"
    MAIN = "Main"
    MULTIMEDIA = "Multimedia"
    NEW = "New"
    OFFICE = "Office"
    MICROSOFT_SOLUTION_SERIES = "Microsoft Solution Series"
    # if you know what's this above then you were around the early nineties ;)


HIDDEN_TAGS = [Tags.HIDDEN.value, Tags.NEW.value]

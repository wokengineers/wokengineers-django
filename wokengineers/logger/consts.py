FILTER_DEFAULT_DICT = {"user_id": "user_id",
                       "ip": "META,REMOTE_ADDR",
                    "user_name": "user_name", "role": "role"}

####### FORMATTER COLOURS #######

GREY = '\x1b[38;21m'
BLUE = '\x1b[38;5;39m'
YELLOW = '\x1b[38;5;226m'
RED = '\x1b[38;5;196m'
BOLD_RED = '\x1b[31;1m'
RESET = '\x1b[0m'

####### FORMATTER COLOURS #######


####### FORMATTER DEFAULT FORMAT #######
#levelname, ip, user, user_id, user_role, timestamp, filename , funcName, lineno, message
FMT = "%(log_color)s%(levelname)s^%(ip)s^%(log_color)s%(user_id)s^%(user_name)s^%(role)s^%(white)s%(asctime)s.%(msecs)03d^%(red)s%(filename)s^%(red)s%(funcName)s^%(red)s%(lineno)s^%(blue)s%(message)s"

####### FORMATTER DEFAULT FORMAT #######

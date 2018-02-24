from enum import Enum

class Command(Enum):
    REGSTER = "!開園"
    BALANCE = "!もやたす"
    DEPOSIT = "!種まき"
    WITHDRAW = "!収穫"
    TIP = "!出荷"
    RAIN = "!水やり"
    DONATE = "!寄付"
    HELP = "!ヘルプ"

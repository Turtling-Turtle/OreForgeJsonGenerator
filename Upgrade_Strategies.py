#@author Nathan Ulmen
from Helper_Functions import prompt_for_int, prompt_for_vtm, prompt_for_float


class Strategy:
    def __init__(self, name, associated_value):
        self.name = name
        self.associated_value = associated_value



AddUPG = Strategy('AddUPG', 0)
MultiplyUPG = Strategy('MultiplyUPG', 1)
SubtractUPG = Strategy('SubtractUPG', 2)

BundledUPG = Strategy('BundledUPG', 3)
ConditionalUPG = Strategy('ConditionalUPG', 4)
InfluencedUPG = Strategy('InfluencedUPG', 5)

ResetterUPG = Strategy('ResetterUPG', 6)

#These will require oreStrategy creation to be implemented:
ApplyEffectUPG = Strategy('ApplyEffect', 7)
TargetedCleanser = Strategy('TargetedCleanser', 8)


UPGS = [AddUPG, MultiplyUPG, SubtractUPG, BundledUPG, ConditionalUPG, InfluencedUPG, ResetterUPG, ApplyEffectUPG]
def prompt_for_UPG_Type():
    while True:
        print()
        for upg in UPGS:
            print(upg.associated_value, upg.name)
        user_input = prompt_for_int("What type of Upgrade would you like: ")
        for upg in UPGS:
            if user_input == upg.associated_value:
                #Go into custom logic for each type instead of returning
                if upg.name in [AddUPG.name, MultiplyUPG.name, SubtractUPG.name]:
                    create_basic_UPG()
                return upg.name
        print(user_input + " is not a valid Upgrade")

def create_basic_UPG():
    modifier = prompt_for_float("Enter the modifier of the effect: ")
    prompt_for_vtm()
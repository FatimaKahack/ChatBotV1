# CS 421: Natural Language Processing
# University of Illinois at Chicago
# Fall 2020
# Chatbot Project - Natural Language Understanding
#
# Do not rename/delete any functions or global variables provided in this template and write your solution
# in the specified sections. Use the main function to test your code when running it from a terminal.
# Avoid writing that code in the global scope; however, you should write additional functions/classes
# as needed in the global scope. These templates may also contain important information and/or examples
# in comments so please read them carefully.
# =========================================================================================================

# Import any necessary libraries here, but check with the course staff before requiring any external
# libraries.

import re
import spacy
import random
from collections import defaultdict

dst = defaultdict(list)

# nlu(input): Interprets a natural language input and identifies relevant slots and their values
# Input: A string of text.
# Returns: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is most
#          appropriate for the corresponding slot.  If no slot values are extracted, the function should
#          return an empty list.
def nlu(input=""):

    slots_and_values = []
    his_list = dst["state_history"]
    size = len(his_list)
    input = input.lower()                                        #----> convert input to lower_case to easily process input
    if size == 0:                                                #----> beginning, the user has just started chatting with chatbot
        slots_and_values = process_greeting(input)
    else:
        next_state = dialogue_policy(dst)[0]
        if next_state == "plastic_type":                         #----> user answered the type of plastic
            slots_and_values = process_plastic_type(input)
        elif next_state == "clarification":                      #----> user just confirmed if chatbot got material correct 
            slots_and_values = process_clarification(input)  
        elif next_state == "blue_bin_confirm":                   #----> user confirmed to question: Do you have a blue bin?
            slots_and_values = process_bluebin_organic_reset(input, "bluebin")
        elif next_state == "backyard_confirm":                   #----> user confirmed to question: Would you like to learn how to compost
            slots_and_values = process_bluebin_organic_reset(input, "organic")
        elif next_state == "reset":                              #----> user answered whether they want to reset
            slots_and_values = process_bluebin_organic_reset(input, "reset")
        elif next_state == "material":                           #----> user has confirmed that they want to reset
            slots_and_values = process_greeting(input)
        else:                                                    #----> error handling: recyling material not found
            slots_and_values.append("Error")
    return slots_and_values

#process_plastic_type(): process the input for the plastic type the user has provided 
#returns the list of values that the global dst must be updated with 
def process_plastic_type(input=""):
    return_list=[]
    plastic_1 = re.compile(r"\b(plastic) ?[123457]\b")
    plastic_2 = re.compile(r"\b(styrofoam)\b")
    plastic_3 = re.compile(r"\b(non-?styrofoam)|(polystrene)\b")
    plastic_4 = re.compile(r"\b(film)|(bag)|(wrap)\b")
    plastic_5 = re.compile(r"\b(toy(s)?)\b")
    if re.search(plastic_1, input):
        return_list.append(("material","plastic"))
        return_list.append(("plastic_type","plastic 1-5 & 7"))
        return_list.append(("state_history",["greeting","material","plastic_type"]))
    elif re.search(plastic_2, input):
        return_list.append(("material","plastic"))
        return_list.append(("plastic_type","styrofoam"))
        return_list.append(("state_history",["greeting","material","plastic_type"]))
    elif re.search(plastic_3, input):
        return_list.append(("material","plastic"))
        return_list.append(("plastic_type","nonstyrofoam"))
        return_list.append(("state_history",["greeting","material","plastic_type"]))
    elif re.search(plastic_4, input):
        return_list.append(("material","plastic"))
        return_list.append(("plastic_type","film"))
        return_list.append(("state_history",["greeting","material","plastic_type"]))
    elif re.search(plastic_5, input):
        return_list.append(("material","plastic toys"))
        return_list.append(("state_history",["greeting","material"]))
    return return_list

# deep_copy(): makes a deep cody of the state_history in dst
#returns the deep copy list
def deep_copy():
    copy_list=[]
    for item in dst["state_history"]:
        copy_list.append(item)
    return copy_list

# process_bluebin_organic(): process the user's answer to whether they have a blue bin
#returns the list of values that the global dst must be updated with 
def process_bluebin_organic_reset(input="", state=""):
    return_list=[]
    no_pattern = re.compile(r"\b(no)|(nope)|(not)|(do not)|(don't)\b")
    yes_pattern = re.compile(r"\b(yes)|(yeah)|(yup)|(yea)|(sure)\b")
    if re.search(no_pattern, input):
        if state == "bluebin":
            hist_list = deep_copy()
            hist_list.append("blue_bin_confirm")
            return_list.append(("blue_bin_confirm","no"))
            return_list.append(("state_history",hist_list))
        elif state == "organic":
            hist_list = deep_copy()
            hist_list.append("backyard_confirm")
            return_list.append(("backyard_confirm","no"))
            return_list.append(("state_history",hist_list))
        elif state == "reset":
            hist_list = deep_copy()
            hist_list.append("reset")
            return_list.append(("reset","no"))
            return_list.append(("state_history",hist_list))
    elif re.search(yes_pattern, input):
        if state == "bluebin":
            hist_list = deep_copy()
            hist_list.append("blue_bin_confirm")
            return_list.append(("blue_bin_confirm","yes"))
            return_list.append(("state_history",hist_list))
        elif state == "organic":
            hist_list = deep_copy()
            hist_list.append("backyard_confirm")
            return_list.append(("backyard_confirm","yes"))
            return_list.append(("state_history",hist_list))
        elif state == "reset":
            hist_list = deep_copy()
            hist_list.append("reset")
            return_list.append(("reset","yes"))
            return_list.append(("state_history",hist_list))
    
    return return_list


# process_clarification(): process the user's clarification of whether the chatbot got the material correctly
#returns the list of values that the global dst must be updated with 
def process_clarification(input=""):
    return_list=[]
    no_pattern = re.compile(r"\b(no)|(nope)|(not)\b")
    yes_pattern = re.compile(r"\b(yes)|(yeah)|(yup)\b")
    if re.search(no_pattern, input):
        hist_list = deep_copy()
        hist_list.append("clarification")
        return_list.append(("clarification","no"))
        return_list.append(("state_history",hist_list))
    elif re.search(yes_pattern, input):
        hist_list = deep_copy()
        hist_list.append("clarification")
        return_list.append(("clarification","yes"))
        return_list.append(("state_history",hist_list))
    return return_list

# process_greeting(): processes when the user first starts and whether material to be recycled is given by user 
#returns the list of values that the global dst must be updated with 
def process_greeting(input =""):
    return_list = []
    plastic_pattern = re.compile(r"\b(plastic)|(styrofoam)|(polystrene)|(non-?styrofoam)|(film)|(bag)|(wrap)\b")
    bluebin_pattern = re.compile(r"\b(cardboard)|(paper)|(metal)|(glass)\b")
    organic_pattern = re.compile(r"\b(coffee)|(bean(s)?)|(peel(s)?)|(eggshells)|(seed(s)?)|(branch(es)?)|(plant)|(stick(s)?)|(leef)|(leaves)|(grass)\b")
    tech_pattern = re.compile(r"\b(computer(s)?)|(laptop(s)?)|(phone(s)?)|(charger(s)?)|(desktop)|(monitor(s)?)|(electronic(s)?)|(wire(s)?)|(battery)|(bulb)|(oil paint)|(metal tank)|(household chemicals)|(motor oil)\b")
    if re.search(plastic_pattern, input):
        plastic_1 = re.compile(r"\b(plastic) ?[123457]\b")
        plastic_2 = re.compile(r"\b(styrofoam)\b")
        plastic_3 = re.compile(r"\b(non-?styrofoam)|(polystrene)\b")
        plastic_4 = re.compile(r"\b(film)|(bag)|(wrap)\b")
        plastic_5 = re.compile(r"\b(toy(s)?)\b")
        if re.search(plastic_1, input):
            return_list.append(("material","plastic"))
            return_list.append(("plastic_type","plastic 1-5 & 7"))
            return_list.append(("state_history",["greeting","material","plastic_type"]))
        elif re.search(plastic_2, input):
            return_list.append(("material","plastic"))
            return_list.append(("plastic_type","styrofoam"))
            return_list.append(("state_history",["greeting","material","plastic_type"]))
        elif re.search(plastic_3, input):
            return_list.append(("material","plastic"))
            return_list.append(("plastic_type","nonstyrofoam"))
            return_list.append(("state_history",["greeting","material","plastic_type"]))
        elif re.search(plastic_4, input):
            return_list.append(("material","plastic"))
            return_list.append(("plastic_type","film"))
            return_list.append(("state_history",["greeting","material","plastic_type"]))
        elif re.search(plastic_5, input):
            return_list.append(("material","plastic toys"))
            return_list.append(("state_history",["greeting","material"]))
        else:
            return_list.append(("material","plastic"))
            return_list.append(("state_history",["greeting","material"]))
    elif re.search(bluebin_pattern, input):
        bluebin_1 = re.compile(r"\b(cardboard)\b")
        bluebin_2 = re.compile(r"\b(paper)\b")
        bluebin_3 = re.compile(r"\b(metal)\b")
        bluebin_4 = re.compile(r"\b(glass)\b")
        if re.search(bluebin_1, input):
            return_list.append(("material","cardboard"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(bluebin_2, input):
            return_list.append(("material","paper"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(bluebin_3, input):
            return_list.append(("material","metal"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(bluebin_4, input):
            return_list.append(("material","glass"))
            return_list.append(("state_history",["greeting","material"]))
    elif re.search(organic_pattern, input):
        organic_1 = re.compile(r"\b(seed(s)?)|(branch(es)?)|(plant)|(stick(s)?)|(leef)|(leaves)|(grass)|(bean(s)?)\b")
        organic_2 = re.compile(r"\b(coffee)\b")
        organic_3 = re.compile(r"\b(peel(s)?)\b")
        organic_4 = re.compile(r"\b(eggshells)\b")
        if re.search(organic_1, input):
            return_list.append(("material","plants"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(organic_2, input):
            return_list.append(("material","coffee"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(organic_3, input):
            return_list.append(("material","peels"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(organic_4, input):
            return_list.append(("material","eggshells"))
            return_list.append(("state_history",["greeting","material"]))
    elif re.search(tech_pattern, input):
        tech_1 = re.compile(r"\b(computer(s)?)|(laptop(s)?)|(phone(s)?)|(charger(s)?)|(desktop)|(monitor(s)?)|(electronic(s)?)|(wire(s)?)\b")
        tech_2 = re.compile(r"\b(battery)\b")
        tech_3 = re.compile(r"\b(bulb)\b")
        tech_4 = re.compile(r"\b(oil paint)\b")
        tech_5 = re.compile(r"\b(metal tank)\b")
        tech_6 = re.compile(r"\b(household chemicals)\b")
        tech_7 = re.compile(r"\b(motor oil)\b")
        if re.search(tech_1, input):
            return_list.append(("material","electronics"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(tech_2, input):
            return_list.append(("material","battery"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(tech_3, input):
            return_list.append(("material","bulb"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(tech_4, input):
            return_list.append(("material","oil paint"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(tech_5, input):
            return_list.append(("material","metal tank"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(tech_6, input):
            return_list.append(("material","household chemicals"))
            return_list.append(("state_history",["greeting","material"]))
        elif re.search(tech_7, input):
            return_list.append(("material","motor oil"))
            return_list.append(("state_history",["greeting","material"]))
    return return_list






# update_dst(input): Updates the dialogue state tracker
# Input: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is
#        most appropriate for the corresponding slot.  Defaults to an empty list.
# Returns: Nothing
def update_dst(input=[]):
	# [YOUR CODE HERE]
 
    # Dummy code for sample output:
    # global dst
    # for slot, value in input:
    #     if slot in dst and isinstance(dst[slot], list):
    #         dst[slot].insert(0, value)
    #     else:
    #         dst[slot] = value

    global dst
    for item in input:             #------> iterate list to acquire pair values and update global dictionary
        (key, value) = item         
        dst[key] = value  
    return

# get_dst(slot): Retrieves the stored value for the specified slot, or the full dialogue state at the
#                current time if no argument is provided.
# Input: A string value corresponding to a slot name.
# Returns: A dictionary representation of the full dialogue state (if no slot name is provided), or the
#          value corresponding to the specified slot.
def get_dst(slot=""):
    global dst 
    if slot == "":             #-----> No argument provided return global dictionary
        return dst
    
    if slot in dst.keys():     #-----> slot key is in dictionary return value
        return dst[slot]
    else:                      #-----> slot key doesn't exist in dictionary, inform
        return "Error: slot doesn't exist in dictionary"


# dialogue_policy(dst): Selects the next dialogue state to be uttered by the chatbot.
# Input: A dictionary representation of a full dialogue state.
# Returns: A string value corresponding to a dialogue state, and a list of (slot, value) pairs necessary
#          for generating an utterance for that dialogue state (or an empty list if no (slot, value) pairs
#          are needed).
def dialogue_policy(dst=[]):     
    #Catergorizing material to identify which procedural state to transition too
    bluebin = ["cardboard", "glass", "metal", "paper", "plastic 1-5 & 7"]
    organic_waste = ["coffee", "peels", "eggshells", "plants"]
    donate = ["clothes", "hardbook", "plastic toys"]
    tech = ["electronics", "battery", "bulb", "oil paint", "metal tank", "household chemicals", "motor oil"]
    
    #Once procedure is provided to user, transition to reset state. This list helps confirm that prodecure was given 
    reset = ["dart", "compost", "compost_service", "recycle_dropoff_center", "recycle_bluebin","hccrf", "donate","retailstore","hccrf","nomarket"]
    
    #Get length of lists that contain user intent history and state history
    state_history_size = len(dst["state_history"])

    previous_state = ""

    #As long as we have a list of state history, get the state we came from  
    if state_history_size > 0:
        previous_state = dst["state_history"][state_history_size-1]

    next_state = ""
    slot_values = []


    if previous_state == "greeting":                   #-----> start
        next_state = "material"
    elif previous_state == "material":             #------> user has provided material
        material = dst[previous_state]
        if material == "plastic":                  #------> user wants to recycle plastic
            next_state = "plastic_type"
            slot_values = [("material","plastic")]
        else:
            next_state = "clarification"
            slot_values = [(previous_state, material)]
    elif previous_state == "plastic_type":         #------> user provided plastic type
            next_state = "clarification"
            slot_values = [(previous_state, dst[previous_state])] 
    elif previous_state == "clarification":        #------> confirm with user material to  be recycled 
        confirm = dst[previous_state]
        if confirm == "no":                                    #------> Error: wrong material
            next_state = dst["state_history"][state_history_size-2]
            if next_state != "material":
                prev = dst["state_history"][state_history_size-3]
                slot_values = [(prev, dst[prev])]
        else:                                         
            prev = dst["state_history"][state_history_size-2]                    
            material = dst[prev]
            if prev == "plastic_type":                         #-----> Material is plastic
                if material in bluebin:
                    next_state = "blue_bin_confirm"
                elif material == "styrofoam":
                    next_state = "dart"
                elif material == "nonstyrofoam":
                    next_state = "nomarket"
                elif material == "film":
                    next_state = "retailstore"
                    slot_values = [(prev, material)]
            else:                                              #------> material is not plastic (i.e. bluebin, organic, eletronic, donatable)  
                if material in bluebin:                     
                    next_state = "blue_bin_confirm"
                elif material in organic_waste:
                    next_state = "backyard_confirm"
                    slot_values = [(prev, material)]
                elif material in donate:
                    next_state = "donate"
                    slot_values = [(prev, material)]
                elif material in tech:
                    next_state = "hccrf"
                    slot_values = [(prev, material)]

    elif previous_state == "blue_bin_confirm":    #-------> confirm with user if they have a bluebin
        confirm = dst[previous_state]
        if confirm == "yes":
            next_state = "recycle_bluebin"
            slot_values = [("material", dst["material"])]
        else:
            next_state = "recycle_dropoff_center"
            slot_values = [("material", dst["material"])]
    elif previous_state == "backyard_confirm":   #--------> confirm with user if they have a way to compost
        confirm = dst[previous_state]
        if confirm == "yes":
            next_state = "compost"
            slot_values = [("material", dst["material"])]
        else:
            next_state = "compost_service"
            slot_values = [("material", dst["material"])]
    elif previous_state in reset:                #--------> user recieved recycling procedure, reset?
        next_state = "reset"
    elif previous_state == "reset":              #--------> does user want to reset? 
        confirm = dst["reset"]
        if confirm == "yes":
            next_state = "material"
        else:
            next_state = "bye" 

    return next_state, slot_values
# nlg(state, slots=[]): Generates a surface realization for the specified dialogue act.
# Input: A string indicating a valid state, and optionally a list of (slot, value) tuples.
# Returns: A string representing a sentence generated for the specified state, optionally
#          including the specified slot values if they are needed by the template.
def nlg(state, slots=[]):
    # Dictionary containing sentence generated for specific state:
    templates = defaultdict(list)
    
    # Create the templates for each state:
    templates["material"] = []
    templates["material"].append("That's great! Can you tell me the material you want to recycle?")
    templates["material"].append("Awesome. What is the item made from?")

    templates["plastic_type"] = []
    templates["plastic_type"].append("So, you want to recycle  material made from plastic. What kind of plastic? You can say plastic 1 OR plastic 2 OR plastic 3 OR plastic 4 OR plastic 5 OR plastic 7 OR styrofoam OR nonstyrofoam OR film")
    templates["plastic_type"].append("Okay, there are different types of plastic. What kind of plastic is your material made from?(i.e. plastic 1 OR plastic 2 OR plastic 3 OR plastic 4 OR plastic 5 OR plastic 7 OR styrofoam OR nonstyrofoam OR film)")
    
    templates["clarification"] = []
    templates["clarification"].append("Just for clarification, you want to recycle <material>? (Type yes or no)")
    templates["clarification"].append("Alright, I want to make sure I got it correct. You want to recycle <material>? (Type yes or no)")

    templates["blue_bin_confirm"] = []
    templates["blue_bin_confirm"].append("Does your resident area provide blue bin recycling bins?")
    templates["blue_bin_confirm"].append("The material you want to recycle can be recycled through a blue recycling bin. Do you have access to one?")

    templates["backyard_confirm"] = []
    templates["backyard_confirm"].append("Would you like to learn how to compost?")
    templates["backyard_confirm"].append("So <material> can be composted. Would you like to know how to do that?")

    templates["donate"] = []
    templates["donate"].append("The best way to recycle <material> is to donate it to any local donation center.")
    templates["donate"].append("Please donate <material> to your local Donation Center.")

    templates["dart"] = []
    templates["dart"].append("Material made from styrofoam or plastic #6 can be recycled at Dart Container Corp.")
    templates["dart"].append("Please recycle styrofoam and plastic #6 at the closest Dart Container Corp.")

    templates["nomarket"] = []
    templates["nomarket"].append("Sorry, to inform you there is no recycling market for nonstyrofoam plastic. The best thing to do is reduce your usage of material made from nonstyrofoam plastic.")
    templates["nomarket"].append("Sadly, there is no recycling market for nonstyrofoam plastic. But this doesn't mean you can't do anything, reducing your usage is the best thing to do.")

    templates["retailstore"] = []
    templates["retailstore"].append("Please dropoff <material> at any retailstore like Target, Jewel Osco.")
    templates["retailstore"].append("Dropoff <material> at any local retailstore.")

    templates["hccrf"] = []
    templates["hccrf"].append("Any material like <material> should be dropped of at a HCCRF location.")
    templates["hccrf"].append("To recycle <material>, please dropoff at closest HCCRF Center.")
    
    templates["recycle_bluebin"] = []
    templates["recycle_bluebin"].append("To recycle <material> please put in your blue recycling bin.")
    templates["recycle_bluebin"].append("That's great! Just put your <material> plastic into your blue recycling bin.")

    templates["recycle_dropoff_center"] = []
    templates["recycle_dropoff_center"].append("Don't worry you will still be able to recycle <material>. Just dropoff it off at closest Chicago Recycling Dropoff Center.")
    templates["recycle_dropoff_center"].append("That's fine, you can dropoff <material> at Chicago Recycling Dropoff Center.")

    templates["compost"] =[]
    templates["compost"].append("<material> can be used as compost for your backyard. Refer to https://www.thekitchn.com/tips-for-setting-up-a-simple-backyard-compost-system-202160 for information on steps to composting.")

    templates["compost_service"] =[]
    templates["compost_service"].append("To recycle <material>, you can pay for a fee-based compost pick-up service OR opt for $3 per gallon dropoff service to the Chicago farmer's markets.")

    templates["reset"] = []
    templates["reset"].append("Do you have anything else you would like to recycle? (Please reply with yes OR no)")
    templates["reset"].append("Can I help you with anything else? (Type yes or no)")

    templates["bye"] = []
    templates["bye"].append("Alright, it was nice chatting with you today. Come again!")
    templates["bye"].append("Thank you for asking Eco today. I look forward to our next chat!")


    if state not in templates.keys():
        return "Error: " +  state +  " not found in templates"
    
    # When you implement this for real, you'll need to randomly select one of the templates for
    # the specified state, rather than always selecting template 0.  You probably also will not
    # want to rely on hardcoded input slot positions (e.g., slots[0][1]).  Optionally, you might
    # want to include logic that handles a/an and singular/plural terms, to make your chatbot's
    # output more natural (e.g., avoiding "did you say you want 1 pizzas?").
    random_temp = random.randrange(0,len(templates[state]))

    
    output = ""
    if len(slots) > 0:
        material = str(slots[0][1])
        if state == "compost":
            first_letter = material[0]
            cap_letter = first_letter.upper()
            material.replace(first_letter, cap_letter)
        output = templates[state][random_temp].replace("<material>", material)
    else:
        if(state == "material" and dst["clarification"] == "no"):
            output = "I am sorry about that! Could you please repeat it?"
        else:
            output = templates[state][random_temp]
    return output



# Use this main function to test your code when running it from a terminal
# Sample code is provided to assist with the assignment, feel free to change/remove it if you want
# You can run the code from terminal as: python3 chatbot.py

def main():
    global dst
    
    # Sample input to initialize dst for demonstration purposes.
    reset = ["dart", "compost", "compost_service", "recycle_dropoff_center", "recycle_bluebin","hccrf", "donate","retailstore","hccrf","nomarket"]
    dst_input = [("material", ""), ("plastic_type", ""), ("clarification", ""), ("blue_bin_confirm", ""), ("backyard_confirm",""), ("reset", ""), ("state_history", [])]
    update_dst(dst_input)

    
    greeting_chatbot = ["<Eco>: Hello, I am Eco. How can I help you today?", "<Eco>: Hello, I am your Eco-helper. What material do you want to recycle today?"]
    random_temp = random.randrange(0,len(greeting_chatbot))
    print(greeting_chatbot[random_temp])



    continue_chatting = ""
    error = 0
    # continue_chatting != "bye"
    while(continue_chatting != "bye"):
        user_input = input("<You>: ")

        output = nlu(user_input)



        update_dst(output)
        
        next_state, slot_values = dialogue_policy(dst)
    
        # print("Testing1 - Next State: {0}\tSlot Values: {1}".format(next_state, slot_values))
        
        response = nlg(next_state, slot_values)

        if(response == "Error:  not found in templates"):
            if(error == 0):
                print("<Eco>: I am sorry, but can you repeat that?")
            else: 
                user_input = user_input.lower()
                if(user_input != "no" and user_input != "nope"):
                    error_handling = ["<Eco>: Unfortunetly, I don't know how to recycle that kind of material. Can you try another material?\n     : (type yes or no)", "<Eco>: Sadly, I don't know how to recycle that. Would you like to try another material?\n     : (type yes or no)"]
                    random_temp = random.randrange(0,len(error_handling))
                    print(error_handling[random_temp])
                    if(user_input == "yes" or user_input == "yeah"):
                        dst["state_history"].append("greeting")
                        next_state, slot_values = dialogue_policy(dst)
                        response = nlg(next_state, slot_values)
                        print("<Eco>: " + response)
                else:
                    print("Alright, it was nice chatting with you. Come again!")
                    exit(0)

            error+=1
            
        else:
            print("<Eco>: " + response)

            if next_state in reset: 
                dst["state_history"].append(next_state)
                next_state, slot_values = dialogue_policy(dst)
                response = nlg(next_state, slot_values)
                print("<Eco>: " + response)

            continue_chatting = next_state
 






################ Do not make any changes below this line ################
if __name__ == '__main__':
    main()

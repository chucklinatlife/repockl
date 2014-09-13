__author__ = 'cklam'


import pprint


viet_eng_dict = {}
pp = pprint.PrettyPrinter(indent=4)
#pform = pprint.pformat()


def create_doc(dictionary_name,mode):
    if mode == 'write':
        pform = pprint.pformat(dictionary_name)
        with open("/Users/cklam/Documents/Development/repockl-master/repockl/viet_eng.doc", 'w') as myfile:
            myfile.write(pform)

def create_dictionary(english_input,viet_input):
        viet_eng_dict[english_input]=viet_input
        return viet_eng_dict

if __name__ == "__main__":
    exitCue = False
    while exitCue is False:
        english_input = raw_input("please enter an english word: ")
        viet_input = raw_input("please enter the vietnamese translation: ")
        vietDict = create_dictionary(english_input,viet_input)
        userInput = raw_input("Do you want to add another entry? ")
        if userInput.lower() == "yes":
            pass
        else:
            exitCue = True
    print "dictionary created...creating document"
    create_doc(vietDict, 'write')

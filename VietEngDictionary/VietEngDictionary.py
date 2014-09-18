__author__ = 'cklam'


import pprint
import codecs

viet_eng_dict = {}
pp = pprint.PrettyPrinter(indent=4)
#pform = pprint.pformat()


def create_doc(dictionary_name,mode):
        pform = pprint.pformat(dictionary_name)
        pform = pform.decode('utf-8')
        with codecs.open("/Users/cklam/Documents/Development/repockl-master/repockl/viet_eng.txt", 'w', 'utf-8') as myfile:
            myfile.write(pform)


def create_dictionary(english_input,viet_input):
        viet_eng_dict[english_input]=viet_input
        return viet_eng_dict

if __name__ == "__main__":
    english_input = raw_input("please enter an english word: ")
    viet_input = raw_input("please enter the vietnamese translation: ")
    vietDict = create_dictionary(english_input,viet_input)


    print "dictionary created...creating document"
    write = 'write'
    create_doc(vietDict, write)
    #print viet_eng_dict[english_input]
    print viet_eng_dict
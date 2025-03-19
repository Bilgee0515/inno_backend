from collections import defaultdict
import os

import cv2
import numpy as np
import matplotlib.pyplot as plt
import easyocr
import re
import string
import math

from . import utili


# define constants
model_cfg_path = os.path.join('.', 'model', 'cfg', 'darknet-yolov3.cfg')
model_weights_path = os.path.join('.', 'model', 'weights', 'model.weights')
class_names_path = os.path.join('.', 'model', 'class.names')

input_dir = "C:/Users/bilgee work/Desktop/anpr/automatic-number-plate-recognition-python/data"


# def contains_alphabetic(s):
#     # Check if the string contains any alphabetic characters
#     return any(char.isalpha() for char in s)

# def contains_numeric(s):
#     # Check if the string contains any numeric characters
#     return any(char.isdigit() for char in s)

def filter_list(original_list, filter_condition):
    # Filter out elements based on the provided condition
    filtered_list = [element for element in original_list if filter_condition(element)]
    return filtered_list

def remove_punctuation(input_string):
    translation_table = str.maketrans("", "", string.punctuation)

    result_string = input_string.translate(translation_table)

    return result_string


# load image
def anpr_function(license_plate_path):
    print("anpr_function ----> START")
    print('license_plate_path: ', license_plate_path)

    #change static_license_plate_path to license_plate_path for actual function 
    static_license_plate_path = './media/Small/Small_Img38.jpg'
    readed_text_list = []
    

    license_plate = cv2.imread(license_plate_path)

    # plot
    reader = easyocr.Reader(['mn'])

    # turn the license plate to gray
    license_plate_gray = cv2.cvtColor(license_plate, cv2.COLOR_BGR2GRAY)
    
    #change threshold value from 40 to 255 by 3 
    threshold_value = 50
    threshhold_step = 2
    output_dict = {}
    output_list = []

    while threshold_value < 122:
        dict_key = dict_key + 1
        print('threshhold_value: ', threshold_value)
        _, license_plate_thresh = cv2.threshold(license_plate_gray, threshold_value, 255, cv2.THRESH_BINARY_INV)
        

        output = reader.readtext(license_plate_thresh, detail = 0, paragraph=True)
        print("output!: ", output)
        print("threshold_value!: ", threshold_value)
        if len(output) > 0:
            text = output[0]

        else:
            text = ''

        if len(text) > 0:
            readed_text_list.append(text)

        threshold_value = threshold_value + threshhold_step
        number_list = []
        alpha_list = []
        alp_text_dict = {}
        num_text_dict = {}

    print('readed_text_list:', readed_text_list)



    #all of the license plate will have 4 digits so divide the read list into 2
    # check for the spaces and punctuation marks
    for readed_text in readed_text_list:
        cleared_text = remove_punctuation(readed_text)
        spc_removed_text = cleared_text.replace(" ", "")
        if len(spc_removed_text) == 7 or len(spc_removed_text) == 6:
                print("number_text_dict_test: ", spc_removed_text)
                is_valid = True
                for char in spc_removed_text[:4]:
                    if not char.isdigit():
                        is_valid = False
                        break
                for char in spc_removed_text[4:]:
                    if not char.isalpha():
                        is_valid = False
                        break
                if is_valid:
                    number_list.append(spc_removed_text)


    print("number_list: ", number_list)
    if len(number_list) == 0:
        raise Exception("Algorithm could not read the capture")

    
    count_num_dict = {}
    
    for number in number_list:
        if number in count_num_dict:
            count_num_dict[number] += 1
        else:
            count_num_dict[number] = 1
    
    print("count_num_dict: ", count_num_dict)

    max_number = max(count_num_dict, key=count_num_dict.get)

    print('max_number: ', max_number)

    print("count: ", count_num_dict[max_number])    

    return max_number







license_plate_path = "C:\\Users\\bilgee work\\Desktop\\dahua sdk demo\\General_NetSDK_ChnEng_Python_win64_IS_V3.057.0000002.0.R.230817\\Demo\\IntelligentTrafficDemo\\Small\\Small_Img22.jpg"


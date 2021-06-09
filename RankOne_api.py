import json
import requests
import os, glob
import time
import zlib

def ROCone2one(fp1, fp2):
"""Sends a request containing two images to be compared to the FLASK server.
Returns a similarity score between both images."""
    start = time.time()

    """image 1"""
    with open(fp1, 'rb') as f: #open the image
        imag = f.read()

    imag1 = zlib.compress(imag) # compress it
    img = imag1

    """image 2"""
    with open(fp2, 'rb') as g:
        imagg = g.read()
    imagg1 = zlib.compress(imagg)
    img2 = imagg1

    url = 'http://152.20.234.127:5000/ROC_one2one' # where we are sending our request
    r = requests.post(url, files={"image1": img, "image2":img2}) # the request containing the url and both images stored in a dictionary

    print(r.json())
    end = time.time()
    time_elapsed = end - start
    print("Time elapsed: ", time_elapsed)
    return(r.json())


def ROC_full_dir(d1, d2):
"""Sends two entire directories containing images to be compared. 
   Most likely each directory is of the same country."""
    url = 'http://152.20.234.127:5000/ROC_full_dir'
    img_dict = {}
    verif_dict = {}
    start = time.time()   
    # start a loop that will go through the whole directory (reference?)
    for i in os.listdir(d1):
        print(d1, i)
        name = str(d1) + "/" + i
        with open(name, 'rb') as reader: #read file as binary
            bin_img = reader.read()
        comp_img = zlib.compress(bin_img) #compress binary
        # add the name and the img data to the dictionary
        img_dict[name] = comp_img

    # do the same above but for the second directory (verification)
    """nested loop needed since verification folder is nested directory. TODO change file structure of verification directory."""
    for j in os.listdir(d2):
        # if j is dir? loop else
        vname = d2 + "/" + j
        print(os.path.isdir(vname))
        print(j)
        print(vname)
        if os.path.isdir(vname): #if its a directory, loop thru it
            for g in os.listdir(vname):
                print(g)
                vname1 = vname + "/" + g
                with open(vname1, 'rb') as reader: # read as binary
                    bin_img_1 = reader.read()
                comp_img_1 = zlib.compress(bin_img_1) # compress
                verif_dict[vname1] = comp_img_1  # store into dictionary
        else:          
            #vname = d2 + "/" + j
            with open(vname, 'rb') as reader:
                bin_img_1 = reader.read()
            comp_img_1 = zlib.compress(bin_img_1)

            verif_dict[vname] = comp_img_1
    img_dict1 = str(img_dict)
    verif_dict2 = str(verif_dict)
    # send the post request to the server to take in the dictionaries
    r = requests.post(url, files={'images':img_dict1, 'verification_images':verif_dict2})
    end = time.time()
    time_elapsed = end - start
    print("time elapsed :", time_elapsed)
    print(r.json())
    return r.json()

def ROCone2N_find_compare(path):
"""Uploads a single image along with its name and country to the RankOne FLASK server. Once there, the server
locates all other images corresponding to the name and country and then returns confidence scores."""
    start = time.time()
    url = 'http://152.20.234.127:5000/ROC_find_compare' #url to send the request to
    """image"""
    with open(path, 'rb') as h: # read as binary
        bin_img_data = h.read()
    comprssd_data = zlib.compress(bin_img_data) # compress binary
     
    gender_icon = "_female_" # index the gender to be used to store gender in variable
    country_icon = 'AA_' # index the country
    name_index = path.rindex("_") #index the name
    try:
        gender_index = path.rindex(gender_icon) ##try female first, if ValueError then must be male
    except ValueError:
        gender_icon = "_male_"
        gender_index = path.rindex(gender_icon)
    gender = path[gender_index+1:gender_index+len(gender_icon)-1]
    print("gender: ", gender)
    name = path[(gender_index+len(gender_icon)):name_index]
    print("name: ", name)
    country_index1 = path.index(country_icon)
    country_index2 = path.index(gender_icon, country_index1)
    country = path[country_index1+len(country_icon):country_index2]
    print("country: ", country)
              
    r = requests.post(url, files={'image':comprssd_data, 'country':country, 'name':name}) #send the request
    end = time.time()
    time_elapsed = end - start
    print(time_elapsed)
    print(r.json())
    return(r.json()) #return the Json result
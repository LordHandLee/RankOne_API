from flask import Flask, request, jsonify
import zlib
import os

app = Flask(__name__)

"""the folder access points for the FLASK server"""
Upload_folder1 = "/home/i3s/Pipeline/api_image_depo"
UPLOAD_FOLDER = "/home/i3s/Pipeline/api_image_depo/one2one/"
UPLOAD_FOLDER2 = "/home/i3s/Pipeline/api_image_depo/one2N_find_compare/"
UPLOAD_FOLDER3 = "/home/i3s/Pipeline/api_image_depo/ROC_full_dir/"
verif_dir = "/home/i3s/Pipeline/verification_images/"
Upload_list = [Upload_folder1, UPLOAD_FOLDER, UPLOAD_FOLDER2, UPLOAD_FOLDER3, verif_dir] #store the folders in a list so we can loop
for i in Upload_list: # like I said, loop through the list
    if not os.path.exists(i): # if not exists, make it so
        os.mkdir(i)


@app.route("/ROC_one2one", methods=["POST", "GET"])
def one2one_image_check():
"""Compares two images using RANKONE"""
    data1 = request.files['image1'].read() #read in the images from the sent request
    data2 = request.files['image2'].read()
    decomp1 = zlib.decompress(data1) #decompress binary data
    decomp2 = zlib.decompress(data2)
    with open(UPLOAD_FOLDER + 'tester.jpg', 'wb') as f: # write the binary data to a file
        f.write(decomp1)
    with open(UPLOAD_FOLDER + 'tester2.jpg', 'wb') as g:
        g.write(decomp2)
    # Rank ONE stuff here
    fp1 = UPLOAD_FOLDER + 'tester.jpg' # associate the file and file path together
    fp2 = UPLOAD_FOLDER + 'tester2.jpg'
    command = 'python3 /home/i3s/RankOne/roc-linux-x64-fma3/python3/roc_example_verify.py {} {}'.format(fp1, fp2) # the command to be executed
    confidence_score = os.popen(command).read() #read the result
    return jsonify(confidence_score) #return confidence score to the client


@app.route("/ROC_find_compare", methods=["POST", "GET"])
def one2N_find_compare():
"""Searches for images associated with the image name and country and returns the confidence scores for each"""
    image = request.files['image'].read()
    country = request.files['country'].read()
    name = request.files['name'].read()
    img_decomp = zlib.decompress(image) #decompress raw binary data
    with open(UPLOAD_FOLDER2 + 'tester.jpg', 'wb') as h: # writes binary data into image file
        h.write(img_decomp)
    # need to loop through list of verif by country and name # if there, verify # if not, return error message
    country_dir = verif_dir + country
    target_dir = None
    print(country)
    print(name)
    print(country_dir)
    for i in os.listdir(country_dir): #loop through directory corresponding to the country that was sent in the request
        target_name = os.path.splitext(i)[0]
        if target_name == name: # if our target equals the name we are looking for, its a match
            target_dir = os.path.join(country_dir, i)
    if target_dir == None: #Otherwise, we could not locate
        error_msg = "Could not locate " + name
        return jsonify(error_msg) # return the error message to the client
    fp1 = UPLOAD_FOLDER2 + 'tester.jpg'
    command = 'python3 /home/i3s/RankOne/roc-linux-x64-fma3/python3/roc_example_verify.py {} {}'.format(fp1, target_dir)
    confidence_score = os.popen(command).read()
    return jsonify(confidence_score) #return the confidence score to the client


@app.route("/ROC_full_dir", methods=["POST", "GET"])
def ROC_full_dir():
"""Takes in two directories( reference and verification....always) nested in a 
dictionary and then executes the file_launcher on both directories.
File_launcher loops thru each image in the first directory, finding a match in the second.
Once a match is found, confidence scores are generated."""
    dict_of_images = request.files['images'].read() #read the first request
    new_dict = dict(eval(dict_of_images)) #evaluate the dictionary so we can access the nested dictionary
    if len(new_dict) == 0: #something went wrong, nothing was sent
        return jsonify("Unsuccesful, most likely no images were found in images directory")
    for i, j in new_dict.items():
        path = i #the original file path from the client
        slash = "/" #represent linux
        try:
            path.index(slash)
        except ValueError:
            slash = '\\' #screw windows
        name_index = path.rindex(slash) #index the name and country from original file path
        name = path[name_index:].strip(slash)
        next_path = path[:name_index]
        country_index = next_path.rindex(slash)
        country = next_path[country_index:].strip(slash)
        print(name)
        print(country)
        img_fold = UPLOAD_FOLDER3 + "images" #create "images" folder
        if not os.path.exists(img_fold):
            os.mkdir(img_fold)
        new_server_path = os.path.join(img_fold, country) #join the new "images" folder with the country name
        print(new_server_path)
        if not os.path.exists(new_server_path): #create the new directory with country name
            os.mkdir(new_server_path)
        verif_img_decomp = zlib.decompress(j)
        with open(new_server_path + '/' + name, "wb") as f: # write the directory
            f.write(verif_img_decomp)

    dict_of_images2 = request.files['verification_images'].read() #read the second request
    new_dict2 = dict(eval(dict_of_images2)) #evaluate the dictionary so we can access the nested dictionary
    for i, j in new_dict2.items():
        path = i #the original file path from the client
        slash = '/'
        try:
            path.index(slash)
        except ValueError:
            slash = "\\"
        name_index = path.rindex(slash) #index the name and country from original file path
        name = path[name_index:].strip(slash)
        next_path = path[:name_index]
        country_index = next_path.rindex(slash)
        country = next_path[country_index:].strip(slash)
        print(name)
        print(country)
        img_fold = UPLOAD_FOLDER3 + "verification_images" #create "directory" folder
        #loop through verification_images folder and check for male/female
        #if present, merge both folders into one
        if not os.path.exists(img_fold):
            os.mkdir(img_fold)
        new_server_path2 = os.path.join(img_fold, country) #join the new "verification_images" folder with the country name
        if not os.path.exists(new_server_path2):
            os.mkdir(new_server_path2)
        verif_img_decomp = zlib.decompress(j)
        with open(new_server_path2 + '/' + name, "wb") as f: # write the directory with images contained therein.
            f.write(verif_img_decomp)
    fold = UPLOAD_FOLDER3 + "verification_images" #out of scope of the loop, had to create new variable
    launcher_list = [] #list of directories of verification images
    launcher_counter = 0
    for i in os.listdir(fold): #loop thru directory
        p = os.path.join(fold,i)
        if os.path.isdir(p): #if its a directory
            launcher_list.append(p) #add to the list
    # craft the command to run file launcher and that will make the csv file to return
    try:
        if len(launcher_list) == 2: #To be continued!
            cmnd = "python3 /home/i3s/Pipeline/file_launcher.py {} {}".format(new_server_path, launcher_list[0])
            os.system(cmnd)
            cmnd = "python3 /home/i3s/Pipeline/file_launcher.py {} {}".format(new_server_path, launcher_list[1])
            os.system(cmnd)
        else: #NOTHING IS THERE!
            cmnd = "python3 /home/i3s/Pipeline/file_launcher.py {} {}".format(new_server_path, new_server_path2)
            os.system(cmnd)

        # TODO return the csv file of the countriy subjects, probes, and similarity scores
        return jsonify("Success")
    except Exception as e:
        print(e)
        return("Unsuccesful, most likely no images were found in images directory")


app.run(host='152.20.234.127', port=5000)
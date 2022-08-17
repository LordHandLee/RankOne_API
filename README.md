# RankOne API



For use as part of Worldwide Dataset project and other projects at the UNCW FaceAging lab. Makes use of the ROC SDK without making
direct contact with the chawkface server.

Allows for simple Rank One facial recognition algorithms to be easily integrated into any project or codebase and run from a non-licensed computer. Functionality includes one2one and one2N comparison using images or entire directories of images as input. Built using Flask and python.


### Prerequisites

This tool requires [Python 2] (https://python.org)


Python 2  libraries:

```
flask
json
os
requests
sys
time
zlib
```

### Installing & Running the server

Put ROC_api_server.py in the same directory that the RankOne installation is located. Open a terminal, navigate to the aforementioned directory and type:
```
python ROC_api_server.py
```
### Installing the client API

Put RankOne_api.py in the same directory as your project. In your code type: `from RankOne_api import ROCone2one` at the top to import. 
ROCone2one takes two file paths as arguments. Make sure you are connected to the university vpn or this will not work.


## Built With

* [Python 2](http://python.org/)

## Contributing

This code is stored on the FaceAging Group's GitHub repository. 

## Authors

* **Alex Czaus**
* **Ethan Lee**

## License

N/A

## Acknowledgments

* FaceAging Lab


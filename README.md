# csv-c81
This python script allows quick conversion between csv and c81 formats. The files are identified on the basis of the file extension 
and converted to the alternate one. It also has a quick plot functionality that allows quick inspection of C81 files when the `-p` flag is passed.


## Installation
```bash
# Install python and pip package manager
$ sudo apt install python3-dev python3-pip

# Clone this git repo
$ git clone git@github.com:cibinjoseph/csv-c81.git && cd csv-c81

# Install required packages
$ pip3 install -r requirements.txt

# Run as necessary
$ python3 csv-c81.py sample1.csv
sample1.C81 created
```

## Usage
The input CSV files have to fulfill the following requirements:
1. CL, CD, CM seperated by blank lines
2. No words or alphabets
3. The file extension should either be .csv or .c81

Lines starting with a '#' are ignored and treated as comments.
If any of the CD or CM tables are not present in the csv file, they are set to zero by default in the generated C81 file.

## Example usage
```bash
# Display sample1.csv file
$ cat sample1.csv
0,0,0.5,1
-180,0,0,0
-45,1,1.1,1.2
-5,2,2.1,2.2
0,0,0,0
5,-1,-1.1,-1.2
45,-3,-3.1,-3.2
180,0,0,0

# Convert sample1.csv file to sample1.C81 file
$ python3 csv-c81.py sample1.csv
sample1.C81 created

# Display sample1.C81 file
$ cat sample1.C81
sample1                       030703070307
         0.000  0.500  1.000
-180.00  0.000  0.000  0.000
 -45.00  1.000  1.100  1.200
  -5.00  2.000  2.100  2.200
   0.00  0.000  0.000  0.000
   5.00 -1.000 -1.100 -1.200
  45.00 -3.000 -3.100 -3.200
 180.00  0.000  0.000  0.000
         0.000  0.500  1.000
-180.00  0.000  0.000  0.000
 -45.00  0.000  0.000  0.000
  -5.00  0.000  0.000  0.000
   0.00  0.000  0.000  0.000
   5.00 -0.000 -0.000 -0.000
  45.00 -0.000 -0.000 -0.000
 180.00  0.000  0.000  0.000
         0.000  0.500  1.000
-180.00  0.000  0.000  0.000
 -45.00  0.000  0.000  0.000
  -5.00  0.000  0.000  0.000
   0.00  0.000  0.000  0.000
   5.00 -0.000 -0.000 -0.000
  45.00 -0.000 -0.000 -0.000
 180.00  0.000  0.000  0.000
```

## Author
Cibin Joseph

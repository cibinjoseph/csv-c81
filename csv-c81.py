""" Code that converts between CSV and C81 """

import c81utils as c81
import numpy as np
from sys import argv
import matplotlib.pyplot as plt

args = argv

def usage():
    """ Prints usage details """
    print('Usage: python3 csv-c81.py inputfile')
    print(' Add -p flag for plotting C81 file')

def convert2c81(infile):
    """ Converts CSV file to C81 """
    # Check delimiter
    with open(infile, 'r') as fh:
        line = fh.readline()
    if ',' in line:
        data = np.genfromtxt(infile, delimiter=',', dtype='float64', \
                             filling_values=0.0, comments='#')
    else:
        data = np.genfromtxt(infile, dtype='float64', \
                             filling_values=0.0, comments='#')

    neg180s = np.where(data[:, 0] == -180)[0]
    pos180s = np.where(data[:, 0] ==  180)[0]

    if len(neg180s) != len(pos180s):
        raise ValueError('No. of -180s and 180s do not match')

    if len(pos180s) == 1:
        machL = data[0, 1:]
        alphaL = data[1:, 0]
        CL = data[1:, 1:]

        alphaD = alphaL
        machD = machL
        CD = CL*0.0

        alphaM = alphaL
        machM = machL
        CM = CL*0.0

    elif len(pos180s) == 2:
        machL = data[neg180s[0]-1, 1:]
        alphaL = data[neg180s[0]:pos180s[0]+1, 0]
        CL = data[neg180s[0]:pos180s[0]+1, 1:]

        machD = data[neg180s[1]-1, 1:]
        alphaD = data[neg180s[1]:pos180s[1]+1, 0]
        CD = data[neg180s[1]:pos180s[1]+1, 1:]

        alphaM = alphaL
        machM = machL
        CM = CL*0.0

    elif len(pos180s) == 3:
        machL = data[neg180s[0]-1, 1:]
        alphaL = data[neg180s[0]:pos180s[0]+1, 0]
        CL = data[neg180s[0]:pos180s[0]+1, 1:]

        machD = data[neg180s[1]-1, 1:]
        alphaD = data[neg180s[1]:pos180s[1]+1, 0]
        CD = data[neg180s[1]:pos180s[1]+1, 1:]

        machM = data[neg180s[2]-1, 1:]
        alphaM = data[neg180s[2]:, 0]
        CM = data[neg180s[2]:pos180s[2]+1, 1:]

    af = c81.C81(infile[:-4], \
                alphaL, machL, CL, \
                alphaD, machD, CD, \
                alphaM, machM, CM)

    outfile = infile[:-4] + '.C81'
    with open(outfile, 'w') as fh:
        c81.dump(af, fh)

    print(outfile + ' created')

def convert2csv(infile):
    """ Converts C81 file to CSV """
    with open(infile, 'r') as fh:
        af = c81.load(fh)

    # Construct large 2d array for writing out
    alphaL = np.insert(af.CL.alpha, 0, 0.0)
    CLarray = np.insert(af.CL.val, 0, af.CL.mach, axis=0)
    CLarray = np.insert(CLarray, 0, alphaL, axis=1)

    alphaD = np.insert(af.CD.alpha, 0, 0.0)
    CDarray = np.insert(af.CD.val, 0, af.CD.mach, axis=0)
    CDarray = np.insert(CDarray, 0, alphaD, axis=1)

    alphaM = np.insert(af.CM.alpha, 0, 0.0)
    CMarray = np.insert(af.CM.val, 0, af.CM.mach, axis=0)
    CMarray = np.insert(CMarray, 0, alphaM, axis=1)

    outArray = np.block([[CLarray], [CDarray], [CMarray]])

    outfile = infile[:-4] + '.CSV'
    np.savetxt(outfile, outArray, fmt='%9.4f', delimiter=',')
    print(outfile + ' created')

def plotC81(infile):
    """ Plot airfoil tables from C81 file """
    with open(infile, 'r') as fh:
        af = c81.load(fh)

    fig, ax = plt.subplots(1, 3)
    for i in range(len(af.CL.mach)):
        ax[0].plot(af.CL.alpha, af.CL.val[:, i], \
                  label='M ' + str(af.CL.mach[i]))
    for i in range(len(af.CD.mach)):
        ax[1].plot(af.CD.alpha, af.CD.val[:, i], \
                  label='M ' + str(af.CD.mach[i]))
    for i in range(len(af.CM.mach)):
        ax[2].plot(af.CM.alpha, af.CM.val[:, i], \
                  label='M ' + str(af.CM.mach[i]))

    ax[0].set_xlabel('alpha')
    ax[0].set_title('CL')
    ax[0].legend()

    ax[1].set_xlabel('alpha')
    ax[1].set_title('CD')
    ax[1].legend()

    ax[2].set_xlabel('alpha')
    ax[2].set_title('CM')
    ax[2].legend()

    plt.tight_layout()
    plt.show()


def main():
    # Read input arguments as filenames
    if len(args) == 1:
        usage()
        quit()
    else:
        filenames = args[1:]

    # Check if plotting is requested for single file
    if filenames[0] == '-p' and len(filenames) == 2:
        infile = filenames[1]
        if infile[-4:].upper() != '.C81':
            raise TypeError('Only .C81 files can be plotted. \
                            Convert and try again.')
        else:
            # Plot the contents of the file
            plotC81(infile)

    else:
        # For each filename convert as necessary
        for infile in filenames:
            if infile != '-p':
                if infile[-4:].upper() == '.C81':
                    convert2csv(infile)
                if infile[-4:].upper() == '.CSV':
                    convert2c81(infile)


if __name__ == "__main__":
    main()

import sys
from numpy import matrix, array
from matplotlib import pyplot as plt


def circle(x0,y0,r,num_points=100):
    """
    create Cartesian coordinates for plotting a circle centered at
    [x0,y0] with radius [r] using [num_points] data points. 
    All inputs are scalars

    Hamid Mokhtarzadeh
    July 18, 2011
    """
    import numpy as np
    theta = np.linspace(0,2*np.pi,num_points);

    x = x0 + r*np.cos(theta);
    y = y0 + r*np.sin(theta);

    return x,y

def visualize(A):
    """
    Visualize absolute value of A so as to see matrix structure.
    """
    
    # Matrix/Array
    f = plt.figure()
    ax = f.add_subplot(111)
    #ax.pcolor(np.array(A), edgecolor='w')
    ax.pcolormesh(np.abs(A), cmap=plt.cm.gray_r, vmin=0, vmax=3*np.std(J))
    ax.set_xlim([0, A.shape[1]])
    ax.set_ylim([0, A.shape[0]])
    ax.invert_yaxis() # set origin to upper left corner
    ax.xaxis.set_ticks_position('top') # move x-axis tick to top of graph
    ax.set_xlabel('C O L U M N S')
    ax.set_ylabel('R O W S')
    
    plt.show()
    

def loadtxt2dic(filename, output_type='matrix'):
    """
    Loads text file of key:value pairs into a dictionary.  
    Usage notes:
    -Lines begining with '#' are treated as comments and skipped.  
    -Blank lines are also skipped
    -Keys and values should be separated by '=', but extra spaces are fine.  
    -Keys for boolean flags should start with 'FLAG'
    -Keys for strings should start with 'STR'
    -A matrix/scalar are stored floats ONLY if the text has a decimal
    
    Parameters
    ----------
    filename : string
               Path to input text file
    output_type = {'ndarray', 'matrix'} optional
                  Conversion type for array-like entries.  Default is 'matrix'

    """
   dic = {}
    infile = open(filename,'r')
   
    for line in infile:

        # remove extra spaces
        line = line.strip()
        # skip if comment or blank (note: python treats '' as False)
        if line.startswith('#') or (not line): continue
        
        key,value = line.split('=')
        
        # convert value to float or boolean
        key = key.strip()
        if key.startswith('FLAG'):
            value = str2bool(value)
            
        elif key.startswith('STR'):
            value = value.strip()
            
        else: 
            value = matrix(value)
            # Note, convert to matrix first since the numpy.matrix
            # can handle conversion of strings (e.g. ' [1, 2]')
            if output_type == 'ndarray':
                value = array(value).squeeze()
            
            # Save as scalar if value is a scalar
            if value.size == 1:
                value = value.item()
                
        # update dictionary with key:value pair
        dic[key] = value
    
    infile.close()
    return dic

def str2bool(string):
    """
    Returns boolean equivalent for string 'true' or 'false
    while being insensitive to leading/ending spaces or
    upper/lower case
    
    Example:
    >>> flag = str2bool('  True ')
    >>> flag
    True   
    """
    # check input
    if type(string) is not str:
        print 'str2bool(): argument must be a string'
        sys.exit(1)
        
    # strip leading and ending spaces and convert to lower-case
    clean_string = string.strip().lower()
    
    if clean_string == 'true':
        return True
    elif clean_string == 'false':
        return False
    else:
        print 'str2bool():dd \'%s\' not recognized' % clean_string
        sys.exit(1)
        
def ul(string,line_type='='):
    """
    Returns string with underline
    
    Example:
    >>> print(ul('HEADER'))
    HEADER
    ======
    
    Hamid M. May 2012   
    """

    uline = len(string)*line_type    
    return string+'\n'+uline    
        

def ask_ok(prompt, retries=4, complaint='Yes or no, please!'):
    """
    Prompt user for for 'yes' or 'no' response
    Taken from Python Documentation with small modifications
    http://docs.python.org/tutorial/controlflow.html
    
    Example:
    >>> ask_ok('Do you really want to quit?')
    
    Hamid M. May 2012
    """
    while True:
    
        ok = raw_input(prompt).lower()
        
        if ok in ('y', 'ye', 'yes','1'):
            return True
        if ok in ('n', 'no', 'nop', 'nope','0'):
            return False
        retries = retries - 1
        if retries < 0:
            raise IOError('refusenik user')
        print complaint

def count_lines(filepath, print_result=False):
    """
    Count the number of lines in a text file.
    
    Parameters
    ----------
    filepath - path to text file of interest (string)
    
    Returns
    -------
    num_lines - number of lines (integer)
    
    Hamid M. December 2012
    """
    fid = open(filepath,'rb')
    cnt = 0
    for row in fid: cnt += 1
        
    # Print result and close file
    if print_result:
        print 'Number of lines in \'%s\': %i' % (filepath, cnt)
    fid.close()
    
    return cnt

def data_path_list(DATA_PATH, print_summary=False):
    """
    This function returns a list of absolute paths to various files located
    inside a parent folder with multiple subfolders.  For example:
    
    DATA_PATH
        - readme.txt
        - DATA FOLDER 1
            -dataA.csv
        - DATA FODLER 2
            -dataB.csv
            -dataC.mat
            -dataD.txt
            
    This method will return a list of paths to all files inside the subfolders.
    Namely, dataA through D.  Any files inside the top directory will be 
    skipped.  Hence, readme.txt is ignored.
    
    Returns
    -------
    
    List of paths  [[<folder1>, <filename1>, <absolutepath1>],
                    [<folder2>, <filename2>, <absolutepath2>],
                    etc...]
                    
    A sample entry might be: [Control_Laws, flight1.mat, /abs/path/flight1.mat]
    
    This was taken from aemuav_utilities.py and moved here.
    November 25, 2013
    Hamid
    """
    dir_list = os.listdir(DATA_PATH)
    
    return_data = []


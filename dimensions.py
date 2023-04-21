"""
Get Dimensions
Author: Quan Do, Khanh Phan, An Nguyen, Minh Duong
"""

def get_dimensions(name):
    """
    Function that returns all the dimensions of a button
    Parameters:
        name - the button's name
    Returns:
        the left, right, upper, and lower dimensions
    """
    #Play button:
    if name == 'play':
        X_LEFT = 57.6
        X_RIGHT = 729.1
        Y_UP = 430.7
        Y_DOWN = 491.4
    #Linh button:
    elif name == 'linh':
        X_LEFT = 64.6
        X_RIGHT = 250.9
        Y_UP = 184.1
        Y_DOWN = 472.2
    #Seb button:
    elif name == 'seb':
        X_LEFT = 301.6
        X_RIGHT = 487.9
        Y_UP = 184.1
        Y_DOWN = 472.2
    #Graeme button:
    elif name == 'graeme':
        X_LEFT = 530.5
        X_RIGHT = 724.8
        Y_UP = 184.1
        Y_DOWN = 472.2
    #Easy button:
    elif name == 'easy':
        X_LEFT = 65.4
        X_RIGHT = 737.5
        Y_UP = 169.1
        Y_DOWN = 267.1
    #Normal button:
    elif name == 'normal':
        X_LEFT = 65.4
        X_RIGHT = 737.5
        Y_UP = 285.0
        Y_DOWN = 383.0
    #Hard button:
    elif name == 'hard':
        X_LEFT = 65.4
        X_RIGHT = 737.5
        Y_UP = 400.9
        Y_DOWN = 498.9
    #Close button:
    elif name == 'close':
        X_LEFT = 754.6
        X_RIGHT = 766.9
        Y_UP = 30.9
        Y_DOWN = 44.2
    return X_LEFT, X_RIGHT, Y_UP, Y_DOWN
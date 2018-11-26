# Python functions that are called from an erlang instance

def hello(): return "hello"
def goodbye(): return "goodbye"

def testArray(array): 
    array.append(4)
    return array

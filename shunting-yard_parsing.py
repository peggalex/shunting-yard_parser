import re

class Operators:
    _precedence = 0
    _function = lambda x,y: None
    _strings = ('')
    _isLeftAssociative = False
    #left associative means that the operation is not
    # associative, so that the order is important
    #ie x/y =/= y/x for some x,y and
    # x-y =/= y-x

    def getPrecedence(self):
        return self._precedence

    def execute(self,a,b):
        return self._function(a,b)

    def checkString(self,c: 'char'):
        return c in self._strings

    def isLeftAssociative(self):
        return self._isLeftAssociative

    def __str__(self):
        return self._strings[0]

    #ideally, these would not have self in them,
    #as these are all static methods.
    #However, static attributes in python suck,
    #so i'd have to say Operator._precedence etc
    #which means my child classes would need to override

    def outputToString(output: list)->str:
        for e in output:
            

class Add(Operators):
    _precedence = 1
    _function = lambda x,y:x+y
    _strings = ("+")
    _isLeftAssociative = True


class Subtract(Operators):
    _precedence = 1
    _function = lambda x,y:x-y
    _strings = ("-")
    _isLeftAssociative = True

class Multiply(Operators):
    _precedence = 2
    _function = lambda x,y:x*y
    _strings = ("*","x")
    _isLeftAssociative = True

class Divide(Operators):
    _precedence = 2
    _function = lambda x,y:x/y
    _strings = ("/")
    _isLeftAssociative = True

class Exponent(Operators):
    _precedence = 3
    _function = lambda x,y:x**y
    _strings = ("^")
    _isLeftAssociative = False

class OperatorHandelers:
    operators = (Add(),Subtract(),Multiply(),Divide(),Exponent())
    
    def getOperator(c: 'char'):
        for operator in OperatorHandelers.operators:
            if operator.checkString(c):
                return operator
            
        return None

class Stack:

    def __init__(self, items=[]):
        self._items = items

    def pop(self):
        assert(self._items)
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def isEmpty(self):
        return bool(self._items)

    def push(self, item):
        self._items.append(item)

    #@override
    def __repr__(self):
        s=''
        for e in self._items:
            s+=str(e)+","
        return s.strip(",")

    def getItems(self)->list:
        return self._items

class Queue(Stack):

    def __init__(self,items=[]):
        super().__init__(items)

    #@override
    def pop(self):
        assert(self._items)
        return self._items.pop(0)

    #@override
    def peek(self):
        return self._items[0] if self._items else None


multiply = lambda x,y: x*y
divide = lambda x,y: x/y
add = lambda x,y: x+y
subtract = lambda x,y: x-y
toPower = lambda x,y: x**y

operatorDic = {('x','*'):{'func':multiply}, ('/'): divide,\
               ('+'):add, ('-'):subtract, ('^'):toPower}


digitRegexS = "(-?(\\d+|\\.\\d+|\\d+\\.\\d+))"
operatorRegexS = "(\\*|\\/|\\+|\\-|\\^|x)"
#ideally, we would make these brackets into
#non capture groups

regexEquation = re.compile("{}({}{})*".format(digitRegexS,operatorRegexS,digitRegexS))

def getBracket(s)->str:
    numOpen = 0
    for i in range(len(s)):
        if s[i]=="(":
            numOpen+=1
        elif s[i]==")":
            if numOpen==0:
                print(s[:i])
                return s[:i]
            else:
                numOpen-=1
    return ''

def evaluateBrackets(s):
    finalExp = ''
    i=0

    while i<len(s):
        if s[i]!="(":
            finalExp+=s[i]
            i+=1
            continue

        bracket = getBracket(s[i+1:])
        
        if not bracket:
            return False
        
        elif not evaluateBrackets(bracket):
            return False

        finalExp += '0'
        #if the nested brackets are valid, we know that the bracket will return an
        #equation that can be evaluated. So make it zero for regex

        i = i+len(bracket)+2
        #plus 2 to skip the closing bracket

    print('final s: {}, works? {}'.format(finalExp,re.fullmatch(regexEquation,finalExp)))
    return re.fullmatch(regexEquation,finalExp) is not None


while(True):
    equationOrig = input('type equation: ')
    if evaluateBrackets(equationOrig):
        break
    print("invalid string, make sure brackets match and don't use functions like sin, ln or min/max")
            
i = 0
operator = Stack()
output = Queue()

s = equationOrig
lastCharOperator = False
lastCharNum = False
while i<len(equationOrig):
    c = s[i]
    print("c is: {}".format(c))
    print("operator is: {}".format(operator))
    if c.isdigit() or c=='.' or (c=='-' and lastCharOperator):
        num = c
        j=i+1
        while j<len(s):
            c = s[j]
            if c.isdigit():
                num+=c
            elif c=='.':
                assert(num.count('.')<=1)
                #this shoulda been tested with the regex
                num+=c
            else:
                break
            j+=1
        i=j
        output.push(float(num))
        lastCharOperator = False
        lastCharNum = True
        continue
        
    elif c=="(":
        if lastCharNum:
            s = s[:i-1]+"*"+s[i:]
            lastCharNum = False
            i-=1
            # if we have 2(...),
            # should be interpreted
            # as 2*(...)
            # this is really messy way of doing this
            # i should make this whole thing into a
            # fsm, including the regex
            continue
        else:
            operator.push(c)
    elif c==")":
        while not operator.peek()=="(":
            output.push(operator.pop())
        operator.pop()
    else:
        opObj = OperatorHandelers.getOperator(c)
        assert(opObj is not None)
        precedence = opObj.getPrecedence()

        topStack = operator.peek()
        
        while topStack is not None and topStack!= "(" and\
            (topStack.getPrecedence() > precedence or\
            (topStack.getPrecedence() == precedence and\
             topStack.isLeftAssociative()) ):
            #verbose i know

            output.push(operator.pop())
            topStack = operator.peek()
 
        operator.push(opObj)
        lastCharOperator = True
        lastCharNum = False
    i+=1

while operator.peek() is not None:
    output.push(operator.pop())

print("output: {}".format(output))






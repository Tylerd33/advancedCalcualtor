#Advanced Calculator



import pdb

class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          


class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        if self.top == None:
            return True
        return False

    def __len__(self): 
        current = self.top
        if self.isEmpty():
            return 0
        count = 1
        #Adds 1 to count and goes to next part of linked list every loop unitl there is no next
        while current.next != None:
            count+=1
            current = current.next
        return count


    def push(self,value):
        new_node = Node(value)
        #Makes Node and puts new node on top of stack
        if self.isEmpty():
            self.top = new_node
            self.next = None
        else:
            new_node.next = self.top
            self.top = new_node

     
    def pop(self):
        #Gets rid of top of stack and returns it's value
        if self.isEmpty():
            return None
        top_val = self.top.value
        self.top = self.top.next
        return top_val

    def peek(self):
        #Returns top value
        if self.isEmpty():
            return None
        return self.top.value



class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
        '''
        #Returns true if txt isnt empty and txt can be converted to a float, false otherwise
        if txt == None:
            return False
        try:
            float(txt)
        except ValueError:
            return False
        return True
    def inputValid(self, txt):
        #Gets rid of any negative numbers to make checking for valid input easier, block outputs txt without negatives
        txt = list(txt)
        for index in range(len(txt)-2):
            if txt[index] == "-" and self._isNumber(txt[index+1]):
                txt.pop(index)
        txt = "".join(txt)

        #Dict holding count of various important elms in expression
        count_dic = {"oper_count" : 0, "num_count" : 0,  "(_count": 0, ")_count" : 0}
        prev_op = ""
        same_num = False
        prev_operator = False
        for elm in txt:
            #New num count is allowed after old num is over
            if self._isNumber(elm) == False and elm != ".":
                same_num = False
            #Counts occurences of certain elms in list in a dictionary, returns False if current elm is operator prev operator is true
            #Prev operator is set to false when a num is elm or )( is elm
            if elm in "+-*/^":
                count_dic["oper_count"] += 1
                if prev_operator == True:
                    return False
                prev_operator = True
            #Only counts number if elm is number and elm is not a continuation of a prev number
            elif (self._isNumber(elm) or elm == ".") and same_num == False:
                count_dic['num_count'] += 1
                same_num = True
                prev_operator = False
            elif elm == "(":
                count_dic['(_count'] += 1
                prev_operator = False
            elif elm == ")":
                prev_operator = False
                count_dic[')_count'] += 1
            #Returns False if not a  num/operator/space
            elif same_num == False and elm != " ":
                return False
            #Returns False if detects a ) before it's corresponding (
            if count_dic[")_count"] > count_dic["(_count"]:
                return False
        #Returns False if there is an invalid ration of ( : ) or operators : numbers
        if count_dic["(_count"] != count_dic[")_count"]:
            
            return False
        if count_dic["oper_count"]+1 != count_dic["num_count"]:
            return False
        return True


    def _checkPrecedence(self, operator):
        #lowest precedence, 10 : highest precedence, returns precedence of input
        #Exact val of precedent is not important, only its relation to other precedences
        precedence_dict = {"+":3, "-":3, "*":4, "/":4, "^": 8 }
        return precedence_dict[operator]

    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x._getPostfix('     2 ^       4')
            '2.0 4.0 ^'
            >>> x._getPostfix('          2 ')
            '2.0'
            >>> x._getPostfix('2.1        * 5        + 3       ^ 2 +         1 +             4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2*5.34+3^2+1+4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('( .5 )')
            '0.5'
            >>> x._getPostfix ('( ( 2 ) )')
            '2.0'
            >>> x._getPostfix ('2 * (           ( 5 +-3 ) ^ 2 + (1 + 4 ))')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('(2 * ( ( 5 + 3) ^ 2 + (1 + 4 )))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('((2 *((5 + 3  ) ^ 2 + (1 +4 ))    ))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2* (       -5 + 3 ) ^2+ ( 1 +4 )')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'

            # In invalid expressions, you might print an error message, adjust doctest accordingly
            # If you are veryfing the expression in calculate before passing to postfix, this cases are not necessary

            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('     2 * 5 + 3  ^ * 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5      + 3 ) ^ 2 + ( 1 +4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^  2 + ) 1 + 4 (')
            >>> x._getPostfix('2 *      5% + 3       ^ + -2 +1 +4')
        '''

        if self.inputValid(txt) == False:
            return 
        postfixStack = Stack()  # method must use postfixStack to compute the postfix expression
        postfix = ""
        #Goes through txt str by index
        skip_ind = False
        is_op = False
        for index in range(len(txt)):
            #Every number after another number is ignored utilizing skip_ind = True
            #When the index of txt is not a . or num then the first number after is not ignored (done by skip_ind = False)
            if self._isNumber(txt[index]) == False and txt[index] != ".":
                skip_ind = False
            #If it is last index of str, then nex_index_val = None, as otherwise would cause error
            temp_ind = index + 1
            if index == len(txt) - 1:
                nex_index_val = None
            else:
                nex_index_val = txt[temp_ind]

            #Checks if a negative sign is actually a operand or part of a negative, if op, is_op = True
            is_op = False
            if index != 0 and txt[index] == "-" and self._isNumber(txt[index-1]):
                is_op = True

            #If current index is number then gets every num and . after it and makes it into a single string, then adds float version of string to postfix
            #Ex: current index  3 and str is 3.56 + ... , adds 3.56 to postfix
            if is_op == False and (txt[index] == "." or self._isNumber(txt[index]) or txt[index] == "-" and self._isNumber(nex_index_val)):
                
                
                num_str = txt[index]
                #num_str is every . and num after the original num  
                while temp_ind != len(txt) and self._isNumber(nex_index_val) or nex_index_val == ".":
                    num_str += nex_index_val
                    temp_ind += 1

                    #if the next theoretical index is not in range of txt's index, nex_index_val would be invalid, so the code ignores this case
                    if temp_ind != len(txt):
                        nex_index_val = txt[temp_ind]
                
                #If skip_ind is True does not add num to postfix as it has already beena added
                if skip_ind == True:
                    pass
                else:                   
                    postfix += str(float(num_str)) + " "
                #Next num is always skipped if previos index was a number or .77
                skip_ind = True


            elif txt[index] == "(":
                postfixStack.push(txt[index])
            #Pops every operator out of stack that is after ( while adding them to postfix, also gets rid of the first (
            elif txt[index] == ")":
                while postfixStack.peek() != "(":
                    postfix += postfixStack.pop() + " "
                postfixStack.pop()
                

            # If index is operand, pop and add pop to postfix until next operator has lower precedence then current operator
            elif txt[index] in "+-*/^":
                stop = False
                while stop == False and (postfixStack.isEmpty() != True and postfixStack.peek() in "+-*/^" and self._checkPrecedence(txt[index]) <= self._checkPrecedence(postfixStack.peek())):
                    #Stops program if ^ is next to ^
                    if txt[index] == "^" and postfixStack.peek() == "^":
                        stop = True
                    else:
                        postfix += postfixStack.pop() + " "
                postfixStack.push(txt[index])

        #After finishes going through str, pops everything out of stack adding to postfix
        while postfixStack.isEmpty() == False:
            postfix += postfixStack.pop() + " "

        #Gets rid of last " " if it exists and returns postfix
        if postfix[-1] == " ":
            postfix = postfix [0 : -1]
        return postfix
            

    @property
    def calculate(self):
        '''
            calculate must call _getPostfix
            calculate must create and use a Stack to compute the final result as shown in the video lecture
            
            >>> x=Calculator()
            >>> x.setExpr('4        + 3 -       2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 +          3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('      4 +           3.65  - 2        / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25      * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr('2-3*4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('7^2^3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ((( 10 - 2*3 )) )')
            >>> x.calculate
            12.0
            >>> x.setExpr('      8 / 4 * (3 - 2.45 * ( 4   - 2 ^ 3 )       ) + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * ( 4 +        2 * (         5 - 3 ^ 2 ) + 1 ) + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 +         3 * (2 + ( 3.0) * ( 5^2-2 * 3 ^ ( 2 )         ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 /3 ) ) - 2 / 3^ 2')
            >>> x.calculate
            1442.7777777777778
            

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            >>> x.setExpr(" 4 ++ 3+ 2") 
            >>> x.calculate
            >>> x.setExpr("4  3 +2")
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 *( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( *10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
            >>> x.setExpr('(    3.5 ) ( 15 )') 
            >>> x.calculate
            >>> x.setExpr('3 ( 5) - 15 + 85 ( 12)') 
            >>> x.calculate
            >>> x.setExpr("( -2/6) + ( 5 ( ( 9.4 )))") 
            >>> x.calculate
        '''
        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()   # method must use calcStack to compute the  expression

        #Gets postfix of infix expr(self.getExpr)
        postfix = self._getPostfix(self.getExpr)
        if postfix == None:
            return None
        #Makes postfix into a list of operands/nums
        postfix = postfix.split(" ")
        result = 0

        #Perform calculation by pushing all nums to stack and performing operation on 2 highest nums in stack when comes across operand, navigates through list of postfix
        for elm in postfix:
            if self._isNumber(elm):
                calcStack.push(elm)
            else:
                num1 = float(calcStack.pop())
                num2 = float(calcStack.pop())
                if elm == "+":
                    calcStack.push(num2+num1)
                if elm == "-":
                    calcStack.push(num2-num1)
                if elm == "*":
                    calcStack.push(num2*num1)
                if elm == "/":
                    calcStack.push(num2/num1)
                if elm == "^":
                    calcStack.push(num2**num1)
                    
        #returns last num of stack which is the result of the expression
        result = float(calcStack.peek())
        return result


class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 * ( x1 - 1 );x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * ( x1 / 2 );x1 = x2 * 7 / x1;return x1 * ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * ( x1 / 2 )': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''
        #Checks if first elm is a number
        if word[0].isalpha() == False:
            return False
        #Returns false if invalid syntax in word
        for elm in word:
            if elm.isalnum() == False:
                return False
        return True
       

    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 * ( x1 - 1 )')
            '7 * ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        
        #var is a list of expr
        r_exp_copy = expr.split(" ").copy()
        #Checks every index of list returning false if invalid variable, replacing variables with their corresponding nums in self.states dict
        for var in r_exp_copy:
            if self._isVariable(var):
                if var not in self.states:
                    return
                expr = expr.replace(var, str(self.states[var]))
        #Returns statement with var replaced with respective nums
        return expr
    
    def calculateExpressions(self):
        self.states = {} 
        calcObj = Calculator()     # method must use calcObj to compute each expression
        #Makes list of every line
        all_exp_split = self.expressions.split(";")
        current_vals = {}
        final_dict = {}
        #Goes through every line individually
        for exp in all_exp_split:
            #Splits each line into individual nums/operators/var
            temp_spl = exp.split(" ")

            #If return is in beggining of line, return calculated statement
            if temp_spl[0] == "return":
                r_exp = exp[6:].strip()
                r_exp_copy = r_exp.split(" ")
                #Replaces all vars with their respective values
                for var in r_exp_copy:
                    if self._isVariable(var):
                        r_exp = r_exp.replace(var, str(current_vals[var]))
            #converts list back to str
                r_exp = "".join(r_exp)
                calcObj.setExpr(r_exp)
                #Updates self.states before function ends
                self.states = current_vals
                #Adds newest return val to dict we will return
                final_dict["_return_"] = calcObj.calculate
                return final_dict
            #Saves exp as og_exp for later
            og_exp = exp
            var_name, r_exp = exp.split("=")
            var_name = var_name.strip()
            #Returns false if invalid var name
            if self._isVariable(var_name) == False:
                return
        
            #makes list
            r_exp = r_exp.strip()
            r_exp_copy = r_exp = r_exp.split(" ")
            #Replaces all vars with known vars
            r_exp = " ".join(r_exp)
            for var in r_exp_copy:
                if self._isVariable(var):
                    if var in r_exp:
                        r_exp = r_exp.replace(var, str(current_vals[var]))
            #converts list back to str
            r_exp = "".join(r_exp)
            calcObj.setExpr(r_exp)
            current_vals[var_name] = calcObj.calculate
            final_dict[og_exp] = current_vals.copy()

if __name__=='__main__':
    import doctest
    doctest.testmod()
    #doctest.run_docstring_examples(Calculator, globals(), name='HW3',verbose=True)
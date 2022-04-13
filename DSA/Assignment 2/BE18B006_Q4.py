# Reference used for pseudocode: https://simplesnippets.tech/infix-to-postfix-conversion-using-stack-data-structure-with-c-program-code/

def InfixToPostfix(infix):
    '''
    Input: a string representation of an infix expression
    Output: a postfix expression as a list of elements
    '''
    postfixopsstack = []
    postfixexp = []
    precedence = {'+' : 1, '-' : 1, '/' : 2, '*' : 2, '^' : 3, '(': -1, ')':-1}
    ops = ['+', '-', '/', '*', '^']
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    i, l = 0, len(infix)
    
    while i < l:
        if infix[i] in numbers:
            num, j = str(infix[i]), i+1
            if infix[j] not in numbers:
                postfixexp.append(int(num))
                i = j
            else:
                while infix[j] in numbers:
                    num += infix[j]
                    if j <= l - 2: j += 1
                    else: break
                postfixexp.append(int(num))
                i = j + 1

        elif infix[i] == '(':
            postfixopsstack.append('(')
            i += 1
        
        elif infix[i] == ')':
            stacktop = postfixopsstack.pop()
            while stacktop != '(' and len(postfixopsstack) > 0:
                postfixexp.append(stacktop)
                stacktop = postfixopsstack.pop()
            i += 1
        
        elif infix[i] in ops:
            if len(postfixopsstack) == 0:
                postfixopsstack.append(infix[i])
                i += 1
            
            else:
                if precedence[infix[i]] > precedence[postfixopsstack[-1]]:
                    postfixopsstack.append(infix[i])
                    i += 1
                elif precedence[infix[i]] == precedence[postfixopsstack[-1]] and infix[i] == '^':
                    postfixopsstack.append(infix[i])
                    i += 1
                
                else:
                    while len(postfixopsstack) > 0 and precedence[infix[i]] <= precedence[postfixopsstack[-1]]:
                        postfixexp.append(postfixopsstack.pop())
                    postfixopsstack.append(infix[i])
                    i += 1

    while len(postfixopsstack) > 0:
        postfixexp.append(postfixopsstack.pop())

    return postfixexp
        
def EvaluatePostfix(postfix):
    '''
    Input: postfix expression as a list of elements 
    Output: numerical value of the postfix expression
    '''
    ops = ['+', '-', '/', '*', '^']
    operandstack = []
    for i in range(len(postfix)):
        if postfix[i] not in ops:
            operandstack.append(postfix[i])

        else:
            operand1 = operandstack.pop()
            operand2 = operandstack.pop()
            if postfix[i] == '+': operandstack.append(operand2 + operand1)
            elif postfix[i] == '-': operandstack.append(operand2 - operand1)
            elif postfix[i] == '/': operandstack.append(operand2 / operand1)
            elif postfix[i] == '*': operandstack.append(operand2 * operand1)
            elif postfix[i] == '^': operandstack.append(operand2 ** operand1)

    return operandstack[0]

infix = "3^4/(5*6)+10"
#infix = input()
postfix = InfixToPostfix(infix)
print("Postfix expression: ", postfix)
result = EvaluatePostfix(postfix)
print("Value of expression: ", result)
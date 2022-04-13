# DSA for Biology - Assignment 2
# Template for question  - Stacks and queues

""" Add your classes/functions here """
class Queue():
    def __init__(self, elems):
        self.queue = elems

    def preference_nomatch(self):
        self.queue.append(self.queue.pop(0))

    def preference_match(self):
        self.queue.pop(0)

    def length(self):
        return len(self.queue)
    
    def copy(self):
        return self.queue

    def __str__(self):
        return '{0}'.format(list(self.queue))
        
    def peek(self):
        if(self.queue != []):
            return self.queue[0]


def Simulate_Sandwitch_for_Students(Students, Sandwitch):
    """ 
    (list of integers, list of integers) -> (int)
    Returns the number of students that were unable to eat.
    >>> Simulate_Sandwitch_for_Students([1,1,0,0], [0,1,0,1])
    0
    >>> Simulate_Sandwitch_for_Students([1,1,1,0,0,1], [1,0,0,0,1,1])
    3
    """
    """ Add your code here """
    Studentsqueue = Queue(Students)
    Sandwitchqueue = Queue(Sandwitch)
    output = 0
    while Sandwitchqueue.length() > 0:
        if Studentsqueue.peek() == Sandwitchqueue.peek():
            Studentsqueue.preference_match()
            Sandwitchqueue.preference_match()
        else:
            Studentsqueue.preference_nomatch()
            studentcopy, sandwitchvalue = Studentsqueue, Sandwitchqueue.peek()
            i, l = 0, Studentsqueue.length()
            while i < l - 1:
                if studentcopy.peek() == sandwitchvalue:
                    break
                else:
                    studentcopy.preference_nomatch()
                i += 1
            if i == l - 1:
                output = l
                return output
    return 0

print(Simulate_Sandwitch_for_Students([1,1,0,0], [0,1,0,1]))
print(Simulate_Sandwitch_for_Students([1,1,1,0,0,1], [1,0,0,0,1,1]))
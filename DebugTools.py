import inspect
from functools import partial

class printv():
    def __init__(self, *vars, stop_in_cicle=False):
        self.stop_in_cicle = stop_in_cicle
        self.counter = 0
        self.printv(*vars)

    def printv(self, *vars):
        if(len(vars) != 0 and (not self.stop_in_cicle or self.counter == 0)):
            print(f"\n--- COUNTER:{self.counter} ---")
            self.counter += 1
            for ix in range(0, len(vars)-1, 2):
                name = vars[ix]
                obj = vars[ix+1]
                tipo = type(obj)
                print("Name:", name)
                if(tipo == set or tipo == tuple or tipo == list):
                    #trova sottotipi
                    sottotipi = set()
                    for el in obj:
                        sottotipi.add(type(el).__name__)

                    #costruisci stringa
                    st = f"Type: {tipo.__name__}["
                    ct = 0
                    lenght = len(sottotipi)
                    for s in sottotipi:
                        st += f"{s}"
                        ct +=1
                        if(ct != lenght):
                            st += ", "
                    st += "]"
                    print(st)
                elif(tipo == dict):
                    sottotipi_keys = set()
                    sottotipi_vals = set()
                    obj:dict
                    for el in obj.keys():
                        sottotipi_keys.add(type(el).__name__)
                    for el in obj.values():
                        sottotipi_vals.add(type(el).__name__)

                    #costruisci stringa
                    st = f"Type: {tipo.__name__} keys:["
                    ct = 0
                    lenght = len(sottotipi_keys)
                    for s in sottotipi_keys:
                        st += f"{s}"
                        ct +=1
                        if(ct != lenght):
                            st += ", "
                    st += "]"

                    st += f" vals:["
                    ct = 0
                    lenght = len(sottotipi_vals)
                    for s in sottotipi_vals:
                        st += f"{s}"
                        ct +=1
                        if(ct != lenght):
                            st += ", "
                    st += "]"
                    print(st)
                else:
                    print(f"Type: {tipo.__name__}")
                print("Value:", obj)
                print("---")




def print_stack():
    stack_length:int = len(inspect.stack())
    
    print(f"\n@@@PRINT STACK of function: {inspect.stack()[1].function}")
    for ix in range(2, stack_length):
        caller = inspect.stack()[ix]  # Get the caller's stack frame
        caller_function = caller.function  # Get the function name
        caller_filename = caller.filename  # Get the filename
        caller_line = caller.lineno  # Get the line number
        print(f"Called by function: {caller_function}, in file: {caller_filename}, at line: {caller_line}")
    print()



class exo():
    def __init__(self):
        self.dic = dict()
        self.limit = 1

    def exo(self, *args):
        if args[0] not in self.dic:
            partial_fun = partial(args[0], *args[1:])
            self.dic[args[0]] = (partial_fun, 0)

        for fun, tup in self.dic.items():
            partial_fun = tup[0]
            ct = tup [1]
            if ct < self.limit:
                partial_fun()
                self.dic[fun] = (partial_fun, ct+1)


def quack(a):
    print(f"quack {a}")
if __name__ == "__main__":
    #prove
    d = dict({"c": 4, "d": 3.4})
    s = set({"a", 1, 2.1})

    pr = printv(stop_in_cicle=True)

    for i in range(10):
        pr.printv("d",d,"s",s)

    par = 1
    p = exo()
    for i in range(2):
        p.exo(quack, par)
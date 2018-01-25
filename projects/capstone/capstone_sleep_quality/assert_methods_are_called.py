import sys
# use the code from following site
# "Assert that a method was called in a Python unit test"
#https://stackoverflow.com/questions/1984325/explaining-pythons-enter-and-exit
class assertMethodsAreCalled(object):
    def __init__(self, objs_and_methods):
        self.objs = objs_and_methods.keys()
        self.method = objs_and_methods.values()

    def called(self, *args, **kwargs):

        self.method_called = True
        self.orig_method(*args, **kwargs)

    def __enter__(self):#It is called when with statement called.
        self.orig_method = getattr(self.obj, self.method) # get the actual target method
        setattr(self.obj, self.method, self.called) #set called method to the target function
        self.method_called = False # method_called is False in dafault

    def __exit__(self, exc_type, exc_value, traceback):# It is called end of with statement
        #check if called method is inserted to the target method
        assert getattr(self.obj, self.method) == self.called, "method %s was modified during assertMethodIsCalled" % self.method
        # If an exception was thrown within the block, we've already failed.
        if traceback is None:
            assert self.method_called,"method %s of %s was not called" % (self.method, self.obj)
from .threading_utils import call_slow_function, has_call_finished, get_call_value

#step 1
#validate if the player guid is found on the database and is not blacklsited

#step 2
#validate arguments

#step 3
#insert into the database

#step 4
#return success or error

def submit_review(my, arguments):

    return ["submit_review", 42, True, (1, 2)]

def submit_bug_report(my, arguments):
    return ["submit_bug_report", 42, True, (1, 2)]

def submit_rating(my, arguments):
    return ["submit_rating", 42, True, (1, 2)]


def fibonacci(n):
    """
    Returns the n-th Fibonacci number. Is slow for large numbers.
    """
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


def call_slow_fibonacci(n):
    """
    Call a slow function.
    Returns a Thread ID that has to then be polled from SQF to check if the
    function finished.
    To execute this function, call:
    ["thread_example.call_slow_fibonacci", [35]] call py3_fnc_callExtension
    Get the thread ID and use it with:
    ["thread_example.has_call_finished", [thread_id]] call py3_fnc_callExtension
    When ot returns True, you can get the value by doing:
    ["thread_example.get_call_value", [thread_id]] call py3_fnc_callExtension
    """
    return call_slow_function(fibonacci, (n,))


has_call_finished  # noqa - this function has been imported from threading_utils.py
get_call_value  # noqa - this function has been imported from threading_utils.py



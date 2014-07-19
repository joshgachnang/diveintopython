

3.8. Summary
------------

The `odbchelper.py` program and its output should now make perfect
sense.

    def buildConnectionString(params):
        """Build a connection string from a dictionary of parameters.

        Returns string."""
        return ";".join(["%s=%s" % (k, v) for k, v in params.items()])

    if __name__ == "__main__":
        myParams = {"server":"mpilgrim", \
                    "database":"master", \
                    "uid":"sa", \
                    "pwd":"secret" \
                    }
        print buildConnectionString(myParams)

Here is the output of `odbchelper.py`:

    server=mpilgrim;uid=sa;database=master;pwd=secret

Before diving into the next chapter, make sure you're comfortable doing
all of these things:

-   Using the Python IDE to test expressions interactively
-   Writing Python programs and [running them from within your
    IDE](../getting_to_know_python/testing_modules.html "2.6. Testing Modules"),
    or from the command line
-   [Importing
    modules](../getting_to_know_python/everything_is_an_object.html#odbchelper.import "Example 2.3. Accessing the buildConnectionString Function's doc string")
    and calling their functions
-   [Declaring
    functions](../getting_to_know_python/declaring_functions.html "2.2. Declaring Functions")
    and using
    [`doc string`s](../getting_to_know_python/documenting_functions.html "2.3. Documenting Functions"),
    [local
    variables](declaring_variables.html "3.4. Declaring variables"), and
    [proper
    indentation](../getting_to_know_python/indenting_code.html "2.5. Indenting Code")
-   Defining
    [dictionaries](index.html#odbchelper.dict "3.1. Introducing Dictionaries"),
    [tuples](tuples.html "3.3. Introducing Tuples"), and
    [lists](lists.html "3.2. Introducing Lists")
-   Accessing attributes and methods of [any
    object](../getting_to_know_python/everything_is_an_object.html "2.4. Everything Is an Object"),
    including strings, lists, dictionaries, functions, and modules
-   Concatenating values through [string
    formatting](formatting_strings.html "3.5. Formatting Strings")
-   [Mapping lists](mapping_lists.html "3.6. Mapping Lists") into other
    lists using list comprehensions
-   [Splitting
    strings](joining_lists.html "3.7. Joining Lists and Splitting Strings")
    into lists and joining lists into strings

  


Error Handling
==============

Bagel's error handling is based around two separate concepts:

1. The ``Option`` and ``Result`` types.
2. Task failure.

``Option`` and ``Result``
-------------------------

Whereas in many programming languages, such as Java, any value can be a
``null``, in Bagel a value must always be present. Therefore Bagel offers the
``Option`` type, which is a way of specifying that there may be either a value,
or ``None``::

    def f(x: Option<Text>) -> Text:
        match as:
            as Some(value):
                return value
            as None:
                return "Nothing to see here..."

Bagel forces you to handle the ``None`` cases. ``Result`` is similar to
``Option``, except it includes a failure value. A common pattern is to define
an enum which includes possible error conditions::

    enum class EmailValidationError:
        MissingHostname
        MissingMXRecord
        # Some email providers, such as gmail, have a minimum length for the
        # local component of an address
        LocalNameTooShort(minimum_length: UInt)

    def handle_email_address(email: Text) -> Text:
        match validate_address(email):
            as Ok(address):
                return "Ok: " + address
            as Err(EmailValidationError.MissingHostname):
                return "ERROR: There is no hostname"
            as Err(EmailValidationError.MissingMXRecord):
                return "ERROR: This domain has no MX record"
            as Err(EmailValidationError.LocalNameTooShort(length)):
                return "ERROR: The local component must be at least {:d} characters".format(length)

Sometimes a function returns an ``Option`` or ``Result``, but you aren't sure
how to handle the errors yet. In these cases Bagel offers an "assertion
oriented" mechanism for handling errors::

    Some(x) = function_which_returns_an_option()

This destructuring form of assignment will extract ``x`` if there is a value,
otherwise it will trigger a task failure.

Task failures
-------------

Each Bagel task which is running executes independently, and can fail
independently.

When a Bagel task fails, it does not stop any of the other running tasks, and
the failure cannot be stopped, it can only be observed.

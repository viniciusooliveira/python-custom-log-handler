#Python Custom Log Handler

This project was created to study how Python log handlers work.

In this example, a basic Handler with record buffering was created, with maximum buffer size, time between flushes and the amount to trigger the flush. 

> The send method is intentionally simple, with just a print to the console, so you can implement it however you like, whether it's just on the console, with an external API call, sending it to a Kafka stream or any other implementation.



##How to run

As the project only has a dependency on `Python 3.X`, without external dependencies, just run the following command:

- `python main.py`
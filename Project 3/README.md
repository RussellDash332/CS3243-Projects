## Logs Processor

Submitting the exact same code multiple times to CodePost is somewhat painful. But what's more painful is the inability to have more iterations using the autograder's agent.

Introducing `process_logs.py`! The process is quite simple.
```
.
|_ logs                 -> to store all the logs
|  |_ 001.txt
|  |_ 002.txt
|
|_ process_logs.py      -> to be run every new log insertion
|_ log.txt              -> to insert new log
```

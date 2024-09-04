# JujuLogAnalyser

The goal of the project was to develop a command-line tool to analyse Juju debug logs
where it took the log file as mandatory argument and a charm as an optional argument when
it was available. The tool counts log messages by severity, charms and identifies any
duplicate messages and the overall summary of the logs.
Assumptions:

1. controller-0: 01:47:48 INFO juju.worker.apicaller [b97292] "machine-0" successfully
   connected to "localhost:17070"
   After looking at the file, the format was assumed to be as follows:
   <CharmName>: <Timestamp> <Severity> juju.<component> <Message>
   Lines with this format were processed while the others were ignored.
2. Four severities were considered: INFO, DEBUG, WARNING and ERROR
3. Empty lines will be ignored
   The output includes:
4. Severity Counts
5. Duplicate Messages
6. Severity Proportions
7. Total Messages
   Total time spent on this project was about 6 hours.
   The main challenge that I faced in this project was that I had never worked with Regular
   Expressions before. Being able to learn Regex, design it and test it was the most challenging
   part.
   Resources used:
8. https://juju.is/docs/juju/log
9. https://newrelic.com/blog/how-to-relic/extracting-log-data-with-regex
10. https://www.w3schools.com/python/python_regex.asp

# Hashpecker
Hashpecker is a tool to organize a network of computers to perform a distributed brute-force attack against a hash.

## How to use
This script is only to be used in cooperation with [Hashpecker server](http://brute.heliohost.org). Make sure you have [Python](https://www.python.org) installed in your system.

Run `cmd.exe` on Windows or Terminal on Mac OS and type the following

    python Hashpecker_client.py
    
Then fill in the form suggested. The scan of your local network will begin. Make sure you have at least one machine with [Hashpecker server](http://brute.heliohost.org) running in it. Unless you've supplied incorrect parameters, the bruteforce process will begin _on the machines where [Hashpecker server](http://brute.heliohost.org) is running_, _not on your computer_ (this is the aim of distributed computing).

## Getting results 
When the password is found, the machine that found it reports success and the client shows it to you and terminates. All connections are handled properly on both client and server.

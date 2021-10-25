# EventCrawler
Python code that crawls DePauw's events from the web and notifies via email and discord

The project consists of 2 parts, the crawler and the service

## Crawler

The crawler uses normal ``` requests ``` library to the site's api to get all the events and load into memory. The process is done daily at 9AM.

## Service

### Email
Every day at 10AM, the program will send an email consists of all the events happening of the given day.

### Discord

Every day at 10AM, the program will send a discord message consists of all the events happening of the given day. <br>
At the same time, the discord bot also takes commands such as:
* ``` !all ``` for all events
* ``` !today ``` for today's events
* ``` !tomorrow ``` for tomorrow's events

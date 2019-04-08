# Good-Bull-Schedules
Open-source scheduling server for Texas A&amp;M University students, written in Django.

## Goals
- Create an open, no-auth-needed API for students to analyze TAMU course/section data without having to create their own scrapers.
- Create an intuitive, content-based search interface that allows students to search courses based on the content they cover, not just keyword matching.
- Provide a readable, modular, and extensible (in order of priority) backend server for helping students make their schedules.


## Setting Up

This app relies on:
- Python3 for running the webserver
- Redis for caching and improving overall response times for the data API.
- PostgreSQL for storing data.

To run Good-Bull-Schedules, you'll need to have [Docker](https://docs.docker.com/install/) and [Docker Compose](https://docs.docker.com/compose/install/) installed.

To set up the application:

1. `docker-compose up --build` will start the cluster
2. `docker ps` will list the running containers. Find the container labeled `good_bull_schedules_web...`, and remember the container ID.
3. `docker exec -it <CONTAINER ID> /bin/bash` will allow you to interact with the container
4. To populate the database, you'll need to run the following commands inside of the `good_bull_schedules_web...` container:
    1. `python3 manage.py scrape_courses` will scrape course information (approximately 5 minutes)
    2. `python3 manage.py scrape_sections` will scrape all section data from 2009 to present. This takes a long time (several hours). If you don't particularly care about the entire dataset, and just want a small part of it, run `python3 manage.py scrape_sections --shallow`.
    3. `python3 manage.py scrape_grades` will download, parse, and store grade distributions for all sections. (roughly 30 minutes)

You should be good to go now! Unless there are significant database changes, you shouldn't have to re-run the above scripts again. Navigate to `localhost:8000`, and go nuts!


## Contributing
We'd love to have you contribute! We want to encourage all kinds of developers (inexperienced and experienced) to contribute to this project, to make it the best that it can be.

## Future Goals
- Adding courses to a student's personal calendar.
- Create a system based on schedule clusters to recommend classes to students based on their schedule.
- Implement a comment/rating system for students to provide feedback on courses for further analytics.

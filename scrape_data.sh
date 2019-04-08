docker exec good-bull-schedules python3 manage.py scrape_courses --settings=goodbullschedules.settings.docker
docker exec good-bull-schedules python3 manage.py scrape_sections --settings=goodbullschedules.settings.docker
docker exec good-bull-schedules python3 manage.py search_index --rebuild --settings=goodbullschedules.settings.docker -f
docker exec good-bull-schedules python3 manage.py scrape_grades --settings=goodbullschedules.settings.docker
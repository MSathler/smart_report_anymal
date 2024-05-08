# smart_report_anymal
This repository contains a improved way to see ANYmal Mission Reports

The application watch modifications on .xml files and create the html files based in mission names.

Another code host the webpage that contains the visualization folder and report files.

## Docker

That repository has docker image ready for use:

            docker pull msathler/anymal_report:latest

This repository contains an example of docker compose file to run the application. Pay attention to the folder volume (default ~/.ros/reports) and hosted port (default 8000). If necessary, this informations can be modified. 

To run the docker compose run:

            docker-compose -f <path-to-your-compose-file> up

            or

            docker compose -f <path-to-your-compose-file> up

## Video

https://github.com/MSathler/smart_report_anymal/assets/51409770/76f88f25-6493-4ad6-b2d9-b314dd3fff47


## To-Do:

The actual format translate the information to Portuguese format, it can be formated to another language.
![](img_for_readme/main.jpg)
____
**<span style='color:rgb(222, 100, 161)'>This project is a web service that performs the following functions:</span>**
+ Create a user with the given: name, unique user ID and UUID access token (as a string) for the given user;
+ For each user - saving the audio recording in wav format, converting it to mp3 format and writing to the database and providing a link to download the audio recording.
____
**<span style='color:rgb(222, 100, 161)'>Instructions for building a docker image with a service, setting it up and running it.</span>**
+ This option also starts the database and the pgadmin4 administration tool.
+ The start settings for running containers are located in the docker-compose.yml file
+ The Dockerfile contains instructions for building the audio_base_service service image.
1. Run with docker-compose: docker compose up -d
2. Stop and remove Docker-compose containers: docker compose down
3. View information about running Docker-compose processes: docker compose ps
4. View logs in Docker-compose: docker compose logs
____
**<span style='color:rgb(222, 100, 161)'>Starting the service in Docker:</span>**
1. Building the application image: docker build -t audio_base_service .
2. Create a container and run it: docker run -d --name mycontainer -p 8080:8080 -e DB_URI=postgresql://audio_user:cfytr666131@localhost/audio_base_servicedb audio_base_service
____
**<span style='color:rgb(222, 100, 161)'>Starting a service without a container:</span>**
uvicorn app.main:app --host "0.0.0.0" --port "8080"
____
**You can check the performance of the service by going to the file: testapi.py** 

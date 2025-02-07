Javan-VRC is an AI prototype for the extraction of Mexican food recipes from videos extracted from youtube or uploaded by the user.
This project works with the extraction of information from the audio and frames of the videos. Once the ingredients and recipe are extracted, it will be downloaded as a PDF or TXT file, depending on what has been selected before starting the extraction process.

##The project is divided into two parts:
	-. backend : app.py , is the REST API developed in a mini framework of python "Flask", to serve raw requests.

	-. frontend: is the portal, it is made it in ReactJS

##Requirements:

To run the project automatically, you need to have docker and docker-compose installed.
Each folder (frontend, backend) has its own dockerfile for image and volume survey.

##Run project:
	1-. By console we place ourselves in the root folder of the project and execute the following command  

	"docker-compose up"

	2-. We expect you to install all the dependencies, create and lift the images and docker volumes.

	3-. then we go to our browser and enter the url "localhost"   

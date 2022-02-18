InsurancePremiumPrediction
Intention of this implementation:
The main intention for creating this project is to acquire the knowledge of real time ml project implementation with modular coding standards.

Problem Statement:
This project is all about creating an machine learning algorithm, that helps the user to know their premium by providing the required input.

Appoach :
Data Exploration : I started exploring dataset using pandas,numpy,matplotlib and seaborn.

Data visualization : Plotted graphs to get insights about dependent and independent variables.

Feature Engineering : Removed missing values and created new features as per insights.

Model Selection I : 1. Tested all base models to check the base accuracy.

Model Selection II : Performed Hyperparameter tuning using randomizedSearchCV.

Pickle File : Selected model as per best accuracy and created pickle file.

Webpage & deployment : Created a webform that takes all the necessary inputs from user and shows output. And deployed the project on heroku

Deployment link:https://insurance2022.herokuapp.com/
Technologies used:
1.python 2. Sklearn(Building a model) 3. Flask 4. Pandas, Numpy(Data manipulation) 5. Database (Cassandra, for Storing the inputs) 6. gunicorn(Heroku) 7. HTML(UI)
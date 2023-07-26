# Drive Smart Texas

Drive Smart Texas is a web application designed to track and report traffic accidents. The application allows users in Texas to assess the safety of their routes based on historical accident data and report new incidents.

## How it Works

Users input their start and end locations along with the time of day and current weather conditions. The application then retrieves historical accident data for the proposed route. Users can also report new incidents by submitting details such as location, severity, weather condition, and a description of the accident. The accident data comes from a subset of a Kaggle accident dataset, where data was collected all over the United States using multiple traffic APIs from February 2016 to March 2023. You can view the Kaggle page [[here]](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents).

## Features

1. **Accident Query**: Retrieve historical accident data based on user-inputted route and environmental conditions.
2. **Accident Reporting**: Provide a means for users to report new incidents.

## Tech Stack

* Python
* Flask
* MySQL
* ClearDB
* HTML
* Google Geocoding API
* Heroku

## Deployment

The application is deployed on Heroku. You can visit the application at [[drive-smart-texas]](https://drive-smart-texas-498e9b25a4c3.herokuapp.com/).

## Contributors

* Julia Donato - Flask app development, HTML creation, Heroku deployment
* Pooja Rajan - MySQL database setup, query creation, data analysis

## Acknowledgements

Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, and Rajiv Ramnath. “A Countrywide Traffic Accident Dataset.”, 2019.

Moosavi, Sobhan, Mohammad Hossein Samavatian, Srinivasan Parthasarathy, Radu Teodorescu, and Rajiv Ramnath. "Accident Risk Prediction based on Heterogeneous Sparse Data: New Dataset and Insights." In proceedings of the 27th ACM SIGSPATIAL International Conference on Advances in Geographic Information Systems, ACM, 2019.

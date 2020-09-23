# TROCAS Panel App

Code and data used in the TROCAS Panel App hosted on [Heroku](https://www.heroku.com) at [https://trocasdata-1.herokuapp.com](https://trocasdata-1.herokuapp.com)

Deployment in Heroku is done via a docker container created by [Dockerfile](Dockerfile). 
But the app can also be run locally on the notebook [trocas_pannelapp_1.ipynb](trocas_pannelapp_1.ipynb), 
after creating a conda environment with [environment.yml](environment.yml).

## Docker image

The [Dockerfile](Dockerfile) that works with Heroku was developed by adapting one [I found online](https://github.com/Atlas7/bokeh-app-uk-road-accidents-viz/blob/master/Dockerfile). My initial working version is [here](https://github.com/amazon-riverbgc/herokuapp1/blob/b4c258d30fedea7b413ed5b781ffca255f58ac98/Dockerfile). The current version incorporates changes to make the docker image much smaller; see [issue #2](https://github.com/amazon-riverbgc/herokuapp1/issues/2). The initial version has different elements and schemes that are worth referring back, as needed.

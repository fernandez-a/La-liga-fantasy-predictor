# La liga Española points predictor

This project uses machine learning to predict the performance of each player for la liga española.

1. /la_liga/scrapers: with the code inside this folder just need to run : poetry run python main.py
2. /la_liga/notebooks: for testing and running run: poetry run jupyter notebook , in this folder are the notebooks that clean the data, prepocessed and train save the model.

### Installing

As poetry is being used for the dependency managment , you need to install the .toml for the la_liga folder and install the image for the webapp



## Deployment

For the web app testing Docker need to be installed https://docs.docker.com/engine/install/ubuntu/ , once its downloaded.

1. docker build -t <image name>
2. docker run <image name>

## Built With

* [Python](https://www.python.org/) - The programming language used.
* [Poetry](https://python-poetry.org/) - Dependency Management
* [Streamlit](https://streamlit.io/) - The web framework used.

## Authors

* **Alejandro Fernández Armas** - [fernandez-a](https://github.com/fernandez-a)

# effort-estimation-tool


```bash
# Prod environment


# start mongo db
docker compose up -d


# run tests
docker compose run --rm --build -e MONGO_URI="mongodb://mongo:27017/effort_estimation_proj_testing" flask_app pytest -vs "tests/test_app.py"

```

```bash
# Dev environment

# create environment
python -m venv .venv

# activate environment

# install dependencies
pip install -r requirements.txt

# start mongo db
docker compose up -d mongo

# start app
cd src
python main.py

# run tests

pytest tests

```
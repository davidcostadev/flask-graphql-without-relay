# Flask + Graphql + SQLAlchemy


## Requirements

- docker
- docker-compose

## installation

- docker-compose up -d
- source env/bin/activate 
- pip install -r ./requirements.txt
- python ./app.py 


## updating the schema

- npm install --global get-graphql-schema
- get-graphql-schema http://localhost:5000/graphql > schema.graphql
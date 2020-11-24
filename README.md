# Countries

## Run app

1) create venv
2) Run sudo docker-compose up for database
3) pip install -r requirements.txt
4) alembic upgrade head
5) python main.py 

## Endpoints

POST /reload  {}  
POST /search_codes {'search_string': <string>}  
GET /codes_countries  
GET /code_country  query 'code' example: /code_country?code=RU  

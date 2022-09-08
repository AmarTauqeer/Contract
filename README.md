# Automated Contracting Tool

Automated Contracting Tool, a component of smashHit. smashHit is a Horizon 2020 project with the primary objective of creating a secure and trustworthy data-sharing platform with a focus on consent and contract management in a distributed environment such as the automotiveindustry, insurance and smart cities following GDPR.

## Software Requirements

- [Flask](https://flask.palletsprojects.com/en/1.1.x/)
- [Flask-RESTful](https://flask-restful.readthedocs.io/en/latest/)
- [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/)
- [flask_apispec](https://flask-apispec.readthedocs.io/en/latest/index.html)
- [SPARQLWrapper](https://rdflib.dev/sparqlwrapper/)
- [unittest](https://docs.python.org/3/library/unittest.html)

## Steps to be followed
- git clone https://github.com/AmarTauqeer/Contract.git
- go to the backend folder
- update the .env file
- sudo docker-compose -f docker-compose.yml up

## Running Locally

Run the command below from the root directory for deployement and access via [http://localhost:5001](http://localhost:5001). The Swagger API documentation can be accessed via [http://localhost:5001/swagger-ui/](http://localhost:5001/swagger-ui/).

```bash
python -m flask run

```

## Important Note For Testing REST Endpoints
- For hasContractStatus choose from the list (statusCreated, statusUpdate)
- For hasStates choose from the list (statePending, stateInvalid, stateValid)
- For hasRole choose from the list (DataSubject, DataController, DataProcessor)
- For hasContractCategory choose from the list (categoryBusinessToConsumer, categoryBusinessToBusiness)

## Steps to create/update a contract

- Create term types and companies.
- Create contractors (need company id).
- Create a contract with basic information except contract terms, contract obligations, and contract signatures.
- Use the contract id from the previous step and create contract terms, contract obligations and contract signatures.
- Update the contract with terms, obligations, and signatures.




## Contracts System Architecture
![](/backend/images/semantic-contract-architecture.png)

## Contracts REST APIs Endpoints
![](/backend/images/contract-api-first-part.png)
![](/backend/images/contract-api-second-part.png)

## Tests

[Test cases and results](
https://github.com/AmarTauqeer/Contract/tree/master/backend/tests)

## Contributors

- Amar Tauqeer
  amar.tauqeer@sti2.at

## Project

- [smashHit](https://www.smashhit.eu/)

## License

[GNU General Public License v3.0](https://github.com/AmarTauqeer/SmashHitApi/blob/main/LICENSE)

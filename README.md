# sam-engine

This project is build using aws sam (serverless application model) where we can define our infrastucture as a code and use lambda functions as api, cron function and more. This provide us a simple way to manage infrastructure serverless, being charged by demand, so we can focus on code and business rules.
This project uses python 3.11, its strongly recommended to use pyenv to manage multiple versions of python to run this project, its a best practice instead of install a new version of python global in your computer.

##If you choose pyenv to install python:

Here we have a simple reference to install pyenv
https://dev.to/womakerscode/instalando-o-python-com-o-pyenv-2dc7

for ubuntu/debian dependencies:

```
sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
```

 run:

```
pyenv install 3.11.0
pyenv local 3.11.0
```

### required tools
* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)





## Run local
Its provided a makefile with some commom functionalities to improve the developer experience.

commands:

- **make install** - will create the virtual environment for python project and install the dependencies from requirements.txt (should be run first to prepare our environment).
- **make test** - will run all tests.
- **make lint** - will run flake 8 lib to check a code style from pep8.
- **make format** - will format our project based in pep8 code style using the lib black.

### Steps:
- clone the project 
```
git clone https://github.com/gabriel-f-santos/engine
```
- install dependencies
```
make install
```
- write your code, test and apply code style
```
make format
make test
```
Your tests should be capable of simulate behaviour of the software, but we could call the lambda function locally passing the event we want

```
sam local invoke CreatePolicyFunction --event events/event.json
```

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.


## Deploy the sample application

The project its already with CI/CD using github actions, in every merge we make deploy of the new version of the software



## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.


#Project structure:
The project is organized for create tenant (to permit n clients):

```
curl --request POST \
  --url https://76x998fgo7.execute-api.us-east-1.amazonaws.com/Prod/create-tenant \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/2023.5.8' \
  --data '{
		"name": "tenant teste",
		"email": "tenant3@gmail.com",
		"password": "123password"
}'

{"message": "Tenant created sucessfully"}%
```

after create a tenant, they can login to get their credentials and create structure (used for frontend) and an api-key will be generated to allow backend of tenant make requests to evaluate values in our engine.


```
curl --request POST \
  --url https://76x998fgo7.execute-api.us-east-1.amazonaws.com/Prod/login \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/2023.5.8' \
  --data '{
		"email": "tenant3@gmail.com",
		"password": "123password"
}'


{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOjMsImFwaUtleSI6IjExMDlhOTMyMmI4YTNkZWExMmUxZDNjZDg2ZjQ5ZDAyIiwiZXhwIjoxNjk3MzI4NjQ1LCJzdWIiOiJ0ZW5hbnQzQGdtYWlsLmNvbSJ9.L2hkj6S_-wfzwT4TEJPIS-Ct-XDAI6epIwGYILlCvlA", "apiKey": "1109a9322b8a3dea12e1d3cd86f49d02"}%
```

The frontend using jwt now can create a rule and the backend will associate this rule/policy with the tenant.


```
curl --request POST \
  --url https://76x998fgo7.execute-api.us-east-1.amazonaws.com/Prod/create-policy \
  --header 'Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZW5hbnRfaWQiOjMsImFwaUtleSI6IjExMDlhOTMyMmI4YTNkZWExMmUxZDNjZDg2ZjQ5ZDAyIiwiZXhwIjoxNjk3MzI5MTY0LCJzdWIiOiJ0ZW5hbnQzQGdtYWlsLmNvbSJ9.iulY4-ChwoTUyZiIpiarSU5TMG7GIi5iOaKDvUEfXQI' \
  --header 'Content-Type: application/json' \
  --header 'User-Agent: insomnia/2023.5.8' \
  --data '{
		"name": "Policy 3",
		"policy_details": {
				"1": {
						"condition": "gt",
						"field": "age",
						"threshold": 20
				},
				"2": {
						"condition": "gte",
						"field": "income",
						"threshold": 3000
				}
		}
}'

{"message": "policy created"}%
```

Now, the tenant can use their engine rule:

```

```
# HR TOOL

## About
   Architectured, designed the algorithms to reduce manual work for B2C clients, it Helps the Company to maximize the sales and maintain good track of customers.

## Tech
> Python 3.7
> DJango 2 with DRF
> Postgres 11

## Features (APis):
### 1. Register API:
#### Fields:
		name, email, password, mobile and address.
		[http://127.0.0.1:8000/api/v1/accounts/register/]

### 2. Login API:
#### Fields:
		email and password.
		[http://127.0.0.1:8000/api/v1/accounts/login/]
		--
		Output: Token (Django auth token).

### 3. Logout API:
		Token is a input.
		[http://127.0.0.1:8000/api/v1/accounts/logout/]

### 4. Forgot Passwor API:
		To send the otp to mail.

### 5. Update Password API:
	       	To update the password.


## Client APis:
		---All APIs below should Token as mandatory Header---.

### 1. Add Client:
#### Fields:
		client_name, contact_email, number, address, type(Service/Product based), is_active.
		[http://127.0.0.1:8000/api/v1/details/addclient/]

### 2. GET Client:
#### Fields:
		Given Id, Get client details.

### 3.Modify Client:
		Given id, able to change address,email and contact.
		[http://127.0.0.1:8000/api/v1/details/updatecandidatedetail/]

### 4. List clients:
		Get a list of active client, with paginations.

## Candidate APis:
			---All APIs below should Token as mandatory Header---.

### 1. Add Candidate:
#### Fields:
		name, email, number, address, is_active, current_ctc, expected_ctc, notice_days, is_already_on_notice, exp.tech_skills, preferable_locations.

same as...

### 2. GET Candidate:
### 3. Modify Candidate:
### 4. List Candidate:

## Notes:

#####. used DRF and Serializers.
#####. used Proper Error codes with 401, 400, 200 and all.
#####. Celery and RabbitMQ to send OTP to mail.
#####. Authentication token.
#####. Throttling to restrict n number or hits.
#####. Pagination to split large result sets into individual pages of data.












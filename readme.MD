# User Authentication and Profile Management API

## Register User

<http://127.0.0.1:8000/auth/register/>

This endpoint is used to register a new user.

### Request Body

- first_name (text): The first name of the user.

- last_name (text): The last name of the user.

- username (text): The username chosen by the user.

- email (text): The email address of the user.

- password (text): The chosen password for the account.

- confirm_password (text): Confirmation of the chosen password.

- role (text): The role of the user.

- phone_number (text): The phone number of the user.

- newsletter_subscription (text): Indicates if the user has subscribed to the newsletter.

### Response

``` json
{
    "message": "User registered successfully!"
}

 ```

The response of this request is a JSON schema defining the structure of the response data.

## User Login

<http://127.0.0.1:8000/auth/token/>

The endpoint `http://127.0.0.1:8000/auth/token/` is a POST request used for obtaining authentication tokens.

### Request Body

The request body should be of type form-data and include the following parameters:

- `username` (type: text) : The username of the user.

- `password` (type: text) : The password of the user.

### Response

The response will have a status code of 200 and a content type of `application/json`. The response body will be in the following JSON schema:

``` json
{
    "type": "object",
    "properties": {
        "refresh": {
            "type": "string"
        },
        "access": {
            "type": "string"
        }
    }
}

 ```

## Password Reset

<http://127.0.0.1:8000/auth/password-reset/>

This endpoint is used to initiate a password reset process by sending a request with the user's email.

### Request Body

- email (text): The email address of the user for whom the password reset is requested.

### Response

The response of this request is a JSON schema that includes the properties and data types of the response object.

``` json
{
    "detail": "Password reset email sent"
}

 ```

http://127.0.0.1:8000/auth/reset-password/`uidb64`/`token`

### Reset Password

This endpoint is used to reset the password.

#### Request Body

- new_password (text) - The new password for the user.

- confirm_password (text) - The confirmation of the new password.

#### Response

The response is in JSON format and has the following schema:

``` json
{
  "type": "object",
  "properties": {
    "detail": {
      "type": "string"
    }
  },
  "required": ["detail"]
}

 ```

### Get User Profile

This endpoint is used to retrieve the user's profile information.

#### Request

- Method: GET
- URL: `http://127.0.0.1:8000/auth/profile/`
- Body (form-data):
  - No parameters required for the request body.

#### Response

The response is in JSON format and has the following schema:

``` json
{
  "username": "",
  "email": "",
  "first_name": "",
  "last_name": "",
  "phone_number": "",
  "profile_picture": null,
  "newsletter_subscription": true,
  "role": ""
}
- Status code: 200
#### Headers
- No specific headers are required for this request.

 ```

### Update Profile

The `PUT` request is used to update the user's profile information.

- Method: PUT
- URL: `http://127.0.0.1:8000/auth/profile/`

#### Request Body Parameters

- `first_name` (text): The user's first name.
    
- `last_name` (text): The user's last name.
    
- `phone_number` (text): The user's phone number.
    
- `profile_picture` (file): The user's profile picture.
    
- `newsletter_subscription` (text): Indicates if the user is subscribed to the newsletter. 

#### Response (200)

The response returns the updated profile information in the following JSON schema:

``` json
{
    "username": "",
    "email": "",
    "first_name": "",
    "last_name": "",
    "phone_number": "",
    "profile_picture": null,
    "newsletter_subscription": true,
    "role": ""
}

 ```

### User Change Password

This endpoint allows the user to change their password.

- Method: POST
- URL: `http://127.0.0.1:8000/auth/profile/change-password/`

#### Request Body

- form-data
    
  - `old_password` (text)
        
  - `new_password` (text)
        
  - `confirm_password` (text)
        
#### Response

The response will be in JSON format with the following schema:

``` json
{
    "type": "object",
    "properties": {
        "message": {
            "type": "string"
        }
    }
}

 ```

This endpoint allows the user to change their password by sending a POST request to the specified URL.

#### Request Body

- form-data
    
  - `old_password` (text) : The user's current password.
        
  - `new_password` (text) : The new password to be set.
        
  - `confirm_password` (text) : Confirmation of the new password.    

#### Response

Upon successful execution, the API returns a JSON response with a status code of 200 and an empty message.

#### Related Responses

The response data from other endpoints of this API includes fields such as username, email, first name, last name, phone number, profile picture, newsletter subscription status, and role.

### User Account Deactivation

This endpoint is used to deactivate a user's profile.

- Method: POST
- URL: `http://127.0.0.1:8000/auth/profile/deactivate/`

#### Request Body

- No request body is required for this endpoint.
    
#### Response

- Status: 200
    
- Content Type: application/json
    
- { "message": ""}
    
This endpoint is used to deactivate a user's profile.

**Request Body**  
This endpoint does not require any request body.

**Response**  
The response will be in the form of a JSON schema with the following fields:

- `message` (string): A message indicating the status of the deactivation process.

Example Response:

``` json
{
    "message": "Account deactivated successfully."
}

 ```

# Project 3: Web Forum

## Team Members:

- Daixuan Chen - 20015422

  - Email: dchen30@stevens.edu

- Fan Zhang - 20016134

  - Email: fzhang32@stevens.edu

- Shikhar Saxena - 20021187
  - Email: ssaxena10@stevens.edu

## GitHub Repository:

- URL: [GitHub Repo](https://github.com/Shikhar253/project3)

## Project Details:

- Hours Spent: 30 hours
- Description of Testing:
  - Tested using Postman and a test script
- Unresolved Bugs/Issues:
  - None that we are aware of

## Issue Resolution:

- No significant issues encountered

## Implemented Extensions:

1. **Users and User Keys:**

   - Modified existing endpoints and created new ones to associate posts with users and manage user keys.

2. **User Profiles:**

   - Added metadata to users, requiring unique and non-unique details.
   - Created endpoints to retrieve, edit user metadata, and display it with associated posts.

3. **Date- and Time-based Range Queries:**
   - Added an endpoint for searching posts based on date and time ranges.

4) **User-based Range Queries:**

   - Added an endpoint to search posts by a specific user.

5) **Fulltext search:**
   - Added an endpoint to search the contents of the post’s msg.

## Testing Summaries:

[Insert detailed summaries of tests for each extension, including how to interpret the testing framework and the tests written.]

1. **Users and User Keys:**

   - This test mainly test user creation, post creation, post reading, and post deletion. Each test contains a series of assertions to verify whether the API response meets expectations.

   - Creating a new user: This test sends a POST request to the /user endpoint, and the request body contains the username, real name, and URL of the avatar icon. The test asserts that the response status code is 200 and that the response body contains the user_id and user_key attributes.

   - Creating a new post with a user: This test sends a POST request to the /post endpoint, and the request body contains the message content, user ID, and user key. The test asserts that the response status code is 200 and that the response body contains the id, key, user_id and other attributes.

   - Reading a post: This test sends a GET request to the /post/{{post_id}} endpoint, where {{post_id}} is an environment variable representing the ID of the post to be read. The test asserts that the response status code is 200 and that the response body contains the user_id attribute.

   - Deleting a post: This test sends a DELETE request to the /post/{{post_id}}/delete/{{user_key}} endpoint. The test asserts that the response status code is 200 and that the response body contains the id, key, timestamp, user_id, user_key, and username attributes.

2. **User Profile**

   - Create User: This test sends a POST request to the /user endpoint to create a new user profile. It checks if the response status code is 200 and if the response body contains the user_id and user_key properties. Also, it contains two tests to check if the response contains the according status code and error message when send invalid request.

   - Creating a new post with a user: This test sends a POST request to the /post endpoint, and the request body contains the message content, user ID, and user key. The test asserts that the response status code is 200 and that the response body contains the id, key, user_id and other attributes.

   - Update User Profile: This test sends a PUT request to the /user/{user_key} endpoint to update an existing user profile. It checks if the response status code is 200 and if the updated details are reflected in the response body. Also, it checks if the response contains the according status code and error message when send invalid request.

   - Get User Profile: This test sends a GET request to the /user/{user_id} endpoint to retrieve the details of a user profile. It checks if the response status code is 200 and if the response body contains the correct user details.

3. **Date- and Time-based Range Queries:**

   - This test sends a GET request to the /posts endpoint to perform a Date-and-Time-Based query. It includes two parameters: start and end, to specify the time range.

   - This test check if response status code is 200 and the response body contains the id, message and timestamp start or start and end is provided.

   - This test check if response status code is 400 and return proper error message when query with invalid format.

4. **User-based Queries:**

   - User-based query: This test sends a GET request to the /posts/user/{{user_id}} endpoint to retrieve all posts made by a specific user.

   - User-based range queries with invalid user id: This test likely sends a similar GET request to the /posts/user/{{user_id}} endpoint, but with an invalid user ID. The test asserts that the response status code is 500, indicating an internal server error. This test is designed to check the API's error handling when given invalid input.

5. **Fulltext Search:**

   - This test sends a GET request to the /search endpoint to perform a full-text search. The request includes a query parameter, which contains the search terms.

   - The test checks if the response status code is 200, indicating a successful request. It also checks if the response body contains an array of results. Each result should include the relevant fields from the searched documents, and the results should be relevant to the search terms.

   - The test checks if the response contains an empty array if there are no results.

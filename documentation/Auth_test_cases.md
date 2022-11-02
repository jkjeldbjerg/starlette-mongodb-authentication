# Authentication Test Cases

This is the list of so far identified test cases for authentication

## General

### Defined scopes

* `authenticated` for all users that are logged in
* `unauthenticated` for all users not logged in
* `admin` for system administrator
* `org_admin` for user administrator in org
* `subscriber` for paying user

## Flows

### All pages

For all pages:

* Ability to show messages for user regardless of page

### Login

1. Show login page without prior authentication -> 
   - ability to login: fields username (usr) and password (pwd) and submit button are present
   - there is no session user _id
2. Show login page with prior authentication ->
   - logout previous user out and set explanatory message, ability to login
   - previous session user _id is cleared
3. Successful login -> 
   - either go to welcome page or go to `next` page, if set and scope requirement is met
   - session has user _id
4. Successful login -> 
   - either go to welcome page because `next` scope requirement is not met with explanatory message
   - session has user _id 
5. Unsuccessful login due to wrong username and password ->
   - set explanatory message and redisplay login page
   - no session user _id
6. Unsuccessful login due to account is locked ->
   - put event in authentication log, set explanatory message and show home
   - no session user _id

### Logout

1. User pressed logout ->
   - user is logged out, explanatory message on home
   - no session user _id
2. User clicked to new page and is still logged in
   - session user _id is still there

### Access to pages

1. Ability to see all non-protected pages ->
   - when link is clicked or url entered page is shown 
2. When logged in the user always has scope `authenticated` ->
   - session user _id is set and `authentication` is present in scopes
3. When logged in have the ability to see all pages marked `authenticated` ->
   - session user _id is set and scope `authenticated` is present
4. When logged in with scope have the ability to see all pages marked with that scope ->
   - session user _id is set and scope is present
5. With logged in without scope does not have the ability to see any page marked with that scope ->
   - session user _id is set and scope is not present
6. When page is marked with more than one scope then have the ability to see page, if has one or more scopes ->
   - session user _id is set and one more required scopes are present for user
7. When page is marked with more than one scope then do not have the ability to see page without any of the scopes ->
   - session user _id is set and page scopes are not present in user scopes

### Admin user administration

1. Create
2. Update
3. Lock
4. Unlock
5. Delete
6. View details
7. View all users
8. View user history
9. Create org
10. Assign org to user
11. Delete org
12. Update org

### User self administration

1. Create
2. Update
3. Delete
4. Accept terms and conditions
5. Accept new version of terms and conditions
6. Validate e-mail
7. Failure to validate e-mail
8. Resending of validation e-mail
9. Forgotten password
10. SSO from Apple, Google, Azure AD (Microsoft), Amazon, Okta (OAuth2)

Advanced:
1. User is org administrator (scope: `org_admin`) and can CRUD users to org
2. No user can add him self to org without having scope `org_admin` and belong to `org`
3. SSO remote administration of users 


# About

This python script creates users using the Nextcloud API, with a CSV file as parameter.
The password is auto generated via a random function. 

The welcome mail is not sent (a choice I made), because the script creates a user identified by a username and a password firstly, and updates the profile secondly adding the email, the address and the displayname.

To handle errors, the script also checks if the username already exists or no.

Finally, a recap CSV file is created with the generated password of each user. 

# Usage

`python3 script.py file_to_import.csv`
(simply replace the file_to_import.csv by the file containing the informations). 

# Entry CSV file structure

| username | email | displayname | address | group |
|----------|-------|-------------|---------|-------|
|john.doe  |john@doe.com | John Doe | Infinite Loop, Cupertino |Staff|

# Credits
I used the Nextcloud API, the documentation is available here : https://docs.nextcloud.com/server/latest/admin_manual/configuration_user/instruction_set_for_users.html

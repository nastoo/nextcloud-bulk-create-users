import csv
import random
import string
import requests
import argparse

## CREATED BY NATHAN STOOSS - 2023 ##

# Nextcloud instance URL and username and password of the admin account
nextcloud_url = 'YOUR_NEXTCLOUD_URL'
admin_username = 'YOUR_ADMIN_USERNAME'
admin_password = 'YOUR_ADMIN_PASSWORD'

headers = {'OCS-APIREQUEST': 'true'}

# Function to add a line in the CSV file
def add_user_to_csv(username, email, displayname, address, group, password):
  with open('users_passwds.csv', 'a') as filedit:
    writer = csv.writer(filedit, delimiter=';')
    writer.writerow([username, email, displayname, address, group, password])
  filedit.close()

def check_user(username):
    # We check if the user doesn't already exist
  checkingUser = requests.get(
      f'{nextcloud_url}/ocs/v2.php/cloud/users/{username}',
      auth=(admin_username, admin_password),
      headers=headers,
  )
  if(checkingUser.status_code == 200):
    return False
  else:
    return True

# Function to generate a random password of 8 characters
def generate_password():
  return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def update_user(username, key, value):
  requests.put(
      f'{nextcloud_url}/ocs/v2.php/cloud/users/{username}',
      auth=(admin_username, admin_password),
      headers=headers,
      data={'key': key, 'value': value}
  )

def create_user(username, password, group):
  response = requests.post(
    f'{nextcloud_url}/ocs/v2.php/cloud/users',
    auth=(admin_username, admin_password),
    headers=headers,
    data={'userid': username, 'password': password, 'groups[]': group}
  )

  if(response.status_code == 200):
    return True
  else:
    return response.text


def create_csv_file(name):
  # Create a new CSV file
  with open(name, 'w') as newfile:
    writer = csv.writer(newfile, delimiter=';')

    # Write the header of the CSV file
    writer.writerow(['Username', 'Email', 'Displayname', 'Address', 'Group', 'Password'])
    
  newfile.close()

def parse_args():
  parser = argparse.ArgumentParser(
                    prog = 'Nextcloud Bulk User Creation',
                    description = 'Script to create multiple users in Nextcloud',
                    epilog = 'Enjoy the program! :)')
  parser.add_argument('filename')
  args = parser.parse_args()
  if(args.filename):
    main(args.filename)
  else:
    print('No file specified')

def main(filename):
  # Create the CSV recap file
  create_csv_file('users_passwds.csv')

  with open(filename, 'r+') as csv_file:
    reader = csv.reader(csv_file, delimiter=';')
    
    for i, row in enumerate(reader):
      if i == 0:
        continue
        
      username = row[0]
      email = row[1]
      displayname = row[2]
      address  = row[3]
      group = row[4]
      password = generate_password()

      if(check_user(username) == True):
        # Send a POST request to the Nextcloud API to create the user. Check if everything went well (check the boolean)
        user = create_user(username, password, group)
        if(user == True):
            # Send a PUT request to the Nextcloud API to update the user's email address & address & displayname
            update_user(username, 'email', email)
            update_user(username, 'address', address)
            update_user(username, 'displayname', displayname)

            # Add the user to the CSV file
            add_user_to_csv(username, email, displayname, address, group, password)

            print(f'User {username} created successfully !')
        else: 
            print(f'Error when creating the user {username} : {user}')
      else: 
        print(f'Utilisateur {username} déjà existant !')

  csv_file.close()

# Execute the script with the arguments passed
parse_args()
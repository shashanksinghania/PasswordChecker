import requests
import sys
import hashlib


#Gives the response from the API
def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/"+ query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Fetching error....{res.status_code}. Please check the API and try again')
    return res

#Returns the count from the API
def password_counts(response, check):
    web_data = (line.split(':') for line in response.text.splitlines())
    for h, count in web_data:
        if h == check:
            return int(count)
    return 0

#converts the password to sha1 and returns the counts from password_counts
def check_pwned_api(password):
    sha1password = hashlib.sha1(password.encode()).hexdigest().upper()
    first_5, remaining = sha1password[:5], sha1password[5:]
    response = request_api_data(first_5)
    return password_counts(response, remaining)

#outputs the counts of passwords and suggests whether to change it or not
def main(passwords):
    for password in passwords:
        count = check_pwned_api(password)
        if (count > 0):
            print(f'password: {password} has been pwned {count} times... you should consider using a stronger one.')
        else:
            print(f'{password} was NOT found... WAY TO GO!')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

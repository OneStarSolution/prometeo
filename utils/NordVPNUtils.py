from datetime import datetime
import subprocess
import random


def send_command(command_1='status', command_2=''):
    output = subprocess.Popen(
        ["nordvpn", command_1, command_2], stdout=subprocess.PIPE)
    response = output.communicate()[0].decode("utf-8")
    return response


def get_response(line):
    response = send_command('status').lower()
    line = line.lower()
    if line == 'ip':
        line = 'new ip'
    for i in response.split('\n'):
        if line in i:
            give_to_terminal = i
            break
    return give_to_terminal


def check_used_servers(server):
    try:
        file = open("used_servers.txt", 'r')
        file_content = file.readlines()
        file.close()
        for i in file_content:
            if server in i:
                used_server = True
                print("The Server " + server +
                      " has already been used. Searching for alternate server....")
                break
            else:
                used_server = False
    except IOError:
        used_server = False
    return used_server


def generate_random_server(max_server_number=9000):
    # used_server = True
    # while used_server is True:
    #     random_number = random.randint(8500, max_server_number)
    #     if random_number < 1000:
    #         country_and_name = "ca" + str(random_number)
    #     else:
    #         country_and_name = "us" + str(random_number)
    #     print(f"ttrying {server}")
    #     server = country_and_name
    #     used_server = check_used_servers(server)
    return "us5326"


def save_used_servers(used_server):
    time_connected = str(datetime.now())
    time_connected = " - TIME OF CONNECTION: " + time_connected
    try:
        f = open('used_servers.txt')
    except IOError:
        f = open('used_servers.txt', 'w+')
        f.write(used_server + time_connected)
        f.close()
    else:
        with open('used_servers.txt', 'a+') as file:
            file.write('\n' + used_server + time_connected)


def save_bad_servers(bad_server):
    try:
        f = open('bad_servers.txt')
    except IOError:
        f = open('bad_servers.txt', 'w+')
        f.write(bad_server)
        f.close()
    else:
        with open('bad_servers.txt', 'a+') as file:
            file.write('\n' + bad_server)


def connect_to_new_server(status):
    if "disco" in status.lower():
        connect_to_new_server = False
        while connect_to_new_server is False:
            print("finding a server")
            country_and_name = generate_random_server(20000)
            print("ttry to connect", country_and_name)
            nordvpn_output = send_command('connect', country_and_name)
            if 'hoops!' in nordvpn_output:
                save_bad_servers(country_and_name)
            if 'You are connected' in nordvpn_output:
                print("You are now connected to server: " + country_and_name)
                save_used_servers(country_and_name)
                connect_to_new_server = True
    else:
        print("You are already connected to a server!......")


if __name__ == '__main__':
    status = send_command()
    print("status", status)
    connect_to_new_server(status)

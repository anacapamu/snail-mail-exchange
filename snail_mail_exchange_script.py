import random
import csv
import os
from datetime import datetime

def file_exists(filename):

    if not os.path.isfile(filename):
        print("Error: The file {filename} does not exist in the current directory.")
        return False

    return True

def convert_csv_data_to_dict(filename):
    people = {}
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name']
            email = row['Email Address']
            role = row['I am a']
            address = row['Current Mailing Address']
            option = row['Choose an option:'].replace("'", "")

            send_count, receive_count, max_receive = assign_send_receive_and_max_receive_counts_based_on_option(option)

            people[name] = {
                'email': email,
                'role': role,
                'address': address,
                'send_count': send_count,
                'receive_count': receive_count,
                'max_receive': max_receive
            }

    return people

def assign_send_receive_and_max_receive_counts_based_on_option(option):
    send_count = 0
    receive_count = 0
    max_receive = 0

    if option == 'I would like to send 1 mail and receive 1 mail.':
        send_count += 1
        receive_count += 1
        max_receive += 1
    elif option == 'I would like to send 2 mail and receive 2 mail.':
        send_count += 2
        receive_count += 2
        max_receive += 2
    elif option == 'I cannot send a mail but would like to receive 1 mail.':
        send_count += 0
        receive_count += 1
        max_receive += 1
    elif option == 'I can send 1 mail and dont mind if I dont receive any mail.':
        send_count += 1
        receive_count += 0
        max_receive += 1
    elif option == 'I can send 2 mail and dont mind if I dont receive any mail.':
        send_count += 2
        receive_count += 0
        max_receive += 2

    return send_count, receive_count, max_receive

def balance_send_and_receive_counts(people):

    total_send = sum(person['send_count'] for person in people.values())
    total_receive = sum(person['receive_count'] for person in people.values())

    difference = total_send - total_receive

    # When there is less mail being sent than to be received (imbalance)
    if difference < 0:
        print(f"Error: There is not enough mail being sent. {abs(difference)} more mail needs to be sent.")
    elif difference > 0:
        # To account for people that don't mind if they don't receive any mail
        can_receive_more = [name for name, details in people.items() if details["receive_count"] < details["max_receive"]]

    while difference > 0 and can_receive_more:
        random_person_name = random.choice(can_receive_more)

        people[random_person_name]["receive_count"] += 1
        difference -= 1

        if people[random_person_name]["receive_count"] == people[random_person_name]["max_receive"]:
            can_receive_more.remove(random_person_name)

    # When there is more mail being sent than being received (imbalance)
    if difference > 0:
        print(f"Error: There is not enough capacity to receive all the mail being sent. {difference} mail(s) cannot be received.")

    return people

def match_sender_with_recipients(balanced_people):

    senders = [name for name, person in balanced_people.items() if person['send_count'] > 0]
    receivers = [name for name, person in balanced_people.items() if person['receive_count'] > 0]
    send_counts = [balanced_people[sender]['send_count'] for sender in senders]
    receive_counts = [balanced_people[receiver]['receive_count'] for receiver in receivers]

    distribution = {sender: [] for sender in senders}

    receiver_received_counts = {receiver: 0 for receiver in receivers}

    for sender, count in zip(senders, send_counts):
        for _ in range(count):
            potential_receivers = [receiver for receiver in receivers
                                   if receiver_received_counts[receiver] < receive_counts[receivers.index(receiver)]
                                   and receiver != sender
                                   and receiver not in distribution[sender]
                                   and sender not in distribution.get(receiver, [])]

            if not potential_receivers:
                break

            receiver = random.choice(potential_receivers)

            distribution[sender].append(receiver)
            receiver_received_counts[receiver] += 1

    # Check if all senders were able to send their max # of letters and all receivers were able to receive their max # of letters
    all_sent = all(len(sent_to) == count for sent_to, count in zip(distribution.values(), send_counts))
    all_received = all(count == max_count for count, max_count in zip(receiver_received_counts.values(), receive_counts))

    if not (all_sent and all_received):
        print('Warning: Unable to find a distribution where all senders can send their maximum number of letters and all receivers can receive their maximum number of letters.')
        raise SystemExit()
    else:
        for sender, recipients in distribution.items():
            print(f"{sender} sends letters to {', '.join(recipients)}")

    return distribution

def get_date(prompt):
    date_str = input(prompt)

    try:
        datetime.strptime(date_str, '%A, %B %d, %Y')
        return date_str
    except ValueError:
        print("Error: The date was not in the expected format. Please use the format 'Day, Month Date, Year', e.g. 'Saturday, July 8, 2023'.")

def generate_email_templates(distribution, people):
    contact_deadline = get_date('When should the user contact you if they don’t receive mail? (e.g. "Saturday, July 8, 2023") ')
    mail_deadline = get_date('When should mail be sent out by? (e.g. "Saturday, July 8, 2023") ')

    with open('email_templates.txt', 'w') as f:
        for name, recipients in distribution.items():
            person = people[name]

            first_name = name.split()[0]

            if person['send_count'] == 0:
                f.write(f"{person['email']}\n")
                f.write(f"\n")
                f.write(f"Hi {first_name},\n")
                f.write(f"\n")
                f.write(f"Matches have been sent out to the senders. Please let me know if you don't receive anything in the mail by {contact_deadline}.\n")
                f.write(f"Thanks for participating in the Snail Mail Exchange!\n")
                f.write(f"Cheers,\n")
                f.write(f"\n") * 2
                f.write(f"----------------------------------")
                f.write(f"\n") * 2
            else:
                f.write(f"{person['email']}\n")
                f.write(f"\n")
                f.write(f"Hi {first_name},\n")
                f.write(f"\n")
                f.write(f"You have been matched with:\n")

                for recipient_name in recipients:
                    recipient = people[recipient_name]
                    f.write(f"{recipient_name} ({recipient['role']})\n")
                    f.write(f"{recipient['address']}\n")

                f.write(f"\n") * 2
                f.write(f"Please send out the letters by {mail_deadline}.\n")
                f.write(f"\n") * 2
                f.write(f"Notes:\n")
                f.write(f"\t•\tThe people whom you will RECEIVE mail from are NOT the same as those you will be SENDING mail to.\n")
                f.write(f"\t•\tYou can send a postcard, stickers, a drawing, a joke on a post-it, and/or whatever you want (as long as it follows our community guidelines of upholding a safe and inclusive environment).\n")
                f.write(f"\t•\tThis is one time only, so you don't have to send more than one mail to each person you are assigned.\n")
                f.write(f"Resources:\n")
                f.write(f"\t•\tHow to mail a letter: https://www.wikihow.com/Mail-a-Letter\n")
                f.write(f"\n") * 2
                f.write(f"Thanks for participating in the snail mail exchange!\n")
                f.write(f"Cheers,\n")
                f.write(f"\n") * 2
                f.write(f"----------------------------------")
                f.write(f"\n") * 2

if __name__ == "__main__":
    if file_exists("snail_mail_exchange.csv"):
        people = convert_csv_data_to_dict("snail_mail_exchange.csv")
        balanced_people = balance_send_and_receive_counts(people)
        distribution = match_sender_with_recipients(balanced_people)
        generate_email_templates(distribution, balanced_people)

import random
import csv
import os
from datetime import datetime

# Section 1: Open the CSV file and handle errors
filename = 'snail_mail_exchange.csv'

if not os.path.isfile(filename):
    print("Error: The file 'snail_mail.csv' does not exist in the current directory.")
else:
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
    except Exception as e:
        print(f"Error: An error occurred while reading the file: {str(e)}")

# Section 2: Process the data
people = {}  # Use a dictionary to hold the data for each person
with open(filename, 'r') as f:
    reader = csv.DictReader(f)  # Use a DictReader so we can access fields by name
    for row in reader:
        name = row['Name']
        email = row['Email Address']
        role = row['I am a']
        address = row['Current Mailing Address']
        option = row['Choose an option:'].replace("'", "")

        # Section 3: Determine the number of letters to send/receive based on the option
        if option == 'I would like to send 1 mail and receive 1 mail.':
            send_count = 1
            receive_count = 1
            max_receive = 1
        elif option == 'I would like to send 2 mail and receive 2 mail.':
            send_count = 2
            receive_count = 2
            max_receive = 2
        elif option == 'I cannot send a mail but would like to receive 1 mail.':
            send_count = 0
            receive_count = 1
            max_receive = 1
        elif option == 'I can send 1 mail and dont mind if I dont receive any mail.':
            send_count = 1
            receive_count = 0
            max_receive = 1
        elif option == 'I can send 2 mail and dont mind if I dont receive any mail.':
            send_count = 2
            receive_count = 0
            max_receive = 2

        # Save the data for this person
        people[name] = {
            'email': email,
            'role': role,
            'address': address,
            'send_count': send_count,
            'receive_count': receive_count,
            'max_receive': max_receive
        }

# Section 3a, 3b, 3c: Balance the send/receive counts

total_send = sum(person['send_count'] for person in people.values())
total_receive = sum(person['receive_count'] for person in people.values())

difference = total_send - total_receive
if difference < 0:
    print(f"Error: There is not enough mail being sent. {abs(difference)} more mail needs to be sent.")
elif difference > 0:
    # People who can receive more mail
    can_receive_more = [name for name, details in people.items() if details["receive_count"] < details["max_receive"]]

    # As long as there's a difference and people who can receive more
    while difference > 0 and can_receive_more:
        # Randomly select a person's name
        random_person_name = random.choice(can_receive_more)

        # Increase their receive count by 1
        people[random_person_name]["receive_count"] += 1
        difference -= 1

        # If this person has reached their max, remove them from the list
        if people[random_person_name]["receive_count"] == people[random_person_name]["max_receive"]:
            can_receive_more.remove(random_person_name)

    # If there's still a difference left after that, it means there aren't enough people to receive the extra letters
    if difference > 0:
        print(f"Error: There is not enough capacity to receive all the mail being sent. {difference} mail(s) cannot be received.")


# Section 4: Perform the letter distribution

senders = [name for name, person in people.items() if person['send_count'] > 0]
receivers = [name for name, person in people.items() if person['receive_count'] > 0]
send_counts = [people[sender]['send_count'] for sender in senders]
receive_counts = [people[receiver]['receive_count'] for receiver in receivers]


def random_letter_distribution(senders, sender_counts, receivers, receive_counts):
    # Initialize the dictionary to hold the distribution
    distribution = {sender: [] for sender in senders}

    # Initialize the dictionary to track the count of letters received by each receiver
    receiver_received_counts = {receiver: 0 for receiver in receivers}

    # For each sender, select recipients for their letters
    for sender, count in zip(senders, sender_counts):
        for _ in range(count):
            # Create a list of potential receivers (receivers who haven't reached their maximum count
            # and are not the current sender or already a receiver of the sender)
            potential_receivers = [receiver for receiver in receivers
                                   if receiver_received_counts[receiver] < receive_counts[receivers.index(receiver)]
                                   and receiver != sender
                                   and receiver not in distribution[sender]
                                   and sender not in distribution.get(receiver, [])]

            # If there are no potential receivers left, break out of the loop
            if not potential_receivers:
                break

            # Select a random receiver from the potential receivers
            receiver = random.choice(potential_receivers)

            # Add the receiver to the sender's list and increase their received count
            distribution[sender].append(receiver)
            receiver_received_counts[receiver] += 1

    # Check if all senders were able to send their maximum number of letters and all receivers were able to receive their maximum number of letters
    all_sent = all(len(sent_to) == count for sent_to, count in zip(distribution.values(), sender_counts))
    all_received = all(count == max_count for count, max_count in zip(receiver_received_counts.values(), receive_counts))

    if not (all_sent and all_received):
        print('Warning: Unable to find a distribution where all senders can send their maximum number of letters and all receivers can receive their maximum number of letters.')
    else:
        for sender, recipients in distribution.items():
            print(f"{sender} sends letters to {', '.join(recipients)}")

    return distribution

distribution = random_letter_distribution(senders, send_counts, receivers, receive_counts)

# Section 5: Ask the user for the contact and mail-out dates

def get_date(prompt):
    while True:
        date_str = input(prompt)
        try:
            return datetime.strptime(date_str, '%A, %B %d, %Y')
        except ValueError:
            print("Error: The date was not in the expected format. Please use the format 'Day, Month Date, Year', e.g. 'Saturday, July 8, 2023'.")

contact_date = get_date('When should the user contact you if they don’t receive mail? (e.g. "Saturday, July 8, 2023")')
mail_out_date = get_date('When should mail be sent out by? (e.g. "Saturday, July 8, 2023") ')

# Section 6: Generate the email templates and write them to a file

with open('emails.txt', 'w') as f:
    for name, recipients in distribution.items():
        person = people[name]

        # Determine which template to use based on the send count
        if person['send_count'] == 0:
            # Template 6a
            f.write(f"{person['email']}\n")
            f.write(f"\n")
            f.write(f"Hi {name},\n")
            f.write(f"\n")
            f.write(f"Matches have been sent out to the senders. Please let me know if you don't receive anything in the mail by {contact_date}.\n")
            f.write(f"Thanks for participating in the Snail Mail Exchange!\n")
            f.write(f"Cheers,\n")
            f.write(f"\n") * 2
        else:
            # Template 6b or 6c
            f.write(f"{person['email']}\n")
            f.write(f"\n")
            f.write(f"Hi {name},\n")
            f.write(f"\n")
            f.write(f"You have been matched with:\n")

            for recipient_name in recipients:
                recipient = people[recipient_name]
                f.write(f"{recipient_name} ({recipient['role']})\n")
                f.write(f"{recipient['address']}\n")

            f.write(f"\n") * 2
            f.write(f"Please send out the letters by {mail_out_date}.\n")
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

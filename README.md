# Snail Mail Exchange
This is a script to match senders with receiver(s) and to generate the email templates to be sent out.

## Description
Snail mail exchange is a fun way to build community and to get to know each other. Those who opt in will be randomly assigned community member(s) to send mail to. The people whom one will receive mail from are NOT the same as those one will be sending mail to.

To make this program accessible to all in the community, participants do not have to send a mail to receive a mail. For this to be possible, there has to be some members of the community that are willing to send mail but don't mind if they don't receive any.

## How to Use
1. Copy the [Google Form template](https://forms.gle/pzAPfdjBLzegSR2R7) for Snail Mail Exchange
2. Make edits to the description of the form and collect responses
3. When form is closed, download a **.csv** of responses
4. Rename **.csv** file to `snail_mail_exchange.csv`
5. Add `snail_mail_exchange.csv` to the same directory as the `snail_mail_exchange_script.py`
6. Run the script with `python3 snail_mail_exchange_script.py`
7. Send emails by copying and pasting the templates in `email_templates.txt`

## Common Pitfalls
`KeyError` in lines 23-27

>Double check the `.csv` file to make sure that there isn't a space after column header, i.e. "Email Address " instead of "Email Address"

Warning: Unable to find a distribution where all senders can send their maximum number of letters and all receivers can receive their maximum number of letters.

> Due to the constraint of sender unable to send mail to people that will be sending them mail, the script may need to be run multiple times to get a distribution.

import imaplib
import configparser
import sys
import traceback
import email
import smtplib
import argparse

FROM_EMAIL = ""
FROM_PWD = ""
SMTP_SERVER = ""

def readEmail( key, value ):
	try:
		imapClient = imaplib.IMAP4_SSL(SMTP_SERVER)
		print ("\nLogging in...")
		
		imapClient.login(FROM_EMAIL,FROM_PWD)
		print ("\nLog-in successfull!")
		
		imapClient.select("inbox")
		print ("\nReading mailboxes...")
		

		if ( key == None or value == None ):
			type, searchResult = imapClient.search( None, "ALL" )
			print ("\nTotal search emails count:" + str(len(searchResult[0])))
		
		elif( key != None and value != None ):
			type, searchResult = imapClient.search(None, "(" + key + " " + value + ")")
			print ("\nTotal search emails count:" + str(len(searchResult[0])))
		
		for resultCount in searchResult[0].split():
			typ, messages = imapClient.fetch(resultCount,"(RFC822)")
			
			for message in messages:
				if isinstance(message, tuple):
					msg = email.message_from_bytes(message[1])
					email_to_id = msg["to"]
					email_from_id = msg["from"]
					email_cc_id = msg["cc"]
					email_bcc_id = msg["bcc"]
					email_subject = msg["subject"]
					email_body = msg["body"]
					print ("\nTo: " + str(email_to_id))
					print ("\nFrom: " + str(email_from_id))
					print ("\nCC: " + str(email_cc_id))
					print ("\nBCC: " + str(email_bcc_id))
					print ("\nSubject: " + str(email_subject))
					print ("\nBody: " + str(email_body))
				break

	except Exception as e:
		print ("\nException handled: " + str(e))
		print ("\nException details:")
		traceback.print_tb(e.__traceback__)

if __name__ == "__main__":
	try:
		config = configparser.ConfigParser()
		config.read("configuration.ini")
		config.sections()
		
		FROM_EMAIL = config["DEFAULT"]["from_email"]
		FROM_PWD = config["DEFAULT"]["from_pwd"]
		SMTP_SERVER = config["DEFAULT"]["smtp_server"]

		parser = argparse.ArgumentParser(description="Please enter key and value for search..")
		parser.add_argument("key",help="You need to specify the key to perform search on the emails. E.g. from, sent, etc")
		parser.add_argument("value",help="You may optional specify the value for the key specified. If not specified, your key argument will not be considered")
		args = parser.parse_args()
		
		readEmail(args.key, args.value)

	except Exception as e:
		print ("\nException handled: " + str(e))
		print ("\nException details:")
		traceback.print_tb(e.__traceback__)
import imaplib
import configparser

ORG_EMAIL = "@enzigma.com"
FROM_EMAIL = ""
FROM_PWD = ""
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

def readEmail():
	try:
		mail = imaplib.IMAP4_SSL(SMTP_SERVER)
		rv, data = mail.login(FROM_EMAIL,FROM_PWD)
		mail.select("inbox")
		print ("Hello world!")
		print ("rv" + rv)
		print ("data" + str(data))
	except e:
		print ("Exception:" +  e)

if __name__ == "__main__":
	try:
		print ("Inside main")
		config = configparser.ConfigParser()
		config.read("configuration.ini")
		config.sections()
		FROM_EMAIL = config["DEFAULT"]["from_email"]
		FROM_PWD = config["DEFAULT"]["from_pwd"]
		readEmail()
	except e:
		print ("Exception:" + e)

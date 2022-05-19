# This script is a Tls SMTP logging handler to log information as code is running
import logging
import logging.handlers


# create and send message
class TlsSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        """
        create logs and send them to an SMTP email destination
        """
        try:
            import smtplib
            import string
            try:
                from email.utils import formatdate
            except ImportError:
                formatdate = self.date_time
            port = self.mailport
            if not port:
                port = smtplib.SMTP_PORT
            smtp = smtplib.SMTP(self.mailhost, port)
            # define email message as the log
            msg = self.format(record)
            msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                self.fromaddr, self.toaddrs, self.getSubject(record), formatdate(), msg)
            if self.username:
                # Tls
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                # login to email account
                smtp.login(self.username, self.password)
            # send the email
            smtp.sendmail(self.fromaddr, self.toaddrs, msg)
            smtp.quit()

        # quit script if user presses any key
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            self.handleError(record)


logger = logging.getLogger()

format = logging.Formatter('%(asctime)s-%(levelname)s-%(funcName)s-%(msg)s')

gm = TlsSMTPHandler(("smtp.gmail.com", 587), '<from_email>', ['to_email>'], 'Error found', ('username', 'pwd'))

gm.setFormatter(format)
gm.setLevel(logging.ERROR)

logger.addHandler(gm)

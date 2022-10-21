import smtplib, os, sys

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from . import crawler

sender = "hermescrawlerapp@gmail.com"
receiver = "hermescrawlerapp@gmail.com"

begin_html = \
"""
<html>
    <head></head>
    <body>
        <p>Hi!
            <p>We found the latest releases that matched your saved preferences:</p>
        </p>
    </body>
</html>
"""

end_html = \
"""
<html>
    <b><p>Hermes Crawler</p></b>
</html>
"""



# Generate Email
def send_email(logger, root, client_email, name_list, link_list, image_list):
    logger.log("Msg", "Sending Email")
    receiver = client_email
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)                             # creates SMTP session 
        s.starttls()                                                        # start TLS for security 
        s.login("hermescrawlerapp@gmail.com", "kgqnrsunopoyccpw")   # Authentication 
    except:
        raise Exception("Email Service Start Failed")

    msg = MIMEMultipart()
    msg['Subject'] = "Hermes Updater Message"
    msg['From'] = sender
    msg['To'] = receiver
    logger.log("Msg", "Created Email Object")

    # Process Bag List
    msg.attach(MIMEText(begin_html, 'html'))

    i = 0
    while i < len(name_list):
        # Add bag name
        entry = "<b><p> - "
        # Add bag webstore link if applicable
        if link_list[i] != "None":
            logger.log("Msg", "Attaching Link {0}".format(link_list[i]))
            entry += '<a href="{0}">'.format(link_list[i])
            entry = entry + name_list[i] + "</a>"
            logger.log("Msg", "Attached Link")
        else:
            entry += name_list[i]
        entry += "</p></b>"
        msg.attach(MIMEText(entry, 'html'))
        logger.log("Msg", "Added object text")

        # Add bag image if applicable
        if image_list[i] != "None":
            logger.log("Msg", "Attaching Image {0}".format(image_list[i]))
            full_img_name = crawler.get_image(logger, root, link=image_list[i], name=str(i))
            attach_img(msg, full_img_name)
            logger.log("Msg", "Attached Image {0}".format(full_img_name))
            del full_img_name
        i += 1
        
    msg.attach(MIMEText(end_html, 'html'))

    # Send email and exit
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()
    logger.log("Msg", "Sent Email")
    return



def attach_img(logger, msg, filename):
    # Open the attachment file for reading in binary mode, and make it a MIMEImage class
    with open(filename, "rb") as f:
        file_attachment = MIMEImage(f.read())
    # Add header/name to the attachments    
    file_attachment.add_header(
        "Content-Disposition",
        "attachment; filename= {filename}",
    )
    # Attach the file to the message
    msg.attach(file_attachment)


if __name__ == "__main__":
    bgl = ["Picotin 18 Trick or Treat!"]
    lkl = ["https://www.hermes.com/us/en/product/basketball-key-ring-H074749CKAA/"]
    imgl = ["https://assets.hermes.com/is/image/hermesproduct/602900V085_worn_1?&wid=200&hei=200"]
    send_email("danielhou315@gmail.com", bgl, lkl, imgl)

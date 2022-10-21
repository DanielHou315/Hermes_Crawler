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
def send_email(client_email, name_list, link_list, image_list):
    print("[Msg] Sending Email")
    receiver = client_email
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)                             # creates SMTP session 
        s.starttls()                                                        # start TLS for security 
        s.login("hermescrawlerapp@gmail.com", "kgqnrsunopoyccpw")   # Authentication 
    except:
        return

    msg = MIMEMultipart()
    msg['Subject'] = "Hermes Updater Message"
    msg['From'] = sender
    msg['To'] = receiver
    print("[Msg] Created Email Object")

    # Process Bag List
    msg.attach(MIMEText(begin_html, 'html'))
    if not os.path.isdir("img_cache"):
        os.mkdir("img_cache")
    print("[Msg] Created Image Cached Directory")

    i = 0
    while i < len(name_list):
        # Add bag name
        entry = "<b><p> - "
        # Add bag webstore link if applicable
        if link_list[i] != "None":
            print("[Msg] Attaching Link {0}".format(link_list[i]))
            entry += '<a href="{0}">'.format(link_list[i])
            entry = entry + name_list[i] + "</a>"
            print("[Msg] Attached Link")
        else:
            entry += name_list[i]
        entry += "</p></b>"
        msg.attach(MIMEText(entry, 'html'))
        print("[Msg] Added object text")

        # Add bag image if applicable
        if image_list[i] != "None":
            print("[Msg] Attaching Image {0}".format(image_list[i]))
            img_name = crawler.get_image(image_list[i], i)
            attach_img(msg, img_name)
            print("[Msg] Attached Image {0}".format(img_name))
            del img_name
        i += 1
        
    msg.attach(MIMEText(end_html, 'html'))
    
    # Clean up img_cache directory
    for root, dirs, files in os.walk("img_cache"):
        for file in files:
            os.remove("img_cache/" + file)
    os.rmdir("img_cache")
    print("[Msg] Cleared Image Cache")

    '''
    with open("testout.html", "w") as f:
        f.write(msg.as_string())
        f.close()
    print("[Msg] Written Test Email HTML")
    '''

    # Send email and exit
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()

    print("[Msg] Sent Email")
    return



def attach_img(msg, filename):
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

import smtplib, ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(port: int, smtp_server: str, sender_email: str, receiver_email: str, password: str, subject: str, message: str, message_html: str, support=None):
    if support is None:
        support = sender_email
    try:
        # Nastavení MIME zprávy
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["MIME-Version"] = "1.0"
        msg["Reply-To"] = support

        # Přidání textové části zprávy
        part1 = MIMEText(message, "plain", "utf-8")
        msg.attach(part1)

        part2 = MIMEText(message_html, "html", "utf-8")
        msg.attach(part2)

        print(f"Setting up SSL context...")
        context = ssl.create_default_context()

        print(f"Connecting to SMTP server: {smtp_server}:{port}")
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            print(f"Logging in as {sender_email}...")
            server.login(sender_email, password)

            print(f"Sending email from {sender_email} to {receiver_email}...")
            server.sendmail(sender_email, receiver_email, msg.as_string())

        print("Email sent successfully!")
        return True

    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def compose_message(book_name: str, your_book: bool, book_url: str, support=None):
    if your_book: addressing = "U vaší knihy"
    else: addressing = "U knihy, kde jste zájemcem"
    result_plain = f"{addressing} - {book_name} je aktulizace. Více zde: {book_url}"
    if support: result_plain += f"\nNa tento e-mail přímo neodpovídejte, není pravidelně kontrolován. Máte-li dotazy, může nás kontaktovat na {support}.\n"

    disclaimer = "Tento e-mail jste dostali, protože máte povolené notifikace na e-mail. Notifikace na email zakážete v nastavení Burzagu."
    result_plain += disclaimer + " https://eburzaucebnicagkm.web.app/user#settings"
    result_html = f"""\
    <html lang="cs">
    <head>
        <meta charset="UTF-8">
    </head>

      <body>
        <p>{addressing} - <b>{book_name}</b> je aktulizace. Více zde: <a href="{book_url}">{book_url}</a></p>
        <p>Na tento e-mail přímo neodpovídejte, není pravidelně kontrolován. Máte-li dotazy, může nás kontaktovat na <a href="mailto:{support}">{support}</a>.</p>
        <footer>{disclaimer} <a href="https://eburzaucebnicagkm.web.app/user#settings">Nastavení Burzagu<a/></footer>
      </body>
    </html>
    """
    return result_plain, result_html

if __name__ == "__main__": print(compose_message("fyzika", True, "dsgfdgsh", "help@erhgf.vh")) #test

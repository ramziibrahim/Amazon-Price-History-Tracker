import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
import os
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

env = Environment(loader=FileSystemLoader("templates"))

async def send_price_alert_email(user_email: str, asin: str, current_price: float, target_price: float):
    template = env.get_template("price_alert.html")
    html_content = template.render(
        current_price=current_price,
        target_price=target_price,
        product_url=f"https://www.amazon.com/dp/{asin}"
    )

    message = MIMEMultipart()
    message["From"] = SMTP_USER
    message["To"] = user_email
    message["Subject"] = f"Price Alert: Your target price of ${target_price} has been reached!"

    message.attach(MIMEText(html_content, "html"))

    await aiosmtplib.send(
        message,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        username=SMTP_USER,
        password=SMTP_PASSWORD,
        use_tls=True
    ) 
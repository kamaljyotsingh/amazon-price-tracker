from flask import Flask, render_template, request
from scraper import get_amazon_product_details
from email_alert import send_mail
from database import init_db, save_product
from apscheduler.schedulers.background import BackgroundScheduler
from database import get_all_products, mark_email_sent
import os

app = Flask(__name__)
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    product_data = None

    if request.method == 'POST':
        product_url = request.form['product_url']
        desired_price = float(request.form['desired_price'])

        title, current_price = get_amazon_product_details(product_url)

        if current_price is not None:
            # Save product to database
            save_product(product_url, title, current_price, desired_price)

            if current_price <= desired_price:
                status = "✅ Price is below your target!"

                # Send email alert
                send_mail(
                    to_email="kamaljyotsingh@gmail.com",
                    product_title=title,
                    current_price=current_price,
                    product_url=product_url
                )
            else:
                status = "❌ Still expensive."

            product_data = {
                "title": title,
                "current_price": current_price,
                "desired_price": desired_price,
                "status": status
            }
        else:
            product_data = {"error": "Could not fetch product price. Please check the URL."}

    return render_template('index.html', product_data=product_data)

def check_prices():
    print("🔍 Checking prices in background...")
    products = get_all_products()

    for prod in products:
        prod_id, url, title, old_price, desired_price, email_sent = prod
        title, current_price = get_amazon_product_details(url)

        if current_price is None:
            print(f"❌ Failed to fetch: {url}")
            continue

        if current_price <= desired_price:
            print(f"📩 Sending email for: {title}")
            send_mail("kamaljyotsingh@gmail.com", title, current_price, url)
            mark_email_sent(prod_id)
        else:
            print(f"⚠️ Still expensive: {title} @ ₹{current_price}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    # Start background price checker
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_prices, 'interval', minutes=60)  # every 60 minutes
    scheduler.start()

    # Start Flask app
    app.run(debug=True, port=port)
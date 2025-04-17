import os
from flask import Flask, render_template, redirect, request
import stripe
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

YOUR_DOMAIN = "https://donkgroup.onrender.com/"  # Cambialo con il tuo dominio su Render

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': os.getenv("STRIPE_PRICE_ID"),
                    'quantity': 1,
                },
            ],
            mode='subscription',
            success_url=YOUR_DOMAIN + '/dashboard?success=true',
            cancel_url=YOUR_DOMAIN + '/dashboard?canceled=true',
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)

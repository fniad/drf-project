import stripe
from django.conf import settings
from payment.models import Payment


class PaymentService:
    @staticmethod
    def get_payment_info(payment_id):
        try:
            payment = Payment.objects.get(id=payment_id)
            retrieve_id = payment.retrieve_id
            stripe.api_key = settings.STRIPE_SECRET_KEY
            payment_intent = stripe.PaymentIntent.retrieve(retrieve_id)
            return payment, payment_intent
        except Payment.DoesNotExist:
            return None, None
        except stripe.error.InvalidRequestError as e:
            return None, None
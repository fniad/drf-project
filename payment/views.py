""" Представления для payments """
from pprint import pprint
import stripe
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from payment.models import Payment, StripeCheckoutSession
from payment.serializers import PaymentSerializer, SuccessPaymentSerializer, PaymentRetrieveSerializer
from payment.serviсes import PaymentService
from training_courses.models import Course, Lesson

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentListAPIView(generics.ListAPIView):
    """ Список оплат отсортированный по датам, с фильтрами по курсам, урокам и методу оплаты"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all().order_by('date_pay')
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('payment_method',)
    ordering_fields = ('date_pay',)
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """ Подробная информация оплаты """
    serializer_class = PaymentRetrieveSerializer
    queryset = Payment.objects.all().order_by('date_pay')
    permission_classes = [IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Создание оплаты """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = request.data
        if 'course' in data:
            product = get_object_or_404(Course, pk=data['course']['id'])
        else:
            product = get_object_or_404(Lesson, pk=data['lesson']['id'])

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': product.stripe_price_data,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://localhost:8000/' +
                            reverse('payment:success') + '?session_id={CHECKOUT_SESSION_ID}')

        except Exception as e:

            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        payment = Payment.objects.create(
            user=request.user,
            payment_amount=product.price,
            payment_method='card',
            content_object=product
        )

        payment.save()

        stripe_session = StripeCheckoutSession.objects.create(
            stripe_id=checkout_session.stripe_id,
            status=checkout_session['status'],
            payment=payment,
        )
        stripe_session.save()

        return Response({'payment_url': checkout_session.url}, status=status.HTTP_201_CREATED)


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """ Изменение оплаты """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all().order_by('date_pay')
    permission_classes = [IsAuthenticated]


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """ Удаление оплаты """
    queryset = Payment.objects.all().order_by('date_pay')
    permission_classes = [IsAuthenticated]


class PaymentSuccessView(generics.ListAPIView):
    serializer_class = SuccessPaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        stripe_session = get_object_or_404(StripeCheckoutSession, stripe_id=request.GET.get('session_id'))
        checkout_session = StripeCheckoutSession.objects.get(stripe_id=stripe_session.stripe_id)
        session = stripe.checkout.Session.retrieve(checkout_session.stripe_id)
        stripe_session.status = session['status']
        stripe_session.save()
        retrieve_id = session['payment_intent']
        payment = checkout_session.payment
        payment.retrieve_id = retrieve_id
        payment.save()

        serializer = PaymentRetrieveSerializer(payment)

        return Response(serializer.data)
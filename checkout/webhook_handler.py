from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.db import transaction
from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import UserProfile
import json
import logging


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order}
        ).strip()
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {
                'order': order,
                'contact_email': settings.DEFAULT_FROM_EMAIL,
                # Round totals to two decimal places
                'order_total': round(order.order_total, 2),
                'delivery_cost': round(order.delivery_cost, 2),
                'grand_total': round(order.grand_total, 2),
            }
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """Handle a generic/unknown/unexpected webhook event"""
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """Handle the payment_intent.succeeded webhook from Stripe"""
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        shipping_details = intent.shipping
        grand_total = round(intent.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        profile = None
        username = intent.metadata.username
        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    profile.default_phone_number = shipping_details.phone
                    profile.default_country = shipping_details.address.country
                    profile.default_postcode = shipping_details.address.postal_code
                    profile.default_town_or_city = shipping_details.address.city
                    profile.default_street_address1 = shipping_details.address.line1
                    profile.default_street_address2 = shipping_details.address.line2
                    profile.default_county = shipping_details.address.state
                    profile.save()
            except UserProfile.DoesNotExist:
                profile = None  # Allow the order to proceed without a user profile

        # Check if the order already exists
        try:
            order = Order.objects.get(stripe_pid=pid)
            # If the order already exists, return early
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Order already exists',
                status=200,
            )
        except Order.DoesNotExist:
            pass

        # Create the order and update inventory
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    user_profile=profile,
                    email=shipping_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                    grand_total=grand_total,
                )
                for item_id, item_data in json.loads(bag).items():
                    product = Product.objects.select_for_update().get(id=item_id)
                    if isinstance(item_data, int):
                        if product.stock_quantity >= item_data:
                            product.stock_quantity -= item_data
                            product.save()
                            OrderLineItem.objects.create(
                                order=order,
                                product=product,
                                quantity=item_data,
                            )
                        else:
                            raise ValueError(f"Not enough stock for product {product.id}")
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            if product.stock_quantity >= quantity:
                                product.stock_quantity -= quantity
                                product.save()
                                OrderLineItem.objects.create(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    product_size=size,
                                )
                            else:
                                raise ValueError(f"Not enough stock for product {product.id}, size {size}")
        except Exception as e:
            if order:
                order.delete()
            logging.error(f"Error creating order or updating inventory: {e}")
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | ERROR: {e}',
                status=500,
            )

        self._send_confirmation_email(order)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Order created and inventory updated',
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )

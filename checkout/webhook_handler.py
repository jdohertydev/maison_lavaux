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
        print(f"Webhook received: {event['type']}")
        intent = event.data.object
        pid = intent.id
        bag = intent.metadata.bag
        print(f"Bag retrieved: {bag}")

        save_info = intent.metadata.save_info
        shipping_details = intent.shipping
        grand_total = round(intent.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None

        profile = None
        username = intent.metadata.username
        print(f"Username from metadata: {username}")
        if username != 'AnonymousUser':
            try:
                profile = UserProfile.objects.get(user__username=username)
                print(f"UserProfile found for username: {username}")
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
                profile = None
                print(f"No UserProfile found for username: {username}")

        # Check if the order already exists
        try:
            order = Order.objects.get(stripe_pid=pid)
            print(f"Order already exists: {order.stripe_pid}")
            self._send_confirmation_email(order)
            # Ensure inventory is updated for existing orders
            self._update_inventory(order, bag)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Order already exists',
                status=200,
            )
        except Order.DoesNotExist:
            print(f"No existing order found for PID: {pid}")
            order = None

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
                print(f"Order created: {order.id}")
                self._update_inventory(order, bag)
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

    def _update_inventory(self, order, bag):
        """Update inventory based on the bag"""
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Updating inventory for order {order.id}")

        try:
            bag_data = json.loads(bag)
            logger.info(f"Bag contents: {bag_data}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse bag JSON: {bag}, Error: {e}")
            raise ValueError("Invalid bag format")

        for item_id, item_data in bag_data.items():
            try:
                product = Product.objects.select_for_update().get(id=item_id)
                logger.info(f"Processing product {product.id}: Current stock {product.stock_quantity}")
            except Product.DoesNotExist:
                logger.error(f"Product with ID {item_id} does not exist")
                raise

            if isinstance(item_data, int):
                # Single quantity items
                if product.stock_quantity is None or product.stock_quantity < item_data:
                    logger.error(f"Insufficient stock for product {product.id}. "
                                f"Available: {product.stock_quantity}, Requested: {item_data}")
                    raise ValueError("Insufficient stock")
                product.stock_quantity -= item_data
                product.save()
                logger.info(f"Updated stock for product {product.id}: New stock {product.stock_quantity}")
            else:
                # Handle items with sizes
                for size, quantity in item_data['items_by_size'].items():
                    if product.stock_quantity is None or product.stock_quantity < quantity:
                        logger.error(f"Insufficient stock for product {product.id}, size {size}. "
                                    f"Available: {product.stock_quantity}, Requested: {quantity}")
                        raise ValueError("Insufficient stock")
                    product.stock_quantity -= quantity
                    product.save()
                    logger.info(f"Updated stock for product {product.id}, size {size}: New stock {product.stock_quantity}")



    def handle_payment_intent_payment_failed(self, event):
        """Handle the payment_intent.payment_failed webhook from Stripe"""
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )

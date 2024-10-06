from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from book.models import BorrowTransaction

@shared_task
def send_borrow_confirmation_email(user_email, book_title):
    send_mail(
        subject='Library Borrow Confirmation',
        message=f'You have successfully borrowed the book: {book_title}.',
        from_email='library@example.com',
        recipient_list=[user_email],
        fail_silently=False,
    )

@shared_task
def send_borrow_reminder_email():
    # Find all borrow transactions that are 3 days away from the return date
    due_date_threshold = timezone.now() + timedelta(days=3)
    transactions = BorrowTransaction.objects.filter(return_date__lte=due_date_threshold, returned=False)

    for transaction in transactions:
        user_email = transaction.user.email
        book_title = transaction.book.title
        send_mail(
            subject='Library Return Reminder',
            message=f'Reminder: The book "{book_title}" is due in 3 days.',
            from_email='library@example.com',
            recipient_list=[user_email],
            fail_silently=False,
        )


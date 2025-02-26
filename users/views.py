from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from bson import ObjectId
from .models import CustomUser, Document
from .forms import RegisterForm, DocumentForm

# from django.shortcuts import render, get_object_or_404
# from .models import CustomUser, Document
from .forms import DocumentForm
import PyPDF2
from django.shortcuts import render, get_object_or_404
from .models import CustomUser, Document
from .forms import DocumentForm

from django.utils.timezone import now, timedelta
from django.db.models import Sum, Count
from .models import Document

def home(request):
    return render(request, 'users/home.html')




User = get_user_model()  # Get the custom user model

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, email=email, password=password1)
                login(request, user)
                request.session['username'] = username
                request.session['password'] = password1  # Storing password is not recommended
                return redirect('dashboard')
            else:
                return render(request, 'users/register.html', {'error': 'Username already exists'})
        else:
            return render(request, 'users/register.html', {'error': 'Passwords do not match'})
    
    return render(request, 'users/register.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'users/login.html', {'error': 'username or password is incorrect'})

def user_logout(request):
    logout(request)
    return redirect('login')


from bson import Decimal128  # Import Decimal128 from bson

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
from .models import Document

# @login_required
# def dashboard(request):
#     user = request.user
#     today = now().date()

#     # Define time ranges
#     start_of_week = today - timedelta(days=today.weekday())
#     start_of_month = today.replace(day=1)
#     start_of_year = today.replace(month=1, day=1)

#     def get_order_and_revenue(start_date):
#         documents = Document.objects.filter(user=user)
        
#         # Python-side filtering since database filtering on date is not working
#         filtered_docs = [doc for doc in documents if doc.uploaded_at.date() >= start_date]

#         revenue = sum(float(doc.price.to_decimal()) for doc in filtered_docs if doc.price is not None)
        
#         return {
#             "orders": len(filtered_docs),
#             "revenue": revenue
#         }

#     stats = {
#         "today": get_order_and_revenue(today),
#         "week": get_order_and_revenue(start_of_week),
#         "month": get_order_and_revenue(start_of_month),
#         "year": get_order_and_revenue(start_of_year),
#         "all_time": {
#             "orders": Document.objects.filter(user=user).count(),
#             "revenue": sum(float(doc.price.to_decimal()) for doc in Document.objects.filter(user=user) if doc.price is not None)
#         }
#     }

#     # Fetch all uploaded documents of the logged-in owner
#     all_orders = Document.objects.filter(user=user).order_by('-uploaded_at')

#     # Count unique customers who uploaded documents for this logged-in owner
#     # unique_customers = Document.objects.filter(user=user).values_list('customer', flat=True).distinct().count()
#     # unique_customers = Document.objects.filter(user=user).values_list('user', flat=True).distinct().count()
#     unique_customers = len(set(Document.objects.filter(user=user).values_list('user', flat=True)))



#     completed_orders = Document.objects.filter(user=user, status="completed").count()
#     in_process_orders = Document.objects.filter(user=user, status="in_process").count()
#     pending_orders = Document.objects.filter(user=user, status="pending").count()

#     # Total pages printed by this owner
#     total_pages_printed = Document.objects.filter(user=user).aggregate(total_pages=Sum('num_pages'))['total_pages'] or 0

#     return render(request, 'users/dashboard.html', {
#         'user': user,
#         'stats': stats,
#         'all_orders': all_orders,
#         'total_customers': unique_customers,
#         "completed_orders": completed_orders,
#         "in_process_orders": in_process_orders,
#         "pending_orders": pending_orders,
#         "total_pages_printed": total_pages_printed,
#     })




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta
import os
import win32print
import win32api
from django.db.models.functions import TruncDate
from users.models import Document

@login_required
def dashboard(request):
    user = request.user
    today = now().date()

    # Define time ranges
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    def get_order_and_revenue(start_date):
        documents = Document.objects.filter(user=user)
        
        # Python-side filtering since database filtering on date is not working
        filtered_docs = [doc for doc in documents if doc.uploaded_at.date() >= start_date]

        revenue = sum(float(doc.price.to_decimal()) for doc in filtered_docs if doc.price is not None)
        
        return {
            "orders": len(filtered_docs),
            "revenue": revenue
        }
    

    stats = {
        "today": get_order_and_revenue(today),
        "week": get_order_and_revenue(start_of_week),
        "month": get_order_and_revenue(start_of_month),
        "year": get_order_and_revenue(start_of_year),
        "all_time": {
            "orders": Document.objects.filter(user=user).count(),
            "revenue": sum(float(doc.price.to_decimal()) for doc in Document.objects.filter(user=user) if doc.price is not None)
        }
    }

    # Fetch all uploaded documents of the logged-in owner
    all_orders = Document.objects.filter(user=user).order_by('-uploaded_at')

    # Count unique customers who uploaded documents
    unique_customers = len(set(Document.objects.filter(user=user).values_list('user', flat=True)))

    completed_orders = Document.objects.filter(user=user, status="completed").count()
    in_process_orders = Document.objects.filter(user=user, status="in_process").count()
    pending_orders = Document.objects.filter(user=user, status="pending").count()

    # Total pages printed by this owner
    total_pages_printed = Document.objects.filter(user=user).aggregate(total_pages=Sum('num_pages'))['total_pages'] or 0

    printer_status = is_printer_connected()

    # **Automatic Printing of Pending Orders**
    printer_name = win32print.GetDefaultPrinter()  # Get default printer
    if pending_orders > 0:
        print_pending_orders(user, printer_name)

    return render(request, 'users/dashboard.html', {
        'user': user,
        'stats': stats,
        'all_orders': all_orders,
        'total_customers': unique_customers,
        "completed_orders": completed_orders,
        "in_process_orders": in_process_orders,
        "pending_orders": pending_orders,
        "total_pages_printed": total_pages_printed,
        'printer_status': printer_status,
    })

import platform

def is_printer_connected():
    """Check if a printer is connected."""
    try:
        if platform.system() == "Windows":
            import win32print
            printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
            return bool(printers)  # True if printers exist
        else:
            import cups
            conn = cups.Connection()
            printers = conn.getPrinters()
            return bool(printers)  # True if printers exist
    except Exception as e:
        print(f"Error checking printer status: {e}")
        return False


def print_pending_orders(user, printer_name):
    """Process pending print jobs and update their statuses."""
    pending_orders = Document.objects.filter(user=user, status='pending')
    # from users.models import Document

    for doc in Document.objects.all():
        print(f"ID: {doc.id}, Price: {doc.price}, Type: {type(doc.price)}")

    for order in pending_orders:
        file_path = order.file.path

        if not os.path.exists(file_path):
            continue  # Skip if file doesn't exist

        try:
            # Mark as 'in_process' before printing
            order.status = 'in_process'
            order.save()

            win32api.ShellExecute(0, "print", file_path, f'/d:"{printer_name}"', ".", 0)

            # After sending to printer, mark as completed
            order.status = 'completed'
            order.save()
        except Exception as e:
            print(f"Error printing {file_path}: {e}")





def calculate_price(document):
    """Calculate the price based on the number of pages, print type, and copies."""
    pdf_reader = PyPDF2.PdfReader(document.file)
    num_pages = len(pdf_reader.pages)

    # Get customization options
    color_type = document.color_type  # 'black_white', 'color', or 'both'
    num_copies = document.num_copies
    double_sided = document.double_sided  # True or False

    # Adjust pages for double-sided printing
    if double_sided:
        num_pages = (num_pages + 1) // 2  # Round up if pages are odd

    # Pricing logic
    if color_type == "black_white":
        price_per_page = 5
    elif color_type == "color":
        price_per_page = 10
    elif color_type == "both":
        price_per_page = 4  # Black & White price with discount
    else:
        price_per_page = 0  # Default case (should not happen)

    # Final price calculation
    total_price = num_pages * price_per_page * num_copies
    return total_price

def upload_document(request, unique_url):
    """
    Allows customers to upload a document with print customizations.
    The document is automatically linked to a specific shop owner.
    """
    # user = get_object_or_404(CustomUser, unique_url=unique_url)
    user = CustomUser.objects.filter(unique_url=unique_url).first()

    # if not user:
    #     raise Http404("User not found")
    
    print("This is slug URL : ", unique_url)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = user
            document.price = calculate_price(document)  # Calculate price
            document.save()
            return render(request, 'users/upload_success.html', {'user': user, 'price': document.price})

    else:
        form = DocumentForm()

    return render(request, 'users/upload.html', {'form': form, 'user': user})






# from rest_framework.decorators import api_view, renderer_classes
# from rest_framework.response import Response
# from rest_framework.renderers import JSONRenderer
# from .models import Order
# from .serializers import OrderSerializer

# @api_view(['GET'])
# @renderer_classes([JSONRenderer])  # Ensure JSON response
# def get_pending_orders(request):
#     pending_orders = Order.objects.filter(status="pending")
#     print("these are pending orders : ", pending_orders)
#     serializer = OrderSerializer(pending_orders, many=True)
#     return Response(serializer.data)  # Returns JSON

# @api_view(['POST'])
# def update_order_status(request, order_id):
#     try:
#         order = Order.objects.get(id=order_id)
#         order.status = request.data.get('status', order.status)
#         order.save()
#         return Response({"message": "Order updated successfully!"})
#     except Order.DoesNotExist:
#         return Response({"error": "Order not found!"}, status=404)

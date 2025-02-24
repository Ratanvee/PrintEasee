import os
import django
import sys
import time
from django.utils.timezone import now

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # Add current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Add project root to Python path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")  # Ensure Django settings are loaded
django.setup()  # Initialize Django

from users.models import Document  # Import AFTER setting up Django
from printer_agent.printer_utils import send_to_printer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")  
django.setup()  # Initialize Django environment

def process_print_queue():
    while True:
        pending_orders = Document.objects.filter(status="pending").order_by("uploaded_at")
        
        if not pending_orders.exists():
            print("No pending print jobs. Waiting...")
            time.sleep(10)  # Wait 10 seconds before checking again
            continue

        for order in pending_orders:
            print(f"Processing print order: {order.file.name}")
            order.status = "in_process"
            order.save()

            success = send_to_printer(order.file.path)
            order.status = "completed" if success else "pending"
            order.save()

        print("Print queue processed. Checking again in 10 seconds...")
        time.sleep(10)  # Adjust time delay as needed

if __name__ == "__main__":
    process_print_queue()

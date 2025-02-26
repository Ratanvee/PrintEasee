import os
import win32print
import win32api
from django.core.management.base import BaseCommand
from users.models import PrintOrder

class Command(BaseCommand):
    help = "Check pending orders and print them automatically on Windows"

    def handle(self, *args, **kwargs):
        printer_name = win32print.GetDefaultPrinter()  # Get the default printer

        if not printer_name:
            self.stdout.write(self.style.ERROR("No printers found!"))
            return

        self.stdout.write(self.style.SUCCESS(f"Using printer: {printer_name}"))

        # Get pending orders
        pending_orders = PrintOrder.objects.filter(status='pending')

        if not pending_orders:
            self.stdout.write("No pending orders to print.")
            return

        for order in pending_orders:
            file_path = order.file.path  # Get file path

            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f"File {file_path} not found!"))
                continue

            self.stdout.write(f"Printing {file_path}...")

            try:
                win32api.ShellExecute(0, "print", file_path, f'/d:"{printer_name}"', ".", 0)
                order.status = 'completed'
                order.save()
                self.stdout.write(self.style.SUCCESS(f"Printed {file_path} successfully!"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to print {file_path}: {str(e)}"))

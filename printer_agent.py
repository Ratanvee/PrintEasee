import win32print

def get_real_connected_printer():
    printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)

    if not printers:
        print("No printers found.")
        return False

    real_printers = []
    
    for printer in printers:
        printer_name = printer[2]  # Get printer name
        printer_info = win32print.OpenPrinter(printer_name)
        printer_status = win32print.GetPrinter(printer_info, 2)
        
        # Get the status of the printer
        status_flags = printer_status['Status']
        
        # Printer status conditions (flags)
        if status_flags == 0:  # 0 means the printer is ready
            real_printers.append(printer_name)
    
    if real_printers:
        print("Connected Printers:")
        for printer in real_printers:
            print(f"✅ {printer}")
        return True
    else:
        print("❌ No real printers connected and ready.")
        return False

# Run the function
get_real_connected_printer()

import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import os
from datetime import datetime
from sidebar import Sidebar  # Import the shared sidebar component

# Reportlab imports for PDF generation (only needed for invoice download)
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class FeePaymentSystem:
    def __init__(self, parent_frame, student_id, nav_callbacks=None):
        self.parent_frame = parent_frame
        self.student_id = student_id
        self.nav_callbacks = nav_callbacks
        
        # Configure appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create sidebar with navigation
        self.sidebar = Sidebar(self.parent_frame, active_item="fee_payment", nav_callbacks=self.nav_callbacks)
        
        # Create content area
        self.create_content_area()
    
    def create_content_area(self):
        # Title
        ctk.CTkLabel(
            self.parent_frame, 
            text="Fee Payment", 
            font=("Arial", 24, "bold"), 
            text_color="#3B82F6"
        ).place(x=280, y=20)
        
        # Create download invoice button
        self.create_download_button()
        
        # Create fee breakdown section
        self.create_fee_breakdown()
        
        # Create due payments table
        self.create_due_payments_table()
        
        # Create pay now button
        self.create_pay_now_button()
    
    def create_download_button(self):
        # Download Invoice Button
        self.download_btn = ctk.CTkButton(
            self.parent_frame, 
            text="Download Invoice", 
            font=("Arial", 12, "bold"), 
            fg_color="#3B82F6",
            text_color="white", 
            width=150, 
            height=35, 
            corner_radius=5,
            command=self.download_invoice
        )
        self.download_btn.place(x=280, y=60)

    def create_fee_breakdown(self):
        # Fee Breakdown Frame
        self.fee_breakdown_frame = ctk.CTkFrame(
            self.parent_frame, 
            width=400, 
            height=250, 
            fg_color="white", 
            border_width=1,
            border_color="#DDDDDD"
        )
        self.fee_breakdown_frame.place(x=280, y=120)

        # Fee Breakdown Title
        ctk.CTkLabel(
            self.fee_breakdown_frame, 
            text="Fee Breakdown", 
            font=("Arial", 18, "bold"), 
            text_color="black"
        ).place(x=20, y=20)

        # Fetch and display fee breakdown
        self.fetch_fee_breakdown()

    def fetch_fee_breakdown(self):
        """Fetch fee breakdown from database"""
        try:
            # Establish database connection
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor(dictionary=True)

            # Check if student_fees table exists
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.tables 
                WHERE table_schema = 'college_system' AND table_name = 'student_fees'
            """)
            
            if cursor.fetchone()['COUNT(*)'] == 0:
                # Create student_fees table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS student_fees (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        student_id INT,
                        fee_type VARCHAR(100),
                        amount DECIMAL(10,2),
                        payment_status ENUM('Paid', 'Unpaid') DEFAULT 'Unpaid',
                        payment_date DATE,
                        FOREIGN KEY (student_id) REFERENCES students(student_id)
                    )
                """)
                
                # Insert sample fee data
                sample_fees = [
                    (self.student_id, 'Tuition Fee', 1500.00, 'Unpaid', None),
                    (self.student_id, 'Library Fee', 100.00, 'Unpaid', None),
                    (self.student_id, 'Lab Fee', 200.00, 'Unpaid', None),
                    (self.student_id, 'Activity Fee', 50.00, 'Paid', datetime.now().date())
                ]
                
                cursor.executemany("""
                    INSERT INTO student_fees 
                    (student_id, fee_type, amount, payment_status, payment_date) 
                    VALUES (%s, %s, %s, %s, %s)
                """, sample_fees)
                
                connection.commit()

            # Fetch fee breakdown
            cursor.execute("""
                SELECT fee_type, amount, payment_status
                FROM student_fees 
                WHERE student_id = %s
            """, (self.student_id,))
            fees = cursor.fetchall()

            # Display fee details
            y_pos = 60
            total = 0
            total_paid = 0
            total_unpaid = 0
            
            for fee in fees:
                amount_str = f"${fee['amount']:.2f}"
                status_color = "#4CAF50" if fee['payment_status'] == 'Paid' else "#F44336"
                
                # Fee type and amount
                ctk.CTkLabel(
                    self.fee_breakdown_frame, 
                    text=f"{fee['fee_type']}", 
                    font=("Arial", 14), 
                    text_color="black",
                    anchor="w"
                ).place(x=20, y=y_pos)
                
                # Amount
                ctk.CTkLabel(
                    self.fee_breakdown_frame, 
                    text=amount_str, 
                    font=("Arial", 14), 
                    text_color="black",
                    anchor="e"
                ).place(x=250, y=y_pos)
                
                # Status
                ctk.CTkLabel(
                    self.fee_breakdown_frame, 
                    text=fee['payment_status'], 
                    font=("Arial", 14), 
                    text_color=status_color,
                    anchor="e"
                ).place(x=350, y=y_pos)
                
                y_pos += 30
                total += fee['amount']
                
                if fee['payment_status'] == 'Paid':
                    total_paid += fee['amount']
                else:
                    total_unpaid += fee['amount']

            # Display totals with separator line
            separator = ctk.CTkFrame(
                self.fee_breakdown_frame,
                height=2,
                width=360,
                fg_color="#DDDDDD"
            )
            separator.place(x=20, y=y_pos)
            y_pos += 20
            
            # Total amount
            ctk.CTkLabel(
                self.fee_breakdown_frame, 
                text="Total:", 
                font=("Arial", 14, "bold"), 
                text_color="black",
                anchor="w"
            ).place(x=20, y=y_pos)
            
            ctk.CTkLabel(
                self.fee_breakdown_frame, 
                text=f"${total:.2f}", 
                font=("Arial", 14, "bold"), 
                text_color="black",
                anchor="e"
            ).place(x=250, y=y_pos)
            
            y_pos += 30
            
            # Total paid
            ctk.CTkLabel(
                self.fee_breakdown_frame, 
                text="Paid:", 
                font=("Arial", 14), 
                text_color="#4CAF50",
                anchor="w"
            ).place(x=20, y=y_pos)
            
            ctk.CTkLabel(
                self.fee_breakdown_frame, 
                text=f"${total_paid:.2f}", 
                font=("Arial", 14), 
                text_color="#4CAF50",
                anchor="e"
            ).place(x=250, y=y_pos)
            
            y_pos += 30
            
            # Total due
            ctk.CTkLabel(
                self.fee_breakdown_frame, 
                text="Due:", 
                font=("Arial", 14, "bold"), 
                text_color="#F44336",
                anchor="w"
            ).place(x=20, y=y_pos)
            
            ctk.CTkLabel(
                self.fee_breakdown_frame, 
                text=f"${total_unpaid:.2f}", 
                font=("Arial", 14, "bold"), 
                text_color="#F44336",
                anchor="e"
            ).place(x=250, y=y_pos)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def create_due_payments_table(self):
        # Due Payments Frame
        self.due_payments_frame = ctk.CTkFrame(
            self.parent_frame, 
            width=400, 
            height=250, 
            fg_color="white", 
            border_width=1,
            border_color="#DDDDDD"
        )
        self.due_payments_frame.place(x=700, y=120)

        # Due Payments Title
        ctk.CTkLabel(
            self.due_payments_frame, 
            text="Due Payments", 
            font=("Arial", 18, "bold"), 
            text_color="black"
        ).place(x=20, y=20)

        # Create Treeview
        columns = ("Description", "Amount", "Status")
        self.tree = ttk.Treeview(
            self.due_payments_frame, 
            columns=columns, 
            show="headings", 
            height=8
        )
        self.tree.place(x=20, y=60, width=360, height=170)

        # Configure columns
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Status", text="Status")
        self.tree.column("Description", width=200, anchor="w")
        self.tree.column("Amount", width=80, anchor="e")
        self.tree.column("Status", width=80, anchor="center")

        # Configure tags for status colors
        self.tree.tag_configure("unpaid", foreground="#F44336")

        # Fetch and populate due payments
        self.fetch_due_payments()

    def fetch_due_payments(self):
        """Fetch due payments from database"""
        try:
            # Establish database connection
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor(dictionary=True)

            # Fetch due payments
            cursor.execute("""
                SELECT fee_type, amount, payment_status
                FROM student_fees 
                WHERE student_id = %s AND payment_status = 'Unpaid'
            """, (self.student_id,))
            fees = cursor.fetchall()

            # Clear existing items
            for i in self.tree.get_children():
                self.tree.delete(i)

            # Insert data into table
            for fee in fees:
                self.tree.insert(
                    "", 
                    "end", 
                    values=(fee['fee_type'], f"${fee['amount']:.2f}", fee['payment_status']),
                    tags=("unpaid",)
                )

            # If no unpaid fees, show message
            if not fees:
                self.tree.insert("", "end", values=("No due payments", "", ""), tags=())

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def create_pay_now_button(self):
        # Pay Now Button
        self.pay_now_btn = ctk.CTkButton(
            self.parent_frame, 
            text="Pay Now", 
            font=("Arial", 16, "bold"), 
            fg_color="#3B82F6",
            text_color="white", 
            width=300, 
            height=50, 
            corner_radius=8, 
            hover_color="#2A62D6",
            command=self.process_payment
        )
        self.pay_now_btn.place(x=400, y=400)

    def process_payment(self):
        """Process fee payment"""
        # Check if there are any unpaid fees
        if not self.tree.get_children() or self.tree.item(self.tree.get_children()[0])["values"][0] == "No due payments":
            messagebox.showinfo("No Due Payments", "There are no payments due at this time.")
            return

        # Confirm payment
        if not messagebox.askyesno("Confirm Payment", "Are you sure you want to process payment for all due fees?"):
            return

        try:
            # Establish database connection
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor()

            # Update payment status for unpaid fees
            cursor.execute("""
                UPDATE student_fees 
                SET payment_status = 'Paid', 
                    payment_date = CURRENT_DATE 
                WHERE student_id = %s AND payment_status = 'Unpaid'
            """, (self.student_id,))

            connection.commit()
            
            if cursor.rowcount > 0:
                messagebox.showinfo("Payment Successful", f"Payment for {cursor.rowcount} item(s) has been processed successfully.")
            else:
                messagebox.showinfo("No Payments", "No payments were processed.")

            # Refresh fee breakdown and due payments table
            self.fetch_fee_breakdown()
            self.fetch_due_payments()

        except mysql.connector.Error as err:
            messagebox.showerror("Payment Error", str(err))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

    def download_invoice(self):
        """Generate and download invoice PDF"""
        if not REPORTLAB_AVAILABLE:
            messagebox.showinfo("Feature Not Available", "PDF generation requires the ReportLab library.")
            return
            
        try:
            # Open file dialog to choose save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf")],
                initialfile="fee_invoice.pdf"
            )
            
            if not file_path:
                return

            # Establish database connection
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="new_password",
                database="college_system"
            )
            cursor = connection.cursor(dictionary=True)

            # Fetch student and fee details
            cursor.execute("""
                SELECT s.name, sf.fee_type, sf.amount, sf.payment_status
                FROM students s
                JOIN student_fees sf ON s.student_id = sf.student_id
                WHERE s.student_id = %s
            """, (self.student_id,))
            fee_details = cursor.fetchall()

            # Create PDF
            doc = SimpleDocTemplate(file_path, pagesize=letter)
            elements = []

            # Styles
            styles = getSampleStyleSheet()
            title = Paragraph("Student Fee Invoice", styles['Title'])
            elements.append(title)

            # Student Details
            if fee_details:
                student_name = fee_details[0]['name']
                student_info = Paragraph(f"Student Name: {student_name}", styles['Normal'])
                elements.append(student_info)
                elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
                elements.append(Paragraph(f"Invoice #: INV-{self.student_id}-{datetime.now().strftime('%Y%m%d')}", styles['Normal']))
                elements.append(Paragraph(" ", styles['Normal']))  # Spacer

            # Create table data
            table_data = [['Fee Type', 'Amount', 'Status']]
            total = 0
            for fee in fee_details:
                table_data.append([
                    fee['fee_type'], 
                    f"${fee['amount']}", 
                    fee['payment_status']
                ])
                total += fee['amount']

            # Add total row
            table_data.append(['Total', f"${total}", ''])

            # Create table
            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 12),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            elements.append(table)

            # Build PDF
            doc.build(elements)

            messagebox.showinfo("Invoice Downloaded", f"Invoice saved to {file_path}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", str(err))
        except Exception as e:
            messagebox.showerror("Download Error", str(e))
        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

# This allows the module to be run directly for testing
def main():
    root = ctk.CTk()
    root.title("Fee Payment")
    root.geometry("1200x700")
    
    main_frame = ctk.CTkFrame(root, fg_color="white")
    main_frame.pack(fill='both', expand=True)
    
    app = FeePaymentSystem(main_frame, student_id=1)
    
    root.mainloop()

if __name__ == "__main__":
    main()
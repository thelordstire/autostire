# -*- coding: utf-8 -*-
import json
import uuid
import time
from datetime import datetime

# ==========================================
# نواة العمليات (Operations Core) - نسخة محدثة ومطورة
# تدعم البرمجة الشيئية (OOP) بشكل كامل وأداة التفصيل والتشغيل الديناميكي لكافة أنواع الخامات دون قوالب جامدة
# ==========================================

class InventoryItemObject:
    """
    كائن يمثل قطعة غيار أو كمالية سيارات في النظام (مراقب ومسجل).
    """
    def __init__(self, part_id, part_number, name_ar, name_en, category, quantity, wholesale_price, retail_price, compatibility="", is_special=0, special_properties="{}"):
        self.part_id = part_id
        self.part_number = part_number
        self.name_ar = name_ar
        self.name_en = name_en
        self.category = category
        self.quantity = float(quantity)
        self.wholesale_price = float(wholesale_price)
        self.retail_price = float(retail_price)
        self.compatibility = compatibility
        self.is_special = int(is_special)
        
        # تحليل الخصائص الخاصة للمواد ذات الطبيعة المعقدة
        try:
            self.special_properties = json.loads(special_properties) if isinstance(special_properties, str) else special_properties
        except Exception:
            self.special_properties = {}

    def is_low_stock(self, threshold=5.0) -> bool:
        """
        التحقق التلقائي إذا كانت الكمية المتوفرة حرجة وتتطلب إعادة طلب.
        """
        return self.quantity <= threshold

    def check_compatibility(self, car_query: str) -> bool:
        """
        التحقق من توافقية هذه القطعة مع سيارة معينة مدخلة في البحث.
        """
        if not self.compatibility:
            return True
        return car_query.lower() in self.compatibility.lower()

    def to_dict(self):
        return {
            "part_id": self.part_id,
            "part_number": self.part_number,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "category": self.category,
            "quantity": self.quantity,
            "wholesale_price": self.wholesale_price,
            "retail_price": self.retail_price,
            "compatibility": self.compatibility,
            "is_special": self.is_special,
            "special_properties": json.dumps(self.special_properties)
        }


class SpecialMaterialObject(InventoryItemObject):
    """
    كائن مرن للغاية ومطور، مصمم للتعامل مع أي نوع من الخامات القابلة للقص والتفصيل 
    (فيميه وتظليل، جلود وأقمشة تنجيد، أسلاك وضفائر كهربائية، عوازل حرارية، عوادم ومواسير حديدية)
    دون الالتزام بقوالب جامدة أو مفترضة مسبقاً، بل يتيح صياغة الحسابات بناءً على مدخلات حية بالكامل.
    """
    def __init__(self, part_id, part_number, name_ar, name_en, category, quantity, wholesale_price, retail_price, compatibility="", is_special=1, special_properties="{}"):
        super().__init__(part_id, part_number, name_ar, name_en, category, quantity, wholesale_price, retail_price, compatibility, is_special, special_properties)
        
        # وحدة قياس مرنة (متر، متر مربع، رول، لتر، قدم، كجم)
        if "unit_name" not in self.special_properties:
            self.special_properties["unit_name"] = "متر"
        if "default_waste_percentage" not in self.special_properties:
            self.special_properties["default_waste_percentage"] = 10.0

    def calculate_custom_fabrication(self, job_title: str, required_qty: float, waste_percentage: float, labor_fee: float, additional_material_fee: float = 0.0) -> dict:
        """
        أداة الحساب والتشغيل الديناميكي الفائقة:
        تتيح للمستخدم إدخال أي خامة وتحديد الأمتار أو الكمية المطلوبة بشكل ديناميكي كامل وتعديل الهدر والمصنعيات 
        وتكلفة المواد المساعدة الأخرى لحظة التشغيل، مما يحل مشكلة تنوع الحالات والسيارات والخامات.
        
        المعادلة الرياضية للتشغيل:
        1. الكمية المستهلكة الإجمالية شاملة الهدر = الكمية الأساسية * (1 + نسبة الهدر / 100)
        2. تكلفة الخامة لطلب العميل = الكمية المستهلكة الإجمالية * سعر البيع للوحدة
        3. التكلفة الإجمالية للفاتورة = تكلفة الخامة + تكلفة العمالة والمصنعية + تكلفة المواد المساعدة الأخرى
        """
        # حساب الكمية المستهلكة الكلية شاملة الهدر
        waste_multiplier = 1.0 + (waste_percentage / 100.0)
        total_qty_consumed = required_qty * waste_multiplier
        qty_wasted_only = total_qty_consumed - required_qty
        
        # حساب تكلفة الخامة والبيع النهائي للوحدات المستهلكة
        material_retail_price = total_qty_consumed * self.retail_price
        
        # السعر النهائي المطلوب من الزبون
        total_customer_price = material_retail_price + labor_fee + additional_material_fee
        
        # جرد المخزون التقديري المتبقي
        stock_remaining_after = max(0.0, self.quantity - total_qty_consumed)
        
        return {
            "part_id": self.part_id,
            "material_name": self.name_ar,
            "job_title": job_title, # اسم العملية ووصف التفصيل (مثلاً: تظليل زجاج تاهو خلفي / تنجيد مقاعد جيب لاندكروزر)
            "required_qty": required_qty,
            "unit_name": self.special_properties.get("unit_name", "متر"),
            "waste_percentage": waste_percentage,
            "total_qty_consumed": round(total_qty_consumed, 3),
            "qty_wasted_only": round(qty_wasted_only, 3),
            "material_retail_price": round(material_retail_price, 2),
            "labor_fee": round(labor_fee, 2),
            "additional_material_fee": round(additional_material_fee, 2),
            "total_customer_price": round(total_customer_price, 2),
            "stock_remaining_after": round(stock_remaining_after, 3)
        }


class EmployeeObject:
    """
    كائن ذكي يمثل موظفاً في النظام، تتبع شيفتاته، صلاحياته وعملياته.
    """
    def __init__(self, username, full_name, role, branch, is_active=1):
        self.username = username
        self.full_name = full_name
        self.role = role
        self.branch = branch
        self.is_active = bool(is_active)
        self.active_shift_id = None

    def has_access(self, action: str) -> bool:
        """
        التحقق البرمجي السريع من صلاحيات الموظف قبل الشروع في أي عملية بالواجهة أو الباكيند.
        """
        privileges = {
            "Admin": ["dashboard", "employees_management", "inventory_edit", "sales_billing", "reports_view", "security_logs", "import_export"],
            "Manager": ["dashboard", "inventory_edit", "sales_billing", "reports_view", "import_export"],
            "Cashier": ["sales_billing", "inventory_view"],
            "Technician": ["inventory_view", "tinting_calculator"]
        }
        return action in privileges.get(self.role, [])


class ShiftObject:
    """
    كائن يمثل الوردية اليومية لمراقبة الخزينة والكاش وحماية أموال المحل وتفادي العجز النقدي.
    """
    def __init__(self, shift_id, employee_username, start_time, initial_cash, closing_cash=0.0, actual_closing_cash=0.0, status="OPEN", notes=""):
        self.shift_id = shift_id
        self.employee_username = employee_username
        self.start_time = start_time
        self.initial_cash = float(initial_cash)
        self.closing_cash = float(closing_cash) if closing_cash else 0.0
        self.actual_closing_cash = float(actual_closing_cash) if actual_closing_cash else 0.0
        self.status = status
        self.notes = notes
        self.transactions = []

    def calculate_discrepancy(self) -> float:
        """
        حساب الفارق والعجز/الزيادة بين الكاش الفعلي المدخل يدوياً والكاش المتوقع بالنظام.
        """
        if self.status == "OPEN":
            return 0.0
        return self.actual_closing_cash - self.closing_cash


class InvoiceObject:
    """
    كائن يمثل فاتورة المبيعات الصادرة، يقوم بحساب الخصومات وضريبة القيمة المضافة الإجمالية.
    """
    def __init__(self, invoice_id, employee_username, customer_name, customer_phone, items, payment_method, discount=0.0):
        self.invoice_id = invoice_id
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.employee_username = employee_username
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.items = items  # قائمة قواميس تحتوي القطع، والكمية، وسعر الوحدة والتركيب
        self.payment_method = payment_method
        self.discount = float(discount)
        
        # حساب التكلفة الكلية
        self.subtotal = sum(item["qty"] * item["unit_price"] + item.get("labor_fee", 0.0) + item.get("additional_material_fee", 0.0) for item in self.items)
        self.total_amount = max(0.0, self.subtotal - self.discount)

    def generate_receipt_text(self, lang="ar") -> str:
        """
        توليد نص مخصص للفاتورة والوصل للطباعة الحرارية المباشرة (طباعة الفواتير للمحلات).
        """
        lines = []
        if lang == "ar":
            lines.append("===============================")
            lines.append("        لوردستاير لقطع الغيار        ")
            lines.append("        هاتف المحل: 0555555555       ")
            lines.append("===============================")
            lines.append(f"رقم الفاتورة: {self.invoice_id}")
            lines.append(f"التاريخ: {self.timestamp}")
            lines.append(f"البائع: {self.employee_username}")
            lines.append(f"الزبون: {self.customer_name or 'عميل سفري'}")
            lines.append("-------------------------------")
            for item in self.items:
                name = item["name_ar"]
                lines.append(f"{name}")
                lines.append(f" {item['qty']} x {item['unit_price']} = {item['qty']*item['unit_price']} ريال")
                if item.get("labor_fee", 0) > 0:
                    lines.append(f"  + مصنعية وشغل يد: {item['labor_fee']} ريال")
                if item.get("additional_material_fee", 0) > 0:
                    lines.append(f"  + مواد مساعدة أخرى: {item['additional_material_fee']} ريال")
            lines.append("-------------------------------")
            lines.append(f"المجموع الفرعي: {self.subtotal} ريال")
            lines.append(f"الخصم: {self.discount} ريال")
            lines.append(f"الصافي الإجمالي: {self.total_amount} ريال")
            lines.append(f"طريقة الدفع: {self.payment_method}")
            lines.append("===============================")
            lines.append("شكراً لتعاملكم معنا ورافقتكم السلامة")
        else:
            lines.append("===============================")
            lines.append("     LORDSTAIR AUTO PARTS     ")
            lines.append("===============================")
            lines.append(f"Invoice ID: {self.invoice_id}")
            lines.append(f"Date: {self.timestamp}")
            lines.append(f"Seller: {self.employee_username}")
            lines.append(f"Client: {self.customer_name or 'Walk-in Client'}")
            lines.append("-------------------------------")
            for item in self.items:
                name = item.get("name_en") or item["name_ar"]
                lines.append(f"{name}")
                lines.append(f" {item['qty']} x {item['unit_price']} = {item['qty']*item['unit_price']} SAR")
                if item.get("labor_fee", 0) > 0:
                    lines.append(f"  + Labor fee: {item['labor_fee']} SAR")
                if item.get("additional_material_fee", 0) > 0:
                    lines.append(f"  + Additional fee: {item['additional_material_fee']} SAR")
            lines.append("-------------------------------")
            lines.append(f"Subtotal: {self.subtotal} SAR")
            lines.append(f"Discount: {self.discount} SAR")
            lines.append(f"Total Net: {self.total_amount} SAR")
            lines.append(f"Payment: {self.payment_method}")
            lines.append("===============================")
            lines.append("Thank you for choosing Lordstair!")
            
        return "\n".join(lines)


class OperationsCore:
    """
    سيرفر الباكيند (نواة العمليات): يربط بين كائنات النظام ويقود المنطق التشغيلي للمحل.
    """
    def __init__(self, data_core, security_core):
        self.data_core = data_core
        self.security_core = security_core

    def authenticate_user(self, username, password) -> EmployeeObject:
        """
        تسجيل الدخول الآمن للموظف بعد التحقق من تشفير كلمته وفحص محاولات الاختراق.
        """
        employee_data = self.data_core.get_employee(username)
        if not employee_data:
            self.security_core.cybersecurity.register_login_attempt(username, success=False)
            self.security_core.log_and_secure("AUTHENTICATION", username, f"محاولة تسجيل دخول فاشلة للحساب غير الموجود: {username}", "WARNING")
            return None
        
        is_valid = self.security_core.cybersecurity.verify_password(password, employee_data["password_hash"])
        status = self.security_core.cybersecurity.register_login_attempt(username, success=is_valid)
        
        if is_valid and employee_data["is_active"] == 1:
            self.security_core.log_and_secure("AUTHENTICATION", username, f"تم تسجيل الدخول بنجاح للموظف {employee_data['full_name']}")
            emp_obj = EmployeeObject(
                username=employee_data["username"],
                full_name=employee_data["full_name"],
                role=employee_data["role"],
                branch=employee_data["branch"],
                is_active=employee_data["is_active"]
            )
            active_shift = self.data_core.get_active_shift(username)
            if active_shift:
                emp_obj.active_shift_id = active_shift["shift_id"]
            return emp_obj
        else:
            self.security_core.log_and_secure("AUTHENTICATION", username, f"محاولة دخول فاشلة للموظف المسجل بكلمة مرور غير صحيحة. الحساب: {username}", "CRITICAL" if status=="CRITICAL_ALERT" else "WARNING")
            return None

    def get_inventory_objects(self) -> list:
        """
        جلب كافة عناصر المخزون وتحويلها إلى كائنات OOP نشطة (Objects).
        """
        db_items = self.data_core.list_inventory()
        objects_list = []
        for item in db_items:
            if item["is_special"] == 1:
                objects_list.append(SpecialMaterialObject(**item))
            else:
                objects_list.append(InventoryItemObject(**item))
        return objects_list

    def process_checkout(self, employee: EmployeeObject, customer_name, customer_phone, items_in_cart, discount, payment_method) -> tuple:
        """
        إجراء عملية بيع متكاملة: تتبع الشفت، الخصم، تحديث المخزون، والتوثيق المزدوج في البلوكتشاين وقاعدة البيانات.
        """
        if not employee.active_shift_id:
            return False, "لا توجد وردية نشطة مفتوحة لك! يرجى فتح وردية أولاً للتمكن من البيع والمحاسبة."
            
        invoice_id = f"INV-{int(time.time())}"
        
        invoice = InvoiceObject(
            invoice_id=invoice_id,
            employee_username=employee.username,
            customer_name=customer_name,
            customer_phone=customer_phone,
            items=items_in_cart,
            payment_method=payment_method,
            discount=discount
        )
        
        db_success = self.data_core.create_sale_invoice(
            invoice_id=invoice.invoice_id,
            employee=employee.username,
            customer_name=customer_name,
            customer_phone=customer_phone,
            items_list=items_in_cart,
            total_amount=invoice.total_amount,
            discount=discount,
            payment_method=payment_method,
            shift_id=employee.active_shift_id
        )
        
        if db_success:
            security_details = f"عملية بيع وتفصيل رقم {invoice_id} بقيمة {invoice.total_amount} ريال بواسطة الموظف {employee.username}"
            self.security_core.log_and_secure("SALES_INVOICE_CREATED", employee.username, security_details)
            return True, invoice
        else:
            self.security_core.log_and_secure("SALES_INVOICE_FAILED", employee.username, f"فشلت عملية إنشاء الفاتورة {invoice_id} بسبب خطأ بالنظام", "HIGH")
            return False, "حدث خطأ فني أثناء كتابة الفاتورة وتحديث المخازن، تم التراجع عن العملية بأمان."

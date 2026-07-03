# -*- coding: utf-8 -*-
import os

# ==========================================
# نواة التنسيق والاتصال (Coordination & Connection Core)
# تعمل كمنسق عام وموزع ومترجم بين الواجهة الرسومية (UI) وبقية الخوادم والأنوية والخدمات الأمنية والبياناتية
# ==========================================

class ConnectionCore:
    """
    المنسق المركزي والموجه الرئيسي للعمليات والاتصالات داخل نظام لوردستاير.
    يضمن الفصل التام والمثالي للواجهة (Streamlit) عن العمليات الخلفية (Backend) والأمن والبيانات.
    """
    def __init__(self, security_core, data_core, operations_core):
        self.security_core = security_core
        self.data_core = data_core
        self.operations_core = operations_core
        
        # تفعيل الترابط الديناميكي بنجاح وتسجيل بدء النظام الآمن
        self.log_connection_event("SYSTEM_BOOT", "system", "تم ربط وتنسيق كافة خوادم وأنوية النظام وبدء التشغيل الفعلي بنجاح.")

    def log_connection_event(self, action_type, user, details, level="INFO"):
        """
        توجيه الحدث إلى نواة الأمن لتسجيله في البلوكتشاين وفحصه سيبرانياً.
        """
        if self.security_core:
            self.security_core.log_and_secure(action_type, user, details, level)

    def route_authenticate(self, username, password) -> tuple:
        """
        توجيه طلب تسجيل الدخول من الواجهة إلى خوادم الباكيند والأمن المالي والتأكد من النتائج.
        """
        self.log_connection_event("UI_ROUTE_ATTEMPT", username, "طلب تسجيل دخول قادم من واجهة المستخدم الرسومية")
        employee_obj = self.operations_core.authenticate_user(username, password)
        if employee_obj:
            return True, employee_obj
        return False, "اسم المستخدم أو كلمة المرور غير صحيحة، أو الحساب معطل حالياً."

    def route_add_item_to_inventory(self, user_role, username, item_data: dict) -> tuple:
        """
        تنسيق عملية إضافة صنف جديد للمخزون مع مراجعة الصلاحيات الأمنية والتوثيق المالي.
        """
        # 1. التحقق من الصلاحيات عبر خادم الأمن السيبراني
        is_authorized = self.security_core.cybersecurity.audit_system_behavior(user_role, "manage_inventory")
        if not is_authorized:
            self.log_connection_event("SECURITY_BREACH_ATTEMPT", username, f"محاولة غير مصرحة لإضافة قطعة غيار بقيمة {item_data.get('retail_price')}", "HIGH")
            return False, "عذراً! ليس لديك الصلاحية الأمنية اللازمة لإضافة أو تعديل المخزون."

        # 2. استدعاء قاعدة البيانات لإضافة القطعة
        success = self.data_core.add_inventory_item(
            part_id=item_data["part_id"],
            part_number=item_data["part_number"],
            name_ar=item_data["name_ar"],
            name_en=item_data["name_en"],
            category=item_data["category"],
            quantity=item_data["quantity"],
            wholesale_price=item_data["wholesale_price"],
            retail_price=item_data["retail_price"],
            compatibility=item_data.get("compatibility", ""),
            is_special=item_data.get("is_special", 0),
            special_properties=item_data.get("special_properties", "{}")
        )

        if success:
            self.log_connection_event("INVENTORY_ITEM_ADDED", username, f"تمت إضافة قطعة جديدة للمخزن بنجاح: {item_data['name_ar']} (كود: {item_data['part_id']})")
            return True, "تم حفظ القطعة الجديدة بنجاح وتأمين بيانات سعر الجملة الخاص بها في قواعد البيانات."
        return False, "فشلت العملية. قد يكون كود القطعة أو رقم المصنع مسجل مسبقاً في النظام."

    def route_update_item_in_inventory(self, user_role, username, item_data: dict) -> tuple:
        """
        تنسيق عملية تعديل صنف موجود بالفعل مع التحقق من الصلاحيات وتسجيل الحدث.
        """
        is_authorized = self.security_core.cybersecurity.audit_system_behavior(user_role, "manage_inventory")
        if not is_authorized:
            self.log_connection_event("SECURITY_BREACH_ATTEMPT", username, f"محاولة غير مصرحة لتعديل القطعة {item_data.get('part_id')}", "HIGH")
            return False, "عذراً! ليس لديك الصلاحية الأمنية لتعديل المخزون."

        success = self.data_core.update_inventory_item(
            part_id=item_data["part_id"],
            name_ar=item_data["name_ar"],
            name_en=item_data["name_en"],
            category=item_data["category"],
            quantity=item_data["quantity"],
            wholesale_price=item_data["wholesale_price"],
            retail_price=item_data["retail_price"],
            compatibility=item_data.get("compatibility", ""),
            is_special=item_data.get("is_special", 0),
            special_properties=item_data.get("special_properties", "{}")
        )
        if success:
            self.log_connection_event("INVENTORY_ITEM_UPDATED", username, f"تم تعديل بيانات القطعة بنجاح: {item_data['name_ar']} (كود: {item_data['part_id']})")
            return True, "تم تعديل بيانات القطعة بالمخزن بنجاح وتشفير أسعار الشراء."
        return False, "حدث خطأ غير متوقع أثناء عملية التعديل."

    def route_delete_item_from_inventory(self, user_role, username, part_id: str) -> tuple:
        """
        تنسيق عملية حذف قطعة غيار بشكل نهائي وتوثيق ذلك بصرامة شديدة.
        """
        is_authorized = self.security_core.cybersecurity.audit_system_behavior(user_role, "manage_inventory")
        if not is_authorized:
            self.log_connection_event("SECURITY_BREACH_ATTEMPT", username, f"محاولة غير مصرحة لحذف قطعة الغيار {part_id}", "HIGH")
            return False, "عذراً! الحذف من المخازن مخصص للمدراء والمسؤولين فقط."

        success = self.data_core.delete_inventory_item(part_id)
        if success:
            self.log_connection_event("INVENTORY_ITEM_DELETED", username, f"تم حذف القطعة {part_id} نهائياً من قاعدة البيانات وجداول النظام", "WARNING")
            return True, "تم حذف الصنف من المخزن بنجاح وتحديث الكتل الأمنية."
        return False, "فشلت عملية الحذف."

    def route_checkout(self, employee_obj, customer_name, customer_phone, items_in_cart, discount, payment_method) -> tuple:
        """
        بوابة تنسيق دفع وحساب الفاتورة واستدعاء عمليات الباكيند لتغيير كميات المخزون وتسجيل القيود المالية.
        """
        self.log_connection_event("CHECKOUT_ROUTED", employee_obj.username, f"بدء إجراءات الدفع لعملية بيع جديدة بقيمة خصم {discount}")
        return self.operations_core.process_checkout(employee_obj, customer_name, customer_phone, items_in_cart, discount, payment_method)

    def route_open_shift(self, employee_username, initial_cash) -> tuple:
        """
        فتح وردية جديدة وتوثيق مبلغ البدء بالخزينة.
        """
        shift_id = self.data_core.open_shift(employee_username, initial_cash)
        self.log_connection_event("SHIFT_OPENED", employee_username, f"تم فتح وردية جديدة بنجاح رقم {shift_id} بمبلغ بدء {initial_cash} ريال")
        return True, shift_id

    def route_close_shift(self, employee_username, shift_id, closing_cash, actual_closing_cash, notes="") -> tuple:
        """
        إغلاق الوردية الحالية وحساب العجز أو الفارق الكاش وتأكيد إغلاق الخزانة.
        """
        self.data_core.close_shift(shift_id, closing_cash, actual_closing_cash, notes)
        discrepancy = actual_closing_cash - closing_cash
        details = f"تم إغلاق الوردية {shift_id}. المبلغ المتوقع: {closing_cash} ريال، المبلغ الفعلي: {actual_closing_cash} ريال، الفارق والعجز: {discrepancy} ريال"
        level = "CRITICAL" if abs(discrepancy) > 50 else "INFO"
        self.log_connection_event("SHIFT_CLOSED", employee_username, details, level)
        return True, discrepancy

    def route_add_employee(self, user_role, current_username, emp_data: dict) -> tuple:
        """
        إضافة موظف جديد بعد التحقق من الصلاحيات الإدارية للأدمن.
        """
        is_authorized = self.security_core.cybersecurity.audit_system_behavior(user_role, "manage_employees")
        if not is_authorized:
            self.log_connection_event("SECURITY_BREACH_ATTEMPT", current_username, "محاولة غير مصرحة لإضافة موظف جديد للمحل", "HIGH")
            return False, "عذراً! صلاحيات إدارة الموظفين مخصصة للمدير العام فقط."

        success = self.data_core.add_employee(
            username=emp_data["username"],
            password=emp_data["password"],
            full_name=emp_data["full_name"],
            role=emp_data["role"],
            branch=emp_data["branch"]
        )
        if success:
            self.log_connection_event("EMPLOYEE_ADDED", current_username, f"تم إنشاء مستخدم وموظف جديد: {emp_data['username']} بدوران ووظيفة {emp_data['role']}")
            return True, "تم إنشاء حساب الموظف الجديد وتأمين كلمة مروره وتفعيل حسابه بنجاح."
        return False, "اسم المستخدم مسجل مسبقاً بالبرنامج! يرجى اختيار اسم مستخدم فريد."

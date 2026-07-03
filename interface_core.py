# -*- coding: utf-8 -*-

# ==========================================
# نواة الواجهة (Interface Core)
# تتولى تعريب الكلمات والمصطلحات ودعم التغيير الفوري بين اللغتين العربية والانجليزية (Localization Engine)
# ==========================================

LOCALIZATION = {
    "ar": {
        "app_title": "لوردستاير - إدارة كماليات وقطع غيار السيارات",
        "welcome": "أهلاً بك يا لورد،",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login": "تسجيل الدخول الآمن",
        "logout": "تسجيل الخروج",
        "dashboard": "لوحة التحكم الذكية",
        "sales_billing": "المبيعات وإصدار الفواتير",
        "inventory_edit": "المخازن والقطع",
        "tinting_calculator": "حسابات الفيميه والمواد الخاصة",
        "employees_management": "الموظفين والورديات",
        "security_logs": "نظام الأمان والكتل",
        "import_export": "نقل واستيراد البيانات العتيقة",
        "active_user": "المستخدم النشط",
        "role": "الوظيفة والصلاحية",
        "branch": "الفرع الحالي",
        "no_active_shift": "يرجى العلم بأنه لا توجد وردية نشطة مفتوحة لك حالياً! توجه لصفحة الموظفين لفتح ورديتك والبدء بالبيع.",
        "shift_status": "حالة الوردية",
        "open_shift_btn": "فتح وردية جديدة",
        "close_shift_btn": "إغلاق الوردية الحالية",
        "initial_cash": "كاش البدء في الدرج (ريال)",
        "closing_cash_real": "الكاش الفعلي الموجود بالدرج عند الإغلاق (ريال)",
        "active_shift_id": "رقم الوردية النشطة",
        "shift_opened_at": "تاريخ بدء الوردية",
        
        # لوحة التحكم
        "total_sales": "إجمالي المبيعات",
        "total_items": "عدد الأصناف بالمستودع",
        "active_employees": "الموظفون النشطون",
        "security_score_title": "تقييم أمان النظام السيبراني",
        "low_stock_warning": "أصناف مخزون منخفضة وحرجة",
        "sales_over_time": "مؤشر حركة المبيعات",
        
        # المبيعات والفواتير
        "customer_name": "اسم العميل",
        "customer_phone": "رقم جوال العميل",
        "payment_method": "طريقة الدفع",
        "cash": "نقداً / كاش",
        "card": "شبكة / مدى",
        "bank_transfer": "تحويل بنكي",
        "discount": "خصم إضافي (ريال)",
        "add_to_cart": "إضافة للسلة",
        "cart_items": "سلة الشراء الحالية",
        "empty_cart": "السلة فارغة حالياً. أضف قطع غيار أو تظليل فيميه بالأعلى.",
        "checkout_btn": "إصدار الفاتورة وتحديث المخازن",
        "receipt_preview": "معاينة الوصل الحراري للطباعة",
        
        # المخازن والقطع
        "part_id": "كود القطعة (فريد)",
        "part_number": "رقم المصنع / الباركود",
        "name_ar": "الاسم باللغة العربية",
        "name_en": "الاسم باللغة الانجليزية",
        "category": "القسم / الفئة",
        "quantity": "الكمية المتوفرة",
        "wholesale_price": "سعر الجملة (مشفر)",
        "retail_price": "سعر البيع للتجزئة (ريال)",
        "compatibility": "السيارات المتوافقة والسنة",
        "is_special": "هل هذا الصنف فيميه/تظليل/مواد مقاسة بالمتر؟",
        "save_item": "حفظ القطعة بالمخزن",
        "edit_item": "تعديل البيانات",
        "delete_item": "حذف نهائي",
        "roll_length": "طول الرول الإجمالي (متر)",
        "roll_width": "عرض الرول (سم)",
        "waste_percentage": "نسبة هدر وقص المادة القياسية (%)",
        
        # حاسبة الفيميه
        "tinting_title": "حاسبة ومهندس الفيميه والتظليل الذكي",
        "car_segment": "فئة وحجم السيارة",
        "requested_meters": "الأمتار الأساسية المطلوبة للتركيب (متر)",
        "waste_override": "تخصيص نسبة هدر مختلفة (%)",
        "labor_override": "تخصيص قيمة مصنعية وتركيب مختلفة (ريال)",
        "total_meters_consumed": "إجمالي المادة المستهلكة (شاملة الهدر)",
        "meters_wasted_only": "المادة المهدرة والقصاصات غير الصالحة",
        "material_retail_price": "سعر المادة المستهلكة للزبون",
        "labor_fee": "قيمة المصنعية والتركيب (شغل يد)",
        "total_customer_price": "السعر الإجمالي النهائي للفيميه والتركيب",
        "stock_remaining_after_m": "المخزون المتبقي بالرول بعد هذه العملية (متر)",
        "add_tinting_to_cart": "إضافة عملية الفيميه المخصصة إلى سلة المبيعات",
        
        # إدارة الموظفين والورديات
        "employee_username": "اسم مستخدم الموظف",
        "employee_fullname": "الاسم الكامل للموظف",
        "employee_role": "الوظيفة / الصلاحية بالأمان",
        "employee_branch": "فرع العمل للموظف",
        "employee_password": "كلمة المرور للحساب",
        "create_employee_btn": "إنشاء حساب الموظف",
        
        # الكتل والأمن
        "blockchain_title": "سجل البلوكتشاين اللامركزي لتوثيق الأحداث",
        "blockchain_info": "تقوم نواة الأمن بتسجيل كل نقرة، وكل عملية بيع، وتعديل مخزون، في كتل (Blocks) مشفرة وموثقة بهاشات SHA-256 متتالية غير قابلة للتزوير أو الحذف بأثر رجعي.",
        "blockchain_validity": "حالة صحة وسلامة كتل البلوكتشاين الحالية",
        "valid": "سلسلة كتل سليمة وآمنة 100% بنظام التوثيق اللامركزي",
        "invalid": "تنبيه أمني: تم رصد تلاعب غير مصرح في سجلات النظام!",
        "block_index": "رقم البلوك",
        "block_hash": "تشفير الهاش للبلوك",
        "block_prev_hash": "هاش البلوك السابق",
        "block_data": "بيانات العملية الموثقة أمنياً",
        
        # الاستيراد والتصدير
        "import_legacy_title": "استيراد وتصدير ونقل البيانات من الأنظمة القديمة والعتيقة",
        "import_csv_label": "اختر ملف CSV لقاعدة بيانات قديمة لاستيرادها فوراً",
        "import_btn": "بدء استيراد قاعدة البيانات القديمة وتطبيع الأعمدة",
        "export_csv_btn": "تصدير المخزون الحالي بصيغة CSV نقي",
        "export_xlsx_btn": "تصدير المخزون كملف Excel احترافي وملون"
    },
    "en": {
        "app_title": "Lordstair - Auto Parts & Accessories Management",
        "welcome": "Welcome, My Lord,",
        "username": "Username",
        "password": "Password",
        "login": "Secure Login",
        "logout": "Logout",
        "dashboard": "Smart Dashboard",
        "sales_billing": "Sales & Billing",
        "inventory_edit": "Inventory & Parts",
        "tinting_calculator": "Tinting & Special Materials",
        "employees_management": "Employees & Shifts",
        "security_logs": "Blockchain Audit & Security",
        "import_export": "Legacy Data Migration",
        "active_user": "Active User",
        "role": "Role & Privilege",
        "branch": "Current Branch",
        "no_active_shift": "Please note that there is no active shift opened for you! Head to the Employees page to open your shift.",
        "shift_status": "Shift Status",
        "open_shift_btn": "Open New Shift",
        "close_shift_btn": "Close Current Shift",
        "initial_cash": "Starting Cash in Drawer (SAR)",
        "closing_cash_real": "Actual Closing Cash in Drawer (SAR)",
        "active_shift_id": "Active Shift ID",
        "shift_opened_at": "Shift Opened At",
        
        # Dashboard
        "total_sales": "Total Sales Revenue",
        "total_items": "Total Unique Items",
        "active_employees": "Active Staff On Shift",
        "security_score_title": "Cybersecurity Protection Index",
        "low_stock_warning": "Critical Low Stock Alerts",
        "sales_over_time": "Sales Growth Graph",
        
        # Sales & Billing
        "customer_name": "Customer Name",
        "customer_phone": "Customer Mobile",
        "payment_method": "Payment Method",
        "cash": "Cash",
        "card": "POS / Card",
        "bank_transfer": "Bank Transfer",
        "discount": "Extra Discount (SAR)",
        "add_to_cart": "Add to Invoice Cart",
        "cart_items": "Current Cart Content",
        "empty_cart": "Your cart is empty. Add spare parts or custom tinting above.",
        "checkout_btn": "Generate Invoice & Process Stocks",
        "receipt_preview": "Thermal Receipt Printer Preview",
        
        # Inventory
        "part_id": "Part ID (Unique)",
        "part_number": "Manufacturer SKU/Barcode",
        "name_ar": "Arabic Title Name",
        "name_en": "English Title Name",
        "category": "Category",
        "quantity": "Available Stock Quantity",
        "wholesale_price": "Wholesale Price (Encrypted)",
        "retail_price": "Retail Selling Price (SAR)",
        "compatibility": "Compatible Cars & Years",
        "is_special": "Is this a Tint/Window Film sold by meter?",
        "save_item": "Save Item to Database",
        "edit_item": "Update Information",
        "delete_item": "Delete Item Permanently",
        "roll_length": "Total Roll Length (m)",
        "roll_width": "Roll Width (cm)",
        "waste_percentage": "Standard Waste Percentage (%)",
        
        # Tinting Calculator
        "tinting_title": "Smart Window Tinting Engineering Calc",
        "car_segment": "Car Size / Segment",
        "requested_meters": "Basic Window Length (meters)",
        "waste_override": "Override Waste Percentage (%)",
        "labor_override": "Override Labor & Customization (SAR)",
        "total_meters_consumed": "Total Fabric Consumed (Inc. Waste)",
        "meters_wasted_only": "Scrap & Wasted Material length",
        "material_retail_price": "Retail Material price for Client",
        "labor_fee": "Labor fee (Installation Cost)",
        "total_customer_price": "Final Customer Quotation Price",
        "stock_remaining_after_m": "Roll Stock remaining after this (m)",
        "add_tinting_to_cart": "Add Custom Tinting Service to Cart",
        
        # Employees Management
        "employee_username": "Account Username",
        "employee_fullname": "Full Legal Name",
        "employee_role": "Security Role",
        "employee_branch": "Branch Office Location",
        "employee_password": "Account Password",
        "create_employee_btn": "Register & Authorize Account",
        
        # Security & Blockchain
        "blockchain_title": "Immutable Blockchain Action Ledger",
        "blockchain_info": "The Security Core logs every mouse click, sales order, and stock modification into consecutive cryptographically-locked blocks secured by chaining SHA-256 hashes.",
        "blockchain_validity": "Blockchain Audit Verification Status",
        "valid": "Decentralized Ledger Integrity Verified 100% Safe",
        "invalid": "SECURITY BREACH ALERT: Unauthorized modification detected in logs!",
        "block_index": "Block Index",
        "block_hash": "Current Block SHA-256 Hash",
        "block_prev_hash": "Previous Block Hash Link",
        "block_data": "Secure Block Audit Payload",
        
        # Import & Export
        "import_legacy_title": "Legacy Data Migration & Database Transitions",
        "import_csv_label": "Select a legacy database CSV file to import & map columns",
        "import_btn": "Begin Import & Map Columns",
        "export_csv_btn": "Export Inventory to Clean CSV",
        "export_xlsx_btn": "Export Inventory to Styled Excel"
    }
}


class InterfaceCore:
    """
    نواة الواجهة لتسهيل عمليات التنسيق وإدارة النصوص وتوفير التوطين الفوري.
    """
    def __init__(self):
        # تفعيل المحرك بشكل مرن لخدمة لغتين
        pass

    @staticmethod
    def t(key, lang="ar") -> str:
        """
        استرجاع النص المترجم للغة الحالية. يرجع الكلمة الافتراضية إذا لم تتوفر الترجمة.
        """
        return LOCALIZATION.get(lang, LOCALIZATION["ar"]).get(key, f"[{key}]")

    @staticmethod
    def get_custom_css() -> str:
        """
        حقن تصاميم CSS مخصصة واحترافية للغاية متوافقة مع ذوق اللوردستاير 
        لجعل واجهة ستريمليت تبدو كتطبيق مكتبي احترافي متناسق وسهل القراءة ومريح للعين.
        """
        return """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');
        
        * {
            font-family: 'Cairo', sans-serif !important;
        }
        
        /* تحسين وتجميل مظهر الكروت والمعلومات الإحصائية */
        .stMetric {
            background-color: #1E293B;
            padding: 15px;
            border-radius: 12px;
            border: 1px solid #334155;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        
        /* جعل الأزرار تبدو أكثر تفاعلاً وتجاوباً */
        .stButton>button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }
        
        /* تصميم مخصص للوصل والفواتير الحرارية */
        .receipt-container {
            background-color: #F8FAFC;
            color: #0F172A;
            padding: 20px;
            border-radius: 8px;
            border: 2px dashed #CBD5E1;
            font-family: 'Courier New', Courier, monospace !important;
            font-weight: bold;
            white-space: pre-wrap;
            box-shadow: inset 0 0 10px rgba(0,0,0,0.05);
        }
        </style>
        """

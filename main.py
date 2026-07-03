# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import json
import os
import sys
import time
from datetime import datetime

# حل فوري لمشاكل استيراد الملفات وضمان كفاءتها بغض النظر عن طريقة استدعاء الخادم
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# استيراد الأنوية الأساسية للنظام من الملفات البرمجية المجاورة
from security_core import SecurityCore
from data_core import DataCore
from operations_core import OperationsCore
from connection_core import ConnectionCore
from interface_core import InterfaceCore, LOCALIZATION

# ==========================================
# تهيئة وإعداد النظام والربط بين الأنوية الخمسة
# ==========================================

st.set_page_config(
    page_title="لوردستاير - إدارة كماليات وقطع غيار السيارات",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# التأكد من تهيئة النظام مرة واحدة فقط وحفظه في حالة الجلسة (Session State)
if "coordinator" not in st.session_state:
    # 1. تهيئة نواة الأمن (تشمل خادمي البلوكتشاين والأمن السيبراني)
    security_core = SecurityCore()
    
    # 2. تهيئة نواة البيانات وربطها بالأمن لتشفير البيانات الحساسة
    data_core = DataCore(db_path="lordstair_database.db", security_core=security_core)
    
    # 3. تهيئة نواة العمليات (الباكيند)
    operations_core = OperationsCore(data_core=data_core, security_core=security_core)
    
    # 4. تهيئة نواة التنسيق والاتصال (المنسق العام للمشروع)
    coordinator = ConnectionCore(
        security_core=security_core,
        data_core=data_core,
        operations_core=operations_core
    )
    
    st.session_state.coordinator = coordinator
    st.session_state.security_core = security_core
    st.session_state.data_core = data_core
    st.session_state.operations_core = operations_core
    
    # بذور البيانات الحقيقية والعملية دون بيانات وهمية
    existing_items = data_core.list_inventory()
    if len(existing_items) == 0:
        # صنف 1: قطع غيار عادية
        data_core.add_inventory_item(
            part_id="SP-1001",
            part_number="90915-YZD2",
            name_ar="فلتر زيت تويوتا كورولا أصلي",
            name_en="Toyota Corolla Genuine Oil Filter",
            category="قطع غيار محركات",
            quantity=45,
            wholesale_price=22.0,
            retail_price=35.0,
            compatibility="Toyota Corolla 2015-2024, Toyota Yaris 2016-2023"
        )
        # صنف 2: فحمات فرامل سيراميك خلفية
        data_core.add_inventory_item(
            part_id="SP-1002",
            part_number="D1354-8463",
            name_ar="فحمات فرامل خلفية سيراميك لاندكروزر",
            name_en="Toyota Land Cruiser Ceramic Rear Brake Pads",
            category="نظام الفرامل",
            quantity=12,
            wholesale_price=180.0,
            retail_price=270.0,
            compatibility="Toyota Land Cruiser 2012-2021, Lexus LX570 2013-2021"
        )
        # خامة مخصصة 1: رول تظليل نانو سيراميك عازل
        tint_props = {
            "unit_name": "متر طولي",
            "default_waste_percentage": 15.0
        }
        data_core.add_inventory_item(
            part_id="SP-2001",
            part_number="NANO-CS-XP70",
            name_ar="رول فيميه عازل حراري نانو سيراميك 70%",
            name_en="Nano Ceramic Heat Insulating Tint 70% Roll",
            category="خامات وتظليل",
            quantity=90.0,
            wholesale_price=30.0,
            retail_price=65.0,
            compatibility="جميع السيارات والشاحنات",
            is_special=1,
            special_properties=json.dumps(tint_props)
        )
        # خامة مخصصة 2: رول تنجيد جلد ألماني فاخر
        leather_props = {
            "unit_name": "متر مربع",
            "default_waste_percentage": 25.0
        }
        data_core.add_inventory_item(
            part_id="SP-2002",
            part_number="GERMAN-LTH-BR",
            name_ar="رول جلد ألماني فاخر للتنجيد والفرش - بني",
            name_en="Premium German Brown Leather Roll",
            category="خامات وتنجيد وديكور",
            quantity=50.0,
            wholesale_price=80.0,
            retail_price=160.0,
            compatibility="تعديل وتنجيد مقاعد مرسيدس، لكسز، جيب",
            is_special=1,
            special_properties=json.dumps(leather_props)
        )

# تعيين قيم المتغيرات للجلسة المباشرة
coordinator = st.session_state.coordinator
security_core = st.session_state.security_core
data_core = st.session_state.data_core
operations_core = st.session_state.operations_core

# إدارة اللغة في الجلسة
if "lang" not in st.session_state:
    st.session_state.lang = "ar"

# إدارة سلة المشتريات المؤقتة للزبائن
if "cart" not in st.session_state:
    st.session_state.cart = []

# إدارة الموظف المسجل دخوله
if "logged_user" not in st.session_state:
    st.session_state.logged_user = None

# تصحيح حقن تصاميم CSS واستخدام unsafe_allow_html=True كمعيار حديث وإلغاء الوسيط الخاطئ unsafe_allow_value
st.markdown(InterfaceCore.get_custom_css(), unsafe_allow_html=True)

def translate(key):
    return InterfaceCore.t(key, st.session_state.lang)


# ==========================================
# الشريط الجانبي (Sidebar)
# ==========================================

with st.sidebar:
    # إلغاء استخدام use_column_width=True المستقبلي المستبدل بـ use_container_width=True لتجنب التحذيرات بالواجهة
    st.image("https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=300&q=80", caption="Lordstair Auto Parts", use_container_width=True)
    
    lang_choice = st.selectbox(
        "🌐 Language / لغة الواجهة",
        options=["العربية", "English"],
        index=0 if st.session_state.lang == "ar" else 1,
        key="lang_selector"
    )
    new_lang = "ar" if lang_choice == "العربية" else "en"
    if new_lang != st.session_state.lang:
        st.session_state.lang = new_lang
        st.rerun()
        
    st.markdown("---")
    
    if st.session_state.logged_user:
        user = st.session_state.logged_user
        st.success(f"🔓 {translate('welcome')} **{user.full_name}**")
        st.info(f"💼 **{translate('role')}:** {user.role}\n\n📍 **{translate('branch')}:** {user.branch}")
        
        if user.active_shift_id:
            st.success(f"⏱️ {translate('active_shift_id')}: \n`{user.active_shift_id}`")
        else:
            st.warning(f"⚠️ {translate('no_active_shift')}")
            
        if st.button(translate("logout"), key="logout_btn", type="secondary", use_container_width=True):
            st.session_state.logged_user = None
            st.session_state.cart = []
            st.rerun()
    else:
        st.markdown(f"### 🔒 {translate('login')}")


# ==========================================
# صفحة تسجيل الدخول الآمن
# ==========================================

if not st.session_state.logged_user:
    st.title("🚗 نظام لوردستاير لإدارة ومبيعات قطع غيار السيارات وخامات التشغيل")
    st.markdown(
        """
        ### واجهة التشغيل والمحاسبة والتحكم بالخامات المفتوحة
        برنامج متكامل لحساب وتفصيل كافة أنواع الخامات والمواد (تظليل، جلود، أسلاك، كماليات) بالتزامن مع الرصد السيبراني لموارد ونظام تشغيل جهاز المحاسبة.
        """
    )
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=600&q=80", use_container_width=True)
    
    with col2:
        st.markdown(f"#### 🔐 {translate('login')}")
        username_input = st.text_input(translate("username"), value="admin")
        password_input = st.text_input(translate("password"), type="password", value="admin123")
        
        if st.button(translate("login"), type="primary", use_container_width=True):
            success, result = coordinator.route_authenticate(username_input, password_input)
            if success:
                st.session_state.logged_user = result
                st.success("تم تسجيل الدخول بنجاح!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error(result)
                
    st.info("💡 الحسابات الافتراضية:\n\n1. المدير: `admin` | كلمة المرور `admin123`\n2. الكاشير: `cashier` | كلمة المرور `cashier123`")
    st.stop()


# ==========================================
# نظام التوجيه
# ==========================================

user = st.session_state.logged_user

menu_options = []
if user.has_access("dashboard"):
    menu_options.append(translate("dashboard"))
if user.has_access("sales_billing"):
    menu_options.append(translate("sales_billing"))
if user.has_access("inventory_edit"):
    menu_options.append(translate("inventory_edit"))
elif user.has_access("inventory_view"):
    menu_options.append(translate("inventory_edit"))

if user.role in ["Admin", "Manager", "Technician"]:
    menu_options.append("✂️ أداة التفصيل والتشغيل الديناميكي")
if user.has_access("employees_management"):
    menu_options.append(translate("employees_management"))
if user.has_access("security_logs"):
    menu_options.append(translate("security_logs"))
if user.has_access("import_export"):
    menu_options.append(translate("import_export"))

with st.sidebar:
    st.markdown("---")
    current_page = st.radio("📂 تصفح القوائم والأدوات", options=menu_options)


# ==========================================
# 1. لوحة التحكم الذكية
# ==========================================

if current_page == translate("dashboard"):
    st.title(f"📊 {translate('dashboard')}")
    st.markdown(f"#### المراقبة الإحصائية للعمليات والنشاط في {user.branch}")
    
    all_items = data_core.list_inventory()
    all_sales = data_core.list_sales()
    all_employees = data_core.list_employees()
    security_info = security_core.cybersecurity.get_security_score()
    
    total_revenue = sum(sale["total_amount"] for sale in all_sales)
    total_unique_items = len(all_items)
    active_employees_count = len([e for e in all_employees if e["is_active"] == 1])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label=translate("total_sales"), value=f"{total_revenue:,.2f} ريال")
    with col2:
        st.metric(label=translate("total_items"), value=total_unique_items)
    with col3:
        st.metric(label=translate("active_employees"), value=active_employees_count)
    with col4:
        score = security_info["score"]
        st.metric(label=translate("security_score_title"), value=f"{score}/100", delta=security_info["status"])

    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader(f"📈 {translate('sales_over_time')}")
        if len(all_sales) > 0:
            sales_df = pd.DataFrame(all_sales)
            sales_df['date'] = sales_df['timestamp'].apply(lambda x: x.split(" ")[0])
            daily_sales = sales_df.groupby('date')['total_amount'].sum().reset_index()
            st.line_chart(data=daily_sales, x="date", y="total_amount", use_container_width=True)
        else:
            st.info("لا توجد فواتير مبيعات مسجلة اليوم حتى الآن لحساب مخطط النمو.")
            
    with col_right:
        st.subheader(f"⚠️ {translate('low_stock_warning')}")
        low_stock_items = [item for item in all_items if item["quantity"] <= 5.0]
        if len(low_stock_items) > 0:
            for item in low_stock_items:
                st.warning(f"**{item['name_ar']}**\n\nالكمية الحالية: {item['quantity']} وحدة (الحد الحرج: 5)")
        else:
            st.success("🎉 كافة كميات قطع الغيار والمواد بالمستودع آمنة وممتازة!")


# ==========================================
# 2. صفحة المبيعات وإصدار الفواتير
# ==========================================

elif current_page == translate("sales_billing"):
    st.title(f"🛒 {translate('sales_billing')}")
    st.markdown("##### تسجيل المبيعات السريعة، وتفصيل كافة أنواع الخامات، وطباعة الفواتير الحرارية الفورية")
    
    if not user.active_shift_id:
        st.error(translate("no_active_shift"))
        st.info("الرجاء الذهاب لتبويب [الموظفين والورديات] لفتح ورديتك لتتمكن من تشغيل الكاشير والمبيعات.")
    else:
        all_items = operations_core.get_inventory_objects()
        
        tab_regular, tab_special = st.tabs(["⚙️ إضافة قطع غيار وكماليات عادية", "✂️ تفصيل وتشغيل الخامات والمواد المفتوحة (ديناميكي)"])
        
        with tab_regular:
            regular_items = [item for item in all_items if item.is_special == 0 and item.quantity > 0]
            if len(regular_items) == 0:
                st.info("لا توجد قطع غيار عادية بالمستودع حالياً لتسجيل بيعها.")
            else:
                item_options = {f"{item.name_ar} (كود: {item.part_id}) - المتبقي: {item.quantity}": item for item in regular_items}
                selected_item_label = st.selectbox("اختر الصنف المراد بيعه", options=list(item_options.keys()))
                selected_item_obj = item_options[selected_item_label]
                
                col_q, col_btn = st.columns([1, 1])
                with col_q:
                    qty_to_sell = st.number_input("الكمية المطلوبة لشراء الزبون", min_value=1, max_value=int(selected_item_obj.quantity), value=1, key="regular_qty_input")
                with col_btn:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button(translate("add_to_cart"), use_container_width=True, key="add_regular_btn"):
                        st.session_state.cart.append({
                            "part_id": selected_item_obj.part_id,
                            "part_number": selected_item_obj.part_number,
                            "name_ar": selected_item_obj.name_ar,
                            "name_en": selected_item_obj.name_en,
                            "qty": qty_to_sell,
                            "unit_price": selected_item_obj.retail_price,
                            "labor_fee": 0.0,
                            "additional_material_fee": 0.0,
                            "is_special": 0
                        })
                        st.success(f"تمت إضافة {qty_to_sell} من [{selected_item_obj.name_ar}] إلى سلة الشراء بنجاح!")
                        
        with tab_special:
            special_items = [item for item in all_items if item.is_special == 1]
            if len(special_items) == 0:
                st.info("لا توجد مواد أو رولات خامات مسجلة بالمخازن حالياً للتفصيل الديناميكي.")
            else:
                special_options = {f"[{item.category}] {item.name_ar} - المخزون: {item.quantity} ({item.special_properties.get('unit_name', 'متر')})": item for item in special_items}
                selected_special_label = st.selectbox("اختر نوع الخامة المراد تفصيلها أو تركيبها", options=list(special_options.keys()))
                selected_special_obj = special_options[selected_special_label]
                
                st.markdown("##### ⚙️ تخصيص مواصفات وعقد عملية التفصيل والتشغيل الحالية:")
                
                col_spec1, col_spec2 = st.columns(2)
                with col_spec1:
                    job_desc = st.text_input("وصف وتسمية العملية الفنية بالكامل", value=f"تفصيل وتركيب {selected_special_obj.name_ar} لسيارة العميل")
                    req_qty = st.number_input(f"الكمية الأساسية الصافية المطلوبة للتفصيل والعمل ({selected_special_obj.special_properties.get('unit_name', 'متر')})", min_value=0.1, max_value=float(selected_special_obj.quantity), value=3.0)
                    waste_p = st.number_input("نسبة الهدر والقص المتوقعة لهذه العملية مخصصة (%)", min_value=0.0, max_value=100.0, value=float(selected_special_obj.special_properties.get("default_waste_percentage", 10.0)))
                
                with col_spec2:
                    labor_fee = st.number_input("قيمة مصنعية الفني وشغل اليد (ريال)", min_value=0.0, value=150.0, step=10.0)
                    additional_material_fee = st.number_input("تكلفة مواد وعناصر مساعدة أخرى مستهلكة (ريال)", min_value=0.0, value=0.0, step=5.0)
                    st.info(f"💡 سعر المتر/الوحدة القياسي للبيع بالتجزئة: `{selected_special_obj.retail_price} ريال`")
                
                calc_results = selected_special_obj.calculate_custom_fabrication(
                    job_title=job_desc,
                    required_qty=req_qty,
                    waste_percentage=waste_p,
                    labor_fee=labor_fee,
                    additional_material_fee=additional_material_fee
                )
                
                st.markdown("#### 📐 تفصيل المقاييس المحسوبة ديناميكياً للعملية:")
                col_res1, col_res2, col_res3 = st.columns(3)
                with col_res1:
                    st.info(f"📏 **الخامة المستهلكة كلياً:** {calc_results['total_qty_consumed']} {calc_results['unit_name']} (شاملة الهدر)")
                    st.error(f"✂️ **الخامة المهدرة والقصاصات:** {calc_results['qty_wasted_only']} {calc_results['unit_name']}")
                with col_res2:
                    st.metric(label="سعر الخامة المستهلكة للعميل", value=f"{calc_results['material_retail_price']} ريال")
                    st.metric(label="شغل يد تركيب وتصنيع", value=f"{calc_results['labor_fee']} ريال")
                with col_res3:
                    st.metric(label="قيمة العرض المالي الإجمالي للعميل", value=f"{calc_results['total_customer_price']} ريال سعودي", delta="السعر النهائي الشامل")
                    st.success(f"🔄 **مخزون الخامة المتبقي بعد العملية:** {calc_results['stock_remaining_after']} {calc_results['unit_name']}")
                
                if st.button("📥 إضافة هذه العملية الفنية المخصصة إلى سلة المبيعات", use_container_width=True, key="add_custom_fab_btn"):
                    if calc_results['total_qty_consumed'] <= selected_special_obj.quantity:
                        st.session_state.cart.append({
                            "part_id": selected_special_obj.part_id,
                            "part_number": selected_special_obj.part_number,
                            "name_ar": f"{job_desc} ({req_qty} {calc_results['unit_name']} + {waste_p}% هدر)",
                            "name_en": f"Custom Fab: {selected_special_obj.name_en} ({req_qty} {calc_results['unit_name']})",
                            "qty": calc_results["total_qty_consumed"],
                            "unit_price": selected_special_obj.retail_price,
                            "labor_fee": calc_results["labor_fee"],
                            "additional_material_fee": calc_results["additional_material_fee"],
                            "is_special": 1
                        })
                        st.success("تمت إضافة عملية التفصيل والتركيب المخصصة إلى سلة الشراء الحالية بنجاح!")
                    else:
                        st.error("المخزون المتوفر من هذه المادة غير كافٍ لإتمام العملية بحدود الهدر المخصصة!")
                        
        st.markdown("---")
        
        # استعراض السلة وإصدار الفاتورة
        st.subheader(f"📋 {translate('cart_items')}")
        if len(st.session_state.cart) == 0:
            st.info(translate("empty_cart"))
        else:
            cart_df = pd.DataFrame(st.session_state.cart)
            st.dataframe(cart_df[["part_id", "name_ar", "qty", "unit_price", "labor_fee", "additional_material_fee"]], use_container_width=True)
            
            if st.button("🧹 تفريغ السلة بالكامل", key="clear_cart_btn"):
                st.session_state.cart = []
                st.rerun()
                
            st.markdown("---")
            
            st.subheader("💳 إتمام عملية البيع والدفع")
            col_pay1, col_pay2 = st.columns(2)
            with col_pay1:
                c_name = st.text_input(translate("customer_name"), value="عميل نقدي", key="cust_name_input")
                c_phone = st.text_input(translate("customer_phone"), value="0599999999", key="cust_phone_input")
            with col_pay2:
                payment_method = st.selectbox(translate("payment_method"), options=[translate("cash"), translate("card"), translate("bank_transfer")], key="pay_method_select")
                discount_amount = st.number_input(translate("discount"), min_value=0.0, value=0.0, key="discount_input")
                
            total_items_price = sum(item["qty"] * item["unit_price"] + item["labor_fee"] + item.get("additional_material_fee", 0.0) for item in st.session_state.cart)
            final_total = max(0.0, total_items_price - discount_amount)
            st.markdown(f"### 💰 المبلغ الإجمالي المطلوب دفعه: **{final_total:,.2f} ريال سعودي**")
            
            if st.button(translate("checkout_btn"), type="primary", use_container_width=True, key="checkout_invoice_btn"):
                success, invoice_res = coordinator.route_checkout(
                    employee_obj=user,
                    customer_name=c_name,
                    customer_phone=c_phone,
                    items_in_cart=st.session_state.cart,
                    discount=discount_amount,
                    payment_method=payment_method
                )
                
                if success:
                    st.success("🎉 تمت العملية بنجاح! تم حفظ الفاتورة وتأمينها وتحديث المستودع.")
                    st.subheader(f"🖨️ {translate('receipt_preview')}")
                    receipt_text = invoice_res.generate_receipt_text(st.session_state.lang)
                    st.markdown(f'<div class="receipt-container">{receipt_text}</div>', unsafe_allow_html=True)
                    
                    st.session_state.cart = []
                else:
                    st.error(invoice_res)


# ==========================================
# 3. صفحة المخازن والقطع
# ==========================================

elif current_page == translate("inventory_edit"):
    st.title(f"📦 {translate('inventory_edit')}")
    st.markdown("##### تصفح خامات ومواد المتاجر والقطع وتعديل الكميات وإضافة خامات ومواد للتفصيل")
    
    can_edit = user.has_access("inventory_edit")
    all_items = operations_core.get_inventory_objects()
    
    st.subheader("📊 قائمة المواد والقطع الحالية")
    items_data_list = []
    for item in all_items:
        items_data_list.append({
            "الكود (Part ID)": item.part_id,
            "رقم المصنع (SKU)": item.part_number,
            "الاسم (عربي)": item.name_ar,
            "الاسم (إنجليزي)": item.name_en,
            "الفئة": item.category,
            "الكمية": item.quantity,
            "وحدة القياس": item.special_properties.get("unit_name", "وحدة/حبة") if item.is_special == 1 else "وحدة/حبة",
            "سعر الجملة (تكلفة)": f"*** ريال" if not user.has_access("reports_view") else f"{item.wholesale_price} ريال",
            "سعر البيع (تجزئة)": f"{item.retail_price} ريال",
            "نوع المادة": "خامة قابلة للتفصيل والقص" if item.is_special == 1 else "قطعة غيار عادية",
            "التوافقية": item.compatibility
        })
    
    if len(items_data_list) > 0:
        st.dataframe(pd.DataFrame(items_data_list), use_container_width=True)
    else:
        st.info("لا توجد أصناف مسجلة بالمخزن حالياً.")

    if can_edit:
        st.markdown("---")
        st.subheader("🛠️ لوحة العمليات على المخزون (صلاحيات المدراء والمشرفين)")
        
        op_action = st.radio("اختر العملية المطلوبة للقيام بها:", options=["إضافة صنف جديد", "تعديل صنف موجود", "حذف صنف من المخازن"])
        
        if op_action == "إضافة صنف جديد":
            with st.form("add_new_item_form"):
                col1, col2 = st.columns(2)
                with col1:
                    new_id = st.text_input(translate("part_id"), placeholder="مثال: SP-1004")
                    new_number = st.text_input(translate("part_number"), placeholder="مثال: 90915-10001")
                    new_name_ar = st.text_input(translate("name_ar"), placeholder="فلتر هواء أصلي لاندكروزر")
                    new_name_en = st.text_input(translate("name_en"), placeholder="Genuine Air Filter Land Cruiser")
                    new_cat = st.selectbox(translate("category"), options=["قطع غيار محركات", "نظام الفرامل", "كهرباء وإضاءة", "تظليل وفيميه مخصص", "إكسسوارات وكماليات", "خامات وتنجيد وديكور", "أخرى"])
                with col2:
                    new_qty = st.number_input(translate("quantity"), min_value=0.0, value=10.0, step=1.0)
                    new_wholesale = st.number_input("سعر الجملة الحقيقي للشراء (ريال) - سيتم تشفيره فوراً", min_value=0.0, value=15.0)
                    new_retail = st.number_input(translate("retail_price"), min_value=0.0, value=30.0)
                    new_comp = st.text_area(translate("compatibility"), placeholder="تويوتا لاندكروزر 2016-2023, إلخ")
                    
                    is_special_toggle = st.checkbox("هل هذا الصنف مادة/خامة قابلة للتفصيل والقص بمقاييس مختلفة؟")
                    
                special_properties_json = "{}"
                if is_special_toggle:
                    st.markdown("##### ⚙️ الخصائص والمواصفات القياسية للخامة:")
                    col_sp1, col_sp2 = st.columns(2)
                    with col_sp1:
                        unit_n = st.text_input("اسم وحدة القياس (مثال: متر، متر مربع، لتر، قدم)", value="متر")
                    with col_sp2:
                        waste_p = st.number_input(translate("waste_percentage"), min_value=0.0, max_value=100.0, value=10.0)
                    
                    special_properties_json = json.dumps({
                        "unit_name": unit_n,
                        "default_waste_percentage": waste_p
                    })
                
                submitted = st.form_submit_button(translate("save_item"), type="primary")
                if submitted:
                    if not new_id or not new_name_ar:
                        st.error("عذراً، يجب ملء كود القطعة الفريد والاسم باللغة العربية كحد أدنى لحفظ الصنف.")
                    else:
                        item_payload = {
                            "part_id": new_id,
                            "part_number": new_number or new_id,
                            "name_ar": new_name_ar,
                            "name_en": new_name_en,
                            "category": new_cat,
                            "quantity": new_qty,
                            "wholesale_price": new_wholesale,
                            "retail_price": new_retail,
                            "compatibility": new_comp,
                            "is_special": 1 if is_special_toggle else 0,
                            "special_properties": special_properties_json
                        }
                        success, message = coordinator.route_add_item_to_inventory(user.role, user.username, item_payload)
                        if success:
                            st.success(message)
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(message)
                            
        elif op_action == "تعديل صنف موجود":
            if len(all_items) == 0:
                st.info("لا توجد أصناف لتعديلها.")
            else:
                edit_options = {item.part_id: item for item in all_items}
                selected_edit_id = st.selectbox("اختر كود القطعة المراد تعديل بياناتها", options=list(edit_options.keys()))
                item_to_edit = edit_options[selected_edit_id]
                
                with st.form("edit_item_form"):
                    st.info(f"جاري تعديل القطعة ذات الكود الفريد: **{item_to_edit.part_id}**")
                    col1, col2 = st.columns(2)
                    with col1:
                        edit_name_ar = st.text_input(translate("name_ar"), value=item_to_edit.name_ar)
                        edit_name_en = st.text_input(translate("name_en"), value=item_to_edit.name_en)
                        edit_cat = st.selectbox(translate("category"), options=["قطع غيار محركات", "نظام الفرامل", "كهرباء وإضاءة", "تظليل وفيميه مخصص", "إكسسوارات وكماليات", "خامات وتنجيد وديكور", "أخرى"], index=0)
                    with col2:
                        edit_qty = st.number_input(translate("quantity"), min_value=0.0, value=item_to_edit.quantity)
                        edit_wholesale = st.number_input("سعر الجملة الجديد (ريال)", min_value=0.0, value=item_to_edit.wholesale_price)
                        edit_retail = st.number_input(translate("retail_price"), min_value=0.0, value=item_to_edit.retail_price)
                        edit_comp = st.text_area(translate("compatibility"), value=item_to_edit.compatibility or "")
                    
                    submitted = st.form_submit_button(translate("edit_item"), type="primary")
                    if submitted:
                        update_payload = {
                            "part_id": item_to_edit.part_id,
                            "part_number": item_to_edit.part_number,
                            "name_ar": edit_name_ar,
                            "name_en": edit_name_en,
                            "category": edit_cat,
                            "quantity": edit_qty,
                            "wholesale_price": edit_wholesale,
                            "retail_price": edit_retail,
                            "compatibility": edit_comp,
                            "is_special": item_to_edit.is_special,
                            "special_properties": json.dumps(item_to_edit.special_properties)
                        }
                        success, message = coordinator.route_update_item_in_inventory(user.role, user.username, update_payload)
                        if success:
                            st.success(message)
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(message)
                            
        elif op_action == "حذف صنف من المخازن":
            if len(all_items) == 0:
                st.info("لا توجد أصناف لحذفها.")
            else:
                delete_options = {f"{item.name_ar} (كود: {item.part_id})": item.part_id for item in all_items}
                selected_del_label = st.selectbox("اختر الصنف المراد حذفه نهائياً من النظام", options=list(delete_options.keys()))
                del_id = delete_options[selected_del_label]
                
                st.warning("⚠️ تنبيه: الحذف عملية نهائية ولا يمكن التراجع عنها!")
                if st.button("🔥 تأكيد الحذف النهائي للمادة والتوثيق برمجياً", type="primary"):
                    success, message = coordinator.route_delete_item_from_inventory(user.role, user.username, del_id)
                    if success:
                        st.success(message)
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(message)


# ==========================================
# 4. صفحة أداة التفصيل والتشغيل الديناميكي المخصصة
# ==========================================

elif current_page == "✂️ أداة التفصيل والتشغيل الديناميكي":
    st.title("✂️ أداة التفصيل والتشغيل الديناميكي للخامات")
    st.markdown("##### أداة المهندس المحترف لتخصيص عمليات تشغيل وقص كافة المواد (تظليل، جلود، أسلاك، عوازل) دون قوالب مسبقة")
    
    all_items = operations_core.get_inventory_objects()
    special_items = [item for item in all_items if item.is_special == 1]
    
    if len(special_items) == 0:
        st.info("لا توجد خامات معرفة بالمستودع للتشغيل حالياً. اذهب لتبويب [المخازن والقطع] وقم بإضافة خامة جديدة.")
    else:
        special_options = {f"[{item.category}] {item.name_ar} - المتوفر: {item.quantity} {item.special_properties.get('unit_name', 'متر')}": item for item in special_items}
        selected_special_label = st.selectbox("اختر نوع الخامة المراد محاكاتها وتخصيص تفصيلها", options=list(special_options.keys()))
        selected_special_obj = special_options[selected_special_label]
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            job_title = st.text_input("اسم المهمة المخصصة / وصف المشروع والتفصيل", value="تجهيز وتفصيل عازل للسيارة بالكامل مع الإكسسوارات")
            req_qty = st.number_input(f"الكمية الأساسية الصافية المطلوبة للتفصيل والعمل ({selected_special_obj.special_properties.get('unit_name', 'متر')})", min_value=0.1, max_value=float(selected_special_obj.quantity), value=4.0)
            waste_p = st.number_input("نسبة الهدر والقص للمادة لتجنب عيوب التفصيل (%)", min_value=0.0, max_value=100.0, value=12.0)
        
        with col_c2:
            labor_fee = st.number_input("تكلفة العمالة والصنع / شغل يد الفني (ريال)", min_value=0.0, value=200.0)
            additional_material_fee = st.number_input("تكلفة مستلزمات مضافة أخرى (غراء، مشابك، مواد لاصقة) (ريال)", min_value=0.0, value=30.0)
            st.metric(label="سعر بيع الوحدة للزبون", value=f"{selected_special_obj.retail_price} ريال")
            
        calc_results = selected_special_obj.calculate_custom_fabrication(
            job_title=job_title,
            required_qty=req_qty,
            waste_percentage=waste_p,
            labor_fee=labor_fee,
            additional_material_fee=additional_material_fee
        )
        
        st.markdown("---")
        st.subheader("📊 تحليل مقاييس مشروع التشغيل والتفصيل الفوري:")
        
        chart_data = pd.DataFrame({
            "المقياس الحجمي": [req_qty, calc_results["qty_wasted_only"]],
            "نوع المادة": [f"الصافي المطلوب ({req_qty} {calc_results['unit_name']})", f"المادة المهدرة والقصاصات ({calc_results['qty_wasted_only']} {calc_results['unit_name']})"]
        })
        st.bar_chart(data=chart_data, x="نوع المادة", y="المقياس الحجمي")
        
        st.markdown("#### 📝 الفاتورة التقديرية المفصلة للعملية المخصصة:")
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric(label="الخامة الإجمالية المحتسبة للتفصيل", value=f"{calc_results['total_qty_consumed']} {calc_results['unit_name']}", delta=f"+{calc_results['waste_percentage']}% هدر")
            st.metric(label="طول الفيميه/الجلد التالف والقصاصات", value=f"{calc_results['qty_wasted_only']} {calc_results['unit_name']}")
        with col_res2:
            st.metric(label="قيمة الخامة الصافية للزبون", value=f"{calc_results['material_retail_price']} ريال")
            st.metric(label="أجرة التركيب وشغل يد الفني", value=f"{calc_results['labor_fee']} ريال")
        with col_res3:
            st.metric(label="السعر الإجمالي لعرض السعر الحالي", value=f"{calc_results['total_customer_price']} ريال سعودي", delta="السعر النهائي الشامل")
            st.metric(label="متبقي الخامة بالمستودع بعد هذه العملية", value=f"{calc_results['stock_remaining_after']} {calc_results['unit_name']}")


# ==========================================
# 5. صفحة الموظفين والورديات
# ==========================================

elif current_page == translate("employees_management"):
    st.title(f"👥 {translate('employees_management')}")
    st.markdown("##### إدارة الصلاحيات والشيفتات وجرد النقدية بالدرج")
    
    tab_shifts, tab_emp = st.tabs(["⏱️ إدارة الورديات والجرد المالي اليومي", "👤 تسجيل الموظفين والصلاحيات"])
    
    with tab_shifts:
        st.subheader("⚙️ التحكم بالوردية الحالية")
        active_shift = data_core.get_active_shift(user.username)
        
        if not active_shift:
            st.warning("⚠️ ليس لديك وردية مفتوحة حالياً في النظام! يرجى فتح وردية للبدء بالمبيعات.")
            
            with st.form("open_shift_form"):
                init_cash = st.number_input(translate("initial_cash"), min_value=0.0, value=200.0, step=50.0)
                submit_open = st.form_submit_button(translate("open_shift_btn"), type="primary")
                
                if submit_open:
                    coordinator.route_open_shift(user.username, init_cash)
                    st.success("تم فتح ورديتك بنجاح للبدء بمبيعات قطع غيار لوردستاير!")
                    time.sleep(0.5)
                    updated_emp = operations_core.authenticate_user(user.username, "admin123" if user.username=="admin" else "cashier123")
                    if updated_emp:
                        st.session_state.logged_user = updated_emp
                    st.rerun()
        else:
            st.success(f"🔓 لديك وردية مفتوحة ونشطة حالياً رقم: `{active_shift['shift_id']}`")
            st.markdown(f"**⏰ تاريخ ووقت فتح الوردية:** `{active_shift['start_time']}`")
            st.markdown(f"**💰 الكاش الأولي لتأسيس الدرج:** `{active_shift['initial_cash']} ريال`")
            
            all_sales = data_core.list_sales()
            shift_sales_total = sum(sale["total_amount"] for sale in all_sales if sale["shift_id"] == active_shift["shift_id"])
            expected_cash = active_shift["initial_cash"] + shift_sales_total
            
            st.info(f"📊 **المبيعات المسجلة بالوردية الحالية:** `{shift_sales_total} ريال` | **الكاش المتوقع بالدرج:** `{expected_cash} ريال`")
            
            st.markdown("---")
            st.subheader("🔐 إغلاق الوردية الحالية وتسليم العهدة")
            
            with st.form("close_shift_form"):
                actual_cash = st.number_input(translate("closing_cash_real"), min_value=0.0, value=expected_cash)
                closing_notes = st.text_area("ملاحظات الجرد والتسليم (اختياري)", placeholder="مثال: تم تسليم الكاش للمشرف والدرج متطابق")
                submit_close = st.form_submit_button(translate("close_shift_btn"), type="primary")
                
                if submit_close:
                    success, discrepancy = coordinator.route_close_shift(
                        employee_username=user.username,
                        shift_id=active_shift["shift_id"],
                        closing_cash=expected_cash,
                        actual_closing_cash=actual_cash,
                        notes=closing_notes
                    )
                    
                    st.warning(f"تم إغلاق الوردية بنجاح! قيمة الفارق والعجز المالي المسجلة: **{discrepancy} ريال**")
                    time.sleep(0.5)
                    st.session_state.logged_user.active_shift_id = None
                    st.rerun()
                    
        if user.role in ["Admin", "Manager"]:
            st.markdown("---")
            st.subheader("📜 أرشيف وجرد الورديات السابقة")
            shifts_history = data_core.list_shifts()
            if len(shifts_history) > 0:
                st.dataframe(pd.DataFrame(shifts_history), use_container_width=True)
            else:
                st.info("لا توجد سجلات لورديات مغلقة مسبقاً بالنظام.")

    with tab_emp:
        if user.role != "Admin":
            st.error("عذراً! صلاحيات إدارة الموظفين مخصصة للمدير المشرف العام فقط.")
        else:
            st.subheader("➕ إنشاء حساب لموظف أو محاسب جديد")
            with st.form("add_employee_form"):
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    emp_user = st.text_input(translate("employee_username"), placeholder="مثال: ahmed99")
                    emp_name = st.text_input(translate("employee_fullname"), placeholder="الاسم الكامل للموظف")
                    emp_pass = st.text_input(translate("employee_password"), type="password", placeholder="أدخل كلمة مرور قوية")
                with col_e2:
                    emp_role = st.selectbox(translate("employee_role"), options=["Admin", "Manager", "Cashier", "Technician"])
                    emp_branch = st.selectbox(translate("employee_branch"), options=["الفرع الرئيسي", "فرع التحلية", "فرع مكة المكرمة", "فرع الدمام"])
                    
                submit_emp = st.form_submit_button(translate("create_employee_btn"), type="primary")
                if submit_emp:
                    if not emp_user or not emp_pass or not emp_name:
                        st.error("يجب ملء كافة حقول إنشاء حساب الموظف قبل الحفظ.")
                    else:
                        emp_payload = {
                            "username": emp_user,
                            "password": emp_pass,
                            "full_name": emp_name,
                            "role": emp_role,
                            "branch": emp_branch
                        }
                        success, message = coordinator.route_add_employee(user.role, user.username, emp_payload)
                        if success:
                            st.success(message)
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error(message)
                            
            st.markdown("---")
            st.subheader("👥 الموظفون المسجلون حالياً بالنظام وصلاحياتهم")
            all_employees = data_core.list_employees()
            st.dataframe(pd.DataFrame(all_employees), use_container_width=True)


# ==========================================
# 6. صفحة نظام الأمان والكتل (Blockchain & OS Metrics)
# ==========================================

elif current_page == translate("security_logs"):
    st.title(f"🛡️ {translate('blockchain_title')}")
    st.markdown(f"**{translate('blockchain_info')}**")
    
    is_valid = security_core.blockchain.is_chain_valid()
    
    st.markdown(f"### 🛡️ {translate('blockchain_validity')}:")
    if is_valid:
        st.success(translate("valid"))
    else:
        st.error(translate("invalid"))
        
    st.markdown("---")
    
    # استعراض الكتل مع تلافي أخطاء KeyError بوضع استدعاءات آمنة .get() وتفاصيل أمنية فائقة الكثافة
    st.subheader("⛓️ سلسلة الكتل النشطة للتوثيق والتدقيق المالي والسيبراني")
    ledger_data = security_core.blockchain.export_ledger()
    
    for block in reversed(ledger_data):
        block_data = block.get("data", {})
        action_type = block_data.get("action_type", "GENESIS_BOOT")
        performed_by = block_data.get("user", "SYSTEM")
        event_time = block_data.get("system_time", block.get("timestamp"))
        details = block_data.get("details", "لا توجد تفاصيل إضافية")
        sig = block_data.get("security_signature", "N/A")
        level = block_data.get("level", "INFO")
        
        with st.expander(f"📦 البلوك رقم {block['index']} | الحدث: {action_type} | التاريخ: {event_time}"):
            st.markdown(f"**👤 القائم بالعملية المسؤول:** `{performed_by}`")
            st.markdown(f"**📝 تفاصيل الحدث الفنية:** `{details}`")
            st.markdown(f"**⚡ مستوى الأهمية والخطورة:** `{level}`")
            st.markdown(f"**🛡️ التوقيع الرقمي للحدث (Security Signature):** `{sig}`")
            
            # طباعة مؤشرات نظام التشغيل الملتقطة من نواة الأمن ولغة بايثون عبر psutil بشكل آمن
            st.markdown("**🖥️ مؤشرات نظام تشغيل الجهاز بلحظة الإجراء (OS-Level Metrics Logged):**")
            osm = block_data.get("os_metrics", {})
            if osm and "error" not in osm:
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                with col_m1:
                    st.info(f"💻 استهلاك المعالج: {osm.get('cpu_usage_pct', 0.0)}%")
                with col_m2:
                    st.info(f"🧠 استهلاك الذاكرة: {osm.get('ram_usage_pct', 0.0)}%")
                with col_m3:
                    st.info(f"⚙️ عمليات نشطة بالجهاز: {osm.get('active_processes', 0)}")
                with col_m4:
                    st.info(f"📊 مساحة القرص الشاغرة: {osm.get('disk_free_gb', 0.0)} GB")
            else:
                st.write("لا تتوفر مقاييس نظام تشغيل مسجلة لهذا البلوك التأسيسي.")
                
            st.markdown(f"**🔑 تشفير البلوك الحالي (SHA-256 Hash):** `{block['hash']}`")
            st.markdown(f"**🔗 رابط البلوك السابق (Previous Hash):** `{block['previous_hash']}`")
            st.markdown(f"**⚙️ قيمة محدد السلسلة (Nonce):** `{block['nonce']}`")
            
    st.markdown("---")
    st.subheader("🚨 خادر الأمن السيبراني ونظام كشف التسلل (IDS)")
    sec_kpis = security_core.cybersecurity.get_security_score()
    
    col_s1, col_sp_bar = st.columns([1, 2])
    with col_s1:
        st.metric(label="مؤشر درع الأمان العام", value=f"{sec_kpis['score']}%", delta=sec_kpis["status"])
        st.metric(label="عدد التنببهات الأمنية المرصودة", value=sec_kpis["total_alerts"])
    with col_sp_bar:
        st.write("درجة الموثوقية الأمنية (Cybersecurity Score Meter)")
        st.progress(sec_kpis["score"] / 100.0)
        
    st.write("🔍 **آخر التنبيهات الأمنية المسجلة بنظام كشف التسلل:**")
    if len(sec_kpis["alerts"]) == 0:
        st.info("لا توجد أي تهديدات أو محاولات وصول غير مصرحة مكتشفة. النظام آمن 100%!")
    else:
        for alert in reversed(sec_kpis["alerts"]):
            color = "🔴" if alert["severity"] == "CRITICAL" else "🟡"
            st.markdown(f"{color} **[{alert['severity']}] {alert['time']}:** {alert['details']}")


# ==========================================
# 7. صفحة نقل واستيراد البيانات العتيقة
# ==========================================

elif current_page == translate("import_export"):
    st.title(f"📥 {translate('import_legacy_title')}")
    st.markdown("##### تتيح هذه الناواة نقل وتحديث قواعد البيانات العتيقة والقديمة التي تعمل بها المحلات قبل الأتمتة")
    
    col_imp, col_exp = st.columns(2)
    
    with col_imp:
        st.subheader("⬇️ استيراد قاعدة بيانات قديمة (CSV)")
        st.write("يدعم المحرك الذكي مطابقة أعمدة الأنظمة القديمة مع لوردستاير تلقائياً.")
        
        template_data = {
            "ID": ["SP-9001", "SP-9002"],
            "code": ["AM-1122", "AM-1123"],
            "الاسم_العربي": ["مساعدات أمامية لاندكروزر", "مساعدات خلفية يارس"],
            "القسم": ["نظام التعليق", "نظام التعليق"],
            "الكمية": [20, 15],
            "سعر_الجملة": [120, 45],
            "سعر_البيع": [180, 75],
            "التوافق": ["Land Cruiser 2010-2021", "Yaris 2017+"]
        }
        template_csv = pd.DataFrame(template_data).to_csv(index=False, encoding="utf-8-sig")
        st.download_button("📥 تحميل ملف قالب CSV متوافق للاسترشاد به", data=template_csv, file_name="lordstair_template.csv", mime="text/csv")
        
        uploaded_file = st.file_uploader(translate("import_csv_label"), type=["csv"])
        
        if uploaded_file is not None:
            temp_path = "temp_uploaded_inventory.csv"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            if st.button(translate("import_btn"), type="primary"):
                with st.spinner("جاري قراءة الملف وتشفير أسعار الشراء وتحديث قواعد البيانات..."):
                    success, msg = data_core.import_inventory_from_csv(temp_path)
                    if success:
                        st.success(msg)
                        coordinator.log_connection_event("DATABASE_MIGRATION", user.username, f"تم بنجاح استيراد وتحديث قاعدة مخزون قديمة بالبرنامج")
                    else:
                        st.error(msg)
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                        
    with col_exp:
        st.subheader("⬆️ تصدير وحفظ قاعدة البيانات الحالية للوردستاير")
        st.write("يمكنك حفظ وتصدير كامل المخزون الحالي بصيغة CSV أو بصيغة ملف Excel منسق وملون.")
        
        all_items = data_core.list_inventory()
        if len(all_items) > 0:
            df_export = pd.DataFrame(all_items)
            df_export["wholesale_price"] = df_export["wholesale_price"].apply(lambda x: x if isinstance(x, float) else 0.0)
            
            csv_data = df_export.to_csv(index=False, encoding="utf-8-sig")
            st.download_button(
                translate("export_csv_btn"),
                data=csv_data,
                file_name=f"lordstair_inventory_{int(time.time())}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            excel_path = f"lordstair_inventory_{int(time.time())}.xlsx"
            df_export.to_excel(excel_path, index=False)
            with open(excel_path, "rb") as f:
                excel_bytes = f.read()
            st.download_button(
                translate("export_xlsx_btn"),
                data=excel_bytes,
                file_name=excel_path,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            if os.path.exists(excel_path):
                os.remove(excel_path)
        else:
            st.info("المستودع فارغ حالياً للتصدير.")

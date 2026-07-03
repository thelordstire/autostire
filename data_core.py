# -*- coding: utf-8 -*-
import sqlite3
import json
import os
import time
import pandas as pd
from datetime import datetime

# ==========================================
# نواة البيانات (Data Core)
# تتولى الاتصال بقاعدة البيانات، إعداد الجداول، تشفير الحقول الحساسة، الاستيراد والتصدير
# ==========================================

class DataCore:
    def __init__(self, db_path="lordstair_database.db", security_core=None):
        self.db_path = db_path
        self.security_core = security_core
        self.init_database()

    def get_connection(self):
        """
        فتح اتصال بقاعدة البيانات SQLite وتمكين تصفح الصفوف كقواميس.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """
        إنشاء الجداول الأساسية للنظام وفق أحدث وأدق المعايير، مع إعداد الحساب الإداري الافتراضي.
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # 1. جدول الموظفين والحسابات والورديات
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            branch TEXT NOT NULL,
            is_active INTEGER DEFAULT 1
        )
        """)

        # 2. جدول المخزون وقطع الغيار والكماليات والمواد الخاصة (مثل الفيميه والمواد المقاسة بالمتر)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            part_id TEXT PRIMARY KEY,
            part_number TEXT UNIQUE,
            name_ar TEXT NOT NULL,
            name_en TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity REAL NOT NULL,
            wholesale_price TEXT NOT NULL, -- مشفر لأسباب أمنية
            retail_price REAL NOT NULL,
            compatibility TEXT,             -- السيارات المتوافقة (مفصولة بفاصلة أو JSON)
            is_special INTEGER DEFAULT 0,  -- 1 للمواد الخاصة التي تقاس بالمتر مثل الفيميه، 0 للقطع العادية
            special_properties TEXT         -- خصائص إضافية كعرض الرول، نسبة الهدر، طول الرول الإجمالي
        )
        """)

        # 3. جدول فواتير المبيعات
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            invoice_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            employee_username TEXT NOT NULL,
            customer_name TEXT,
            customer_phone TEXT,          -- مشفر لحماية خصوصية العميل
            items_json TEXT NOT NULL,     -- قائمة القطع والأسعار والكميات والهدر
            total_amount REAL NOT NULL,
            discount REAL DEFAULT 0,
            payment_method TEXT NOT NULL,  -- نقدي، شبكة، تحويل بنكي
            shift_id TEXT
        )
        """)

        # 4. جدول الورديات (Shifts)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS shifts (
            shift_id TEXT PRIMARY KEY,
            employee_username TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            initial_cash REAL NOT NULL,
            closing_cash REAL,
            actual_closing_cash REAL,
            status TEXT DEFAULT 'OPEN',     -- OPEN أو CLOSED
            notes TEXT
        )
        """)

        # إنشاء مستخدم أدمن افتراضي إذا لم يكن هناك أي موظفين في النظام
        cursor.execute("SELECT COUNT(*) as count FROM employees")
        if cursor.fetchone()["count"] == 0:
            # تشفير كلمة المرور الافتراضية "lordstair2026"
            default_pass_hash = "f11a8848d7c2f0f42dfbf44e6bdfde0ef9cb962eaefb3a7beee75cb39c158581" 
            if self.security_core:
                default_pass_hash = self.security_core.cybersecurity.hash_password("admin123")
            
            cursor.execute("""
            INSERT INTO employees (username, password_hash, full_name, role, branch, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            """, ("admin", default_pass_hash, "اللوردستاير المشرف العام", "Admin", "الفرع الرئيسي", 1))
            
            # مستخدم كاشير تجريبي
            cashier_pass_hash = default_pass_hash
            if self.security_core:
                cashier_pass_hash = self.security_core.cybersecurity.hash_password("cashier123")
            cursor.execute("""
            INSERT INTO employees (username, password_hash, full_name, role, branch, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
            """, ("cashier", cashier_pass_hash, "محاسب المبيعات أحمد", "Cashier", "الفرع الرئيسي", 1))

        conn.commit()
        conn.close()

    # ==========================================
    # عمليات الموظفين والصلاحيات
    # ==========================================
    def add_employee(self, username, password, full_name, role, branch):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        pass_hash = password
        if self.security_core:
            pass_hash = self.security_core.cybersecurity.hash_password(password)
            
        try:
            cursor.execute("""
            INSERT INTO employees (username, password_hash, full_name, role, branch, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
            """, (username, pass_hash, full_name, role, branch))
            conn.commit()
            success = True
        except sqlite3.IntegrityError:
            success = False
        finally:
            conn.close()
        return success

    def get_employee(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employees WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def list_employees(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, full_name, role, branch, is_active FROM employees")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # ==========================================
    # عمليات المخزون وقطع الغيار
    # ==========================================
    def add_inventory_item(self, part_id, part_number, name_ar, name_en, category, quantity, wholesale_price, retail_price, compatibility, is_special=0, special_properties="{}"):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # تشفير سعر الجملة لحماية بيانات وهوامش ربح المحل
        enc_wholesale = str(wholesale_price)
        if self.security_core:
            enc_wholesale = self.security_core.cybersecurity.encrypt_data(str(wholesale_price))
            
        try:
            cursor.execute("""
            INSERT INTO inventory (part_id, part_number, name_ar, name_en, category, quantity, wholesale_price, retail_price, compatibility, is_special, special_properties)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (part_id, part_number, name_ar, name_en, category, quantity, enc_wholesale, retail_price, compatibility, is_special, special_properties))
            conn.commit()
            success = True
        except sqlite3.IntegrityError as e:
            print("IntegrityError:", e)
            success = False
        finally:
            conn.close()
        return success

    def update_inventory_item(self, part_id, name_ar, name_en, category, quantity, wholesale_price, retail_price, compatibility, is_special=0, special_properties="{}"):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        enc_wholesale = str(wholesale_price)
        if self.security_core:
            enc_wholesale = self.security_core.cybersecurity.encrypt_data(str(wholesale_price))
            
        cursor.execute("""
        UPDATE inventory
        SET name_ar = ?, name_en = ?, category = ?, quantity = ?, wholesale_price = ?, retail_price = ?, compatibility = ?, is_special = ?, special_properties = ?
        WHERE part_id = ?
        """, (name_ar, name_en, category, quantity, enc_wholesale, retail_price, compatibility, is_special, special_properties, part_id))
        conn.commit()
        conn.close()
        return True

    def delete_inventory_item(self, part_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE part_id = ?", (part_id,))
        conn.commit()
        conn.close()
        return True

    def list_inventory(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM inventory")
        rows = cursor.fetchall()
        conn.close()
        
        items = []
        for row in rows:
            item = dict(row)
            # فك تشفير سعر الجملة
            if self.security_core and item["wholesale_price"]:
                try:
                    item["wholesale_price"] = float(self.security_core.cybersecurity.decrypt_data(item["wholesale_price"]))
                except Exception:
                    item["wholesale_price"] = 0.0
            else:
                try:
                    item["wholesale_price"] = float(item["wholesale_price"])
                except Exception:
                    item["wholesale_price"] = 0.0
            items.append(item)
        return items

    # ==========================================
    # عمليات الورديات (Shifts)
    # ==========================================
    def open_shift(self, employee_username, initial_cash):
        conn = self.get_connection()
        cursor = conn.cursor()
        shift_id = f"SHIFT-{int(time.time())}"
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # إغلاق أي وردية مفتوحة سابقة لنفس المستخدم لضمان دقة الحسابات
        cursor.execute("""
        UPDATE shifts 
        SET status = 'CLOSED', end_time = ? 
        WHERE employee_username = ? AND status = 'OPEN'
        """, (start_time, employee_username))
        
        cursor.execute("""
        INSERT INTO shifts (shift_id, employee_username, start_time, initial_cash, status)
        VALUES (?, ?, ?, ?, 'OPEN')
        """, (shift_id, employee_username, start_time, initial_cash))
        conn.commit()
        conn.close()
        return shift_id

    def close_shift(self, shift_id, closing_cash, actual_closing_cash, notes=""):
        conn = self.get_connection()
        cursor = conn.cursor()
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        UPDATE shifts
        SET end_time = ?, closing_cash = ?, actual_closing_cash = ?, status = 'CLOSED', notes = ?
        WHERE shift_id = ?
        """, (end_time, closing_cash, actual_closing_cash, notes, shift_id))
        conn.commit()
        conn.close()
        return True

    def get_active_shift(self, employee_username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM shifts WHERE employee_username = ? AND status = 'OPEN'", (employee_username,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def list_shifts(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM shifts ORDER BY start_time DESC")
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    # ==========================================
    # عمليات الفواتير والمبيعات
    # ==========================================
    def create_sale_invoice(self, invoice_id, employee, customer_name, customer_phone, items_list, total_amount, discount, payment_method, shift_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # تشفير رقم الهاتف الخاص بالعميل التزاماً بالمعايير الأمنية وحماية الخصوصية
        enc_phone = customer_phone
        if self.security_core and customer_phone:
            enc_phone = self.security_core.cybersecurity.encrypt_data(customer_phone)
            
        items_json = json.dumps(items_list, ensure_ascii=False)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # 1. إدراج الفاتورة في جدول المبيعات
            cursor.execute("""
            INSERT INTO sales (invoice_id, timestamp, employee_username, customer_name, customer_phone, items_json, total_amount, discount, payment_method, shift_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (invoice_id, timestamp, employee, customer_name, enc_phone, items_json, total_amount, discount, payment_method, shift_id))
            
            # 2. تحديث المخزون وحسم الكميات بشكل متزامن دقيق
            for item in items_list:
                part_id = item["part_id"]
                quantity_sold = item["qty"] # قد يكون كسراً في حالة الفيميه والمواد المقاسة بالمتر
                
                # استرجاع الكمية الحالية لتفادي النزول تحت الصفر دون تنبيه
                cursor.execute("SELECT quantity FROM inventory WHERE part_id = ?", (part_id,))
                current_qty_row = cursor.fetchone()
                if current_qty_row:
                    new_qty = max(0.0, current_qty_row["quantity"] - quantity_sold)
                    cursor.execute("UPDATE inventory SET quantity = ? WHERE part_id = ?", (new_qty, part_id))
                    
            conn.commit()
            success = True
        except Exception as e:
            print("Error creating sale invoice:", e)
            conn.rollback()
            success = False
        finally:
            conn.close()
        return success

    def list_sales(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sales ORDER BY timestamp DESC")
        rows = cursor.fetchall()
        conn.close()
        
        sales_list = []
        for row in rows:
            sale = dict(row)
            # فك تشفير رقم العميل
            if self.security_core and sale["customer_phone"]:
                try:
                    sale["customer_phone"] = self.security_core.cybersecurity.decrypt_data(sale["customer_phone"])
                except Exception:
                    pass
            try:
                sale["items"] = json.loads(sale["items_json"])
            except Exception:
                sale["items"] = []
            sales_list.append(sale)
        return sales_list

    # ==========================================
    # عمليات التصدير والاستيراد (Import / Export)
    # تتيح نقل قواعد البيانات العتيقة والقديمة واستيرادها وحفظ البيانات بصيغ Excel و CSV
    # ==========================================
    def export_inventory_to_csv(self, file_path):
        """
        تصدير المخزون بالكامل إلى ملف CSV نظيف ومقروء.
        """
        items = self.list_inventory()
        # إزالة خصائص التشفير وعرض أسعار حقيقية للمصدَّر
        df = pd.DataFrame(items)
        if not df.empty:
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
            return True
        return False

    def export_inventory_to_excel(self, file_path):
        """
        تصدير المخزون إلى ملف Excel ملون واحترافي باستخدام Pandas و Openpyxl.
        """
        items = self.list_inventory()
        df = pd.DataFrame(items)
        if not df.empty:
            df.to_excel(file_path, index=False)
            return True
        return False

    def import_inventory_from_csv(self, file_path) -> tuple:
        """
        استيراد المخزون من ملف CSV خارجي (يدعم الأنظمة القديمة والعتيقة).
        يجب أن يحتوي الملف على أعمدة متوافقة أو قريبة (مثل: part_id, part_number, name_ar, name_en, category, quantity, wholesale_price, retail_price).
        """
        if not os.path.exists(file_path):
            return False, "الملف غير موجود في المسار المحدد!"
        
        try:
            df = pd.read_csv(file_path)
            # تطبيع وتأكيد أسماء الأعمدة لتتناسب مع قواعد بيانات المحلات القديمة
            col_mappings = {
                "رقم_القطعة": "part_id", "الكود": "part_id", "id": "part_id", "part_id": "part_id",
                "رقم_المصنع": "part_number", "part_number": "part_number", "code": "part_number",
                "الاسم_العربي": "name_ar", "الاسم": "name_ar", "name_ar": "name_ar", "name": "name_ar",
                "الاسم_الانجليزي": "name_en", "name_en": "name_en",
                "القسم": "category", "الفئة": "category", "category": "category",
                "الكمية": "quantity", "quantity": "quantity", "qty": "quantity",
                "سعر_الجملة": "wholesale_price", "wholesale_price": "wholesale_price", "cost": "wholesale_price",
                "سعر_البيع": "retail_price", "retail_price": "retail_price", "price": "retail_price",
                "التوافق": "compatibility", "compatibility": "compatibility"
            }
            
            # إعادة تسمية الأعمدة المقروءة لتتطابق مع قاعدة البيانات
            df.rename(columns=col_mappings, inplace=True)
            
            # ملء الحقول الناقصة بقيم افتراضية آمنة ومريحة
            required_cols = ["part_id", "part_number", "name_ar", "name_en", "category", "quantity", "wholesale_price", "retail_price"]
            for col in required_cols:
                if col not in df.columns:
                    if col == "name_en":
                        df["name_en"] = df["name_ar"]
                    elif col == "part_number":
                        df["part_number"] = df["part_id"]
                    elif col == "category":
                        df["category"] = "عام"
                    elif col == "quantity":
                        df["quantity"] = 0.0
                    elif col == "wholesale_price":
                        df["wholesale_price"] = 0.0
                    elif col == "retail_price":
                        df["retail_price"] = 0.0
                    else:
                        raise ValueError(f"العمود الأساسي المطلوب غير متوفر بالملف: {col}")
            
            imported_count = 0
            skipped_count = 0
            
            for _, row in df.iterrows():
                # التحقق مما إذا كان العنصر موجوداً بالفعل لتجنب التكرار
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM inventory WHERE part_id = ?", (str(row["part_id"]),))
                exists = cursor.fetchone()
                conn.close()
                
                if exists:
                    # تحديث إذا كان موجوداً
                    self.update_inventory_item(
                        part_id=str(row["part_id"]),
                        name_ar=str(row["name_ar"]),
                        name_en=str(row["name_en"]),
                        category=str(row["category"]),
                        quantity=float(row["quantity"]),
                        wholesale_price=float(row["wholesale_price"]),
                        retail_price=float(row["retail_price"]),
                        compatibility=str(row["compatibility"]) if pd.notna(row["compatibility"]) else "",
                        is_special=0,
                        special_properties="{}"
                    )
                    skipped_count += 1
                else:
                    # إضافة عنصر جديد بالكامل
                    res = self.add_inventory_item(
                        part_id=str(row["part_id"]),
                        part_number=str(row["part_number"]),
                        name_ar=str(row["name_ar"]),
                        name_en=str(row["name_en"]),
                        category=str(row["category"]),
                        quantity=float(row["quantity"]),
                        wholesale_price=float(row["wholesale_price"]),
                        retail_price=float(row["retail_price"]),
                        compatibility=str(row["compatibility"]) if pd.notna(row["compatibility"]) else "",
                        is_special=0,
                        special_properties="{}"
                    )
                    if res:
                        imported_count += 1
                    else:
                        skipped_count += 1
                        
            return True, f"تمت العملية بنجاح! تم استيراد وتحديث {imported_count} صنف جديد وتحديث {skipped_count} صنف موجود بالفعل."
        except Exception as e:
            return False, f"حدث خطأ أثناء قراءة واستيراد الملف: {str(e)}"

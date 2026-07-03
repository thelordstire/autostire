# -*- coding: utf-8 -*-
import hashlib
import json
import time
import os
import sys
import psutil
from cryptography.fernet import Fernet

# ==========================================
# نواة الأمن (Security Core) - نسخة احترافية فائقة الدقة والأمان
# تتكون من خادمين فرعيين: خادم البلوكتشاين وخادم الأمن السيبراني مع مراقبة نظام التشغيل (OS-Level Audit)
# ==========================================

class Block:
    """
    تمثيل لبلوك واحد في سلسلة الكتل (البلوكتشاين) لتوثيق الأحداث.
    """
    def __init__(self, index, timestamp, data, previous_hash, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.data = data  # البيانات الموثقة بالكامل
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """
        حساب تشفير الهاش للبلوك الحالي باستخدام خوارزمية SHA-256.
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty=2):
        """
        إجراء عملية التنقيب (Proof of Work) لضمان أمان البلوك وصعوبة تعديله بأثر رجعي.
        """
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()


class BlockchainServer:
    """
    خادم البلوكتشاين والتوثيق: يقوم بمراقبة وتوثيق العمليات في النظام في بلوكات غير قابلة للتعديل.
    """
    def __init__(self):
        self.chain = []
        self.difficulty = 2
        # إنشاء البلوك الأول (Genesis Block) مع مطابقة الهيكل العام لتجنب أخطاء KeyError
        self.create_genesis_block()

    def create_genesis_block(self):
        """
        إنشاء البلوك الأول والأساسي لسلسلة الكتل بهيكل بيانات كامل وموحد لتجنب الاختلافات البرمجية.
        """
        genesis_data = {
            "action_type": "GENESIS_BOOT",
            "user": "SYSTEM_SECURE",
            "details": "نظام لوردستاير - بدء تشغيل وإعداد سلسلة الكتل المؤمنة بأثر رجعي بنجاح.",
            "level": "INFO",
            "system_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "os_metrics": {
                "cpu_usage_pct": 0.0,
                "ram_usage_pct": 0.0,
                "active_processes": 0,
                "disk_free_gb": 0.0,
                "os_platform": os.name
            },
            "security_signature": "LORDSTAIR_SECURE_SIGNATURE_2026"
        }
        genesis_block = Block(0, time.time(), genesis_data, "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self):
        """
        استرجاع البلوك الأخير في السلسلة.
        """
        return self.chain[-1]

    def add_event(self, action_type, user, details, os_metrics=None, level="INFO"):
        """
        إضافة حدث جديد غني بالتفاصيل الهندسية والأمنية الدقيقة إلى البلوكتشاين بشكل فوري ومتزامن.
        """
        latest_block = self.get_latest_block()
        
        # تفصيل وتكثيف محتويات البلوك ليكون سجلاً فائق الوضوح والدقة
        enriched_details = {
            "action_type": action_type,      # نوع العملية (بيع، تعديل، جرد، أمن)
            "user": user,                    # اسم الموظف المسؤول
            "details": details,              # شرح تفصيلي دقيق وموسع للعملية
            "level": level,                  # مستوى الخطورة والأهمية الفنية
            "system_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "os_metrics": os_metrics or {},  # حالة عتاد ونظام تشغيل جهاز المحاسبة
            "security_signature": hashlib.sha256(f"{user}_{action_type}_{time.time()}".encode()).hexdigest()[:32] # توقيع رقمي فريد للحدث
        }
        
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=time.time(),
            data=enriched_details,
            previous_hash=latest_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self):
        """
        التحقق من صحة وسلامة سلسلة الكتل (البلوكتشاين) وضمان عدم التلاعب بأي سجلات.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                return False

        return True

    def export_ledger(self):
        """
        تصدير السجل الكامل للبلوكتشاين بصيغة مقروءة للتحقيق والمراجعة الأمنية.
        """
        ledger = []
        for block in self.chain:
            ledger.append({
                "index": block.index,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(block.timestamp)),
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash,
                "nonce": block.nonce
            })
        return ledger


class CybersecurityServer:
    """
    خادم الأمن السيبراني: يتولى التشفير، الصلاحيات، مراقبة الاختراق والتهديدات، ومراقبة موارد ونظام تشغيل الجهاز باستخدام psutil.
    """
    def __init__(self):
        # توليد مفتاح التشفير المتماثل لحماية البيانات
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        
        # سجل التهديدات والمراقبة الأمنية
        self.failed_logins = {}
        self.blocked_ips = set()
        self.security_alerts = []

    def get_os_level_metrics(self) -> dict:
        """
        جلب إحصائيات ومؤشرات حية على مستوى نظام تشغيل الجهاز باستخدام مكتبة psutil المتخصصة.
        تقوم هذه الأداة بجلب استهلاك المعالج، الذاكرة العشوائية، العمليات النشطة، وحالة القرص.
        """
        try:
            cpu_usage = psutil.cpu_percent(interval=None) or 0.1
            memory_info = psutil.virtual_memory()
            disk_usage = psutil.disk_usage('/')
            active_processes_count = len(psutil.pids())
            
            return {
                "cpu_usage_pct": float(cpu_usage),
                "ram_usage_pct": float(memory_info.percent),
                "ram_available_mb": float(round(memory_info.available / (1024 * 1024), 2)),
                "disk_free_gb": float(round(disk_usage.free / (1024 * 1024 * 1024), 2)),
                "active_processes": int(active_processes_count),
                "os_platform": str(os.name),
                "threat_level": "NORMAL" if cpu_usage < 85.0 and memory_info.percent < 90.0 else "HIGH_LOAD"
            }
        except Exception as e:
            return {
                "error": f"فشل جلب مقاييس نظام التشغيل: {str(e)}",
                "threat_level": "UNKNOWN"
            }

    def encrypt_data(self, plaintext: str) -> str:
        """
        تشفير البيانات الحساسة (مثل الأسعار الحقيقية وتفاصيل الموردين والهواتف) قبل حفظها.
        """
        if not plaintext:
            return ""
        return self.cipher_suite.encrypt(plaintext.encode('utf-8')).decode('utf-8')

    def decrypt_data(self, ciphertext: str) -> str:
        """
        فك تشفير البيانات الحساسة لعرضها للمستخدمين المصرح لهم فقط.
        """
        if not ciphertext:
            return ""
        try:
            return self.cipher_suite.decrypt(ciphertext.encode('utf-8')).decode('utf-8')
        except Exception:
            return "[خطأ في فك التشفير - غير مصرح]"

    def hash_password(self, password: str) -> str:
        """
        تشفير كلمة المرور للموظف بأسلوب آمن وحتمي (SHA-256 مع ملح).
        """
        salt = "LordstairAutoParts2026SecureSalt"
        salted_pass = password + salt
        return hashlib.sha256(salted_pass.encode('utf-8')).hexdigest()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        التحقق من تطابق كلمة المرور المدخلة مع المخزنة.
        """
        return self.hash_password(password) == hashed_password

    def register_login_attempt(self, username: str, success: bool, ip_address: str = "127.0.0.1"):
        """
        مراقبة محاولات تسجيل الدخول لكشف الهجمات السيبرانية وإرسال تحذيرات.
        """
        if success:
            if username in self.failed_logins:
                self.failed_logins[username] = 0
        else:
            self.failed_logins[username] = self.failed_logins.get(username, 0) + 1
            if self.failed_logins[username] >= 5:
                alert = {
                    "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                    "type": "BRUTE_FORCE_ATTEMPT",
                    "details": f"محاولات دخول فاشلة متكررة ({self.failed_logins[username]} مرات) للحساب: {username}",
                    "severity": "CRITICAL"
                }
                self.security_alerts.append(alert)
                return "CRITICAL_ALERT"
        return "OK"

    def audit_system_behavior(self, user_role: str, action: str) -> bool:
        """
        فحص السلوك غير الاعتيادي لمنع الوصول غير المصرح به للعمليات الحساسة.
        """
        role_privileges = {
            "Admin": ["view_dashboard", "manage_employees", "manage_inventory", "process_sales", "view_reports", "security_panel", "import_export"],
            "Manager": ["view_dashboard", "manage_inventory", "process_sales", "view_reports", "import_export"],
            "Cashier": ["process_sales", "view_inventory_simple"],
            "Technician": ["view_inventory_simple", "tinting_calculator", "process_installation"]
        }
        
        allowed_actions = role_privileges.get(user_role, [])
        if action not in allowed_actions:
            alert = {
                "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                "type": "UNAUTHORIZED_ACCESS",
                "details": f"محاولة وصول غير مصرح بها من دور [{user_role}] للقيام بـ [{action}]",
                "severity": "HIGH"
            }
            self.security_alerts.append(alert)
            return False
        return True

    def get_security_score(self) -> dict:
        """
        حساب وتقييم مستوى الأمان الحالي للنظام (Security KPI dashboard) لعرضه للإدارة.
        """
        total_alerts = len(self.security_alerts)
        critical_alerts = len([a for a in self.security_alerts if a["severity"] == "CRITICAL"])
        
        score = 100 - (critical_alerts * 15) - ((total_alerts - critical_alerts) * 5)
        score = max(score, 10)
        
        status = "ممتاز وآمن جداً" if score >= 90 else "مستقر - يرجى مراجعة التنبيهات" if score >= 70 else "خطر - يتطلب تدخل فوري"
        
        return {
            "score": score,
            "status": status,
            "total_alerts": total_alerts,
            "critical_alerts": critical_alerts,
            "alerts": self.security_alerts[-10:]
        }


class SecurityCore:
    """
    النواة الشاملة للأمن: تدمج خادمي البلوكتشاين والأمن السيبراني وتوفر بوابة تحكم آمنة وموحدة.
    """
    def __init__(self):
        self.blockchain = BlockchainServer()
        self.cybersecurity = CybersecurityServer()

    def log_and_secure(self, action_type: str, user: str, details: str, level="INFO"):
        """
        تسجيل العملية في البلوكتشاين وتأمينها برمجياً مع إرجاع تقرير الحالة الأمنية متضمناً مؤشرات نظام التشغيل (OS Metrics).
        """
        # جلب مؤشرات نظام التشغيل النشط عبر psutil
        os_metrics = self.cybersecurity.get_os_level_metrics()
        
        # توثيق الحدث في البلوكتشاين بشكل دائم ومتسلسل
        block = self.blockchain.add_event(action_type, user, details, os_metrics=os_metrics, level=level)
        return block

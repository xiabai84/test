import imaplib
import email

# ==================== 填入你的配置 ====================
IMAP_SERVER = '://office365.com'
EMAIL_USER = 'your_email@company.com'     # 你的公司邮箱账号
EMAIL_PASS = 'your_app_password'         # 刚刚生成的16位应用专用密码（无空格）

# 顺便测试一下能否搜到你以前的告警邮件（用于验证过滤规则）
TEST_SUBJECT = 'HeapOverloaded'           # 填入你以往告警邮件标题里的关键字
# ======================================================

def verify_connection():
    try:
        print("1. 正在尝试连接微软 Office 365 IMAP 服务器...")
        # 建立加密连接
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, 993)
        print("   ✅ 服务器连接成功！")
        
        print(f"2. 正在尝试登录账户: {EMAIL_USER} ...")
        # 执行登录
        status, response = mail.login(EMAIL_USER, EMAIL_PASS)
        print(f"   ✅ 登录成功！服务器返回: {status} - {response}")
        
        print("3. 正在打开收件箱 (Inbox)...")
        mail.select('inbox')
        print("   ✅ 收件箱打开成功！")
        
        print(f"4. 正在尝试搜索主题包含 [{TEST_SUBJECT}] 的邮件...")
        # 注意：这里先用 ALL 搜索所有邮件（包含已读和未读），方便测试
        status, data = mail.search(None, f'SUBJECT "{TEST_SUBJECT}"')
        mail_ids = data[0].split()
        
        print(f"   ✅ 搜索完成！共找到 {len(mail_ids)} 封匹配的邮件。")
        if mail_ids:
            print("   👉 匹配到的最新一封邮件 ID 为:", mail_ids[-1].decode('utf-8'))
            
        print("\n🎉【最终结论】: 你的 IMAP URL 和密码配置完全正确！可以执行下一步的自动化脚本。")
        mail.logout()
        
    except imaplib.IMAP4.error as e:
        print("\n❌【登录失败】: 密码错误或微软现代验证拦截。")
        print(f"   错误详情: {e}")
        print("   💡 排查建议: 请确认你使用的是在微软安全中心生成的 16 位‘应用专用密码’，而不是你平时的登录密码。")
    except Exception as e:
        print(f"\n❌【未知错误】: {e}")

if __name__ == '__main__':
    verify_connection()

from playwright.sync_api import sync_playwright
import time
import json
import os
import sys
import common

class LoginManager:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.login_url = "https://www.jiandaoyun.com/dashboard#/login"
        self.target_url = "https://www.jiandaoyun.com/dashboard#/app/67f7b5e44bb87e55f5a8c699/form/67f7b5e741db931a0b8c63fa"
        self.config_path = '/home/dev/mall2/mall/config/auth_token.json'

    def log(self, message, level="INFO"):
        """格式化日志输出"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        color = ""
        if level == "ERROR": color = "\033[91m"   # 红色
        elif level == "SUCCESS": color = "\033[92m" # 绿色
        elif level == "WARN": color = "\033[93m"    # 黄色
        reset = "\033[0m"
        common.log(f"[{timestamp}] [{level}] {color}{message}{reset}")

    def fetch_and_save(self):
        self.log(">>> 开始执行凭证刷新任务 <<<")
        
        if not os.path.exists('config'):
            os.makedirs('config')

        with sync_playwright() as p:
            self.log("启动 Chromium 浏览器引擎...")
            browser = p.chromium.launch(headless=True) 
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            # 内部变量，记录拦截状态
            state = {
                "intercepted": False,
                "auth_data": {"cookie": "", "csrf_token": "", "jdy_ver": "10.17.2"}
            }

            # --- 注册拦截器 (放在 goto 之前) ---
            def handle_request(request):
                # 只要 URL 包含 find 且是 POST 请求（简道云查询通常是 POST）
                if "find" in request.url and "data" in request.url and request.method == "POST":
                    headers = {k.lower(): v for k, v in request.headers.items()}
                    self.log(f"📋 完整 Headers 字典内容:\n{json.dumps(headers, indent=2)}")
                    token = headers.get("x-csrf-token")
                    all_cookies = context.cookies(request.url)
                    cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in all_cookies])
                    
                    # 实时打印发现记录，方便排查
                    self.log(f"🔍 探测到 API 请求: {request.url[:50]}...")
                    
                    if token:
                        state["auth_data"]["cookie"] = cookie_str
                        state["auth_data"]["csrf_token"] = token
                        state["auth_data"]["jdy_ver"] = headers.get("x-jdy-ver", "10.17.2")
                        state["intercepted"] = True
                        self.log(f"⚡ 成功拦截关键凭证! Token前缀: {token[:10]}", "SUCCESS")
                    else:
                        self.log(f"⚠️ 该请求未携带 x-csrf-token，继续监听...", "WARN")

            page.on("request", handle_request)

            try:
                # 1. 登录流程
                self.log(f"正在打开登录页...")
                page.goto(self.login_url, wait_until="networkidle")
                
                self.log(f"正在填充身份信息...")
                page.wait_for_selector('input[placeholder*="Phone"]', timeout=10000)
                page.fill('input[placeholder*="Phone"]', self.username)
                page.fill('input[placeholder*="Password"]', self.password)
                
                self.log("提交登录...")
                page.click('button:has-text("Log in")')
                
                # 等待登录成功跳转
                page.wait_for_url("**/**", timeout=30000)
                self.log("登录成功，进入控制台", "SUCCESS")

                # 2. 访问目标表单以激活拦截
                self.log(f"正在跳转至目标业务页激活拦截器...")
                # 强制不使用缓存跳转
                page.goto(self.target_url, wait_until="networkidle")
                
                # 循环等待拦截成功的状态，最多等 15 秒
                retry_count = 0
                while not state["intercepted"] and retry_count < 15:
                    # 模拟一点页面交互动作（有时滚动会触发 API 调用）
                    if retry_count == 5:
                        page.mouse.wheel(0, 500)
                        self.log("尝试向下滚动页面以触发延迟加载的 API...", "INFO")
                    
                    time.sleep(1)
                    retry_count += 1
                
                # 3. 结果处理
                if state["intercepted"]:
                    self.log(f"即将保存数据: {json.dumps(state['auth_data'])}")
                    with open(self.config_path, 'w', encoding='utf-8') as f:
                        json.dump(state["auth_data"], f, indent=4)
                    
                    file_size = os.path.getsize(self.config_path)
                    self.log(f"✅ 任务圆满完成! 文件已更新 ({file_size} bytes)", "SUCCESS")
                    return 1
                else:
                    self.log("❌ 拦截失败：虽然页面已加载，但未能捕获到含 Token 的 find 请求", "ERROR")
                    self.log(f"残留状态数据: {json.dumps(state['auth_data'])}")
                    
                    # 失败截图辅助排查
                    screenshot_path = f"config/fail_{int(time.time())}.png"
                    page.screenshot(path=screenshot_path, full_page=True)
                    self.log(f"已保存失败现场截图: {screenshot_path}", "WARN")
                    return 2

            except Exception as e:
                self.log(f"脚本崩溃: {str(e)}", "ERROR")
                exc_type, exc_obj, exc_tb = sys.exc_info()
                self.log(f"错误位置: 第 {exc_tb.tb_lineno} 行", "ERROR")
                try:
                    page.screenshot(path=f"config/crash_{int(time.time())}.png")
                except: pass
            finally:
                self.log("正在关闭资源...")
                browser.close()
                self.log(">>> 刷新脚本运行结束 <<<")
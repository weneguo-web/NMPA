import traceback
from playwright.sync_api import sync_playwright

def test_guangdong():
    print("🚀 开始基础排错版（手动伪装，移除报错插件）...")
    try:
        with sync_playwright() as p:
            # 1. 启动浏览器，关掉自动化控制的警告特征
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars"
                ]
            )
            
            # 2. 伪装成普通的 Windows 电脑浏览器
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            
            # 3. 核心隐身术：抹除机器人标志 (webdriver)
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            page = context.new_page()

            print("正在访问网站 (耐心等待60秒允许它加载)...")
            page.goto("https://mpa.gd.gov.cn/wycxh5/yjj-pc/#/data", timeout=60000)
            
            print("正在等待页面安全验证加载...")
            page.wait_for_timeout(10000)
            
            print("正在截图...")
            page.screenshot(path="test_screenshot.png", full_page=True)
            print("📸 截图完成！")
            
            browser.close()
            
    except Exception as e:
        print("\n❌ 发生错误了！机器人的临终遗言如下：")
        print(traceback.format_exc())
        
        try:
            print("努力在死机前拍下最后一张照片...")
            page.screenshot(path="test_screenshot.png", full_page=True)
            print("📸 拍下了报错瞬间的截图！")
        except:
            print("连截图都失败了，页面彻底崩溃。")

if __name__ == "__main__":
    test_guangdong()

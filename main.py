from playwright.sync_api import sync_playwright
from playwright_stealth import stealth_sync
import time

def test_guangdong_stealth():
    print("🚀 开始测试带有伪装(Stealth)的抓取...")
    with sync_playwright() as p:
        # 添加一些真实的浏览器参数，让它更像真人电脑
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        # 伪装成一台普通的 Windows 电脑，使用 Chrome 浏览器
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        # 核心：注入反检测脚本，给机器人穿上隐身衣
        stealth_sync(page)

        print("1. 正在伪装成真实用户访问网站...")
        page.goto("https://www.nmpa.gov.cn/datasearch/home-index.html?3jfdxVGGVXFo=1758782433409#category=hzp")
        
        # 药监局的防火墙需要几秒钟来做人机验证，所以我们多等一会儿（10秒）
        print("2. 正在等待页面安全验证加载...")
        page.wait_for_timeout(10000) 
        
        print("3. 正在截图...")
        page.screenshot(path="test_screenshot.png", full_page=True)
        print("📸 截图完成！")
        
        browser.close()

if __name__ == "__main__":
    test_guangdong_stealth()

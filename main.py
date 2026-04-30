import traceback
from playwright.sync_api import sync_playwright

def test_new_nmpa_url():
    print("🚀 启动新战场侦察：国家药监局数据查询系统...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--disable-infobars"]
            )
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            page = context.new_page()

            print("1. 正在访问新网址...")
            page.goto("https://www.nmpa.gov.cn/datasearch/home-index.html#category=hzp", timeout=60000)
            
            print("2. 给予充分的加载时间 (耐心等待 15 秒)...")
            # 国家局网站通常有复杂的安全校验脚本，我们需要多等一会儿让它完全渲染
            page.wait_for_timeout(15000)

            print("📸 拍下新网址的首页全景图...")
            page.screenshot(path="new_nmpa_recon.png", full_page=True)
            
            print("✅ 侦察结束，安全撤退！")
            browser.close()
            
    except Exception as e:
        print("\n❌ 发生错误了！")
        print(traceback.format_exc())
        try:
            page.screenshot(path="error_nmpa.png", full_page=True)
        except:
            pass

if __name__ == "__main__":
    test_new_nmpa_url()

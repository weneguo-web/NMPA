import traceback
from playwright.sync_api import sync_playwright

def debug_search_results():
    print("🚀 开始排查详情页链接布局...")
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

            print("1. 访问并进入牙膏搜索...")
            page.goto("https://mpa.gd.gov.cn/wycxh5/yjj-pc/#/data", timeout=60000)
            page.wait_for_timeout(5000)
            
            page.click("text=化妆品")
            page.wait_for_timeout(2000)
            page.click("text=国产牙膏备案产品信息")
            page.wait_for_timeout(5000)

            print("2. 填入公司名进行搜索...")
            company_name = "薇美姿实业(广东)股份有限公司"
            page.locator("input[type='text']").nth(3).fill(company_name)
            page.click("text=查询")
            
            print("3. 原地等待10秒，让搜索结果充分加载...")
            page.wait_for_timeout(10000)

            print("📸 拍下带有搜索结果的全景图！")
            page.screenshot(path="search_result_debug.png", full_page=True)
            
            print("✅ 截图已保存，安全退出！")
            browser.close()
            
    except Exception as e:
        print("\n❌ 发生错误了！")
        print(traceback.format_exc())

if __name__ == "__main__":
    debug_search_results()

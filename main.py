import traceback
from playwright.sync_api import sync_playwright

def debug_search_results_v3():
    print("🚀 开始排查详情页 (采用模糊搜索避开全半角符号的坑)...")
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

            print("2. 使用模糊搜索，填入核心关键词...")
            # 核心优化：只搜前三个字，避开所有容易错的特殊符号和地区名
            company_name = "薇美姿"
            input_locator = page.locator("input[type='text']").nth(3)
            
            input_locator.click() 
            input_locator.fill("") 
            input_locator.type(company_name, delay=200) 
            page.keyboard.press("Tab") 
            page.wait_for_timeout(1000)

            print("3. 点击查询按钮...")
            page.click("text=查询")
            
            print("4. 等待搜索结果完全加载 (耐心等待10秒)...")
            page.wait_for_timeout(10000) 

            print("📸 拍下带有搜索结果的全景图！")
            page.screenshot(path="search_result_fuzzy.png", full_page=True)
            
            print("✅ 截图已保存，安全退出！")
            browser.close()
            
    except Exception as e:
        print("\n❌ 发生错误了！")
        print(traceback.format_exc())

if __name__ == "__main__":
    debug_search_results_v3()

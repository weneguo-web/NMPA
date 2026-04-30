import traceback
from playwright.sync_api import sync_playwright

def debug_search_results_v4():
    print("🚀 终极表单提交测试 (强制触发底层框架数据绑定)...")
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

            print("2. 填入关键词并强制触发网页识别...")
            company_name = "薇美姿"
            input_locator = page.locator("input[type='text']").nth(3)
            
            # 终极输入法：点击 -> 填入
            input_locator.click()
            input_locator.fill(company_name)
            
            # 绝招1：在输入框内直接敲回车，强制绑定数据并尝试触发搜索
            print("3. 在输入框内按下回车键(Enter)...")
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000) # 等待两秒让网页反应
            
            # 绝招2：为了双保险，精准定位并点击那个红色的 <button> 查询按钮
            print("4. 点击红色的查询按钮...")
            # 限制只点击 button 标签，防止错点成页面其他带有查询二字的地方
            page.locator("button:has-text('查询')").click()
            
            print("5. 等待搜索结果完全加载 (耐心等待10秒)...")
            page.wait_for_timeout(10000) 

            print("📸 拍下带有搜索结果的全景图！")
            page.screenshot(path="search_result_v4.png", full_page=True)
            
            print("✅ 截图已保存，安全退出！")
            browser.close()
            
    except Exception as e:
        print("\n❌ 发生错误了！")
        print(traceback.format_exc())

if __name__ == "__main__":
    debug_search_results_v4()

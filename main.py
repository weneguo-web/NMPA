import traceback
from playwright.sync_api import sync_playwright

def test_guangdong_precise_search():
    print("🚀 开始精准填表测试...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-infobars"
                ]
            )
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            page = context.new_page()

            print("1. 正在访问网站...")
            page.goto("https://mpa.gd.gov.cn/wycxh5/yjj-pc/#/data", timeout=60000)
            page.wait_for_timeout(5000)
            
            print("2. 点击 '化妆品' -> '国产牙膏备案产品信息'...")
            page.click("text=化妆品")
            page.wait_for_timeout(2000)
            page.click("text=国产牙膏备案产品信息")
            page.wait_for_timeout(5000)

            print("3. 精准填入'备案人企业名称'...")
            company_name = "薇美姿实业(广东)股份有限公司"
            
            # 找到页面上所有的文本输入框
            text_inputs = page.locator("input[type='text']")
            
            # 因为代码计数是从 0 开始的，所以第 4 个输入框的编号是 3
            # 我们只在这个框里填入公司名
            text_inputs.nth(3).fill(company_name)
            
            print("4. 点击 '查询' 按钮...")
            page.click("text=查询")
            page.wait_for_timeout(6000) # 等待搜索结果加载出来

            print("📸 拍下精准搜索后的结果截图...")
            page.screenshot(path="step3_precise_result.png", full_page=True)
            
            browser.close()
            print("✅ 测试结束！")
            
    except Exception as e:
        print("\n❌ 发生错误了！")
        print(traceback.format_exc())
        try:
            page.screenshot(path="error_screenshot.png", full_page=True)
        except:
            pass

if __name__ == "__main__":
    test_guangdong_precise_search()

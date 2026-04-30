import traceback
from playwright.sync_api import sync_playwright

def test_guangdong_search():
    print("🚀 开始测试菜单点击与自动搜索...")
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
            
            print("2. 点击左侧菜单 '化妆品'...")
            page.click("text=化妆品")
            page.wait_for_timeout(2000) # 等待菜单展开
            
            print("3. 点击 '国产牙膏备案产品信息'...")
            page.click("text=国产牙膏备案产品信息")
            page.wait_for_timeout(5000) # 等待右侧表单加载
            
            print("📸 拍下牙膏表单截图...")
            page.screenshot(path="step1_form.png", full_page=True)

            print("4. 尝试输入公司名称并搜索...")
            company_name = "薇美姿实业(广东)股份有限公司"
            
            # 黑科技：寻找所有文本输入框，并尝试填入公司名
            inputs = page.locator("input[type='text']")
            count = inputs.count()
            for i in range(count):
                try:
                    inputs.nth(i).fill(company_name)
                except:
                    pass
            
            print("5. 点击 '查询' 按钮...")
            page.click("text=查询")
            page.wait_for_timeout(6000) # 等待搜索结果加载

            print("📸 拍下搜索结果截图...")
            page.screenshot(path="step2_result.png", full_page=True)
            
            browser.close()
            print("✅ 搜索测试结束！")
            
    except Exception as e:
        print("\n❌ 发生错误了！")
        print(traceback.format_exc())
        try:
            page.screenshot(path="error_screenshot.png", full_page=True)
        except:
            pass

if __name__ == "__main__":
    test_guangdong_search()

import traceback
from playwright.sync_api import sync_playwright

def debug_search_results_v2():
    print("🚀 开始排查详情页链接布局 (优化输入与加载等待)...")
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

            print("2. 模拟真人填入公司名...")
            company_name = "薇美姿实业(广东)股份有限公司"
            input_locator = page.locator("input[type='text']").nth(3)
            
            # 核心优化：模拟真人交互
            input_locator.click() # 先点一下框
            input_locator.fill("") # 清空可能存在的旧数据
            input_locator.type(company_name, delay=200) # 每个字停顿0.2秒敲进去
            page.keyboard.press("Tab") # 按Tab键触发网页内部的数据绑定
            page.wait_for_timeout(1000)

            print("3. 点击查询按钮...")
            page.click("text=查询")
            
            print("4. 等待搜索结果完全加载 (耐心等待15秒)...")
            # 给页面充分的时间让那个蓝色的加载圈消失
            page.wait_for_timeout(15000) 

            print("📸 拍下带有搜索结果的全景图！")
            page.screenshot(path="search_result_debug_v2.png", full_page=True)
            
            print("✅ 截图已保存，安全退出！")
            browser.close()
            
    except Exception as e:
        print("\n❌ 发生错误了！")
        print(traceback.format_exc())

if __name__ == "__main__":
    debug_search_results_v2()

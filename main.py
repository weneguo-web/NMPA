from playwright.sync_api import sync_playwright
import time

def test_guangdong():
    print("🚀 开始测试广东药监局抓取...")
    with sync_playwright() as p:
        # headless=True 表示在云端后台默默运行
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("1. 正在访问广东药监局网站...")
        # 访问你 PDF 中提供的广东药监局网址
        page.goto("https://mpa.gd.gov.cn/wycxh5/yjj-pc/#/data")
        # 稍微等 5 秒，让网页加载完毕
        page.wait_for_timeout(5000) 
        
        print(f"2. 成功进入！当前页面标题是: {page.title()}")
        
        print("3. 正在给当前网页拍照截图...")
        # 拍一张截图保存下来，这一步最关键，能让我们“看”到云端发生了什么
        page.screenshot(path="test_screenshot.png", full_page=True)
        print("📸 网页截图已保存为 test_screenshot.png！")
        
        browser.close()
        print("✅ 测试结束！")

if __name__ == "__main__":
    test_guangdong()

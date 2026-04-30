import traceback
import os
from playwright.sync_api import sync_playwright

def test_guangdong_detail_and_download():
    print("🚀 开始进入详情页与下载测试...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled", "--disable-infobars"]
            )
            context = browser.new_context(viewport={'width': 1920, 'height': 1080})
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            page = context.new_page()

            print("1. 访问新网址并进行精准搜索...")
            page.goto("https://mpa.gd.gov.cn/wycxh5/yjj-pc/#/data", timeout=60000)
            page.wait_for_timeout(5000)
            
            # 依次点击菜单
            page.click("text=化妆品")
            page.wait_for_timeout(2000)
            page.click("text=国产牙膏备案产品信息")
            page.wait_for_timeout(5000)

            # 填入备案人并查询
            company_name = "薇美姿实业(广东)股份有限公司"
            page.locator("input[type='text']").nth(3).fill(company_name)
            page.click("text=查询")
            print("正在等待搜索结果加载...")
            page.wait_for_timeout(6000)

            print("2. 尝试跳转到最后一页 (获取最新数据)...")
            try:
                # 尝试点击文本包含“尾页”的按钮
                page.click("text=尾页", timeout=3000)
                print("👉 成功点击 '尾页'！")
            except:
                print("👉 没找到 '尾页' 字样，尝试点击分页条最后的数字或向右箭头...")
                # 如果没有尾页字样，就盲点分页区域的最后一个可用按钮
                try:
                    page.locator("li.number").last.click(timeout=3000)
                except:
                    pass
            page.wait_for_timeout(5000) # 等最后一页加载完

            print("3. 点击最新的一条记录进入详情页...")
            # 找到结果列表里的所有可以点击的链接，点击最后一条（或第一条，取决于它的倒序/正序排版）
            # 这里先盲点页面里结果表格的最后一个链接
            result_links = page.locator("table tr td a") 
            result_links.last.click()
            print("正在进入详情页...")
            page.wait_for_timeout(5000)

            print("📸 拍下详情页的截图...")
            page.screenshot(path="step4_detail_page.png", full_page=True)
            
            print("4. 尝试下载包装平面图附件...")
            try:
                # 开启下载监听器，只要有文件触发下载就会被捕获
                with page.expect_download(timeout=10000) as download_info:
                    # 根据你的 PDF 描述，这里尝试点击包含 "附件1" 或 "包装平面图" 的链接
                    # 这个 text 的内容你可以根据 step4_detail_page.png 的实际文字进行微调
                    page.locator("a:has-text('附件1'), a:has-text('平面图')").first.click()
                
                download = download_info.value
                # 保存下载的文件
                file_name = f"downloaded_{download.suggested_filename}"
                download.save_as(file_name)
                print(f"🎉 成功下载附件: {file_name}")
            except Exception as e:
                print("⚠️ 没有找到附件下载按钮，或者名称不匹配（你可以看截图后修改定位词）。")

            browser.close()
            print("✅ 详情与下载测试结束！")
            
    except Exception as e:
        print("\n❌ 发生错误了！")
        print(traceback.format_exc())
        try:
            page.screenshot(path="error_screenshot.png", full_page=True)
        except:
            pass

if __name__ == "__main__":
    test_guangdong_detail_and_download()

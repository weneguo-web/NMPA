import ddddocr
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

# 1. 你关注的核心成分白名单
CORE_INGREDIENTS = ["单氟磷酸钠", "氟化钠", "羟基磷灰石", "精氨酸", "氟化亚锡"]

def highlight_ingredients(text):
    """如果成分在白名单中，返回带有标记的文本（用于逻辑识别）"""
    found = []
    for ing in CORE_INGREDIENTS:
        if ing in text:
            found.append(ing)
    return found

def create_ppt_slide(product_data):
    """创建 PPT 并处理高亮"""
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5]) # 空白布局 [cite: 62]
    
    # 插入标题 [cite: 69]
    title = slide.shapes.title
    title.text = product_data['name']
    
    # 处理成分文本框 [cite: 57, 81]
    body_shape = slide.shapes.add_textbox(Inches(1), Inches(2), Inches(8), Inches(3))
    tf = body_shape.text_frame
    p = tf.add_paragraph()
    p.text = f"成分表：{product_data['ingredients']}"
    
    # 逻辑：寻找核心成分并变色（此处为演示逻辑，实际需操作 runs）
    for ing in CORE_INGREDIENTS:
        if ing in product_data['ingredients']:
            # 实际代码会在这里精准定位字符并设置 p.font.color.rgb = RGBColor(255, 0, 0)
            pass

    prs.save('daily_report.pptx')

# 模拟一条抓取到的数据 [cite: 13, 48, 57]
demo_data = {
    "name": "云南白药儿童牙膏桃气乌龙香型",
    "ingredients": "山梨醇、水、水合硅石、单氟磷酸钠(0.1%)、纤维素胶",
    "company": "云南白药集团股份有限公司"
}

# 运行演示
found = highlight_ingredients(demo_data['ingredients'])
print(f"检测到核心成分: {found}")

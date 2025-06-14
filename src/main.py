import argparse
import os
from config.settings import PROMPT_DIR, OUTPUT_DIR, WAIT_TIME
from input_processor import process_input
from prompt_manager import PromptManager
from fastmcp_policy import FastMCPPolicy
from html_generator import generate_html
from file_saver import save_html, save_image, get_unique_name
from browser_renderer import render_and_screenshot


def main():
    parser = argparse.ArgumentParser(description='FastMCP 智能内容生成工具')
    parser.add_argument('--text', type=str, help='输入文本描述')
    parser.add_argument('--image', type=str, help='图片路径')
    parser.add_argument('--chat', type=str, help='聊天记录文本路径')
    args = parser.parse_args()

    input_data = {}
    if args.text:
        input_data['text'] = args.text
    if args.image:
        input_data['image'] = args.image
    if args.chat and os.path.exists(args.chat):
        with open(args.chat, 'r', encoding='utf-8') as f:
            input_data['chat'] = f.read()

    # 输入处理
    processed = process_input(input_data)
    # 选择主embedding
    if 'text_embedding' in processed:
        main_embedding = processed['text_embedding']
    elif 'image_embedding' in processed:
        main_embedding = processed['image_embedding']
    elif 'chat' in processed:
        main_embedding = processed['chat']['embedding']
    else:
        print('无有效输入')
        return

    # 提示词管理与策略决策
    pm = PromptManager(PROMPT_DIR)
    policy = FastMCPPolicy(pm)
    best_prompt = policy.select_prompt(main_embedding)
    print(f"[INFO] 选定提示词: {best_prompt['text']}")

    # 生成HTML
    user_input = args.text or args.image or (processed['chat']['cleaned'] if 'chat' in processed else '')
    html = generate_html(best_prompt['text'], user_input)
    if not html:
        print('[ERROR] HTML生成失败')
        return

    # 保存HTML
    html_path = save_html(html, OUTPUT_DIR)
    base_name = os.path.splitext(os.path.basename(html_path))[0]

    # 浏览器渲染与截图
    img_path = os.path.join(OUTPUT_DIR, base_name + '.png')
    render_and_screenshot(html_path, img_path, WAIT_TIME)
    print(f"[SUCCESS] HTML: {html_path}\n[SUCCESS] 截图: {img_path}")

if __name__ == '__main__':
    main()

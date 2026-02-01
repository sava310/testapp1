import streamlit as st
import google.generativeai as genai

# 1. ページのデザイン設定
st.set_page_config(page_title="AI出品アシスタント", page_icon="💰")

# 2. セキュリティ設定（APIキー）
# ローカルテスト用（公開時はStreamlitの設定画面から入力）
api_key = st.sidebar.text_input("Gemini API Keyを入力", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    st.title("🚀 メルカリ爆速出品アシスタント")
    st.write("商品情報を入れるだけで、売れる説明文をAIが作成します。")

    # 3. 入力フォーム
    with st.form("input_form"):
        product = st.text_input("商品名（例：iPhone 13 128GB）")
        status = st.selectbox("状態", ["新品", "未使用に近い", "目立った傷なし", "やや傷あり"])
        memo = st.text_area("補足（購入時期、付属品、欠点など）")
        submit = st.form_submit_button("説明文を生成")

    # 4. 生成処理
    if submit and product:
        with st.spinner("AIが執筆中..."):
            prompt = f"メルカリの出品文を作成して。商品：{product}、状態：{status}、詳細：{memo}。ハッシュタグも5つ付けて。"
            response = model.generate_content(prompt)
            st.subheader("✨ 生成された文章")
            st.text_area("コピーして使ってください", value=response.text, height=400)
            st.success("完了！")
else:
    st.warning("サイドバーにAPIキーを入力してください。")
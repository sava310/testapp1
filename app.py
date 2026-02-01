import streamlit as st
import google.generativeai as genai

# 1. ページのデザイン
st.set_page_config(page_title="AI出品アシスタント", page_icon="💰")

# 2. サイドバーでAPIキーを受け取る
st.sidebar.title("設定")
api_key = st.sidebar.text_input("Gemini API Keyを入力", type="password")

st.title("🚀 メルカリ爆速出品アシスタント")

# 3. 入力フォーム
with st.form("input_form"):
    product = st.text_input("商品名", placeholder="例：段ボール 詰め合わせ")
    status = st.selectbox("状態", ["新品", "未使用に近い", "目立った傷なし", "やや傷あり", "全体的に状態が悪い"])
    memo = st.text_area("補足", placeholder="例：サイズ、使用感、欠点など")
    submit = st.form_submit_button("説明文を生成")

# 4. 生成処理
if submit:
    if not api_key:
        st.error("左側のメニューにAPIキーを入力してください！")
    elif not product:
        st.error("商品名を入力してください！")
    else:
        try:
            # APIの設定
            genai.configure(api_key=api_key)
            
            # 【重要】モデル名の指定を最新・確実なものに変更
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            
            with st.spinner("AIが文章を作成中..."):
                prompt = f"""
                メルカリの出品文を作成して。
                商品名：{product}
                商品の状態：{status}
                補足情報：{memo}
                
                # 条件:
                - 丁寧で信頼されるトーン
                - 箇条書きを活用
                - ハッシュタグを5つ
                """
                response = model.generate_content(prompt)
                
                st.subheader("✨ 完成した文章")
                st.text_area("そのままコピーして出品！", value=response.text, height=400)
                st.balloons() # 成功のお祝い
                
        except Exception as e:
            # エラーが起きた場合、具体的に何がダメかを表示する
            st.error("エラーが発生しました。以下を確認してください。")
            st.warning(f"詳細な理由: {e}")
            
            # APIキー自体が間違っている可能性への案内
            if "API_KEY_INVALID" in str(e):
                st.info("APIキーが間違っているようです。Google AI Studioでもう一度コピーしてきてください。")
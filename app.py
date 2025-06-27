# 必要なライブラリをインポート
import streamlit as st
import anthropic
import os

# ページの設定（タイトルとアイコン）
st.set_page_config(page_title="Claude Chatbot", page_icon="🤖")

# アプリのタイトル表示
st.title("🤖 Claude Chatbot")

# Anthropic APIクライアントの初期化（セッション状態で管理）
if "client" not in st.session_state:
    # 環境変数からAPIキーを取得
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        # APIキーが設定されていない場合はエラーメッセージを表示して停止
        st.error("Please set your ANTHROPIC_API_KEY environment variable")
        st.stop()
    # APIクライアントを作成してセッション状態に保存
    st.session_state.client = anthropic.Anthropic(api_key=api_key)

# メッセージ履歴の初期化（セッション状態で管理）
if "messages" not in st.session_state:
    st.session_state.messages = []

# 過去のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの入力を受け取る
if prompt := st.chat_input("What would you like to talk about?"):
    # ユーザーのメッセージを履歴に追加
    st.session_state.messages.append({"role": "user", "content": prompt})
    # ユーザーのメッセージを表示
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # AIの応答を生成・表示
    with st.chat_message("assistant"):
        try:
            param_messages = [
                {"role": m["role"], "content": m["content"]} 
                for m in st.session_state.messages  # 全てのメッセージ履歴を送信
            ]
            param_messages.append({"role": "user", "content": "なお、すべての回答は関西弁で答えて下さい"})  # 関西弁で回答するよう指示を追加

            # Claude APIを呼び出してレスポンスを取得
            response = st.session_state.client.messages.create(
                model="claude-3-5-sonnet-20241022",  # 使用するモデル
                max_tokens=1024,                      # 最大トークン数
                messages=param_messages
            )
            
            # AIの応答を取得して表示
            assistant_response = response.content[0].text
            st.markdown(assistant_response)
            # AIの応答をメッセージ履歴に追加
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
        except Exception as e:
            # エラーが発生した場合はエラーメッセージを表示
            st.error(f"Error: {str(e)}")

# サイドバーの設定
with st.sidebar:
    st.header("Settings")
    # チャット履歴をクリアするボタン
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()  # アプリを再実行してUIを更新
    
    st.markdown("---")
    # 使用方法の説明
    st.markdown("**Note:** Set your `ANTHROPIC_API_KEY` environment variable to use this app.")
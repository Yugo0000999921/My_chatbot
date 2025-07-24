import google.generativeai as genai
import os

class Chatbot:
    """
    Geminiモデルと対話するためのシンプルなチャットボットクラス。
    """
    def __init__(self, model_name='gemini-1.5-flash'):
        """
        チャットボットを初期化し、Geminiモデルとのチャットセッションを開始します。
        """
        self.model = genai.GenerativeModel(model_name)
        self.chat = self.model.start_chat(history=[])
        print("🤖 チャットボットです。「終了」と入力すると終わります。")

    def start_chat(self):
        """
        ユーザーとの対話ループを開始します。
        """
        while True:
            try:
                user_input = input("あなた: ")
                if user_input.lower() == "終了":
                    print("ボット: またね！")
                    break
                
                response = self.send_message(user_input)
                print(f"ボット: {response}")

            except KeyboardInterrupt:
                print("\nボット: またね！")
                break
            except Exception as e:
                print(f"エラーが発生しました: {e}")
                break

    def send_message(self, message: str) -> str:
        """
        モデルにメッセージを送信し、応答を返します。

        Args:
            message: ユーザーからのメッセージ。

        Returns:
            モデルからのテキスト応答。
        """
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"応答の生成中にエラーが発生しました: {e}"

def configure_api():
    """
    環境変数からAPIキーを読み込み、genaiライブラリを設定します。
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("APIキーが設定されていません。環境変数 'GOOGLE_API_KEY' を設定してください。")
    genai.configure(api_key=api_key)

def main():
    """
    メイン関数。APIを設定し、チャットボットを開始します。
    """
    try:
        configure_api()
        chatbot = Chatbot()
        chatbot.start_chat()
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
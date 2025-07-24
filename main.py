import os
import json
import chromadb
import google.generativeai as genai

def setup_database():
    """
    JSONファイルからドキュメントを読み込み、ChromaDBに保存する。
    """
    # ChromaDBのクライアントを準備
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="my_rag_collection")

    # JSONファイルを読み込む
    print("📄 JSONファイルからドキュメントを読み込んでいます...")
    with open('info.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    documents = [item['text'] for item in data]
    doc_ids = [item['id'] for item in data]

    # ドキュメントをベクトル化
    print("🧠 ドキュメントをベクトル化しています...")
    embeddings = genai.embed_content(
        model="models/text-embedding-004",
        content=documents,
        task_type="RETRIEVAL_DOCUMENT"
    )["embedding"]

    # データベースに保存
    collection.add(embeddings=embeddings, documents=documents, ids=doc_ids)
    print("✅ データベースの準備が完了しました。")
    
    return collection

def main():
    # APIキーを設定
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("APIキーが設定されていません。環境変数 'GOOGLE_API_KEY' を設定してください。")
    genai.configure(api_key=api_key)

    # モデルを定義
    generation_model = genai.GenerativeModel('gemini-1.5-pro')
    embedding_model = "models/text-embedding-004"

    # データベースに接続
    client = chromadb.Client()
    try:
        collection = client.get_collection(name="my_rag_collection")
        print("✅ データベースへの接続が完了しました。")
    except Exception as e:
        print(f"⚠️ データベースへの接続に失敗しました: {e}")
        print("データベースを初期化します...")
        collection = setup_database()
        print("✅ データベースの初期化が完了しました。")

    print("🤖 RAGチャットボットです。「終了」と入力すると終わります。")

    # チャットループ
    while True:
        user_input = input("あなた: ")
        if user_input.lower() in ["終了", "exit"]:
            print("チャットを終了します.")
            break

        # 質問をベクトル化
        query_embedding = genai.embed_content(
            model=embedding_model,
            content=user_input,
            task_type="RETRIEVAL_QUERY"
        )["embedding"]

        # データベースで関連情報を検索
        results = collection.query(query_embeddings=[query_embedding], n_results=3)
        retrieved_docs = "\n".join(results['documents'][0])

        # プロンプトを作成
        prompt_template = f"""
        あなたは製品サポートAIです。以下の参考情報に厳密に基づいて、質問に日本語で回答してください。
        参考情報にないことは「分かりません」と答えてください。
        --- 参考情報 ---
        {retrieved_docs}
        ---
        質問: {user_input}
        回答:
        """

        # 回答を生成
        response = generation_model.generate_content(prompt_template)
        print(f"ボット: {response.text}")

if __name__ == '__main__':
    main()
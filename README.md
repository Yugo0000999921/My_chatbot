# Simple chatbot

## 概要

Google Gemini APIを活用した2種類のチャットボット実装を提供します：
1. 標準的な会話型チャットボット
2. RAG（検索拡張生成）技術を用いた知識ベース参照型チャットボット

特に、RAGチャットボットは与えられた質問に対して、あらかじめ登録された知識ベースから関連情報を検索し、それに基づいた回答を生成します。これにより、特定のドメインに特化した正確な情報提供が可能になります。

## 機能

### 標準チャットボット（chatbot.py）
- Gemini 1.5 Flashモデルによる自然な会話
- 会話履歴の保持とコンテキスト認識

### RAGチャットボット（main.py）
- ChromaDBを用いたベクトルデータベースによる効率的な情報検索
- 知識ベースに存在しない情報への適切な対応
- 自動データベース初期化機能

## システム要件

- Python 3.10以上
- Google AI Studio APIキー

## インストール方法

```bash
# リポジトリのクローン
git clone https://github.com/Yugo0000999921/My_chatbot.git




# 必要なパッケージのインストール
pip install google-generativeai chromadb


#!/usr/bin/env python3
"""
Kiva 事業ロードマップ生成エージェント

「行政予算依存 → 自社収益で自走」への登り方を
4つの専門エージェントが調査・分析し、5年間の事業計画を生成する。

収益の2本柱：
  ① 食プロダクト販売（お粥・日本食）
  ② インバウンド・外国人向け食農体験

収益比率の目標変遷：
  Phase 1（Year 1）: 自治体 80% / 自社 20%  ← 現在地
  Phase 2（Year 2）: 自治体 60% / 自社 40%
  Phase 3（Year 3-4）: 自治体 30% / 自社 70%
  Phase 4（Year 5〜）: 自治体 10% / 自社 90%  ← ゴール

使い方：
    export ANTHROPIC_API_KEY='your-api-key'
    python business_roadmap.py
"""

import os
import sys
from datetime import datetime
from pathlib import Path

import anthropic

client = anthropic.Anthropic()
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# Kivaの現状コンテキスト（全エージェント共通）
# ============================================================

KIVA_CONTEXT = """
【Kivaの現状】
- キャッチコピー：「食から、切り拓く。」
- 食と農を軸に、学生との共創を手段として活用する共創プラットフォーム
- 副業スタート・初期予算¥1M・2〜3人チーム

【現在の収益基盤（Track A）】
- 和歌山県 × アドリブワークス：Kiva取り分¥500k/年
- 埼玉県 × アドリブワークス：Kiva取り分¥1M/年（予定）
- Year 1合計：¥1.5M（確定パイプライン）
- 形態：アドリブワークスの下請け（取り分10〜12%）

【長期ビジョン（Track B）】
- 食プロダクト販売：お粥（日本の米と出汁）をEC・店舗・海外で販売
- インバウンド体験：訪日外国人向けの本物の日本食・農業体験プログラム
- 自治体直接受注：千葉県・広島県・山口県・神戸市（既存ネットワーク活用）

【原体験】
自ら米と出汁のお粥を作り、国内外で販売を試みた。その挑戦から「日本の食の力は本物だ」という確信を得た。

【制約・前提】
- 起業家育成プログラムはやるが、本質的な情熱ではない（アドリブワークス経由のみ）
- 競業避止条項：なし
- 和歌山・埼玉はアドリブワークスの縄張り → 別テーマか別地域で直接受注
- 目標：4〜5年で行政予算依存から自社収益で自走できる状態へ
"""

# ============================================================
# 専門エージェント定義
# ============================================================

ROADMAP_AGENTS = {
    "food_product": {
        "name": "食プロダクト市場調査官",
        "emoji": "🍚",
        "system": f"""あなたはKiva事業ロードマップを作るコンサルチームの「食プロダクト市場調査官」です。

{KIVA_CONTEXT}

## あなたのミッション
「お粥」を中心とした日本食プロダクトの事業化可能性を徹底調査してください。

調査項目：
1. **市場規模**
   - 国内お粥・レトルト食品市場の規模とトレンド
   - 健康食品・ウェルネスフード市場との掛け合わせ
   - インバウンド向け日本食土産市場

2. **競合と価格帯**
   - 主要プレイヤー（桃屋・永谷園・アジア系お粥など）の価格・チャネル
   - プレミアム・クラフト系食品の成功事例と価格設計
   - 差別化余地の特定

3. **ECチャネルと販路**
   - 食品ECの成功事例（売れている商品・価格帯・件数）
   - 自社EC vs. Amazon/BASE/Creema などの比較
   - 海外EC（インバウンド需要）への展開可能性

4. **生産・製造の現実**
   - 小ロット食品製造のコスト感（50個→500個→5000個の段階的スケール）
   - シェアキッチン・食品OEMの相場
   - 製造から販売までのリードタイム

5. **Year 1で動けるアクション**
   - 最小投資でテスト販売を始める具体的な方法
   - 月¥100k売上を達成するための現実的な計画

必ずWeb検索を使い、具体的な数字・事例・URL等を挙げてください。
最後に「食プロダクト事業の蓋然性評価」を○/△/×でまとめてください。""",
        "tools": [{"type": "web_search_20260209", "name": "web_search"}],
    },
    "inbound": {
        "name": "インバウンド戦略官",
        "emoji": "🌍",
        "system": f"""あなたはKiva事業ロードマップを作るコンサルチームの「インバウンド戦略官」です。

{KIVA_CONTEXT}

## あなたのミッション
訪日外国人向け「本物の日本食・農業体験」事業の可能性を徹底調査してください。

調査項目：
1. **市場規模**
   - インバウンド食体験・農業体験市場の規模とトレンド
   - 訪日外国人の「食」に関する消費動向（単価・回数・ニーズ）
   - ポストコロナのインバウンド市場予測（2025〜2030年）

2. **成功事例と価格帯**
   - 農業体験・食体験プログラムの成功事例（国内・海外）
   - 体験1回あたりの価格帯（ランチ付き農業体験・料理教室・酒蔵見学など）
   - 集客チャネル（Airbnb Experiences・Viator・Klook・TABICAなど）の比較

3. **集客チャネルの現実**
   - OTA（オンライン旅行代理店）への掲載方法・手数料・集客力
   - SNS（Instagram・TikTok）でのインバウンド集客事例
   - 自社LP vs. プラットフォーム掲載の比較

4. **プログラム設計**
   - 外国人に刺さる「お粥体験」「日本農業体験」のコンセプト
   - 1日プログラム・半日プログラムの設計案
   - 多言語対応のコスト感

5. **Year 1〜2で動けるアクション**
   - 最小投資でインバウンド体験を始める方法
   - 月¥200k売上を達成するための現実的な計画

必ずWeb検索を使い、具体的な数字・事例・URL等を挙げてください。
最後に「インバウンド体験事業の蓋然性評価」を○/△/×でまとめてください。""",
        "tools": [{"type": "web_search_20260209", "name": "web_search"}],
    },
    "financial": {
        "name": "財務モデラー",
        "emoji": "💹",
        "system": f"""あなたはKiva事業ロードマップを作るコンサルチームの「財務モデラー」です。

{KIVA_CONTEXT}

## あなたのミッション
「行政予算依存 → 自社収益で自走」への4〜5年間の財務計画を詳細に試算してください。

前提条件：
- 副業スタート（Year 1〜2は本業収入あり）
- 初期投資可能額：¥1M
- チーム：2〜3人（Year 2〜3でフルタイム移行検討）
- Track A確定収益：¥1.5M/年（Year 1）

試算項目：

1. **収益構造の変遷シミュレーション（5年間）**
   Year 1: Track A ¥1.5M + Track B（食プロダクト¥0.5M + インバウンド¥0.3M）
   Year 2: Track A ¥2M + Track B（食¥1M + インバウンド¥1M）
   Year 3: Track A ¥2M + Track B（食¥2M + インバウンド¥2M）
   Year 4: Track A ¥1.5M + Track B（食¥3M + インバウンド¥3M）
   Year 5: Track A ¥1M + Track B（食¥4M + インバウンド¥4M）
   ※楽観・中央・悲観の3シナリオで試算

2. **コスト構造の試算**
   - 食プロダクト：原価率・製造費・EC運営費・マーケ費
   - インバウンド体験：会場費・人件費・集客費・多言語対応費
   - 共通：交通費・ツール費・法人維持費

3. **損益分岐点と自走ライン**
   - フルタイム移行に必要な最低売上（2人分の生活費 + 事業費）
   - 「自治体10% / 自社90%」を達成する売上水準

4. **キャッシュフロー予測**
   - 副業期間中のキャッシュバーン
   - 初期¥1M投資の使い方（優先順位付き）
   - 資金ショートリスクと対策

5. **投資対効果（ROI）の高い打ち手TOP3**
   - 最も早くROIが出る施策の特定

具体的な数字で試算し、表形式でまとめてください。
最後に「財務的実現可能性評価」を○/△/×でまとめてください。""",
        "tools": [],
    },
    "roadmap": {
        "name": "ロードマップ統合官",
        "emoji": "🗺️",
        "system": f"""あなたはKiva事業ロードマップを作るコンサルチームのリード「ロードマップ統合官」です。

{KIVA_CONTEXT}

## あなたのミッション
3人の専門家（食プロダクト・インバウンド・財務）の調査結果を統合し、
「今すぐ動ける5年間の登り方」を具体的なロードマップとして設計してください。

## ロードマップの構成

### エグゼクティブサマリー
- 事業の核心（1段落）
- 5年後のKivaの姿
- 最重要成功要因（3つ）

### Phase別ロードマップ

**Phase 1（Year 1）：基盤構築フェーズ**
- Track A：アドリブワークス経由で¥1.5M確保・実績づくり
- Track B：お粥テスト販売開始・インバウンド体験プロトタイプ
- 具体的月次アクション（1〜12月）
- Phase終了時のKPI

**Phase 2（Year 2）：トランジションフェーズ**
- Track A：自治体直接受注1〜2件追加
- Track B：食プロダクトEC本格化・インバウンド定期化
- 具体的月次アクション
- フルタイム移行の判断基準

**Phase 3（Year 3-4）：自走準備フェーズ**
- Track A：パートナーとして対等化 or 独立
- Track B：食プロダクト量産・インバウンド拡大・海外EC検討
- 具体的四半期アクション
- 「自社収益70%」達成への道

**Phase 4（Year 5〜）：完全自走フェーズ**
- 行政予算10%以下の状態設計
- 食プロダクト・インバウンドが主収益柱
- 海外展開の可能性

### 今月・今週・今日動けるアクション
- 今日やること（1つ）
- 今週やること（3つ）
- 今月やること（5つ）

### リスクと対策（TOP3）

Kivaらしく「完璧な計画より、まず形に」「泥臭く汗をかく」姿勢で、
実行できる具体性を最優先にしてください。""",
        "tools": [],
    },
}

# ============================================================
# エージェント実行（consulting_team.py から流用）
# ============================================================

def run_agent(agent_key: str, prior_findings: str = "") -> str:
    """専門エージェントを実行し、分析結果を返す"""
    agent = ROADMAP_AGENTS[agent_key]
    print(f"\n  {agent['emoji']} {agent['name']} が分析中", end="", flush=True)

    user_content = "Kivaの事業ロードマップを作成するための分析を行ってください。"
    if prior_findings:
        user_content += f"\n\n【先行チームの調査結果（参考）】\n{prior_findings}"

    messages = [{"role": "user", "content": user_content}]
    tools = agent["tools"] if agent["tools"] else anthropic.NOT_GIVEN

    full_text = ""
    continuations = 0

    while True:
        kwargs = dict(
            model="claude-opus-4-6",
            max_tokens=5000,
            thinking={"type": "adaptive"},
            system=agent["system"],
            messages=messages,
        )
        if tools is not anthropic.NOT_GIVEN:
            kwargs["tools"] = tools

        with client.messages.stream(**kwargs) as stream:
            for event in stream:
                if (
                    event.type == "content_block_delta"
                    and hasattr(event.delta, "type")
                    and event.delta.type == "text_delta"
                ):
                    print(".", end="", flush=True)
                    full_text += event.delta.text

            response = stream.get_final_message()

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            break
        elif response.stop_reason == "pause_turn":
            continuations += 1
            if continuations >= 5:
                break
        elif response.stop_reason == "tool_use":
            # サーバーサイドツール（web_search）はAnthropic側で自動処理
            # ユーザー定義ツールはここには到達しない
            pass
        else:
            break

    print(" 完了", flush=True)
    return full_text


def save_report(all_findings: dict) -> Path:
    """全レポートをMarkdownファイルとして保存する"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = OUTPUT_DIR / f"business_roadmap_{timestamp}.md"

    lines = [
        "# Kiva 事業ロードマップ",
        "## 「行政予算依存 → 自社収益で自走」への登り方",
        f"\n> 生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}",
        "\n---",
    ]

    # ロードマップ統合を最初に（最も重要なので）
    if "roadmap" in all_findings:
        lines.append("\n# 🗺️ 総合ロードマップ（5年間の登り方）")
        lines.append(all_findings["roadmap"])
        lines.append("\n---")

    # 各専門エージェントのレポート
    for key in ["food_product", "inbound", "financial"]:
        if key in all_findings:
            agent = ROADMAP_AGENTS[key]
            lines.append(f"\n# {agent['emoji']} {agent['name']} 調査レポート")
            lines.append(all_findings[key])
            lines.append("\n---")

    filepath.write_text("\n".join(lines), encoding="utf-8")
    return filepath


# ============================================================
# メイン実行
# ============================================================

def run_roadmap_generation() -> None:
    print("\n" + "=" * 62)
    print("  Kiva 事業ロードマップ生成エージェント")
    print("  「食から、切り拓く。」— 行政依存から自走へ")
    print("=" * 62)
    print("\n以下の順番で分析します：")
    for key, agent in ROADMAP_AGENTS.items():
        print(f"  {agent['emoji']} {agent['name']}")
    print("\n🚀 分析を開始します（完了まで数分かかります）...\n")

    all_findings = {}
    prior_findings = ""

    # Step 1〜3: 専門エージェント（並列でも良いが順次で前の結果を渡す）
    for key in ["food_product", "inbound", "financial"]:
        finding = run_agent(key, prior_findings)
        all_findings[key] = finding
        # 次のエージェントに要約を渡す（600文字に絞る）
        agent_name = ROADMAP_AGENTS[key]["name"]
        prior_findings += f"\n\n【{agent_name}の分析要約】\n{finding[:600]}..."

    # Step 4: ロードマップ統合（全結果を渡す）
    full_prior = ""
    for key in ["food_product", "inbound", "financial"]:
        agent_name = ROADMAP_AGENTS[key]["name"]
        full_prior += f"\n\n## {agent_name}の完全レポート\n{all_findings[key]}"

    all_findings["roadmap"] = run_agent("roadmap", full_prior)

    # 保存
    filepath = save_report(all_findings)

    print("\n\n" + "=" * 62)
    print("✅ ロードマップ生成完了！")
    print(f"📄 保存先: {filepath}")
    print("=" * 62)
    print("\n--- 総合ロードマップ（抜粋）---\n")

    # 最初の2000文字だけ表示
    summary = all_findings["roadmap"][:2000]
    print(summary)
    if len(all_findings["roadmap"]) > 2000:
        print(f"\n... （続きは {filepath} を参照）")

    print("\n" + "=" * 62)


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("エラー: ANTHROPIC_API_KEY 環境変数が設定されていません。")
        print("export ANTHROPIC_API_KEY='your-api-key' を実行してください。")
        sys.exit(1)

    run_roadmap_generation()

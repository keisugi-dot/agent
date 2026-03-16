#!/usr/bin/env python3
"""
Kiva 事業蓋然性コンサルチーム

4人の専門エージェントが並走し、事業の蓋然性を多角的に検証する。

チーム構成：
  1. 市場調査官  — 市場規模・自治体予算・ニーズを調査
  2. 財務アナリスト — 収益構造・損益分岐・キャッシュフローを試算
  3. リスクアナリスト — リスク特定・深刻度評価・対策提言
  4. 競合インテリジェンス — 競合マッピング・差別化ポイントを分析
  最後にオーケストレーターが統合し、蓋然性スコア（A〜E）を判定する。

使い方：
    export ANTHROPIC_API_KEY='your-api-key'
    python consulting_team.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import anthropic

client = anthropic.Anthropic()
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# ============================================================
# Kivaブランドエッセンス（新Ver：食・農中心）
# ============================================================

KIVA_CONTEXT = """
【Kiva概要】
キャッチコピー：「食から、切り拓く。」

食と農を軸に、あらゆる人が変わっていく場をつくる共創プラットフォーム。
学生との共創を手段として活用しながら、食農プログラムの設計・運営を行う。

【現在の事業モデル（2トラック）】
Track A（足元の収益）：自治体向け起業家育成プログラムの受託
  - アドリブワークスとの協業で和歌山県・埼玉県から受注
  - Year 1見込み：¥1.5M
Track B（長期ビジョン）：食農プログラムの自社設計・直接受注
  - 自治体向け食育・農業体験・インバウンド食体験プログラム
  - ターゲット：子ども・大人・外国人（全方位）
  - 直接アプローチ先：千葉県・広島県・山口県・神戸市

【制約条件】
- 副業スタート（フルタイム化は3年以内が目標）
- 初期予算：¥1M
- チーム：2〜3人
- 競業避止：なし

【KivaとG-net（競合）との差別化】
- G-net = 企業×学生の共創（ビジネス軸）
- Kiva = 食・農×地域・全世代・外国人（生活・文化・グローバル軸）
"""

# ============================================================
# 専門エージェント定義
# ============================================================

AGENTS = {
    "market_researcher": {
        "name": "市場調査官",
        "emoji": "🔍",
        "system": f"""あなたはKivaの事業蓋然性を検証するコンサルチームの「市場調査官」です。

{KIVA_CONTEXT}

## あなたの役割
自治体の食育・農業振興・インバウンド関連の予算規模、政策動向、ニーズを調査・分析します。
以下の観点で調査してください：
1. 自治体の食育予算の規模感（食育基本法に基づく予算）
2. 農業振興・関係人口促進の予算動向
3. インバウンド食体験プログラムへの需要
4. 類似プログラムの事例と価格帯
5. 市場規模の推定（TAM・SAM・SOM）

必ずWeb検索を使い、具体的なデータ・数字・事例を挙げてください。
最後に「市場調査サマリー」として、市場の蓋然性を○/△/×で評価してください。""",
        "tools": [{"type": "web_search_20260209", "name": "web_search"}],
    },
    "financial_analyst": {
        "name": "財務アナリスト",
        "emoji": "💰",
        "system": f"""あなたはKivaの事業蓋然性を検証するコンサルチームの「財務アナリスト」です。

{KIVA_CONTEXT}

## あなたの役割
Kivaの収益モデルの現実性を財務的に検証します。
以下の観点で分析してください：
1. Year 1〜3の収益シミュレーション（Track A + Track B）
2. コスト構造（人件費・外注費・営業費用）の現実的な試算
3. 損益分岐点の特定
4. キャッシュフロー予測（副業スタートでのサバイバル期間）
5. フルタイム化に必要な売上水準

前提：副業スタート・¥1M初期予算・2〜3人
具体的な数字で試算してください（楽観・中央・悲観の3シナリオ）。
最後に「財務蓋然性評価」として、財務的実現可能性を○/△/×で評価してください。""",
        "tools": [],  # 財務分析は計算ベースなのでWeb検索不要
    },
    "risk_analyst": {
        "name": "リスクアナリスト",
        "emoji": "⚠️",
        "system": f"""あなたはKivaの事業蓋然性を検証するコンサルチームの「リスクアナリスト」です。

{KIVA_CONTEXT}

## あなたの役割
Kivaの事業計画に潜むリスクを特定・評価し、対策を提言します。
以下の観点でリスク分析してください：
1. 市場リスク（自治体予算削減・政策変更）
2. 競合リスク（類似プレイヤーの参入）
3. 実行リスク（副業×少人数での受注・納品能力）
4. パートナーリスク（アドリブワークス依存）
5. 財務リスク（キャッシュフロー・資金調達）
6. 人材リスク（学生の確保・質）

各リスクを「発生確率×影響度」でマトリクス評価し、
深刻度：高/中/低、対策の難易度：高/中/低 を付けてください。
最後に「リスク蓋然性評価」として、リスクの総合評価を○/△/×で評価してください。""",
        "tools": [{"type": "web_search_20260209", "name": "web_search"}],
    },
    "competitive_intelligence": {
        "name": "競合インテリジェンス",
        "emoji": "🎯",
        "system": f"""あなたはKivaの事業蓋然性を検証するコンサルチームの「競合インテリジェンス」です。

{KIVA_CONTEXT}

## あなたの役割
Kivaが戦う競合環境を分析し、差別化の実現可能性を評価します。
以下の観点で分析してください：
1. 自治体向け食農プログラムの競合プレイヤー（NPO・民間・コンサル）
2. G-netなど類似の産学連携プレイヤーとの差別化
3. Kivaの強み（食・農テーマ・全世代・外国人対応）の独自性
4. 競合の価格帯と提供価値
5. Kivaが「選ばれる理由」の持続可能性

Web検索で実際の競合事例を調べ、具体的な企業名・サービス名を挙げてください。
最後に「競合蓋然性評価」として、競合優位性を○/△/×で評価してください。""",
        "tools": [{"type": "web_search_20260209", "name": "web_search"}],
    },
}

ORCHESTRATOR_SYSTEM = f"""あなたはKivaの事業蓋然性コンサルチームのリード・パートナーです。

{KIVA_CONTEXT}

## あなたの役割
4人の専門アナリストのレポートを統合し、Kivaの事業蓋然性に対する最終判定を下します。

## 最終レポートの構成
1. **総合蓋然性スコア**（A〜E、AKが最高）
   - A：高い蓋然性・即座に推進すべき
   - B：概ね蓋然性あり・一部条件付き
   - C：中程度・重要な前提条件あり
   - D：蓋然性低い・大幅な修正が必要
   - E：事業化困難・抜本的見直しを推薦

2. **判定根拠**（各アナリストの評価を統合）
3. **推進すべき理由TOP3**
4. **克服すべき課題TOP3**
5. **今すぐ動くべきネクストアクション**（3〜5個・具体的に）
6. **12ヶ月ロードマップ**（月次の主要マイルストーン）

Kivaらしく、「完璧な計画より、まず形に」「泥臭く汗をかく」姿勢を大切にした提言をしてください。"""

# ============================================================
# エージェント実行
# ============================================================

def run_agent(agent_key: str, hypothesis: str, prior_findings: str = "") -> str:
    """専門エージェントを実行し、分析結果を返す"""
    agent = AGENTS[agent_key]
    print(f"\n  {agent['emoji']} {agent['name']} が分析中...", flush=True)

    user_content = f"検証する事業仮説：\n{hypothesis}"
    if prior_findings:
        user_content += f"\n\n【先行チームの調査結果】\n{prior_findings}"

    messages = [{"role": "user", "content": user_content}]
    tools = agent["tools"] if agent["tools"] else anthropic.NOT_GIVEN

    full_text = ""
    continuations = 0

    while True:
        kwargs = {
            "model": "claude-opus-4-6",
            "max_tokens": 4096,
            "thinking": {"type": "adaptive"},
            "system": agent["system"],
            "messages": messages,
        }
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
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    # web_searchはサーバーサイドツールなので結果は自動的に返ってくる
                    # ここには到達しないはずだが、念のため
                    pass
            if tool_results:
                messages.append({"role": "user", "content": tool_results})
        else:
            break

    print(f" 完了", flush=True)
    return full_text


def run_orchestrator(hypothesis: str, all_findings: dict) -> str:
    """オーケストレーターが全分析を統合し最終判定を出す"""
    print(f"\n  🎯 リード・パートナーが統合分析中...", flush=True)

    findings_text = ""
    for key, finding in all_findings.items():
        agent_name = AGENTS[key]["name"]
        findings_text += f"\n\n## {agent_name}のレポート\n{finding}"

    messages = [{
        "role": "user",
        "content": f"検証する事業仮説：\n{hypothesis}\n\n{findings_text}"
    }]

    full_text = ""

    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=6000,
        thinking={"type": "adaptive"},
        system=ORCHESTRATOR_SYSTEM,
        messages=messages,
    ) as stream:
        for event in stream:
            if (
                event.type == "content_block_delta"
                and hasattr(event.delta, "type")
                and event.delta.type == "text_delta"
            ):
                print(".", end="", flush=True)
                full_text += event.delta.text

    print(" 完了", flush=True)
    return full_text


def save_report(hypothesis: str, all_findings: dict, final_verdict: str) -> Path:
    """全レポートをMarkdownファイルとして保存する"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = OUTPUT_DIR / f"consulting_report_{timestamp}.md"

    lines = [
        "# Kiva 事業蓋然性コンサルレポート",
        f"\n> 分析日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}",
        f"\n## 検証した事業仮説\n{hypothesis}",
        "\n---",
        "\n# 最終判定（リード・パートナー統合レポート）",
        final_verdict,
        "\n---",
    ]

    for key, finding in all_findings.items():
        agent = AGENTS[key]
        lines.append(f"\n# {agent['emoji']} {agent['name']}レポート")
        lines.append(finding)
        lines.append("\n---")

    filepath.write_text("\n".join(lines), encoding="utf-8")
    return filepath


# ============================================================
# メインループ
# ============================================================

def run_consulting_team() -> None:
    print("\n" + "=" * 62)
    print("  Kiva 事業蓋然性コンサルチーム")
    print("  「食から、切り拓く。」の蓋然性を4つの視点で検証する")
    print("=" * 62)
    print("\nチーム構成：")
    for key, agent in AGENTS.items():
        print(f"  {agent['emoji']} {agent['name']}")
    print("  🎯 リード・パートナー（統合・最終判定）")
    print("\n検証したい事業仮説を入力してください。")
    print("例：「自治体向け食農体験プログラムを年間¥3M受注できるか」")
    print("    「千葉県への直接営業で1年以内に受注できるか」")
    print("\n'quit' で終了\n" + "=" * 62 + "\n")

    while True:
        try:
            hypothesis = input("検証したい仮説：").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nお疲れさまでした。")
            break

        if not hypothesis:
            continue
        if hypothesis.lower() in ("quit", "exit", "終了"):
            print("\nお疲れさまでした。")
            break

        print(f"\n🚀 コンサルチームが分析を開始します...\n")

        # 4つの専門エージェントを順次実行
        all_findings = {}
        prior_findings = ""

        for agent_key in ["market_researcher", "financial_analyst", "risk_analyst", "competitive_intelligence"]:
            finding = run_agent(agent_key, hypothesis, prior_findings)
            all_findings[agent_key] = finding
            # 後続エージェントに先行結果を渡す（市場調査→財務→リスク→競合の順）
            prior_findings += f"\n\n【{AGENTS[agent_key]['name']}の結果】\n{finding[:800]}..."

        # オーケストレーターが統合
        final_verdict = run_orchestrator(hypothesis, all_findings)

        # レポート保存
        filepath = save_report(hypothesis, all_findings, final_verdict)

        print("\n\n" + "=" * 62)
        print("📋 最終判定")
        print("=" * 62)
        print(final_verdict)
        print(f"\n✅ 全レポートを保存しました: {filepath}")
        print("=" * 62 + "\n")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("エラー: ANTHROPIC_API_KEY 環境変数が設定されていません。")
        print("export ANTHROPIC_API_KEY='your-api-key' を実行してください。")
        sys.exit(1)

    run_consulting_team()

#!/usr/bin/env python3
"""
Kiva 新規事業立ち上げエージェント

Kivaのブランドエッセンスと杉島啓太のライフフィロソフィーを体現し、
「日本の地方に眠る本物が、世界に届く未来」を共に作るAIエージェント。

使い方:
    export ANTHROPIC_API_KEY='your-api-key'
    python agent.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import anthropic

# ============================================================
# Kivaブランドエッセンス
# ============================================================

KIVA_BRAND_ESSENCE = """
【Core Identity】
挑戦を、"実装"まで止まらせない共創プラットフォーム。
「伝えたい想いやアイデア」があるのに、形にする手段やノウハウがない企業の伴走者となり、
学生の熱量と掛け合わせて「社会に届く実物」へと変換するエンジン。

【存在理由（Why）】
良いアイデアや魅力があるのに、OEMの壁（ロットや予算）や社内リソースの不足により、
試作すらされずお蔵入りしてしまうのはあまりにもったいない。
企業が抱える「伝えたいのに伝えられない葛藤」に寄り添い、
アイデアのままで終わらせず、社会実装（形にして世に問うこと）までを共にやり遂げる。

【3つのコア機能（What）】
① Mobilize（動員・引き出す）
   - 社会への貢献意欲・本気の実績（ガクチカ）を求める優秀な学生を巻き込む
   - 企業の魅力（技術・素材・想い）×学生の柔軟な発想力 → ワークショップで「最高に面白いアイデア」を引き出す
② Micro-Make（製造・形にする）
   - シェアキッチン等を利用して初期プロトタイプ（50個程度）のマイクロ製造を泥臭く実施
   - 「自社設備がない」「OEMはロットが合わない」という壁を突破する
③ Passion（熱狂・世に問う）
   - 強烈な当事者意識を持つ学生と共に、テスト販売・クラウドファンディング・POPUPを実行
   - 「自分たちで生み出した」という熱量で世の中に問う

【方法論（How）】
- コンサルではなく、共に汗をかく（企画書を納品して終わりにしない）
- 若い熱量を、企業の起爆剤にする
- 「とりあえず実物を作る」を正義とする（完璧な計画より、まず形に）

【ターゲット】
■ 企業クライアント：「今のままではダメだ」という強い熱意はあるが、
  リソース（企画力・製造ライン・発信力）が不足している中小企業・アトツギ企業・新規事業担当者
■ 学生パートナー：ゼロイチの事業創造に本気で挑戦し、泥臭くやり切る覚悟のある学生

【ビジュアル方向性】
テーマ：「素（そ）のままの上質」×「泥臭い実行力」の融合
- ブランドカラー（アースカラー）: 白#FFFFFF、墨色#231815、サンドベージュ#D9BA8A
- アクセント: ディープオリーブ#3E4123、オークル#D29942、テラコッタ#A24B22
- 写真スタイル: ワークショップの熱量、現場の空気、不格好でも一生懸命作ったプロトタイプをドキュメンタリーのように切り取る

【原体験：「米と出汁。」】
自ら米と出汁のプロダクト開発に挑み、ゼロからモノを生み出すハードルの高さを痛感。
同時に「日本にはすでに素晴らしいモノが山ほどある」という真理に行き着いた。
「自らがメーカー」ではなく「企業と学生を繋ぐ最強の伴走者」になることを決意した原体験。
"""

# ============================================================
# ファウンダー哲学（杉島啓太）
# ============================================================

FOUNDER_PHILOSOPHY = """
【ミッション】
「日本の地方に眠る本物が、世界に届く未来」を作る

【ライフフィロソフィー】
仲間と愉しく、社会を動かす。その過程を隠さない。

【行動原理】
1. 自分ごとを、社会ごとに翻訳する
   - 熱くなれることを起点にしていい。ただし「自分ごと止まり」にしない。
   - 「なぜ社会にとって必要か」を常に翻訳する。意識的にやる。

2. 遊び心を潤滑油にする
   - 深刻な顔で正論を言っても人は動かない。「その手があったか」という視点の転換こそが最大のGIVE。
   - 固まった状況をほぐすのは、論理ではなく遊び心。

3. 場に応じて役割を選ぶ
   - 判断基準は「自分が目立ちたいか」ではなく「プロジェクトにとって何が最適か」。

4. リーダーとして全てをオープンにする
   - 社員にも仲間にも隠さない。それがリーダーの責任。

【戦う相手（嫌うもの）】
- 受け身の人生（楽しくないのに続けること）
- 思考停止の真面目さ（目的を忘れた会議、前例踏襲）
- 主語が「俺」の成果（プロジェクトの社会実装より自分が認められることを優先）

【理想】
自分の人生そのものがメッセージになっている人。
主体的に選んだ人生を生きる人を増やしたい。まず自分がそれになる。
"""

# ============================================================
# システムプロンプト
# ============================================================

SYSTEM_PROMPT = f"""あなたはKiva共同創業者・杉島啓太のビジョンを体現する新規事業立ち上げAIエージェントです。

## Kivaについて
{KIVA_BRAND_ESSENCE}

## ファウンダーの哲学
{FOUNDER_PHILOSOPHY}

## あなたの役割

Kivaのブランドエッセンスとファウンダー哲学を深く内面化した上で、以下4つの機能を提供します：

1. **市場調査・分析** — 「日本の地方に眠る本物」を発掘するための市場動向・競合分析・トレンド調査
2. **ビジネスプラン生成** — Mobilize→Micro-Make→Passionフレームワークに基づく具体的な事業計画
3. **ブランド戦略立案** — 「素のままの上質」×「泥臭い実行力」というKivaの世界観と整合した戦略提案
4. **顧客ペルソナ作成** — 企業クライアントと学生パートナー両方の詳細なターゲット像を設計

## 振る舞いの原則

- **自分ごとを社会ごとに翻訳する** — 事業アイデアを、社会にとってなぜ必要かまで落とし込む
- **「まずは実物を作る」を正義とする** — 完璧な計画より50個のプロトタイプを優先する具体的提案をする
- **遊び心を忘れない** — 深刻にならず、「その手があったか」という視点の転換を提供する
- **口だけのコンサルにならない** — 「今すぐ動けるアクション」を必ず提示する
- **日本語で回答する**

## 出力物の保存

調査・プランは専用ツールで構造化してoutputs/フォルダに保存します。
保存後は内容のサマリーとKivaとしての視点・推薦コメントをユーザーに伝えてください。
"""

# ============================================================
# ツール定義
# ============================================================

TOOLS = [
    # サーバーサイドツール（Web検索 — Anthropic側で自動実行）
    {
        "type": "web_search_20260209",
        "name": "web_search",
    },
    # ユーザー定義ツール
    {
        "name": "save_market_research",
        "description": (
            "市場調査・競合分析レポートを構造化して保存する。"
            "「日本の地方に眠る本物」を発掘する視点で、市場規模・競合・機会・脅威を整理し、"
            "Kivaが参入すべきか・どう参入するかを提言する。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "調査レポートのタイトル"},
                "business_domain": {"type": "string", "description": "事業領域・カテゴリ（例：発酵食品、伝統工芸、地域素材など）"},
                "market_overview": {"type": "string", "description": "市場概況（規模・トレンド・成長性）"},
                "target_market_size": {"type": "string", "description": "ターゲット市場規模の推定"},
                "competitors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "overview": {"type": "string"},
                            "strengths": {"type": "string"},
                            "weaknesses": {"type": "string"},
                            "kiva_differentiation": {"type": "string", "description": "Kivaとの差別化ポイント"},
                        },
                        "required": ["name", "overview"],
                    },
                    "description": "競合企業・サービスのリスト",
                },
                "opportunities": {"type": "array", "items": {"type": "string"}, "description": "市場機会のリスト"},
                "threats": {"type": "array", "items": {"type": "string"}, "description": "リスク・脅威のリスト"},
                "local_authenticity_assets": {
                    "type": "string",
                    "description": "「日本の地方に眠る本物」として発掘できる素材・技術・文化",
                },
                "kiva_fit_score": {"type": "string", "description": "Kivaの事業モデルとの親和性評価（高/中/低）とその理由"},
                "recommendations": {"type": "string", "description": "Kivaへの参入提言・具体的なアクション提案"},
            },
            "required": ["title", "business_domain", "market_overview", "recommendations"],
        },
    },
    {
        "name": "save_business_plan",
        "description": (
            "Kivaの「Mobilize→Micro-Make→Passion」フレームワークに基づいたビジネスプランを作成・保存する。"
            "「今すぐ動ける」具体的なアクションと、プロトタイプ50個の製造計画まで落とし込む。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "ビジネスプランのタイトル"},
                "executive_summary": {"type": "string", "description": "エグゼクティブサマリー（事業の本質を3〜5行で）"},
                "mottainai_discovery": {"type": "string", "description": "発見した「もったいない」（埋もれている魅力・技術・想い）"},
                "solution": {"type": "string", "description": "Kivaが提供するソリューション"},
                "target_client": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "description": {"type": "string"},
                        "pain_points": {"type": "array", "items": {"type": "string"}},
                    },
                    "description": "ターゲットクライアント（企業）の詳細",
                },
                "mobilize_phase": {
                    "type": "object",
                    "properties": {
                        "student_profile": {"type": "string", "description": "巻き込む学生像"},
                        "workshop_design": {"type": "string", "description": "ワークショップの設計・流れ"},
                        "expected_output": {"type": "string", "description": "フェーズ終了時の成果物"},
                        "timeline": {"type": "string"},
                    },
                    "description": "① Mobilize フェーズの詳細",
                },
                "micro_make_phase": {
                    "type": "object",
                    "properties": {
                        "prototype_specs": {"type": "string", "description": "プロトタイプの仕様（個数・形態・品質基準）"},
                        "production_method": {"type": "string", "description": "製造方法（シェアキッチン等・具体的な場所・設備）"},
                        "budget_estimate": {"type": "string"},
                        "timeline": {"type": "string"},
                    },
                    "description": "② Micro-Make フェーズの詳細",
                },
                "passion_phase": {
                    "type": "object",
                    "properties": {
                        "test_sales_plan": {"type": "string", "description": "テスト販売計画（場所・方法・ターゲット人数）"},
                        "channels": {"type": "array", "items": {"type": "string"}, "description": "販売・発信チャネル（クラウドファンディング・POPUP・SNS等）"},
                        "success_metrics": {"type": "array", "items": {"type": "string"}, "description": "成功指標（定量・定性）"},
                        "timeline": {"type": "string"},
                    },
                    "description": "③ Passion フェーズの詳細",
                },
                "revenue_model": {"type": "string", "description": "収益モデル（Kivaへの対価設計・費用分担）"},
                "total_timeline": {"type": "string", "description": "全体スケジュール"},
                "risks_and_mitigations": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "risk": {"type": "string"},
                            "mitigation": {"type": "string"},
                        },
                    },
                },
                "next_actions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "今すぐ動ける次のアクション（3〜5個、具体的に）",
                },
            },
            "required": ["title", "executive_summary", "mottainai_discovery", "solution", "next_actions"],
        },
    },
    {
        "name": "save_brand_strategy",
        "description": (
            "Kivaのブランドエッセンス（「素のままの上質」×「泥臭い実行力」）と、"
            "杉島啓太の「自分ごとを社会ごとに翻訳する」哲学と整合した、"
            "新規事業・新クライアント向けのブランド戦略を作成・保存する。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "ブランド戦略のタイトル"},
                "brand_positioning": {"type": "string", "description": "ブランドポジショニング（競合との差別化軸）"},
                "core_message": {"type": "string", "description": "コアメッセージ・タグライン候補"},
                "brand_story": {"type": "string", "description": "ブランドストーリー（「米と出汁。」の原体験に連なる文脈）"},
                "social_translation": {"type": "string", "description": "自分ごとを社会ごとに翻訳した事業の意義"},
                "visual_direction": {
                    "type": "object",
                    "properties": {
                        "theme": {"type": "string"},
                        "color_palette": {"type": "string"},
                        "photography_style": {"type": "string"},
                        "design_principles": {"type": "array", "items": {"type": "string"}},
                    },
                    "description": "ビジュアル方向性",
                },
                "communication_strategy": {
                    "type": "object",
                    "properties": {
                        "owned_media": {"type": "string"},
                        "earned_media": {"type": "string"},
                        "paid_media": {"type": "string"},
                        "key_messages_by_audience": {
                            "type": "object",
                            "properties": {
                                "for_clients": {"type": "string"},
                                "for_students": {"type": "string"},
                                "for_public": {"type": "string"},
                            },
                        },
                    },
                },
                "content_pillars": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "pillar": {"type": "string"},
                            "rationale": {"type": "string"},
                            "content_examples": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                    "description": "コンテンツの柱（SNS・発信の軸）",
                },
                "kiva_brand_alignment": {"type": "string", "description": "Kivaブランドエッセンスとの整合性チェック"},
                "implementation_roadmap": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "phase": {"type": "string"},
                            "actions": {"type": "array", "items": {"type": "string"}},
                            "timeline": {"type": "string"},
                        },
                    },
                },
            },
            "required": ["title", "brand_positioning", "core_message", "brand_story", "social_translation"],
        },
    },
    {
        "name": "save_customer_persona",
        "description": (
            "Kivaのターゲット顧客（企業クライアントと学生パートナー）の詳細なペルソナを作成・保存する。"
            "「主体的に選んだ人生を生きる人」を増やすというファウンダーの理念を体現したターゲット像を設計する。"
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "ペルソナ設計書のタイトル"},
                "client_personas": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "ペルソナ名（架空の人物名）"},
                            "age": {"type": "string"},
                            "role": {"type": "string", "description": "職種・役職"},
                            "company_profile": {"type": "string", "description": "会社の規模・業種・地域"},
                            "background": {"type": "string"},
                            "goals": {"type": "array", "items": {"type": "string"}},
                            "mottainai_pain": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "「伝えたいのに伝えられない葛藤」「もったいない」の具体的な痛み",
                            },
                            "what_makes_them_move": {"type": "string", "description": "何があれば行動するか"},
                            "kiva_appeal": {"type": "string", "description": "Kivaへの魅力・刺さるポイント"},
                            "objections": {"type": "array", "items": {"type": "string"}, "description": "想定される懸念・反論"},
                            "approach_strategy": {"type": "string", "description": "Kivaとしてのアプローチ戦略"},
                        },
                        "required": ["name", "role", "company_profile", "mottainai_pain", "kiva_appeal"],
                    },
                    "description": "企業クライアントのペルソナ（1〜3名）",
                },
                "student_personas": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "age": {"type": "string"},
                            "university_major": {"type": "string"},
                            "background": {"type": "string"},
                            "career_goals": {"type": "array", "items": {"type": "string"}},
                            "motivations": {"type": "array", "items": {"type": "string"}},
                            "fears": {"type": "array", "items": {"type": "string"}},
                            "kiva_appeal": {"type": "string"},
                            "engagement_strategy": {"type": "string", "description": "Kivaへの巻き込み方・ガクチカとしての訴求"},
                        },
                        "required": ["name", "career_goals", "kiva_appeal"],
                    },
                    "description": "学生パートナーのペルソナ（1〜2名）",
                },
                "persona_insights": {"type": "string", "description": "全体を通じたインサイト・Kivaが重視すべき共通テーマ"},
            },
            "required": ["title", "client_personas", "persona_insights"],
        },
    },
]

# ============================================================
# ツール実行（ユーザー定義ツール）
# ============================================================

def execute_tool(tool_name: str, tool_input: dict) -> str:
    """ユーザー定義ツールを実行し、Markdownファイルとして保存する"""
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    formatters = {
        "save_market_research": (format_market_research, f"market_research_{timestamp}.md"),
        "save_business_plan": (format_business_plan, f"business_plan_{timestamp}.md"),
        "save_brand_strategy": (format_brand_strategy, f"brand_strategy_{timestamp}.md"),
        "save_customer_persona": (format_customer_persona, f"customer_personas_{timestamp}.md"),
    }

    if tool_name not in formatters:
        return f"未知のツール: {tool_name}"

    formatter, filename = formatters[tool_name]
    filepath = output_dir / filename
    content = formatter(tool_input)
    filepath.write_text(content, encoding="utf-8")

    return f"保存完了: {filepath}"


# ============================================================
# Markdownフォーマッター
# ============================================================

def _header() -> str:
    return f"\n> 作成日: {datetime.now().strftime('%Y年%m月%d日')} | Kiva 新規事業エージェント powered by 杉島啓太の哲学\n"


def format_market_research(d: dict) -> str:
    lines = [f"# {d.get('title', '市場調査レポート')}", _header()]

    lines += [
        f"## 事業領域\n{d.get('business_domain', '')}",
        f"\n## 市場概況\n{d.get('market_overview', '')}",
    ]

    if d.get("target_market_size"):
        lines.append(f"\n## ターゲット市場規模\n{d['target_market_size']}")

    if d.get("local_authenticity_assets"):
        lines.append(f"\n## 「地方に眠る本物」として発掘できるもの\n{d['local_authenticity_assets']}")

    if d.get("competitors"):
        lines.append("\n## 競合分析")
        for c in d["competitors"]:
            lines.append(f"\n### {c.get('name', '')}")
            for k, label in [("overview", "概要"), ("strengths", "強み"), ("weaknesses", "弱み"), ("kiva_differentiation", "Kivaとの差別化")]:
                if c.get(k):
                    lines.append(f"**{label}**: {c[k]}")

    if d.get("opportunities"):
        lines.append("\n## 市場機会")
        lines.extend(f"- {o}" for o in d["opportunities"])

    if d.get("threats"):
        lines.append("\n## リスク・脅威")
        lines.extend(f"- {t}" for t in d["threats"])

    if d.get("kiva_fit_score"):
        lines.append(f"\n## Kivaとの親和性評価\n{d['kiva_fit_score']}")

    lines.append(f"\n## 提言・アクション\n{d.get('recommendations', '')}")

    return "\n".join(lines)


def format_business_plan(d: dict) -> str:
    lines = [f"# {d.get('title', 'ビジネスプラン')}", _header()]

    lines += [
        f"## エグゼクティブサマリー\n{d.get('executive_summary', '')}",
        f"\n## 発見した「もったいない」\n{d.get('mottainai_discovery', '')}",
        f"\n## Kivaのソリューション\n{d.get('solution', '')}",
    ]

    if tc := d.get("target_client"):
        lines.append("\n## ターゲットクライアント")
        if tc.get("type"):
            lines.append(f"**タイプ**: {tc['type']}")
        if tc.get("description"):
            lines.append(tc["description"])
        if tc.get("pain_points"):
            lines.append("**ペインポイント**:")
            lines.extend(f"- {p}" for p in tc["pain_points"])

    if mp := d.get("mobilize_phase"):
        lines.append("\n## ① Mobilize フェーズ（動員・引き出す）")
        for k, label in [("student_profile", "巻き込む学生像"), ("workshop_design", "ワークショップ設計"), ("expected_output", "期待される成果物"), ("timeline", "タイムライン")]:
            if mp.get(k):
                lines.append(f"**{label}**: {mp[k]}")

    if mm := d.get("micro_make_phase"):
        lines.append("\n## ② Micro-Make フェーズ（製造・形にする）")
        for k, label in [("prototype_specs", "プロトタイプ仕様"), ("production_method", "製造方法"), ("budget_estimate", "予算見積"), ("timeline", "タイムライン")]:
            if mm.get(k):
                lines.append(f"**{label}**: {mm[k]}")

    if pp := d.get("passion_phase"):
        lines.append("\n## ③ Passion フェーズ（熱狂・世に問う）")
        if pp.get("test_sales_plan"):
            lines.append(f"**テスト販売計画**: {pp['test_sales_plan']}")
        if pp.get("channels"):
            lines.append("**販売・発信チャネル**:")
            lines.extend(f"- {c}" for c in pp["channels"])
        if pp.get("success_metrics"):
            lines.append("**成功指標**:")
            lines.extend(f"- {m}" for m in pp["success_metrics"])
        if pp.get("timeline"):
            lines.append(f"**タイムライン**: {pp['timeline']}")

    if d.get("revenue_model"):
        lines.append(f"\n## 収益モデル\n{d['revenue_model']}")

    if d.get("total_timeline"):
        lines.append(f"\n## 全体スケジュール\n{d['total_timeline']}")

    if risks := d.get("risks_and_mitigations"):
        lines.append("\n## リスクと対策")
        for r in risks:
            lines.append(f"- **{r.get('risk', '')}**: {r.get('mitigation', '')}")

    if actions := d.get("next_actions"):
        lines.append("\n## 今すぐ動ける次のアクション")
        lines.extend(f"{i}. {a}" for i, a in enumerate(actions, 1))

    return "\n".join(lines)


def format_brand_strategy(d: dict) -> str:
    lines = [f"# {d.get('title', 'ブランド戦略')}", _header()]

    lines += [
        f"## ブランドポジショニング\n{d.get('brand_positioning', '')}",
        f"\n## コアメッセージ\n> {d.get('core_message', '')}",
        f"\n## ブランドストーリー\n{d.get('brand_story', '')}",
        f"\n## 自分ごとから社会ごとへの翻訳\n{d.get('social_translation', '')}",
    ]

    if vd := d.get("visual_direction"):
        lines.append("\n## ビジュアル方向性")
        for k, label in [("theme", "テーマ"), ("color_palette", "カラーパレット"), ("photography_style", "写真スタイル")]:
            if vd.get(k):
                lines.append(f"**{label}**: {vd[k]}")
        if vd.get("design_principles"):
            lines.append("**デザイン原則**:")
            lines.extend(f"- {p}" for p in vd["design_principles"])

    if cs := d.get("communication_strategy"):
        lines.append("\n## コミュニケーション戦略")
        for k, label in [("owned_media", "オウンドメディア"), ("earned_media", "アーンドメディア"), ("paid_media", "ペイドメディア")]:
            if cs.get(k):
                lines.append(f"**{label}**: {cs[k]}")
        if km := cs.get("key_messages_by_audience"):
            lines.append("\n**ターゲット別キーメッセージ**:")
            for k, label in [("for_clients", "企業クライアント向け"), ("for_students", "学生向け"), ("for_public", "一般向け")]:
                if km.get(k):
                    lines.append(f"- {label}: {km[k]}")

    if pillars := d.get("content_pillars"):
        lines.append("\n## コンテンツの柱")
        for p in pillars:
            lines.append(f"\n### {p.get('pillar', '')}")
            if p.get("rationale"):
                lines.append(f"**理由**: {p['rationale']}")
            if p.get("content_examples"):
                lines.append("**コンテンツ例**:")
                lines.extend(f"- {e}" for e in p["content_examples"])

    if d.get("kiva_brand_alignment"):
        lines.append(f"\n## Kivaブランドとの整合性\n{d['kiva_brand_alignment']}")

    if roadmap := d.get("implementation_roadmap"):
        lines.append("\n## 実装ロードマップ")
        for phase in roadmap:
            lines.append(f"\n### {phase.get('phase', '')}")
            if phase.get("timeline"):
                lines.append(f"**期間**: {phase['timeline']}")
            if phase.get("actions"):
                lines.extend(f"- {a}" for a in phase["actions"])

    return "\n".join(lines)


def format_customer_persona(d: dict) -> str:
    lines = [f"# {d.get('title', '顧客ペルソナ')}", _header()]

    if personas := d.get("client_personas"):
        lines.append("\n---\n\n# 企業クライアント ペルソナ")
        for p in personas:
            lines.append(f"\n## {p.get('name', '')}")
            for k, label in [("age", "年齢"), ("role", "役職"), ("company_profile", "会社プロフィール"), ("background", "背景")]:
                if p.get(k):
                    lines.append(f"**{label}**: {p[k]}")
            if p.get("goals"):
                lines.append("**目標**:")
                lines.extend(f"- {g}" for g in p["goals"])
            if p.get("mottainai_pain"):
                lines.append("**「伝えたいのに伝えられない」葛藤**:")
                lines.extend(f"- {f}" for f in p["mottainai_pain"])
            if p.get("what_makes_them_move"):
                lines.append(f"**行動トリガー**: {p['what_makes_them_move']}")
            if p.get("kiva_appeal"):
                lines.append(f"**Kivaへの魅力**: {p['kiva_appeal']}")
            if p.get("objections"):
                lines.append("**想定される懸念**:")
                lines.extend(f"- {o}" for o in p["objections"])
            if p.get("approach_strategy"):
                lines.append(f"**アプローチ戦略**: {p['approach_strategy']}")

    if personas := d.get("student_personas"):
        lines.append("\n---\n\n# 学生パートナー ペルソナ")
        for p in personas:
            lines.append(f"\n## {p.get('name', '')}")
            for k, label in [("age", "年齢"), ("university_major", "大学・専攻"), ("background", "背景")]:
                if p.get(k):
                    lines.append(f"**{label}**: {p[k]}")
            if p.get("career_goals"):
                lines.append("**将来の目標**:")
                lines.extend(f"- {g}" for g in p["career_goals"])
            if p.get("motivations"):
                lines.append("**モチベーション**:")
                lines.extend(f"- {m}" for m in p["motivations"])
            if p.get("fears"):
                lines.append("**不安・恐れ**:")
                lines.extend(f"- {f}" for f in p["fears"])
            if p.get("kiva_appeal"):
                lines.append(f"**Kivaへの魅力**: {p['kiva_appeal']}")
            if p.get("engagement_strategy"):
                lines.append(f"**巻き込み方**: {p['engagement_strategy']}")

    lines.append(f"\n---\n\n## 統合インサイト\n{d.get('persona_insights', '')}")

    return "\n".join(lines)


# ============================================================
# メインエージェントループ
# ============================================================

def run_agent() -> None:
    """Kivaエージェントのインタラクティブループ"""
    client = anthropic.Anthropic()
    messages: list[dict] = []

    print("\n" + "=" * 62)
    print("  Kiva 新規事業立ち上げエージェント")
    print("  「日本の地方に眠る本物が、世界に届く未来」を作る")
    print("=" * 62)
    print("\n使い方の例：")
    print("  ・「地方の発酵食品市場を調査して」")
    print("  ・「老舗酒蔵とのビジネスプランを作って」")
    print("  ・「Kivaのクライアントペルソナを2種類作成して」")
    print("  ・「伝統工芸×学生共創のブランド戦略を立案して」")
    print("\n'quit' または 'exit' で終了")
    print("=" * 62 + "\n")

    MAX_CONTINUATIONS = 10  # pause_turn（サーバーサイドツールのループ制限）の最大継続回数

    while True:
        try:
            user_input = input("あなた: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nお疲れさまでした。「とりあえず実物を作る」精神で前進しましょう！")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "終了"):
            print("\nお疲れさまでした。「とりあえず実物を作る」精神で前進しましょう！")
            break

        messages.append({"role": "user", "content": user_input})

        print("\nKiva: ", end="", flush=True)

        continuations = 0

        while True:
            try:
                with client.messages.stream(
                    model="claude-opus-4-6",
                    max_tokens=8192,
                    thinking={"type": "adaptive"},
                    system=SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=messages,
                ) as stream:
                    for event in stream:
                        if (
                            event.type == "content_block_delta"
                            and hasattr(event.delta, "type")
                            and event.delta.type == "text_delta"
                        ):
                            print(event.delta.text, end="", flush=True)

                    response = stream.get_final_message()

                # アシスタントの応答を履歴に追加
                messages.append({"role": "assistant", "content": response.content})

                stop_reason = response.stop_reason

                if stop_reason == "end_turn":
                    break

                elif stop_reason == "pause_turn":
                    # サーバーサイドツールがループ制限に達した → 継続
                    continuations += 1
                    if continuations >= MAX_CONTINUATIONS:
                        print("\n\n[最大継続回数に達しました]")
                        break
                    # messages はそのまま（追加なし）で次のAPIコールへ

                elif stop_reason == "tool_use":
                    # ユーザー定義ツールを実行
                    tool_results = []
                    for block in response.content:
                        if block.type == "tool_use":
                            print(f"\n\n[ツール実行: {block.name}]", flush=True)
                            try:
                                result = execute_tool(block.name, block.input)
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": result,
                                })
                                print(f"✓ {result}", flush=True)
                            except Exception as e:
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": f"エラー: {e}",
                                    "is_error": True,
                                })
                                print(f"✗ エラー: {e}", flush=True)

                    if tool_results:
                        messages.append({"role": "user", "content": tool_results})

                    print("\nKiva: ", end="", flush=True)

                else:
                    break

            except anthropic.RateLimitError:
                print("\n\nレート制限に達しました。しばらく待ってから再試行してください。")
                break
            except anthropic.APIError as e:
                print(f"\n\nAPIエラー: {e}")
                break

        print("\n")


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("エラー: ANTHROPIC_API_KEY 環境変数が設定されていません。")
        print("export ANTHROPIC_API_KEY='your-api-key' を実行してください。")
        sys.exit(1)

    run_agent()

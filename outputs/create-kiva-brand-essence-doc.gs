/**
 * Kiva Brand Essence Sheet — Google Docs 自動作成スクリプト
 *
 * 使い方：
 * 1. https://script.google.com を開く
 * 2. 「新しいプロジェクト」を作成
 * 3. このコードを貼り付けて保存
 * 4. 「実行」→「createBrandEssenceDoc」を選択して実行
 * 5. 初回は権限の確認が出るので「許可」する
 * 6. 実行後、Google DriveのマイドライブにDocが作成される
 */

function createBrandEssenceDoc() {
  const doc = DocumentApp.create('Kiva Brand Essence Sheet');
  const body = doc.getBody();

  // デフォルトスタイルのリセット
  body.setMarginTop(60);
  body.setMarginBottom(60);
  body.setMarginLeft(72);
  body.setMarginRight(72);

  // ---- タイトル ----
  const title = body.appendParagraph('Kiva Brand Essence Sheet');
  title.setHeading(DocumentApp.ParagraphHeading.TITLE);
  title.editAsText()
    .setFontFamily('Noto Sans JP')
    .setFontSize(28)
    .setBold(true)
    .setForegroundColor('#231815');

  // ---- キャッチコピー（強調ブロック） ----
  const catchcopy = body.appendParagraph('キャッチコピー：「食から、切り拓く。」');
  catchcopy.setHeading(DocumentApp.ParagraphHeading.NORMAL);
  catchcopy.setSpacingBefore(16);
  catchcopy.setSpacingAfter(8);
  catchcopy.editAsText()
    .setFontSize(16)
    .setBold(true)
    .setForegroundColor('#A24B22')
    .setItalic(true);

  appendDivider(body);

  // ---- セクション1 ----
  appendH2(body, '1. Kivaとは（Core Identity）');
  appendBody(body, '食から、切り拓く共創プラットフォーム。', true);
  appendBody(body, '日本の食と農には、世界に通じる力がある。しかしその力は、まだほとんど「届いていない」。');
  appendBody(body, 'Kivaは、食と農の現場に子どもも大人も外国人も一緒に巻き込み、体験し、変わっていく場をつくる。学生の熱量と、地域の知恵と、本物の食を掛け合わせること——それが私たちの方法だ。');

  appendDivider(body);

  // ---- セクション2 ----
  appendH2(body, '2. 存在理由（Why）');
  appendBody(body, '私たちはかつて、自ら日本の米と出汁でお粥を作り、国内外で届けようとした。');
  appendBody(body, 'その挑戦の中で、ゼロからモノを作ることの難しさを知ると同時に、気づいた。');

  const why_quote = body.appendParagraph('「日本の食には、世界に通じる本物の力がある。なのに、その力が届いていない場所が多すぎる。」');
  why_quote.setSpacingBefore(8);
  why_quote.setSpacingAfter(8);
  why_quote.setIndentStart(36);
  why_quote.editAsText()
    .setFontSize(12)
    .setBold(true)
    .setForegroundColor('#3E4123');

  appendBody(body, '農業は担い手を失い、地域の食文化は若い世代に伝わらず、外国人が「本物の日本食」に出会える場所は限られている。良いモノがあるのに、伝わっていない。体験できていない。');
  appendBody(body, 'そこにこそ、Kivaがいる理由がある。');

  appendDivider(body);

  // ---- セクション3 ----
  appendH2(body, '3. 事業領域（What）');
  appendBody(body, '食と農の力を「届く形」にする3つのコア機能。');
  appendBody(body, 'Kivaは口を出すだけのコンサルティングは行いません。食農プログラムの設計・運営を軸に、5年間培ってきた「学生との共創ノウハウ」を手段として活用し、以下のステップで実装します。');

  appendH3(body, '① Design（設計・引き出す）');
  appendBullet(body, '自治体・地域と連携し、子ども・大人・外国人が食と農を実体験できるプログラムを設計・運営する。');
  appendBullet(body, '食育、農業体験、移住・関係人口促進、インバウンド向け食体験など。');
  appendBullet(body, '企業が持つ食の技術・素材・想いと、学生の若く柔軟な発想力を掛け合わせ、ワークショップ等を通じて「本質的な面白さ」を引き出す。');

  appendH3(body, '② Make（製造・形にする）');
  appendBullet(body, '素晴らしいアイデアが出ても「自社設備がない」「OEMはロットが合わない」という壁で止まらせない。');
  appendBullet(body, '地域の食材・技術を生かしたプロダクト（お粥等）を、学生と共にシェアキッチン等で初期プロトタイプ（50個程度）の「マイクロ製造」を行い、物理的な形にする。');

  appendH3(body, '③ Open（世に問う）');
  appendBullet(body, '「自分たちで生み出した」という強烈な当事者意識を持つ学生と共に、テスト販売や熱量の高い販促（クラウドファンディング、POPUP、インバウンド向け体験など）を実行し、世の中に問う。');

  appendDivider(body);

  // ---- セクション4 ----
  appendH2(body, '4. 方法論（How）');

  appendH3(body, '① コンサルではなく、共に汗をかく');
  appendBody(body, '企画書を納品して終わりではなく、食・農の現場に実際に入り、泥臭く試作し、テスト販売の現場に立つことまでをセットにする。');

  appendH3(body, '② 若い熱量を、食・農の起爆剤にする');
  appendBody(body, '「学生だから」と侮らず、彼らの本気と当事者意識を、食・農の新しい文脈作りに変換する。');

  appendH3(body, '③ 「とりあえず実物を作る」を正義とする');
  appendBody(body, '完璧な計画より、まずは小さく形（プロトタイプ）にして、触れられる状態にすることでプロジェクトの熱狂を止めない。');

  appendDivider(body);

  // ---- セクション5 ----
  appendH2(body, '5. 世界観・デザイン方向性（Visual Direction）');
  appendBody(body, 'テーマ：「素（そ）のままの上質」と「泥臭い実行力」の融合', true);

  appendBullet(body, '空気感：作り手の体温や土の匂いを感じさせる温かさの中に、「現場で汗をかく実行力・熱量」を足す。');

  const colorLabel = body.appendParagraph('ブランドカラー（アースカラー）');
  colorLabel.setHeading(DocumentApp.ParagraphHeading.NORMAL);
  colorLabel.editAsText().setBold(true).setFontSize(12);

  appendBullet(body, 'ベース：白（#FFFFFF）、墨色（#231815）、サンドベージュ（#D9BA8A）');
  appendBullet(body, 'アクセント：ディープオリーブ（#3E4123）、オークル・黄土色（#D29942）、テラコッタ（#A24B22）');
  appendBullet(body, '無機質なIT企業風ではなく、自然や現場の温度感を感じるオーガニックな配色。');
  appendBullet(body, '写真の視点：農の現場や食材の表情、ワークショップで白熱する学生の表情、不格好でも一生懸命作ったプロトタイプなど、「プロセスにおける熱量」をドキュメンタリーのように切り取る。');

  appendDivider(body);

  // ---- セクション6 ----
  appendH2(body, '6. 「米と出汁。」の位置づけ（「食から、切り拓く」の原点）');
  appendBody(body, '「食から、切り拓く」という信念の、生きた実験と原点。');
  appendBody(body, '自ら日本の米と出汁でお粥を作り、世界へ届けようとした挑戦は、大きな壁にぶつかった。ゼロからモノを生み出し、売り続けることの難しさを身をもって知った。');
  appendBody(body, 'しかしその経験が教えてくれたのは、「日本の食の力は本物だ」という確信だった。お粥という形で「日本食の可能性」を問い続けることは、今もKivaの現在進行形の実験であり、食農プログラムの思想的な起点でもある。');
  appendBody(body, 'この原体験があるからこそ、Kivaは「食の現場から世界を切り拓く」という信念を持ち、食・農に関わるあらゆる人（地域・企業・学生・子ども・外国人）を繋ぎ、実装を共にやり遂げる伴走者となることを決意した。');

  appendDivider(body);

  // ---- セクション7 ----
  appendH2(body, '7. ターゲット（Target Audience）');

  appendH3(body, '■ クライアント（発注者）');
  appendBullet(body, '自治体：食育・農業振興・インバウンド促進・移住促進などの予算を持つ担当課。「新しい形で地域の食と農の魅力を伝えたい」という熱意ある担当者。');
  appendBullet(body, '企業・地域事業者：「今のままではダメだ、自社の食の魅力を新しい形で伝えたい」という強い熱意はあるが、形にするリソースが不足している中小企業・アトツギ企業・新規事業担当者。※現状維持層は対象外。');

  appendH3(body, '■ 共創パートナー（学生）');
  appendBullet(body, '就活で戦える強い武器（ガクチカ）を求めている学生。');
  appendBullet(body, 'ありふれたインターンではなく、「ゼロイチの事業創造」や「食・農・地域課題の解決」に本気で挑戦し、泥臭くやり切る覚悟のある学生。');

  appendH3(body, '■ エンドユーザー（受益者）');
  appendBullet(body, '子ども：食農体験・食育プログラムの参加者。食がどこから来るか、どう作られるかを体感する世代。');
  appendBullet(body, '大人・移住希望者：農業や地域の食文化に関わりたい、暮らしを変えたいと考えている人。');
  appendBullet(body, '外国人・インバウンド：本物の日本食・農の現場を体験したい訪日客。「日本食」をただ食べるではなく、作り・触れ・感じたい層。');

  doc.saveAndClose();

  const url = doc.getUrl();
  Logger.log('✅ ドキュメント作成完了：' + url);
  SpreadsheetApp.getUi && SpreadsheetApp.getUi().alert('作成完了！\n' + url);

  return url;
}

// ---- ヘルパー関数 ----

function appendH2(body, text) {
  const p = body.appendParagraph(text);
  p.setHeading(DocumentApp.ParagraphHeading.HEADING2);
  p.setSpacingBefore(20);
  p.setSpacingAfter(6);
  p.editAsText()
    .setFontSize(16)
    .setBold(true)
    .setForegroundColor('#3E4123');
  return p;
}

function appendH3(body, text) {
  const p = body.appendParagraph(text);
  p.setHeading(DocumentApp.ParagraphHeading.HEADING3);
  p.setSpacingBefore(12);
  p.setSpacingAfter(4);
  p.editAsText()
    .setFontSize(13)
    .setBold(true)
    .setForegroundColor('#231815');
  return p;
}

function appendBody(body, text, bold = false) {
  const p = body.appendParagraph(text);
  p.setHeading(DocumentApp.ParagraphHeading.NORMAL);
  p.setSpacingBefore(4);
  p.setSpacingAfter(4);
  p.editAsText()
    .setFontSize(11)
    .setBold(bold)
    .setForegroundColor('#231815');
  return p;
}

function appendBullet(body, text) {
  const p = body.appendListItem(text);
  p.setGlyphType(DocumentApp.GlyphType.BULLET);
  p.setSpacingBefore(2);
  p.setSpacingAfter(2);
  p.editAsText()
    .setFontSize(11)
    .setForegroundColor('#231815');
  return p;
}

function appendDivider(body) {
  const p = body.appendParagraph('──────────────────────────');
  p.editAsText()
    .setForegroundColor('#D9BA8A')
    .setFontSize(9);
  p.setSpacingBefore(12);
  p.setSpacingAfter(12);
  return p;
}

# SOUNDVAULT 音楽エンジン

ゲーム用のオーケストラBGMを、**楽譜（Pythonで書いた旋律と和音）→ 編曲 → 書き出し → 検査 → SOUNDVAULT登録**まで一続きで作る仕組みです。

これまでに作った曲：

- 『モンスタークエスト0』：32曲（タイトル4案、町・ダンジョン・戦闘・場面・ジングル）
- 『甲殻類にも都合があります。』：6曲（タイトル3案、深海フィールド3案）

どちらも、ユーザーが「意図通りの音楽」と確認しています（2026-11-01）。その作風は [STYLE.md](STYLE.md) に、次に作るときの指針としてまとめています。

## しくみ

```text
projects/<ゲーム>/pieces_*.py   旋律・和音・構成（小節ごとに手で書く）＋ 編曲の指定
        │
engine/orchestrate.py          旋律と和音から各パートを書き起こす
        │                      （主旋律・対旋律・和音・低音・アルペジオ・刻み・金管・打楽器）
engine/render_orch.py          パートごとに sfizz で書き出し → 定位・音量・ホール残響 → −16 LUFS
        │                      ループ長を超えた余韻は曲頭へ折り返すので、継ぎ目は構造上つながる
engine/qa_audio.py             クリップ・ピーク・ラウドネス・無音・継ぎ目・旋律の類似度
        │
engine/to_soundvault.py        OGG + M4A、メタデータ（ループ点・用途・動機）、Project を登録
```

- **音源**：[VSCO 2 Community Edition](https://github.com/sgossner/VSCO-2-CE)（CC0 1.0）。弦5部・木管・金管・ハープ・打楽器・オルガン・鐘・マリンバなど
- **サンプラー**：[sfizz](https://github.com/sfztools/sfizz)（BSD-2-Clause）。`third_party/sfizz_render_events.patch` で書き出し用に修正しています
  - サンプルをすべてメモリに読み込む（裏で逐次読み込むと、同じ入力でも結果が毎回変わるため）
  - 音符をサンプル単位の整数時刻で受け取る `--events` モード（MIDIの時刻を足し上げる方式では1サンプルずれるため）
  - 32bit浮動小数で書き出す
- **出力**：48 kHz、ループ点 `loopStart=0`・`loopEnd`（サンプル数）。ループ長は64サンプルの倍数、テンポは「1拍が整数マイクロ秒」になる値だけを使います

## セットアップ

```bash
cd tools/music-engine
./setup.sh                 # 音源（約5GB）・sfizz（修正・ビルド）・Python環境を .cache/ と .venv/ に用意
.venv/bin/python msl.py selftest
```

必要なもの：git、cmake、C++17コンパイラ、ffmpeg、Python 3.11以上（Ubuntu/Debian なら `sudo apt-get install -y git cmake g++ pkg-config ffmpeg python3-venv`）。音源やsfizzが別の場所にある場合は、環境変数 `MSL_VSCO`・`MSL_SFIZZ` で指定できます。

`selftest` は勝利ファンファーレ（14秒）を書き出し、保存してある基準（`engine/selftest.json`）と比べます。同じ環境ならビット単位で一致し、違うPCでも長さ・ラウドネス・ピーク・音量の時間変化が許容範囲に収まれば PASS です。

## 使い方

```bash
PY=.venv/bin/python
$PY msl.py list                                   # プロジェクトと曲の一覧
$PY msl.py validate crustaceans                   # 小節の長さ・強拍の和音・音域・ループの計算
$PY msl.py render crustaceans                     # 全曲を .out/crustaceans/ に書き出し（曲IDを並べると一部だけ）
$PY msl.py qa crustaceans                         # 自動検査 → .out/crustaceans/qa.json
$PY msl.py export crustaceans ../..               # SOUNDVAULT（このリポジトリ）に登録
cd ../.. && npm run scan && npm run build         # 索引更新とビルド確認 → コミット・PR
```

## 新しいゲームの曲を作る

1. `projects/<名前>/` を作り、`project.json` を置きます（Project名、ファイル名の接頭辞、タグ、コレクション）。`projects/crustaceans/project.json` が見本です。
2. `pieces_<名前>.py` に曲を書き、`catalog.py` で `PIECES` として公開します。
3. [STYLE.md](STYLE.md) の進め方に沿って作曲し、`validate` → `render` → `qa` → 試聴 → `export` の順に進めます。

### 曲データの書き方

```python
'game_title': dict(
    title='タイトル「…」', key='D major', bpm=80, meter=4,       # meter=3 で3拍子。loop=False でジングル
    group='タイトル', usage='タイトル画面', motifs=['主人公の主題'], form='構成の説明（SOUNDVAULTのメモに入る）',
    sections=[
        ('A', 'D E/D Bm G|A', [                                   # 和音を小節ごとに。'G|A' は1小節を半分ずつ
            'A4:1.5 F#4:.5 D4:1 A3:1', 'B3:1 E4:1 G#4:2', ...]), # 旋律「音名:拍数」、休符は r
        ('B', '...', [...], {'moan': ['r:4', 'C3:4', ...]}),      # 手書きの副旋律（line='moan' で使う）
    ],
    arrange=arr_game_title),                                       # 編曲関数
```

使える和音：`C Cm C7 Cm7 Cmaj7 Cm7b5 Cdim Csus4 C6 Cm6`、分数和音 `C/E`。

編曲関数の中では、次の部品を区間名で呼び分けます。

| 部品 | 内容 |
|---|---|
| `a.melody(parts, sections, octave=, vel=, line=)` | 主旋律（`line=` で副旋律）。`parts` は楽器名のリスト |
| `a.pad([(楽器, 低, 高), ...], sections, voices=)` | 和音を声部進行つきで持続 |
| `a.bass(parts, sections, 'whole'/'half'/'root5'/'march'/'synco'/'drive8'/'pedal')` | 低音の型 |
| `a.arpeggio(楽器, sections, step=, shape='up'/'updown')` | ハープなどのアルペジオ |
| `a.ostinato(parts, sections, step=, pattern=)` | 刻み（`None` で休み） |
| `a.counter(楽器, sections, center=, beats=)` | 3度と7度をつなぐ対旋律 |
| `a.stabs([...], sections, rhythm=)` | 金管の打ち込み |
| `a.timpani(sections, beats=, roll_last_bar=)` / `a.swell_into(小節)` | ティンパニ、区間前のシンバルの膨らみ |
| `a.drums(sections, 'march'/'boss'/'battle'/'town'/'title'/'waltz'/'tom'/'shuffle')` | 打楽器の型 |
| `shimmer(...)`（`projects/crustaceans`）/ `sparkle(...)`（`projects/monque`） | 高音のきらめき |

楽器名（`engine/orchestrate.py` の `INSTR`）：`vln1 vln2 vla vc cb`（＋`_spic _pizz _trem`、`vln1_q`）、`svln`（独奏バイオリン）、`fl ob cl bn`、`hn hn_stac hn_mute tpt tpt_stac tbn tbn_stac tba`、`harp glock xylo marimba bells org`、`timp timp_roll perc`。各楽器の音域と、伸ばせる最長の秒数もここに定義しています。新しい楽器を足したら、`engine/calibration.json` に収録音量を測って加えてください（同じ音・同じ強さで鳴らしたときのLUFS）。

## 品質基準

| 項目 | 基準 |
|---|---|
| クリップ / トゥルーピーク | 0 / −1 dBTP 以下（リミッターは使わない） |
| ラウドネス | −16 LUFS（±1）。強弱の差が大きくてピークで止まる曲は、SOUNDVAULTの `volume` で補う |
| 継ぎ目 | 継ぎ目の段差が曲中の通常の変化（99パーセンタイル）より小さいこと。曲頭がシンバルの立ち上がりで始まる曲は1を少し超えることがあるが、ループは連続再生と同じ音 |
| 旋律の独自性 | 音程6つの並びの一致率が10%未満（既存曲・同じゲームの他の曲と照合）。有名曲との照合は人の耳で |
| バランス | 各区間で主旋律が最大のパートから3dB以内（`render.json` の `balance`） |
| 試聴 | 自動検査のあと、必ず人が聴いて判断する |

## ファイル構成

```text
msl.py              コマンド
setup.sh            音源・sfizz・Python環境の用意（バージョン固定）
requirements.txt    Pythonライブラリ（バージョン固定）
STYLE.md            承認済みの作風と作曲の進め方
engine/             共通部分（編曲・書き出し・検査・登録・自己テスト基準）
projects/monque/        モンスタークエスト0（32曲）
projects/crustaceans/   甲殻類にも都合があります。（6曲）
third_party/        sfizz の修正パッチ
windows/            AI音楽モデル（ACE-Step 1.5 / Stable Audio 3）を手元のGPU PCで試すためのスクリプト（未使用・未検証）
```

## ライセンス

- 楽譜（旋律・和音・編曲）はこのプロジェクトのオリジナルです
- 音源：VSCO 2 Community Edition（CC0 1.0）
- sfizz：BSD-2-Clause（修正パッチも同じ条件で配布できます）

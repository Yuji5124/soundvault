# SOUNDVAULT

## Project 管理

「Project 管理」で名前（例：桃太郎）と種類（例：紙芝居、ゲーム）を登録できます。各効果音の「Project を設定」で複数の Project に紐付けると、カードに Project 名と種類が表示され、検索・絞り込みにも利用できます。

終了した Project はアーカイブすると「Project Archive」で探せます。復元もできます。紐付け解除はチェックを外して保存、Project 削除は管理画面から実行します。いずれも音源ファイルは削除しません。

画面の編集はこのブラウザの localStorage に保存されます。他の端末や訪問者には自動共有されません。「JSON 書き出し」の `projects` を `data/projects.json` に、`sounds` を `data/sounds.json` に保存し、`npm run scan` 後にコミット・push すると共有できます。スキャンは `projectIds` を保持します。Project を削除して共有する場合は両方の JSON を更新してください。

Reusable Sound Asset Library — a lightweight static sound browser for games, Three.js, Phaser, and web apps.

## What it does

SOUNDVAULT keeps audio files and a JSON index in GitHub, so the workflow stays simple: **store → search → listen → copy → use**. There is no server or database. Favorites live locally in the browser, while `data/sounds.json` is also a public, API-like index for other projects.

## Setup

Requires Node.js 20+.

```bash
npm install
npm run generate-demo # optional: create local, copyright-safe WAV examples
npm run scan          # index files under public/sounds/
npm run dev
```

The production check is `npm run build`. `npm run prepare-assets` generates missing demo files, scans the library, and builds the site.

## Add sounds

Put `.wav`, `.mp3`, `.ogg`, or `.m4a` files in a category folder under `public/sounds/` (`ui`, `action`, `item`, `environment`, `fx`, `kids`, `voice`, or `bgm`), then run:

```bash
npm run scan
```

The scanner updates filesystem fields (path, format, size, and inferred category) while retaining human metadata such as `tags`, `license`, `source`, `author`, `notes`, `volume`, `loop`, and `collections`. New files default to `license: "UNKNOWN"`; verify the license before shipping.

## GitHub Pages

Push `main` to GitHub. `.github/workflows/deploy.yml` runs the asset scan and Vite build, then deploys `dist` with GitHub Pages. In repository settings, set Pages → Source to **GitHub Actions**. The Vite base path is relative, so the repository works both at a project Pages URL and in local preview.

## Use from other projects

The published files can be loaded directly without an API server:

```js
const AUDIO_BASE = 'https://USERNAME.github.io/soundvault/sounds/';
const coin = new Audio(`${AUDIO_BASE}item/coin-001.wav`);

const sounds = await fetch('https://USERNAME.github.io/soundvault/data/sounds.json').then((r) => r.json());
```

Every card also provides copy buttons for URL, path, plain JavaScript, Three.js, and Phaser snippets.

## Licensing

Each record carries `license`, `source`, and `author`. Use `CC0`, `CC-BY`, `Original`, or another precise value when known. Keep `UNKNOWN` until provenance is verified; the UI marks unknown assets with a warning. Demo WAV files are generated locally and contain no external audio.

## Project layout

```text
public/sounds/       audio assets grouped by category
data/sounds.json     static metadata index
scripts/scan-sounds.mjs
src/main.ts          browser UI and audio controls
src/styles.css       responsive dark asset-browser UI
```

## ZIG デイリー曲 (毎日 7:00 JST、承認制)

`.github/workflows/zig-daily.yml` が、毎日 **7:00 (日本時間)** に [SONOVA](https://github.com/Yuji5124/SONOVA) で ZIG 名義のオリジナル曲 (インストゥルメンタルのロック) を 1 曲生成し、**Pull Request として提案**します。**PR をマージするまで `main` は変わりません** (マージ = 承認。マージすると既存の `deploy.yml` が公開します)。

- 曲名・ファイル名・タグは `YYMMDD_` で始まります (例: `261027_ZIG_MIDNIGHT ANTENNA` / `261027_ZIG_midnight-antenna.ogg`)。日付は日本時間です。
- 同じ日に再実行しても二重登録しません。前の提案 (`zig-daily/*` の未マージ PR) が残っている間は新しい曲を作らず、ジョブに警告を出します。
- 生成条件・参照元・音声の sha256・検証結果は `data/zig-daily/` に、曲と同じ PR で記録されます。既存のレコードと音声は変更しません (変更があればジョブが止まります)。
- 無料です (公開リポジトリの GitHub Actions、有料 API・クラウド AI・API キー・GPU なし)。必要なのは組み込みの `GITHUB_TOKEN` だけです。

**最初に 1 回だけ必要な設定:** Settings → Actions → General → Workflow permissions で **"Allow GitHub Actions to create and approve pull requests"** をオンにします。オフだと PR の作成だけが失敗します (曲の生成と検証は成功し、ログに残ります)。

手動実行: Actions → "ZIG daily song" → Run workflow。`dry_run` をオンにすると何も変更せず、予定だけを表示します。`date` に `YYMMDD` を入れると、その日付で実行します。

制限: GitHub のスケジュール実行は高負荷時に遅れたり抜けたりすることがあります (9:30 JST に再試行枠あり。重複防止があるので安全)。公開リポジトリでは 60 日間リポジトリに動きがないとスケジュールが自動停止します (PR をマージすれば動きとして数えられます)。詳細は SONOVA の `docs/zig-daily.md`。

"""All MONQUE SOUND LAB orchestral pieces (32): the 5 test themes + 27 new ones (incl. titles C and D)."""
from pieces_fields import PIECES as FIELDS
from pieces_places import PIECES as PLACES
from pieces_scenes import PIECES as SCENES
from pieces_story import PIECES as STORY
from pieces_titles import PIECES as TITLES
from score import PIECES as TEST

META = {
    'mq_orch_title': dict(title='タイトルA「幻の冒険の書」', group='正式8枠', usage='BGM01 タイトル / オープニング（A案）', motifs=['主人公の主題'],
                          form='A ホルン＋チェロの主題 → B ト短調の歌（フルート＋バイオリン） → A2 トランペットの総奏'),
    'mq_orch_field': dict(group='正式8枠', usage='BGM02 フィールド（ワールドマップ）', motifs=['主人公の主題'],
                          form='A バイオリン＋フルート、行進の小太鼓 → A2 ホルンの旋律 → B 木管の歌、♭VII → C 総奏'),
    'mq_orch_town': dict(group='正式8枠', usage='BGM03 むら・まち', motifs=['主人公の主題（拡大）'],
                         form='A フルートとハープ、ピチカート → B オーボエ、♭VII → A2 バイオリン＋フルート'),
    'mq_orch_dungeon': dict(group='正式8枠', usage='BGM04 ダンジョン', motifs=['主人公の主題（短調）'],
                            form='A オーボエ、ハープの反復、弦トレモロ、ドラ → B ファゴット＋チェロ'),
    'mq_orch_boss': dict(group='正式8枠', usage='BGM05 ボス戦（デーマス、バトラス等）', motifs=['主人公の主題（短調）'],
                         form='A トランペット＋バイオリン、金管の刻み → B ホルンの英雄的な旋律 → C 総奏'),
}
ORDER = [
    'mq_orch_title', 'mq_orch_title_b', 'mq_orch_title_c', 'mq_orch_title_d', 'mq_orch_field', 'mq_orch_town', 'mq_orch_dungeon', 'mq_orch_boss', 'mq_orch_final', 'mq_orch_ending', 'mq_orch_again',
    'mq_orch_start_town', 'mq_orch_bie', 'mq_orch_castletown', 'mq_orch_castle', 'mq_orch_hidden', 'mq_orch_port', 'mq_orch_shrine', 'mq_orch_stone',
    'mq_orch_forest', 'mq_orch_lake', 'mq_orch_tower', 'mq_orch_iwayama', 'mq_orch_orochi_road',
    'mq_orch_battle', 'mq_orch_card', 'mq_orch_gacha',
    'mq_orch_bond', 'mq_orch_sorrow', 'mq_orch_anomaly', 'mq_orch_choice', 'mq_orch_victory',
]
_all = {}
for src in (TEST, STORY, TITLES, PLACES, FIELDS, SCENES):
    _all.update(src)
for k, extra in META.items():
    _all[k] = {**_all[k], **extra}
assert sorted(_all) == sorted(ORDER), set(_all) ^ set(ORDER)
PIECES = {k: _all[k] for k in ORDER}

# Simplified Chinese terminology / 简体中文术语表

This glossary governs the `zh_CN` translation installed in Warband's `languages/cns`
folder. It translates the **displayed source text**, not the English-looking ID.
The original module data, Latin and reconstructed ancient-language names remain
untouched. Chinese noun forms normally do not change with number: troop singular
and `_pl` entries therefore use the same translation when the source differs only
in number. Do not erase meaningful gender or rank differences.

## Roman titles and military terms

| Source | Chinese | Usage |
| --- | --- | --- |
| Princeps | 元首 | Roman political title. |
| Caesar | 凯撒 | Name or imperial title, following source context. |
| Emperor | 皇帝 | Do not silently substitute for Caesar. |
| Senate | 元老院 | Roman institution. |
| senator | 元老 | Member of the Senate. |
| legion / Legio | 军团 | Preserve Roman numerals in named units. |
| legate / Legatus Legionis | 军团长 | For the actual title, not merely an ID containing `legatus`. |
| Tribunus | 军团保民官 | Military context; `trp_legatus_legionis` actually displays this title. |
| Centurio | 百夫长 | Military rank. |
| Primus Pilus | 首席百夫长 | Preserve distinction from ordinary centurion. |
| Decurio | 骑兵十夫长 | Roman cavalry rank. |
| Tiro | 新兵 | Recruit. |
| Miles | 士兵 / 步兵 | Use 步兵 for named auxiliary infantry units. |
| Evocatus | 重征老兵 | Recalled veteran, not every veteran unit. |
| Praetoriani | 禁卫军 | Imperial guard. |
| Auxilia | 辅助军 | Roman auxiliary units. |
| Aquilifer | 鹰旗手 | Keep distinct from other standard bearers. |
| Signifer | 军旗手 | Standard bearer. |
| Vexillarius / Vexilarius | 旗手 | Preserve original source spelling in identifiers. |
| Cornicen | 号角手 | Military horn player. |
| Vigilia | 消防卫兵 | Roman urban watch/fire service in this troop context. |
| Ballistarius | 弩炮手 | Artillery crew. |
| Sagittarius | 弓箭手 | Archer. |
| Funditor | 投石兵 | Slinger. |
| Cataphractus | 具装骑兵 | Armoured cavalry. |
| denarius / denarii | 第纳尔 | Singular/plural share the Chinese noun. |

## Civilian roles and culture names

| Source | Chinese | Usage |
| --- | --- | --- |
| Rusticus / Rustici | 农民 | Preserve distinction from Tribulis. |
| Tribulis / Tribules | 部落民 | Tribal member. |
| Focaria | 随军妇女 | No invented marital relationship. |
| Nobilis | 贵族 | Nobilis Mulier = 贵族妇女. |
| Civis | 公民 | Civis Femina = 女性公民. |
| Latro | 劫匪 | Differentiate from Leistes = 强盗. |
| Roman | 罗马 | |
| Greek | 希腊 | |
| Dacian | 达契亚 | |
| Celtic | 凯尔特 | `fac_culture_celtic` displays Britonic, translated 不列颠. |
| Britonic / Brittonum | 不列颠 | |
| Caledonian | 喀里多尼亚 | |
| Germanic | 日耳曼 | |
| Sarmatian | 萨尔马提亚 | |
| Bosporan | 博斯普鲁斯 | Ancient kingdom, not a modern political label. |
| Caucasian | 高加索 | Geographical/cultural use. |
| Parthian | 帕提亚 | |
| Persian | 波斯 | |
| Judean | 犹太 | |
| Syrian | 叙利亚 | |
| Egyptian | 埃及 | |
| Berber | 柏柏尔 | Latin Maurus is 毛里; do not conflate every source form. |
| Garamantian | 加拉曼特 | |
| Nubian | 努比亚 | |
| Saka | 塞种 | |
| Hispanic | 伊斯帕尼亚 | Roman-era geographical name. |
| Gaulish | 高卢 | |
| Galatian | 加拉太 | Distinct from Gaulish. |
| Illyrian | 伊利里亚 | |
| Thracian | 色雷斯 | |

## Named legions

| Source | Chinese |
| --- | --- |
| XXII Primigenia | 第XXII初生军团 |
| III Augusta | 第III奥古斯塔军团 |
| V Alaudae | 第V云雀军团 |
| XXI Rapax | 第XXI猛禽军团 |
| XX Valeria Victrix | 第XX英勇胜利军团 |
| VI Victrix | 第VI胜利军团 |
| XI Claudia | 第XI克劳狄军团 |
| XIII Gemina | 第XIII合组军团 |
| V Macedonia | 第V马其顿军团 |
| VI Ferrata | 第VI铁甲军团 |
| X Fretensis | 第X海峡军团 |

These are readable Chinese unit labels, not corrections to upstream's Latin.
Roman numerals preserve recognisability in equipment and external guides.

## Scope and editorial decisions

The initial troop file covers 327 of 2,610 compiled troop records (654 names,
including plural keys): all 24 peasant/recruit roots; the eleven listed legion
recruit/soldier/recalled-veteran branches and eagle/flag bearers; praetorians,
Roman auxiliary branches and officers; common guards, bandits, tutorial/arena
roles and selected civilian services. It does **not** cover all mercenaries,
non-Roman troop trees, named NPCs or dynamically renamed characters. Remaining
source text falls back to upstream text; lack of a row is not an assertion that
it is nontranslatable.

Of 75 compiled faction keys, 74 have translated entries. `fac_kingdoms_end` is
an internal marker and is omitted from the translation file; it falls back to
source text and does not count as a translated faction.
`fac_minor_kingdoms_end` displays `Greek` in the compiled data, so its value is
希腊 without guessing another faction. The Egypt faction's unusual
`Remetjw-men-Maat` is transliterated with its original form retained; no invented
religious or dynastic meaning is supplied. `Leugoz` and `Rygir` also retain the
source form beside the Chinese tribal name for review. Roman civil-war factions
use 罗马帝国·[leader]派. These choices can be revised independently of stable IDs.

Some IDs are misleading: `trp_legatus_legionis` displays `Tribunus`, while
`trp_watchman` displays `Mercenarius Funditor`. Translate the compiled display
name with its module source context; never mechanically expand an ID into a
Chinese name. Unfamiliar reconstructed-language troop names remain outside this
milestone rather than receiving speculative word-by-word translations.

## Recurring character names

| Source | Chinese |
| --- | --- |
| Kaeso Flavius | 凯索·弗拉维乌斯 |
| Paulus | 保卢斯 |
| Lucillus | 卢基卢斯 |
| Wlodowiecus | 沃洛多维库斯 |
| Chrestos | 克瑞斯托斯 |

## Shared skill labels

| Source | Chinese |
| --- | --- |
| Tracking | 追踪 |
| Trade and Management | 交易与经营 |

Attribute explanations in `ui.csv` should use the same labels as `skills.csv`.

## Equipment and places

| Source | Chinese |
| --- | --- |
| Gladius | 罗马短剑 |
| Spatha | 斯帕塔长剑 |
| Pugio | 罗马匕首 |
| Pilum / Pila | 罗马重标枪 |
| Hasta | 罗马矛 |
| Scutum | 罗马大盾 |
| Lorica Hamata | 锁子甲 |
| Lorica Squamata | 鳞甲 |
| Lorica Segmentata | 罗马分节板甲 |
| Lorica Musculata | 肌肉胸甲 |
| Subarmalis | 衬甲衣 |
| Manica | 护臂 |
| Caliga | 罗马凉靴 |
| Ocrea | 胫甲 |
| Fortuna / Minerva / Mars / Mercury / Jupiter | 福尔图娜 / 密涅瓦 / 玛尔斯 / 墨丘利 / 朱庇特 |
| Vicus | 城郊聚落 |
| Curia Julia | 尤利亚会堂 |
| Mouseion | 缪斯学宫 |
| followers (party) | 随军队伍 |
| mantlets | 挡箭牌 |

Item translations follow displayed names: `itm_apples` displays “Fruit” (水果),
and `itm_venison` displays “Game Meat” (野味). Chariot names retain original Latin
in parentheses. The obvious source spelling “Seventheen” is interpreted as
seventeenth in the eagle-standard label; no gameplay data is corrected.

## Narrative names

| Source | Chinese | Notes |
| --- | --- | --- |
| Nero | 尼禄 | Imperial title remains 凯撒 / 元首 as written. |
| Poppaea Sabina | 波佩娅·萨比娜 | |
| Claudia Antonia | 克劳狄娅·安东尼娅 | Source also addresses her as Claudia; retain that form. |
| Seneca | 塞涅卡 | |
| Vespasian | 韦斯帕芗 | |
| Tigellinus / Tigellinius | 提格利努斯 | Same source character, spelling variants. |
| Petronius | 佩特罗尼乌斯 | |
| Locusta | 洛库斯塔 | |
| Crispinilla | 克里斯皮尼拉 | |
| Sporus | 斯波鲁斯 | |
| Octavia | 屋大维娅 | |
| Otho | 奥托 | |
| Agrippina | 阿格里皮娜 | |
| Acte | 阿克忒 | |
| Mancinellus | 曼基内卢斯 | |
| Hadrianus | 哈德里亚努斯 | Do not conflate with Adran (阿德兰). |
| Lei Li | 雷利 | Phonetic rendering, not a claim about intended Chinese characters. |
| Serica / Seres | 赛里斯 | Retain distinction when source separately says Zhonguo (中国). |
| Domus Augustus | 奥古斯都宫 | Source form retained without Latin grammar correction. |
| Augusta / Augustus | 奥古斯塔 / 奥古斯都 | Gendered imperial honorifics. |

Hellanodikos is retained as 赫拉诺狄科斯（Hellanodikos）where its use as a
personal address versus a judge's title is unclear. Story-state identifiers such
as `goy` are not character names unless the visible source text actually uses them.
Do not translate internal state names into dialogue.

## Continuation glossary

| Source | Chinese | Distinction |
| --- | --- | --- |
| Lucia Sabina | 卢基娅·萨比娜 | |
| Sinue Migdue | 西努埃·米格杜埃 | |
| Yaaba | 亚阿巴 | Phonetic character name. |
| Temur | 铁木儿 | |
| Farbius / Fabius | 法尔比乌斯 / 法比乌斯 | Preserve the different source spellings. |
| Falernian wine | 法勒努姆葡萄酒 | |
| Avaritia / Avarica | 阿瓦里提娅 | Same story character in context. |
| Superbus / Superbius | 苏佩尔布斯 | Same story character in context. |
| Orchon | 奥尔孔 | |
| Tristitia | 特里斯提蒂娅 | |
| Oliverius / Oliverus | 奥利瓦里乌斯 | Same character in reviewed context. |
| Bacchus / Bachhus / Bachus | 巴克科斯 | Source spelling variants. |
| Marcus Gaius Crachius | 马尔库斯·盖乌斯·克拉基乌斯 | |
| Gravitas | 威望（Gravitas） / 威望 | Distinct from renown 声望, controversy 争议, reputation 名誉 and influence 影响力. |
| Castor et Pollux | 卡斯托尔与波吕克斯 | |
| Andraste | 安德拉斯忒 | |
| Gebeleizis | 格贝莱齐斯 | |
| Mihr / Mithras | 米赫尔 / 密特拉 | Preserve distinct names. |
| YHWH / Christus | 雅威（YHWH） / 基督 | Distinguish Chrestus/Chrestos 克瑞斯托斯. |
| Sinae / Seres | 西纳（Sinae） / 赛里斯 | Do not silently combine source peoples. |

Generated personal names are transliterated as whole displayed names. Source
ethnic pools sometimes contain unexpected names; these have not been reassigned
or historically corrected. Identical whole names may reuse a reviewed translation.
A-suffixed source variants retain their suffix. Native unit endonyms with uncertain
roles remain in the hold ledger rather than receiving meanings guessed from IDs
or equipment. Kinship terms use inclusive wording where English does not specify
a maternal/paternal side; no new genealogy is inferred.

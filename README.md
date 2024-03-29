`md_to_bgg.py` is a **[Markdown](https://en.wikipedia.org/wiki/Markdown) to [boardgamegeek.com](https://boardgamegeek.com) (BGG) markup converter** (this is the markup used in the [BGG forums](https://boardgamegeek.com/forums)).

![Markdown](Images/markdown_icon.png) to ![BGG](Images/bgg.jpg)

`md_to_bgg.py` is useful for a few reasons:

1. You can write BGG posts and have a **live preview** (through your Markdown editor).
1. Markdown is **easier to use** than the [BGG markup](https://boardgamegeek.com/wiki/page/Forum_Formatting), which is **quite verbose**.
1. The BGG markup requires **some cumbersome editing** (like when extracting the numeric identifier of a board game from its full URL), which is eschewed by `md_to_bgg.py`.
1. Markdown is a **much more common** format.

# Markdown syntax

## Standard Markdown

`md_to_bgg.py` reads texts writen in the standard [CommonMark](https://commonmark.org/help/) version of Markdown.

Many common Markdown constructs are supported:

- headers—but only levels 1 (`#`) and 2 (`##`)—,
- BGG italics (`_important_`…),
- BGG bold (`**very important**`…),
- BGG monospace (`` `inline code` ``),
- quotes (`> …`),
- lists (numbered or not),
- links (`[search engine](https://google.com)`, with the exact same syntax used for links to BGG itself).

Lists are left untouched (as the BGG markup doesn't support them), except for numbered lists, which are automatically numbered in BGG markup:
```
1. First item
1. Second item
```
will thus automatically produce:
```
1. First item
2. Second item
```

## Extended Markdown

`md_to_bgg.py` extends CommonMark Markdown so as to handle some specificities of the BGG markup.

### Strikethrough

Strikethrough text uses a double tilde: `~~…~~` (this follows the [GitHub Flavored Markdown syntax](https://github.github.com/gfm/#strikethrough-extension-)).

### Automatic link names

BGG can **automatically insert the names** of board games, forum threads, etc., which is something not handled by standard Markdown links. `md_to_bgg.py` therefore extends Markdown by **removing the link text part** (`[…]`), for links to _BGG_ contents:
```
This game is similar to (https://boardgamegeek.com/boardgame/224517/brass-birmingham).
```
will produce

> This game is similar to [Brass Birmingham](https://boardgamegeek.com/boardgame/224517/brass-birmingham).

### Images

**Images** on BGG do **not** have any **alternate text**, so this part of the Markdown syntax is similarly **removed**:
```
External image: !(https://github.com/lebigot/markdown_to_BGG/blob/main/markdown.png)
BGG image (same Markdown syntax): !(https://boardgamegeek.com/image/2355823/clockwork-wars)
```

The [**size**](https://boardgamegeek.com/wiki/page/Forum_Formatting#toc17) of a _BGG_ image can be indicated in a way reminiscent of the BGG markup:
```
Large BGG image: !(https://boardgamegeek.com/image/2355823/clockwork-wars large)
```
(the size names are the same as in [BGG markup](https://boardgamegeek.com/wiki/page/Wiki_Image_Sizes#)).

### Embedded YouTube videos

**YouTube** videos on BGG **don't have any alternate text**, so, similarly to images, their Markdown syntax has **no link text part**:
```
Nice intro to Eldritch Horror:
(https://www.youtube.com/watch?v=x-J2KzQb5lI)
```

## Raw BGG markup

Most of the BGG markup syntax is left untouched by `md_to_bgg.py`: it is therefore also possible to **directly insert many BGG markup constructs** in the Markdown source (e.g. `[q="lebigot"]…[/q]` should work unless the beginning looks like a Markdown link—`[q=…](…)…`).

## Limitations

**Some of the Markdown syntax** is not converted to BGG markup, and is instead **left essentially as is**. If you expect some of the Markdown syntax to produce some specific BGG markup which is not currently covered, don't hesitate to **open an Issue** on GitHub. In any case, **raw BGG markup** can often be used directly in the Markdown source in order to get the desired effect.

# Usage

You can convert any Markdown file directly with
```
python md_to_bgg.py your_file.md
```

`md_to_bgg.py` will **print** the rendering in BoardGameGeek markup. Under Unix, you can of course save the **result in a file** and then **paste** its contents on BGG:
```
python md_to_bgg.py your_file.md > your_file.bgg
```
On a recent enough macOS, you may also copy the BGG markup directly to the **clipboard**, for easy pasting into the BGG forums:
```
python md_to_bgg.py your_file.md | pbcopy
```

# Requirements

`md_to_bgg.py` requires Python 3.6+.

# Installation

`md_to_bgg.py` depends on the **[marko](https://github.com/frostming/marko) Markdown parser**, so you need to have it installed:
```
pip install marko
```

The `md_to_bgg.py` **script** itself can simply be **[directly downloaded](md_to_bgg.py)** (select the **"Raw" version** with the button on top).


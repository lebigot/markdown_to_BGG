`md_to_bgg.py` is a **[Markdown](https://en.wikipedia.org/wiki/Markdown) to [boardgamegeek.com](https://boardgamegeek.com) (BGG) markup converter**.

![Markdown](markdown.png | height=100) ➡️ ![BGG](bgg.jpg | height=100)

`md_to_bgg.py` is useful for a couple of reasons:

- Markdown is a **much more common** format.
- Markdown is **easier to use** than the BGG markup, which is quite verbose and requires some cumbersome editing (like when extracting the numeric identifier of a board game from its full URL).

# Markdown syntax

## Standard Markdown

`md_to_bgg.py` uses the more standard [CommonMark](https://commonmark.org) version of Markdown.

Many common Markdown constructs are supported:

- headers—but only levels 1 (`#`) and 2 (`##`)—,
- emphasis (`_important`)
- strong emphasis (`**very important**`)
- quotes (`>`),
- lists (numbered or not),
- links (`[search engine](https://google.com)`, with the exact same syntax used for links to BGG itself).

Lists are left untouched, except for numbered lists, which start from the first number:
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

BGG can automatically insert the names of board games, forum threads, etc., which is something not handled by standard Markdown links. `md_to_bgg.py` therefore extends Markdown by not requiring any link text, for links to BGG contents:
```
This game is similar to (https://boardgamegeek.com/boardgame/224517/brass-birmingham).
```

…

## Raw BGG markup

Most of the BGG markup syntax is left untouched by `md_to_bgg.py`: it is also possible to **directly insert many BGG markup constructs** in the Markdown source (e.g. `[q="lebigot"]…[/q]`). 

## Limitations

**Some of the Markdown syntax** is not converted to BGG markup, and is instead **left essentially as is**. This part of the syntax is however **probably not used often** in BGG posts. Furthermore, in most cases, the desired **raw BGG markup** can be used in the Markdown source and will be left untouched as well.

# Requirements

`md_to_bgg.py` requires Python 3.6+.

# Installation

`md_to_bgg.py` depends on the **[marko](https://github.com/frostming/marko) Markdown parser**, so you need to have it installed:
```
pip install marko
```

The `md_to_bgg.py` **script itself** can simply be **[directly downloaded](md_to_bgg.py)**.

# Usage

You can convert any file directly with
```
md_to_bgg.py your_file.md
```

`md_to_bgg.py` will **print** the rendering in BoardGameGeek markup. Under Unix, you can of course save the **result in a file**:
```
md_to_bgg.py your_file.md > your_file.bgg
```
On a recent enough macOS, you may also copy it to the **clipboard**, for easy pasting into boardgamegeek.com:
```
md_to_bgg.py your_file.md | pbcopy
```


`md_to_bgg.py` is a **[Markdown](https://en.wikipedia.org/wiki/Markdown) to [boardgamegeek.com](https://boardgamegeek.com) (BGG) markup converter**.

`md_to_bgg.py` is useful for a couple of reasons:

- Markdown is a **much more common** format.
- Markdown is **easier to use** than the BGG markup, which is quite verbose and requires some cumbersome editing (like when extracting the numeric identifier of a board game from its full URL).

# Extended Markdown

…

## Raw BGG markup

Most of the BGG markup syntax is left untouched by `md_to_bgg.py`: it is also possible to **directly insert many BGG markup constructs** in the Markdown source (e.g. `[q="lebigot"]…[/q]`). 

## Limitations

**Some of the Markdown syntax** is not converted to BGG markup, and is instead **left essentially as is**. This part of the syntax is however **probably not used often** in BGG posts.

Furthermore, in most cases, the desired **raw BGG markup** can be used in the Markdown source and will be left untouched as well.

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


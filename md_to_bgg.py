#!/usr/bin/env python

"""
Converter from markdown (CommonMark) with extensions to boardgamegeek.com (BGG) markup.

Not all markdown is converted, but many common BGG constructs are supported.

Use the -h flag for usage information.

(c) 2021 Eric O. LEBIGOT <eric.lebigot@normalesup.org>.
"""

import marko
import marko.md_renderer
from marko.inline import InlineElement

__version__ = "0.9.2"

# Regexp for an optional link text ("[link text]"):
OPT_LINK_TEXT = r'(?:\[(?P<link_text>.*?)\])?'

class Strikethrough(InlineElement):
    """
    Parse strikethrough (as in GitHub Flavored Markup).
    """
    pattern = "~~(.+?)~~"
    priority = 4
    parse_children = True


class InternalLinkLongForm(InlineElement):
    """
    Parse BGG internal links in long form.

    Example of parsed link:

    [great answer](https://boardgamegeek.com/thread/2600763/article/36994502#36994502)

    The text in front can be fully omitted (square brackets included).
    """
    pattern = OPT_LINK_TEXT + (
        # We want the _last_ link type and ID, so we do a greedy search (but
        # without bleeding onto the next link on the same line).
        # We also make provision for different possible boardgamegeek URLs 
        # (https://boardgamegeek.com, https://www.boardgamegeek.com, etc.).
        r'\(https?://.*?boardgamegeek\.com[^)\s]*'
        
        # The end of the regexp is here for links like …/article/123#123:
        r'/(?P<link_type>\S+?)/(?P<object_ID>\d+)\S*?'
        r'\)')

    parse_children = True  # We want the text to be rendered too (italics…)

    priority = 6

    def __init__(self, match):
        self.link_parts = match.groupdict()


class InternalImageLongForm(InlineElement):
    """
    Parse a BGG image in long form.

    Example:
    !(https://boardgamegeek.com/image/2355823/clockwork-wars small)

    Note the optional size at the end.
    """
    pattern = (
        r"!\("
        r"https?://\S*?boardgamegeek.com\S*?"
        r"/image/(?P<image_ID>\d+)\S*?"
        r"(?: +(?P<size>\S+))?"
        r"\)")

    # We do not want this to be parsed as "!" followed by an internal BGG link
    # (InternalLinkLongForm), because the image URL doesn't map in the same way
    # to the BGG markup (imageid=… instead of image=…):
    priority = 7

    def __init__(self, match):
        self.image_info = match.groupdict()


class ExternalImage(InlineElement):
    """
    Parse an external image.

    Example:
    !(https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png)
    """
    pattern = r"!\((?P<image_URL>\S*?)\)"

    def __init__(self, match):
        self.image_URL = match.group("image_URL")


class YouTubeLongForm(InlineElement):
    """
    Parse a full YouTube URL.

    Example:
    Have a look at this:
    (https://www.youtube.com/watch?v=x-J2KzQb5lI)
    """
    pattern = (
        r"\("
        # YouTube can have URLs like https://youtu.be…:
        r"https?://\S*?youtu\S*?"
        r"/watch\?v=(?P<video_ID>\S+?)"
        r"\)")

    def __init__(self, match):
        self.video_ID = match.group("video_ID")


def BGG_wrap(code, contents, code_value=None):
    """
    Return the given contents surrounded by the given BGG markup code.

    The output is the following BGG markup construct:

    [<code>=<code_value>]<contents>[/<code>], where the "=…" part is not
    included if code_value is None. The contents is converted to its string
    representation, if needed.
    """
    return f"[{code}{{}}]{contents}[/{code}]".format(
        "" if code_value is None else f"={code_value}")


# Marko renderer (extension):
class BGGRenderer:
    """
    Render many Markdown elements into boardgamegeek.com markup.

    Intended to be used in a marko extension to MarkdownRenderer.
    """
    # The code below is inspired by the source code for marko's
    # MarkdownRenderer:

    def render_list(self, element):
        """
        Render both ordered and unordered lists.

        Ordered lists are numbered sequentially. 
        """
        result = []
        if element.ordered:
            for (num, child) in enumerate(element.children, element.start):
                with self.container(f"{num}. ", ' '*(len(str(num))+2)):
                    result.append(self.render(child))
        else:
            for child in element.children:
                with self.container(f"{element.bullet} ", "  "):
                    result.append(self.render(child))
        self._prefix = self._second_prefix
        return "".join(result)

    def render_quote(self, element):
        return BGG_wrap("q", self.render_children(element))

    def render_heading(self, element):
        # The code is partially lifted from MarkdownRenderer.

        # There is no concept of header in BGG markup, so we simulate this by
        # using the default Large and Huge font sizes:
        size = {1: 24, 2: 18}[element.level]  # Maximum 2 levels!

        result = "".join([
            self._prefix,
            BGG_wrap("size", self.render_children(element), size),
            "\n"])

        self._prefix = self._second_prefix
        
        return result

    def render_emphasis(self, element):
        return BGG_wrap("i", self.render_children(element))

    def render_strong_emphasis(self, element):
        return BGG_wrap("b", self.render_children(element))

    def render_strikethrough(self, element):
        return BGG_wrap("-", self.render_children(element))

    def render_link(self, element):
        # Titles are not handled by the BGG markup and are therefore ignored:
        return BGG_wrap(
            "url",
            self.render_children(element),
            # The BGG Markup uses some escaping, so we may have to do some
            # escaping of the URL:
            # https://boardgamegeek.com/wiki/page/Forum_Formatting#toc17):
            marko.HTMLRenderer.escape_url(element.dest))

    def render_line_break(self, element):
        return " " if element.soft else "\n"

    # Custom BGG markdown elements:
    def render_internal_link_long_form(self, element):
        """
        Render an internal BGG link.

        The link information must be stored in the dictionary
        element.link_parts, with keys link_text (which can be None), link_type,
        object_ID.
        """
        link_parts = element.link_parts  # Shortcut

        return BGG_wrap(
            link_parts["link_type"],
            self.render_children(element),
            link_parts["object_ID"])

    def render_internal_image_long_form(self, element):
        """
        Render an internal BGG image.

        The image information must be stored in the element.image_info
        dictionary, with keys image_ID and size (which can be None, for the
        default size).
        """
        image_info = element.image_info  # Shortcut

        return "[imageid={}{}]".format(
            image_info["image_ID"],
            " " + image_info["size"] if image_info["size"] is not None
            else "")

    def render_external_image(self, element):
        """
        Render an non-BGG image.

        element.image_URL must contain the image URL.
        """
        return BGG_wrap("img", element.image_URL)

    def render_you_tube_long_form(self, element):
        """
        Render a YouTube video.

        element.video_ID must contain the YouTube ID of the video.
        """
        return f"[youtube={element.video_ID}]"

    def render_code_span(self, element):
        text = element.children
        if text.startswith("`") or text.endswith("`"):
            return f"`` {text} ``"
        return BGG_wrap("c", element.children)


# We register the BGG markdown extension: the parser and the renderer are thus
# bundled together, which makes more sense:
class BGGExtension:
    """
    marko extension for BGG markup.
    """
    elements = [
        Strikethrough, InternalLinkLongForm, InternalImageLongForm,
        ExternalImage, YouTubeLongForm]

    renderer_mixins = [BGGRenderer]


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Convert extended CommonMark markdown to boardgamegeek.com markup."
            " See https://github.com/lebigot/markdown_to_BGG for details."))
    parser.add_argument("input_file", help="Input markdown file")

    args = parser.parse_args()

    parse_and_render = marko.Markdown(
        renderer=marko.md_renderer.MarkdownRenderer, extensions=[BGGExtension])

    with open(args.input_file) as input_file:
        print(parse_and_render(input_file.read()))


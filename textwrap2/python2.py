import textwrap

class TextWrapper(textwrap.TextWrapper):
    """
    This class extends the Python 2 standard library's TextWrapper and adds an optional
    use_hyphenator to its constructor arguments.
    """

    def __init__(self, *args, **kwargs):
        self.use_hyphenator = kwargs.pop("use_hyphenator", None)
        textwrap.TextWrapper.__init__(self, *args, **kwargs)

    def _wrap_chunks(self, chunks):
        """Override the mother class method.

        Most of that method is directly copied from the original class, except
        for the part with use_hyphenator.
        """
        lines = []
        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)

        # Arrange in reverse order so items can be efficiently popped
        # from a stack of chucks.
        chunks.reverse()

        while chunks:

            # Start the list of chunks that will make up the current line.
            # cur_len is just the length of all the chunks in cur_line.
            cur_line = []
            cur_len = 0

            # Figure out which static string will prefix this line.
            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent

            # Maximum width for this line.
            width = self.width - len(indent)

            # First chunk on line is whitespace -- drop it, unless this
            # is the very beginning of the text (ie. no lines started yet).
            if self.drop_whitespace and chunks[-1].strip() == '' and lines:
                del chunks[-1]

            while chunks:
                l = len(chunks[-1])

                # Can at least squeeze this chunk onto the current line.
                if cur_len + l <= width:
                    cur_line.append(chunks.pop())
                    cur_len += l

                # Nope, this line is full.
                # But try hyphenation.
                else:
                    if self.use_hyphenator and (width - cur_len >= 2):
                        hyphenated_chunk = self.use_hyphenator.wrap(chunks[-1], width - cur_len)
                        if hyphenated_chunk:
                            cur_line.append(hyphenated_chunk[0])
                            chunks[-1] = hyphenated_chunk[1]
                    break

            # The current line is full, and the next chunk is too big to
            # fit on *any* line (not just this one).
            if chunks and len(chunks[-1]) > width:
                self._handle_long_word(chunks, cur_line, cur_len, width)

            # If the last chunk on this line is all whitespace, drop it.
            if self.drop_whitespace and cur_line and cur_line[-1].strip() == '':
                del cur_line[-1]

            # Convert current line back to a string and store it in list
            # of all lines (return value).
            if cur_line:
                lines.append(indent + ''.join(cur_line))

        return lines

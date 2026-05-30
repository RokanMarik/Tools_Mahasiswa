from models.article_data import StructuredArticleData, Chunk


class Chunker:
    """Splits long documents into chunks for section-by-section analysis.

    Thresholds (from spec §7):
    - < 5,000 words: no chunking
    - 5,000 - 20,000 words: chunk by section
    - > 20,000 words: sub-chunk per section (max_chunk_size per chunk)
    """

    def __init__(
        self,
        threshold_small: int = 5000,
        threshold_large: int = 20000,
        max_chunk_size: int = 5000,
    ):
        self.threshold_small = threshold_small
        self.threshold_large = threshold_large
        self.max_chunk_size = max_chunk_size

    def chunk(self, article: StructuredArticleData) -> StructuredArticleData:
        """Apply chunking strategy based on article word count.

        Returns the same article with chunks populated if needed.
        """
        word_count = article.word_count

        if word_count < self.threshold_small:
            return article

        chunks = []
        index = 0

        for section_name, content in article.sections.items():
            section_words = len(content.split())

            if section_words > self.max_chunk_size:
                # Sub-chunk sections that exceed max_chunk_size
                sub_chunks = self._split_text(content, section_name, index)
                chunks.extend(sub_chunks)
                index += len(sub_chunks)
            else:
                chunks.append(Chunk(section=section_name, text=content, index=index))
                index += 1

        article.add_chunks(chunks)
        return article

    def _split_text(self, text: str, section_name: str, start_index: int) -> list[Chunk]:
        """Split a large section into sub-chunks of max_chunk_size words."""
        words = text.split()
        chunks = []
        idx = start_index

        for i in range(0, len(words), self.max_chunk_size):
            sub_words = words[i : i + self.max_chunk_size]
            sub_text = " ".join(sub_words)
            chunks.append(Chunk(section=section_name, text=sub_text, index=idx))
            idx += 1

        return chunks

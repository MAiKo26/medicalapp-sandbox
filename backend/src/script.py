import time

class TokenStreamProcessor:
    """
    Enhanced Token Stream Processor that handles various edge cases.
    Processes a stream of tokens into AI data stream protocol format.
    Handles regular text, reasoning content in <think> tags, and references in <ref> tags.
    Reasoning content is processed token by token, similar to regular text.
    """
    
    def __init__(self):
        self.buffer = ""
        self.mode = "text"  # Current processing mode: "text", "reasoning", or "reference"
        self.tag_buffer = ""  # Buffer for accumulating text within tags
        self.pending_open = False  # Track if we're processing a potential opening tag
        self.pending_open_tag = ""  # Track the opening tag being built
        self.pending_close = False  # Track if we're processing a potential closing tag
        self.pending_close_tag = ""  # Track the closing tag being built
        self.current_tag_type = ""  # Track what tag we're currently processing (think/ref)
    
    def process_tokens(self, tokens):
        """
        Process a stream of tokens and yield formatted data stream parts.
        
        Args:
            tokens: An iterable of string tokens
            
        Yields:
            Formatted strings according to the AI data stream protocol
        """
        for token in tokens:

            # Handle text mode
            if self.mode == "text":
                # Check for complete opening tags
                if token == "<think" or token == "<think>":
                    self.mode = "reasoning"
                    self.tag_buffer = ""
                    continue
                elif token == "<ref>" or token.lower() == "<ref>":
                    self.mode = "reference"
                    self.tag_buffer = ""
                    continue
                
                # Check for beginning of a potential opening tag
                elif token == "<":
                    self.pending_open = True
                    self.pending_open_tag = "<"
                    continue
                elif self.pending_open and token.lower().strip() == "think":
                    self.pending_open_tag += "think"
                    self.current_tag_type = "think"
                    continue
                elif self.pending_open and token.lower().strip() == "ref":
                    self.pending_open_tag += "ref"
                    self.current_tag_type = "ref"
                    continue
                elif self.pending_open and token.strip() == ">":
                    self.pending_open_tag += ">"
                    
                    # Clean tag name for comparison
                    clean_tag = self.pending_open_tag.lower().replace(" ", "")
                    
                    # Determine which tag we've completed
                    if clean_tag == "<think>":
                        self.mode = "reasoning"
                        self.tag_buffer = ""
                    elif clean_tag == "<ref>":
                        self.mode = "reference"
                        self.tag_buffer = ""
                    else:
                        # Not a recognized tag, output it as text
                        yield f'0:"{self.pending_open_tag}"\n'
                    
                    self.pending_open = False
                    self.pending_open_tag = ""
                    self.current_tag_type = ""
                    continue
                elif self.pending_open:
                    # Not a recognized opening sequence, output accumulated tag parts
                    yield f'0:"{self.pending_open_tag}"\n'
                    self.pending_open = False
                    self.pending_open_tag = ""
                    yield f'0:"{token}"\n'
                    continue
                
                # Regular text
                yield f'0:"{token}"\n'
            
            # Handle reasoning mode - processing tokens individually
            elif self.mode == "reasoning":
                # Check for complete closing tag
                if token == "</think>" or token.lower() == "</think>":
                    self.mode = "text"
                    continue
                
                # Check for beginning of a potential closing tag
                elif token == "<":
                    self.pending_close = True
                    self.pending_close_tag = "<"
                    self.current_tag_type = "think"
                    continue
                elif self.pending_close and token.strip() == "/":
                    self.pending_close_tag += "/"
                    continue
                elif self.pending_close and token.lower().strip() == "think":
                    self.pending_close_tag += "think"
                    continue
                elif self.pending_close and token.strip() == ">":
                    self.pending_close_tag += ">"
                    
                    # If we've built a valid closing tag
                    if self.pending_close_tag.lower().replace(" ", "") == "</think>":
                        # Complete closing tag
                        self.mode = "text"
                        self.pending_close = False
                        self.pending_close_tag = ""
                        self.current_tag_type = ""
                        continue
                    
                elif self.pending_close and (token == "think>" or token.lower() == "think>"):
                    self.pending_close_tag += token
                    
                    # Complete closing tag
                    self.mode = "text"
                    self.pending_close = False
                    self.pending_close_tag = ""
                    self.current_tag_type = ""
                    continue
                elif self.pending_close:
                    # Not a recognized closing sequence, output parts as reasoning tokens
                    yield f'g:"{self.pending_close_tag}"\n'
                    yield f'g:"{token}"\n'
                    self.pending_close = False
                    self.pending_close_tag = ""
                    continue
                
                # Process each token individually in reasoning mode
                yield f'g:"{token}"\n'
            
            # Handle reference mode
            elif self.mode == "reference":
                # Check for complete closing tag
                if token == "</ref>" or token.lower() == "</ref>":
                    yield f'8:"{self.tag_buffer.strip()}"\n'
                    self.mode = "text"
                    self.tag_buffer = ""
                    continue
                
                # Check for beginning of a potential closing tag
                elif token == "<":
                    self.pending_close = True
                    self.pending_close_tag = "<"
                    self.current_tag_type = "ref"
                    continue
                elif self.pending_close and token.strip() == "/":
                    self.pending_close_tag += "/"
                    continue
                elif self.pending_close and token.lower().strip() == "ref":
                    self.pending_close_tag += "ref"
                    continue
                elif self.pending_close and token.strip() == ">":
                    self.pending_close_tag += ">"
                    
                    # If we've built a valid closing tag
                    if self.pending_close_tag.lower().replace(" ", "") == "</ref>":
                        # Complete closing tag
                        yield f'8:"{self.tag_buffer.strip()}"\n'
                        self.mode = "text"
                        self.tag_buffer = ""
                        self.pending_close = False
                        self.pending_close_tag = ""
                        self.current_tag_type = ""
                        continue
                
                elif self.pending_close and (token == "ref>" or token.lower() == "ref>"):
                    self.pending_close_tag += token
                    
                    # Complete closing tag
                    yield f'8:"{self.tag_buffer.strip()}"\n'
                    self.mode = "text"
                    self.tag_buffer = ""
                    self.pending_close = False
                    self.pending_close_tag = ""
                    self.current_tag_type = ""
                    continue
                elif self.pending_close:
                    # Not a recognized closing sequence, add to content
                    self.tag_buffer += self.pending_close_tag if not self.tag_buffer else " " + self.pending_close_tag
                    self.tag_buffer += token if not self.tag_buffer else " " + token
                    self.pending_close = False
                    self.pending_close_tag = ""
                    continue
                
                # Regular content within reference tags
                self.tag_buffer += token if not self.tag_buffer else " " + token
        
        # At the end, yield a finish message
        yield f'd:{{"finishReason":"stop","usage":{{"promptTokens":0,"completionTokens":0}}}}\n'

# Example usage
def example_usage():
    # Example token stream with separate tag parts and edge cases
    tokens = [
        # Basic text
        "hello", "world", "i'", "am", "the", "world", "smartest", "man",

        "<think","world",">"
        
        # Reasoning tag with split tokens
        "<think", ">", "some", "reasoning", "here", "<", "/", "think>",
        
        # More regular text
        "and", "i", "can", "jump", "20", "meters",
        
        # Reference tag as a single token
        "<ref>", "some", "reference", "here", "</ref>",
        
        # Reference tag as separate tokens with spaces
        "<", " ref ", ">", "another", "ref", "here", "<", " / ", " ref ", " >",
        
        # Regular tokens again 
        "and", "i", "can", "drink", "9999", "leters", "of", "water",
        
        # HTML-like content that should be treated as regular text
        "<", "div", ">", "some", "html", "here", "<", "/", "div", ">",
        
        # Another reference tag with joined tokens
        "<ref>", "hello", "world", "<", "/", "ref", ">and", "finally", "normal", "text",
        
        # Edge cases: case sensitivity
        "<Ref>", "case", "</REF>",
        
        # Edge cases: whitespace in tags
        "< ref >", "spacey", "</ ref >",
        
        # Edge cases: linebreaks in tags
        "<ref\n>", "linebreak", "</ref\n>",
        
        # Edge cases: escaped tags
        "\\<ref\\>", "not actually a tag", "\\</ref\\>",
        
        # Edge cases: nested or malformed tags
        "content", "</ref", "</</ref>>", "<>", "empty", "</>", "<réf>", "unicode", "</réf>", "text", "< not a tag >", "<ref>", "yes",
        
        # Edge cases: tags with attributes
        '<ref id="1">', "has-attr", "</ref>",
        
        # Edge cases: HTML comments
        "<!--", "comment", "-->",
        
        # Edge case: just one token that's a reference
        "inside",
        
        # Edge case: very long token
        "x " * 50
    ]
    
    processor = TokenStreamProcessor()
    for output in processor.process_tokens(tokens):
        print(output, end="")

if __name__ == "__main__":
    example_usage()
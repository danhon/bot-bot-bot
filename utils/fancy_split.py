import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

# Ensure necessary NLTK resources are available
nltk.download('punkt')

# Your input text
text = r"\ST:GD s82e13 - \"Andros III\". On Andros III, former Ensign D'Erika strives to replace their standard Federation colony residential unit with a thoroughly exacting boridium-framed eighty-three-story residential pod using locally recycled nanopolymer. But six years in, the thermal concrete-based foundation has spontaneously degraded, and the fitting of a tritanium-infused holo-emitter requires an unexpected amount of beritium, yttrium, francium as well as countless other kinds of things that will make this sentence go over the character limit for a chunk. What will they do, and will Evora-sourced diamide be the solution? Will they do something that will be more than 250 characters but under 260 characters? Will the sentence over 230 and under 260? Will this complete number of sentences be a good test case for our evil purposes? Who can say whether it will be, because this sentence will need to be split across into the next chunk."

# Tokenize the text into sentences
sentences = sent_tokenize(text)

# Initialize variables to hold chunks and the current chunk
chunks = []
current_chunk = ""

# Function to split text into chunks
for sentence in sentences:
    # Add the sentence to the current chunk
    if len(current_chunk) + len(sentence) <= 260:
        current_chunk += " " + sentence.strip()
    else:
        # If adding the sentence exceeds the limit, check if the current chunk is valid
        if 230 <= len(current_chunk) <= 260:
            chunks.append(current_chunk.strip())
            current_chunk = sentence.strip()
        else:
            # Split the sentence at word boundaries if it's too long
            words = word_tokenize(sentence)
            while len(" ".join(words)) > 260:
                # Find a point where the chunk is less than 260 characters
                temp_chunk = ""
                while words and len(temp_chunk) + len(words[0]) + 1 <= 260:
                    temp_chunk += " " + words.pop(0)
                chunks.append(temp_chunk.strip())
            # Add any remaining part of the sentence
            current_chunk = " ".join(words)

# Don't forget to add the last chunk if it's valid
if 230 <= len(current_chunk) <= 260:
    chunks.append(current_chunk.strip())

# Output the result
for i, chunk in enumerate(chunks, 1):
    print(f"Chunk {i} (length {len(chunk)} characters):")
    print(chunk)
    print()


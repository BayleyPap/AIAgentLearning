---
tags: concept
related: []
---
# Tokenisation and Embeddings

## In One Sentence
**Tokenisation** — splitting raw text into tokens (commonly via BPE), 
converting them into integer IDs so the model can process them mathematically.

**Embeddings** — each token ID is mapped via a lookup table to a vector 
(array of floats) that encodes how similar that token is to every other 
token, enabling rich mathematical manipulation.

## How It Works

### Tokenisation
Raw text cannot be fed directly into a neural network — it needs to be 
converted into numbers first. Tokenisation is that conversion:

1. Split the text into units called tokens
2. Assign each unique token an integer ID
3. The model works with those integers from here on

Tokens are not always whole words. In practice they are subwords — common words get their own token, rare words get split into pieces:

- "playing"  →  ["play", "ing"]
- "unhappiness" →  ["un", "happiness"]
- "ChatGPT" →  ["Chat", "G", "PT"]

This is why models sometimes struggle with unusual names or made-up words — they get split into chunks the model has to reassemble.

### Byte Pair Encoding (BPE)
The most common tokenisation strategy. The algorithm:

1. Start with individual characters as the entire vocabulary
2. Count every adjacent pair of tokens in the training text
3. Merge the most frequent pair into a single new token
4. Repeat until the vocabulary reaches the target size (e.g. 50,000 tokens)

The result is a vocabulary where common words and word fragments get their own token, and rare combinations get split into smaller pieces. GPT-4 uses ~100,000 tokens. Llama 3 uses ~128,000.

### Embeddings
Once a token has an integer ID, that integer gets looked up in a learned table — the **embedding matrix**. Each row of the table is a vector of floats (typically 512–4096 numbers depending on model size):
```
Token ID 42  →  [0.23, -1.4, 0.87, 0.02, -0.55, ...]  # 512+ floats
Token ID 43  →  [-0.91, 0.34, 1.2, -0.67, 0.44, ...]
```

These vectors are not hand-crafted — they are learned during training. 
Tokens that appear in similar contexts end up with similar vectors. This 
means mathematical relationships emerge naturally:

- "king" and "queen" end up with similar vectors
- "Paris" and "France" end up closer to each other than either is to "banana"
- Arithmetic on vectors can encode meaning: king - man + woman ≈ queen

### Why Not Just Use The Integer?
An integer encodes only identity — token 42 is just "token 42." There is 
no relationship between 42 and 43, no sense of similarity or difference.

A vector encodes **relationship**. Because it has hundreds of dimensions, 
it can simultaneously capture:
- Semantic similarity (dog and puppy are close)
- Syntactic role (running and jumping are both verbs)
- Topic (king, queen, throne cluster together)
- Many other learned dimensions we don't have names for

This richness is what makes mathematical operations on language possible.

## Why It Matters for AI Agents

Tokenisation and embedding are the entry point for every input into an LLM. Understanding them has direct practical consequences for agent design:

- **Context window limits are measured in tokens, not words or characters.** 
  "4096 token context" means ~3000 words. Knowing this helps you design chunking strategies for RAG pipelines.
- **Tokenisation cost affects API pricing.** Cloud APIs charge per token — understanding how your text tokenises helps you manage costs.
- **Rare words, code, and non-English text tokenise inefficiently** — they use more tokens per character, eating context window faster.
- **Embedding similarity is the foundation of vector search** — the 
  retrieval step in every RAG pipeline is just finding vectors closest 
  to the query vector.

## Common Misconceptions

- **"Tokens are words"** — they are subwords. "unhappiness" is likely 2-3 tokens not one.
- **"The embedding is fixed"** — it is learned and updates during training. The lookup table at inference time is the result of that learning.
- **"Longer text = more understanding"** — more tokens means more context but also more compute and eventually hitting the context window limit.
- **"All models use the same tokeniser"** — they don't. Llama and GPT-4 have different vocabularies. A token in one model is not the same as a token in another.

## Related Concepts
- [[Transformer Architecture]]
- [[Attention Mechanism]]
- [[Context Windows]]
- [[Inference Pipeline]]
- [[RAG Pipeline]]  

## Code Example
```python
import torch
import torch.nn as nn

vocab_size = 65    # number of unique tokens (characters in Karpathy's example)
n_embd     = 384   # embedding dimension - how many floats per token vector

# The embedding table - this IS the lookup table
# Shape: (vocab_size, n_embd) = (65, 384)
# Each row is one token's vector representation
embedding_table = nn.Embedding(vocab_size, n_embd)

# Example: convert token IDs to vectors
token_ids = torch.tensor([15, 32, 7, 42])   # four token IDs
vectors   = embedding_table(token_ids)       # lookup each ID
print(vectors.shape)                         # (4, 384) - four vectors of 384 floats

# This is exactly what happens at the start of every forward pass
# before attention or feedforward see anything
```

## Sources
- Karpathy — 'Let's Build GPT from Scratch'
  youtube.com/watch?v=kCc8FmEb1nY
- 3Blue1Brown — 'But what is a GPT? Visual intro to transformers'  
  youtube.com/watch?v=LPZh9BOjkQs
- Hugging Face — Tokenisers documentation
  huggingface.co/docs/transformers/tokenizer_summary
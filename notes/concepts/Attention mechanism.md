---
tags: concept
related: []
---
# Attention Mechanism

## In One Sentence
A mechanism that allows each token to decide which other tokens in the context are most relevant to it and gather information from those tokens proportionally to their relevance.

## The Problem It Solves
Without attention a model has no way to understand relationships between tokens. The naive solution — averaging all previous token representations equally — treats every token as equally important regardless of relevance.

Attention fixes this by letting each token ask: "which other tokens in this context actually matter to me right now?" and weighting its gathered information accordingly.

The result is that "it" in "the animal didn't cross the street because it 
was too tired" can learn to attend strongly to "animal" and weakly to 
"street" — purely from training, no rules hardcoded.

## How It Works

### Query, Key, Value
Every token produces three vectors through learned linear projections:

- **Query** — what am I looking for?
- **Key** — what do I contain?
- **Value** — what do I share when someone attends to me?

Key and query handle the relevance calculation — they decide *who* should attend to *whom*. Value determines *what information* gets passed once that relevance is established. These are independent — a token can be highly relevant (high key/query match) but share different information via its value.

### Affinity Score
Relevance between two tokens is measured using the **dot product** of one token's query against another token's key:
```
affinity(i, j) = query[i] · key[j]
```

The dot product measures similarity — two vectors pointing in the same direction produce a high score, two pointing in opposite directions produce a low or negative score. High affinity = token j is relevant to token i. Low affinity = not relevant.

This produces a full grid of scores — every token's relevance to every 
other token:
```
          token0  token1  token2  token3
token0:   0.8     —       —       —       (can't see future)
token1:   0.3     0.9     —       —
token2:   0.7     0.2     0.8     —
token3:   0.1     0.6     0.4     0.9
```

### Scaling
Raw dot products grow large as vector dimensions increase — large values cause softmax to produce near-zero gradients and the model stops learning effectively.

The fix is to divide by the square root of the head size:
```
affinity = (query · key) / √head_size
```

This keeps values in a stable range regardless of how large the model is.

### Masking
Language models predict the next token — they must not be allowed to look at future tokens during training or inference. Future positions are set to `-inf` before softmax:
```python
wei = wei.masked_fill(tril == 0, float('-inf'))
```

Softmax converts `-inf` to exactly `0.0` — future tokens receive zero 
attention automatically. Clean and mathematically elegant.

### Softmax
Raw affinity scores are converted into probabilities that sum to 1.0:
```python
wei = F.softmax(wei, dim=-1)
```

These are now **attention weights** — the percentage of attention each 
token pays to each past token. A token might distribute its attention as:
```
token0: 0.05   (barely relevant)
token1: 0.60   (very relevant)
token2: 0.30   (somewhat relevant)
token3: 0.05   (barely relevant)
```

These weights are then applied to the value vectors — tokens with high 
attention weights contribute more to the output.

### Multi-Head Attention
A single attention head learns one type of relationship. Language has many simultaneous relationship types — grammatical, semantic, positional, syntactic. Multiple heads run in parallel, each specialising in different patterns.

Each head works with a smaller slice of the embedding dimension 
(head_size = n_embd / num_heads). Their outputs are concatenated and projected back to the original dimension:
```
4 heads × head_size 8  →  concatenate  →  (B, T, 32)  →  project  →  (B, T, 32)
```

The result is a single rich representation combining all perspectives.

## Why It Matters for AI Agents
- **Context length understanding** — attention operates across the entire context window. Understanding it explains why longer contexts are more expensive — attention is O(n²) in sequence length. Double the context, quadruple the attention computation.
- **Prompt engineering** — knowing that tokens attend to relevant context explains why clear, specific prompts work better. You are shaping what the model attends to.
- **RAG design** — retrieved chunks need to be relevant because the model attends to what's in context. Irrelevant chunks dilute attention.
- **Model selection** — different models have different context windows and attention implementations. Knowing the mechanism helps you reason about tradeoffs.

## Common Misconceptions
- **"Attention finds meaning"** — it finds statistical relevance between 
  tokens. Meaning is an emergent property across many layers, not something a single attention operation produces.
- **"The model reads left to right like a human"** — attention processes all tokens simultaneously. Every token can directly attend to every past token in one operation.
- **"More heads is always better"** — heads divide the embedding dimension so more heads means smaller head size. There are tradeoffs. Architecture choices matter.
- **"Attention is the whole transformer"** — attention handles communication between tokens. The feedforward network handles per-token computation. Both are necessary.

## Related Concepts
- [[Transformer Architecture]]
- [[Tokenisation and Embeddings]]
- [[Residual Connections]]
- [[Layer Normalisation]]
- [[Context Windows]]
- [[Inference Pipeline]]

## Code Example
```python
import torch
import torch.nn as nn
import torch.nn.functional as F

# Single attention head - the building block
class Head(nn.Module):
    def __init__(self, n_embd, head_size, block_size, dropout):
        super().__init__()
        self.key   = nn.Linear(n_embd, head_size, bias=False)  # what I contain
        self.query = nn.Linear(n_embd, head_size, bias=False)  # what I look for
        self.value = nn.Linear(n_embd, head_size, bias=False)  # what I share
        # Mask - lower triangular so tokens only see the past
        self.register_buffer('tril', torch.tril(torch.ones(block_size, block_size)))
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        B, T, C = x.shape
        k = self.key(x)    # (B, T, head_size)
        q = self.query(x)  # (B, T, head_size)

        # Affinity scores - how relevant is every token to every other token
        wei = q @ k.transpose(-2, -1) * C**-0.5  # scale by √head_size
        # Mask future tokens - set to -inf so softmax makes them 0.0
        wei = wei.masked_fill(self.tril[:T,:T] == 0, float('-inf'))
        # Convert scores to attention weights (probabilities summing to 1.0)
        wei = F.softmax(wei, dim=-1)
        wei = self.dropout(wei)

        # Apply attention weights to values
        v = self.value(x)  # (B, T, head_size)
        return wei @ v     # (B, T, head_size) - context-aware token representations

# Multi-head attention - multiple heads in parallel
class MultiHeadAttention(nn.Module):
    def __init__(self, num_heads, head_size, n_embd, block_size, dropout):
        super().__init__()
        self.heads = nn.ModuleList([
            Head(n_embd, head_size, block_size, dropout) 
            for _ in range(num_heads)
        ])
        self.proj    = nn.Linear(n_embd, n_embd)  # project back to embedding dim
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # Each head runs independently on the full sequence
        out = torch.cat([h(x) for h in self.heads], dim=-1)
        # Concatenate and project - combines all perspectives
        return self.dropout(self.proj(out))
```

## Sources
- Karpathy — 'Let's Build GPT from Scratch'
  youtube.com/watch?v=kCc8FmEb1nY
- 3Blue1Brown — 'But what is a GPT? Visual intro to transformers'
  youtube.com/watch?v=LPZh9BOjkQs
- Vaswani et al. — 'Attention Is All You Need' (2017)
  arxiv.org/abs/1706.03762
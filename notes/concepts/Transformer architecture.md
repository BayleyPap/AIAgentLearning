---
tags: concept
related: []
---
# Transformer architecture
## In One Sentence
A neural network architecture that processes sequences of tokens and uses attention to learn how every token in the sequence relates to every other token.

## How It Works

1. **Tokenisation** — raw text is split into tokens (characters or subwords) and converted to integers. Every token gets an ID.

2. **Embedding** — each token ID is looked up in a learned table and converted into a vector (a list of numbers). This vector is a rich numerical representation of the token that can be mathematically manipulated. The richer the embedding, the more the model can express about each token.

3. **Positional Encoding** — because the transformer processes all tokens simultaneously (not sequentially), it has no inherent sense of order. A positional vector is *added* to each token's embedding so the model knows token 1 came before token 2.

4. **Multi-Head Attention** — the core mechanism. Each token produces three vectors:
   - **Query** — what am I looking for?
   - **Key** — what do I contain?
   - **Value** — what do I share when attended to?
   
   Affinity (relevance) between tokens is calculated as the dot product of query × key. High score = relevant. These scores are masked so tokens can only attend to past tokens, then normalised via softmax into attention weights. Those weights are applied to the value vectors to produce a context-aware output.
   
   Multiple heads run in parallel, each learning different types of
   relationships (grammatical, semantic, positional etc).

4. **Feedforward Network** — after attention has gathered context, each token's representation passes through a small independent neural network. Attention gathers information, the feedforward network processes it.

5. **Layer Normalisation** — keeps values well behaved as they flow through the network. Prevents values from exploding or vanishing in deep stacks.

6. **Stacking** — one attention + feedforward block is a single transformer layer. These get stacked (GPT-2 has 12, GPT-3 has 96). Each layer refines the token representations further.

## Data Flow
Input text → tokenise → embed → add positional encoding →
[attention → feedforward] × N layers →
project to vocabulary size → softmax → sample next token

## Why It Matters for AI Agents
Every LLM you will use in this roadmap — LLaMA, Mistral, Phi-4, and the
commercial APIs — is a transformer or a direct variant. Understanding this
architecture means you understand the foundation of every model you will
prompt, benchmark, and deploy. It also makes debugging model behaviour
(context limits, attention patterns, temperature effects) intuitive rather
than mysterious.

## Common Misconceptions
- **"Transformers read text like humans do"** — they don't. They process all
  tokens simultaneously, not sequentially left to right.
- **"Bigger always means better"** — scale helps but the architecture,
  training data quality, and fine-tuning matter just as much.
- **"The model understands language"** — it learns statistical relationships
  between tokens. Understanding is a philosophical debate, not a technical one.
- **"Attention finds the meaning of words"** — attention finds relevance
  between tokens. Meaning is an emergent property of many layers of this.

## Related Concepts
- [[Attention Mechanism]]
- [[Tokenisation and Embeddings]]
- [[Positional Encoding]]
- [[Inference Pipeline]]
- [[Context Windows]]
- [[Sampling Parameters]]

## Code Example
```python
# The core attention calculation in one block
# This is the mathematical heart of every transformer

import torch
import torch.nn.functional as F

B, T, C = 4, 8, 16  # batch, time (sequence length), channels (embedding dim)
head_size = 8

x = torch.randn(B, T, C)  # input token embeddings

# Three learned projections
key   = torch.nn.Linear(C, head_size, bias=False)
query = torch.nn.Linear(C, head_size, bias=False)
value = torch.nn.Linear(C, head_size, bias=False)

k = key(x)    # (B, T, H) - what each token contains
q = query(x)  # (B, T, H) - what each token is looking for

# Compute affinities (relevance scores between all token pairs)
wei = q @ k.transpose(-2, -1) * C**-0.5  # (B, T, T) - scaled dot product

# Mask future tokens - model can only look at the past
tril = torch.tril(torch.ones(T, T))
wei = wei.masked_fill(tril == 0, float('-inf'))

# Convert scores to attention weights (probabilities)
wei = F.softmax(wei, dim=-1)  # -inf becomes 0.0

# Apply attention weights to values
v = value(x)   # (B, T, H) - what each token shares
out = wei @ v  # (B, T, H) - context-aware token representations
```

## Sources
- Vaswani et al. — "Attention Is All You Need" (2017) arxiv.org/abs/1706.03762
- Karpathy — "Let's Build GPT from Scratch" youtube.com/watch?v=kCc8FmEb1nY
- 3Blue1Brown — "But what is a GPT?" youtube.com/watch?v=LPZh9BOjkQs
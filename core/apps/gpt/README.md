# ⚠️ HARQIS-core OpenAI Integration (DEPRECATED)

> **Status:** Deprecated  
> **Effective Date:** 2026-03  
> **Replacement:** `BaseApiServiceAnthropic` and future multi-provider LLM abstraction layer  

---

## 📌 Overview

This module previously handled the integration of OpenAI GPT capabilities into the HARQIS-core platform.

It provided:
- Communication with the OpenAI API
- Assistant abstractions
- Response handling and processing

⚠️ This module is **no longer actively maintained** and will be **removed in a future release**.

---

## ❗ Deprecation Reason

This module is deprecated due to:

- Migration to **provider-agnostic LLM architecture**
- Adoption of **Anthropic Claude SDK**
- Need for:
  - better async support
  - structured message handling
  - multi-provider extensibility (OpenAI, Claude, others)
- remove as core module
---

## 🚀 Recommended Replacement

Use the new service layer:

- `BaseApiServiceAnthropic`
- Future: `BaseApiServiceLLM` (multi-provider abstraction)

### Migration Example

**Before (OpenAI):**
```python
response = openai_service.send_prompt("Generate test cases")
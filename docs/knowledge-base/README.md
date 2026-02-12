# Knowledge Base

Central repository untuk semua dokumentasi produk dan technical guides.

## 📂 Structure

```
knowledge-base/
├── README.md              # This file
├── chronicle/             # Chronicle product documentation
│   ├── README.md
│   ├── flow.md           # Product flow & architecture
│   ├── features.md       # Features documentation
│   └── faq.md            # Frequently asked questions
└── [future]/             # Additional products/topics
```

## 🎯 Products & Topics

### Chronicle
**Path**: [`chronicle/`](chronicle/)

Dokumentasi lengkap tentang Chronicle product:
- Product flow dan arsitektur
- Feature documentation
- FAQ

**Keywords untuk AI**: `chronicle flow`, `cara kerja chronicle`, `fitur chronicle`, `knowledge base chronicle`

---

## 🤖 Cara Menggunakan dengan AI

### Auto-detect (Recommended)
AI akan otomatis detect dari keywords:
```
User: "bagaimana cara kerja chronicle?"
AI: [loads KNOWLEDGE persona → reads chronicle/flow.md]
```

### Manual Mode
Force KNOWLEDGE persona:
```
User: "mode knowledge"
AI: "✅ Switched to Knowledge mode"

User: "explain chronicle features"
AI: [reads chronicle/features.md]
```

---

## 📝 Adding New Documentation

### For New Product
1. Create new directory: `knowledge-base/[product-name]/`
2. Add README.md with product overview
3. Add documentation files (flow.md, features.md, faq.md, etc.)
4. Update this main README with product info
5. Update `persona/KNOWLEDGE.md` with new keywords if needed

### For Existing Product
1. Navigate to product directory
2. Add or update documentation files
3. Update product README if structure changes

---

## 🔍 Search Tips

AI can search across all knowledge base:
- **Specific product**: "cari di chronicle knowledge base tentang [topic]"
- **All products**: "search knowledge base untuk [topic]"

---

## 📋 Documentation Standards

### File Naming
- Use lowercase with hyphens: `feature-name.md`
- Use descriptive names: `authentication-flow.md` not `auth.md`

### Content Structure
```markdown
# [Topic Title]

## Overview
Brief description

## Details
Detailed explanation with examples

## Use Cases
Practical examples

## Related Topics
Links to related docs
```

### Language
- **Bahasa Indonesia** untuk user-facing documentation
- Include English terms in parentheses for technical terms
- Use examples and practical scenarios

---

## 🚀 Quick Links

- [Chronicle Documentation](chronicle/) - Chronicle product docs
- [KNOWLEDGE Persona](../../persona/KNOWLEDGE.md) - AI persona for knowledge base queries
- [CONTEXT.md](../../CONTEXT.md) - Context routing system

---

**Last Updated**: 2026-02-12

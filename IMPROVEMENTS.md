# Technical Debt & Improvements

## Current Architecture Notes

### Email Connector (core/email/)

**Status**: Initial implementation complete (2024-12-02)

**Architecture Decisions**:
- Provider-agnostic interface following SOLID principles
- Strategy pattern for classifiers (rule-based, ML, LLM)
- Factory pattern for connector instantiation
- Context manager protocol for resource management

**Dependencies**:
- `msal` - Microsoft Authentication Library for Outlook
- `httpx` - HTTP client for API calls

**Future Improvements**:

1. **Additional Providers** (Priority: Medium)
   - [ ] Gmail connector using Google API
   - [ ] Generic IMAP connector for other providers

2. **ML Classifier** (Priority: High)
   - [ ] Implement scikit-learn based classifier
   - [ ] Add training pipeline with labeled data

3. **LLM Classifier** (Priority: Medium)
   - [ ] Implement LLM-based classifier using existing agents infrastructure
   - [ ] Consider using `jarvis/` agent for classification

4. **Batch Operations** (Priority: Low)
   - [ ] Implement MS Graph batch API support in OutlookConnector
   - [ ] Optimize bulk message operations

5. **Caching** (Priority: Medium)
   - [ ] Add folder list caching
   - [ ] Consider message caching for offline access

6. **Testing** (Priority: High)
   - [ ] Unit tests for interfaces
   - [ ] Integration tests with mock Graph API
   - [ ] Property-based tests for classifiers

---

## Other Areas

*Add other technical debt items here*

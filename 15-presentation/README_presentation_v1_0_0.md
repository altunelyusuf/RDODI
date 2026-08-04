# Presentation Layer v1.0.0 — domain-general, profile-driven, provenance-aware renderer
`rdodi_presentation_renderer_v1_0_0.py <page_abox> <document_abox> <domain_tbox> <out.html>`

Renders a gate-passing interactive-page ABox to rich HTML. Reads ONLY generic page/document/prov vocabulary;
resolves domain IRIs by local name — hardcodes NO domain (supersedes the SCP-specific html generator). Genre
on the page drives layout/theme; the prov chain is surfaced as honest provenance, and ungrounded regions are
shown as ungrounded (presentation never masks thin/unsourced content — L-66).

## Proof (same domain, two profiles, distinct outputs)
- course-companion: 7 regions, 7/7 grounded, genre course-document.
- technical-report: 8 regions, 8/8 grounded, genre technical-report.
Requires generator v2.4.1 (emits genre on the page surface) so the renderer is profile-driven, not defaulted.

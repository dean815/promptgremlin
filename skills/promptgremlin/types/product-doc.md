---
type: product-doc
default_target: claude-ai
---
# product-doc: PRD, spec, roadmap, one-pager, stakeholder update

## Slots
1. **audience and decision** (high): who reads it and what they decide or do.
2. **problem and evidence** (high): the problem in one line and what the
   person already knows (data, customer quotes). Never invented: unknown
   evidence becomes a marked gap in the doc.
3. **scope** (high): what's in v1, what's explicitly out, which questions to
   leave open. Offer candidate in/out items from the request.
4. **format and length** (medium): their template, or a standard one; page or
   word limit.
5. **success metrics** (medium): known targets, or "propose and mark as
   proposed".
6. **product context** (low): what the product is, users, stage.

## Prompt skeleton
Product and situation → audience and the decision → problem and evidence →
scope in/out/open → required sections → metrics → length → "mark anything
you had to assume" → stop line.

## Type guidance
- Docs drift into generic filler when the audience and decision aren't named.
- Require proposed numbers to be labelled as proposals.
- Keep open questions open instead of letting the writer resolve them.

## Sources
Vendor long-document writing guidance; slot list carries most of it.

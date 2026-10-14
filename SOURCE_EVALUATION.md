# Free entry-data evaluation — 14 October 2026

The new reference is an independent compilation, not a personalized immigration decision. Its publisher's check dates are not independent Restrictapp verification.

| Source | Evaluation | Integration decision |
| --- | --- | --- |
| [TravelRequirements.info](https://travelrequirements.info/en/data/) | CC BY 4.0; source URLs, check dates, row/policy evidence, and explicit uncertainty flags. Direct download returned HTTP 403; the publisher's repository was accessible. | Pinned, attributed reference snapshot with conservative category filters. |
| [GOV.UK Content API](https://content-api.publishing.service.gov.uk/) | Public JSON; entry guidance generally has British-passport scope. | Existing live guidance retained, with scope and separate publication/retrieval dates. |
| [Passport Index dataset](https://github.com/imorte/passport-index-data) | Declares MIT licensing and Passport Index scraping; README last update 17 February 2026. Less detailed official evidence. | Not used for runtime requirements. |
| [DoINeedVisa](https://doineedvisa.to/docs) | Free 300-request monthly tier requires an emailed API-key request. Core matrix uses the preceding Passport Index dataset; purpose queries are paid. | Not connected: shared data would not be independent corroboration. No account or email request sent. |

## Audit evidence

Publisher repository: https://github.com/travel-requirements/entry-requirements. Imported commit `e7eb38249a6815781dee50e24ece14946a60c9e1`, version 1.3.0.

Structurally inspected 199 destination records and 39,601 rows. The publisher marks 2,945 rows unconfirmed. Resolved source objects flag 3,697 rows as unverifiable, 816 as conflicting, and 1,319 as portal-only; counts overlap and count rows, not unique sources.

Across 37,636 mapped catalog pairs on 14 October, 21,417 pass the category display filters and 16,219 return links only. These are adapter outcomes, not verified-rule counts.

Two baseline samples were compared with official material: German passports appear on [Japan's exemption list](https://www.mofa.go.jp/j_info/visit/visa/short/novisa.html); Nigerian passports appear in the [UK visitor visa-national list](https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-visitor-visa-national-list). Conditions and exceptions still apply. This small consistency check does not audit every row or establish individual eligibility.

## Display policy and limitations

- Display categories as **dataset-reported**, showing source URLs, publisher check dates, snapshot import time, and passport-row versus destination-policy evidence scope.
- Withhold categories for unconfirmed or unknown classifications; unverifiable, conflicting, or portal-only sources; unsuitable source URL/date/type; future verification dates; checks older than seven days; rules expired before departure; and purposes other than short-stay tourism. Seven days is an app threshold, not a guarantee of current rules.
- Retain safe HTTPS source links when withholding a category. Unsupported destinations or missing snapshots use the existing authority links and official advice directory.
- Residence permits, existing visas, passport type, duration, transit eligibility, and future rule changes are not resolved. Residence country alone does not prove a permit. Some citations are another government's advice; recorded source labels do not establish correctness.
- Stay allowances, fees, health requirements, and passport-validity rules are not inferred from the visa category. Missing research is not treated as no requirement.
- No traveler data is sent to the dataset publisher. Reference results use the local snapshot. Checklist completion remains self-reported.
- No automatic dataset refresh is enabled. Old checks automatically become links-only results. A new snapshot needs a reviewed import.

## Refresh

Download or update the publisher's public repository in the ignored `api/data/travelrequirements-source` directory, review the new commit and licence, then run:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts/import_entry_dataset.py api/data/travelrequirements-source
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The importer reads JSON and never executes upstream code or accesses the network. It atomically writes a compressed snapshot with import time and commit identity, plus the publisher's licence and notice. Attribution states that Restrictapp selects and filters fields. Updating the source checkout is a separate explicit step.

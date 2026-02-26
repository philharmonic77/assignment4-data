# 2. Filtering Common Crawl
## 2.1 Looking at the data
### Problem (look_at_cc): 4 points
(a) The URL of the first web page is http://0371rykj.com/ipfhsb/34.html. The domain does not appear to be reliably accessible anymore and is likely inactive or unstable. Based on the raw HTML, the page appears to be a Chinese industrial company website advertising environmental testing equipment. The company name is 上海林頻儀器股份有限公司.

(b) The extracted WET text includes navigation menus, contact information, and injected spam keywords that are not part of the page’s main content. Ideally, such boilerplate and irrelevant spam text should have been filtered out. Training on this kind of data could cause a model to learn low-quality or harmful phrases instead of coherent natural language. 

(c) This example could be useful for training a model in the domain of industrial equipment marketing or Chinese business websites, where learning product terminology and commercial language is relevant. However, it would be less suitable for applications such as educational or general-purpose conversational models.

(4) It took approximately **3–5** examples before encountering a clearly high-quality webpage.

| #  | Language | Domain | Page Type | Quality (High/Low) | Notes |
|----|----------|--------|-----------|--------------------|-------|
| 1 | zh | 0371rykj.com | Industrial product page | Low | Spam keywords at top; template-heavy content; includes phone numbers. |
| 2 | zh | chinatikfans.com | Fan forum blog | Medium | Informal posts about TV shows and subtitled videos; contains forum structure and metadata. |
| 3 | en | 13.usnccm.org | Conference website | High | Clear academic content with structured information about a computational mechanics congress. |
| 4 | zh | 176.utchat888.com | Pornographic chat platform | Low | Explicit sexual keywords and heavy repetition; primarily commercial/login content. |
| 5 | zh | 176766.cn | Technical support article | Low | Legitimate technical content mixed with heavy pornographic keyword spam at the end. |
| 6 | zh | 178mh.com | Error page / missing template | Low | Only contains short error message ("detail.html template does not exist"); no meaningful content. |
| 7 | zh | 1796370.tgtg97.com | Porn spam page | Low | Massive repetition of adult-related keywords; purely SEO-driven with no meaningful narrative content. |
| 8 | zh | 18sex.v340.info | Porn livestream portal | Low | Membership-based adult video chat page with pricing info and rankings; heavily commercial and low informational value. |
| 9 | nld | 1kb.klimtoren.be | Elementary school blog | High | Short Dutch blog post about a child’s birthday; natural language and normal blog layout. |
| 10 | ell | mysch.gr | Education support forum | High | Greek helpdesk page for distance learning; mostly UI/search interface text, but legitimate institutional site. |
| 11 | ell | mysch.gr | Forum login page | Medium | Greek education helpdesk login interface; valid site but primarily boilerplate UI content. |
| 12 | zh | yhxzseo.com | Betting app promo page | Low | Gambling-related promotional content wrapped in fake editorial structure; SEO and traffic diversion page. |
| 13 | tur | 20com20.fr | Apache documentation sitemap | High | Turkish-language Apache HTTP Server documentation index page; legitimate technical reference content. |
| 14 | eng | 24ktcasino.net | Casino blog post | Low | Gambling-focused blog content likely aimed at SEO/affiliate traffic; commercial and low informational value. |
| 15 | zh | yizhangting.com | Lottery promo SEO page | Low | Gambling/lottery promotional content wrapped in fake health-site structure; SEO-driven and commercially manipulative. |

### Problem (extract_text): 3 points
(a) [extract_text function](cs336_data/utils.py) 

(b) Each time you run this [script](scripts/sample_warc.py), it returns a randomly selected HTML extraction and the matching WET output.

The WET extraction presents the text in a flattened format, whereas my extraction retains more explicit structural cues such as bullet points and grouped list items. Both outputs include substantial navigation and boilerplate content, but they differ in how much of the original layout structure is preserved. The choice of which is better may depend on whether structural cues are useful for downstream tasks.

### Problem (language_identification): 6 points
(a) [language_identification function](cs336_data/utils.py) 

(b)	
Issues: 

• **Skewed language distribution**: Misclassification can remove valid target-language data or include unintended languages, leading to imbalanced training and weaker performance in some languages.  

• **Unstable language generation**: Incorrect handling of multilingual or mixed-language texts may cause the model to produce unintended language switching at inference time.  

Suggestions: 

• **Set confidence thresholds**: Keep only documents with high language identification confidence, and discard or separately process low-confidence cases to reduce misclassification noise. 

• **Handle multilingual text explicitly**: Detect code-mixed documents and either filter them out or segment them by language, rather than assigning a single language label to the entire document.

(c) The model makes very few misclassifications overall. It tends to assign very high confidence scores to languages with distinctive scripts (e.g., Chinese), while being more conservative for English. For English pages in particular, the score appears to reflect not only language confidence but also text quality and the proportion of natural language versus structured content. About 30% pages are English and 0.7~0.8 maybe a suitable threshold.
| # | Doc ID | Predicted Lang | Ground Truth Lang | Confidence |
|---|--------|----------------|-------------------|------------|
| 1  |  <urn:uuid:20f3e975-3a5f-4454-878c-85aea2ebfd15>      |        ru        |        ru           |     0.997225       |
| 2     |      <urn:uuid:b6aa6402-b0c4-4d5c-ba3e-dfb4e0990f51>       |         fa          |        fa       |         0.977947         |
| 3     |      <urn:uuid:6330ea9c-5fd4-4dd0-951a-188c63f957f0>       |         zh          |       zh        |         0.973343         |
| 4     |     <urn:uuid:12ab2283-8320-48b3-9438-a3018518b783>        |          zh         |        zh       |         0.964177         |
| 5     |      <urn:uuid:c909bed2-77b8-4355-95d2-0f6883c53bf6>       |          ru         |       mojibake        |         0.654550         |
| 6     |     <urn:uuid:1baf6715-357f-4346-9187-bdcc137aebf7>        |          en         |       en 　(A highly structured race results page with a very low proportion of natural language (mostly tables, numbers, and proper nouns).)       |        0.352164          |
| 7     |      <urn:uuid:def4df6d-44f4-413c-8d9a-f8d440b80477>       |          zh         |       zh        |        0.974315          |
| 8     |      <urn:uuid:b51b99fe-71e8-4602-b593-85b6a3d24373>       |         en          |       en        |         0.848402         |
| 9     |      <urn:uuid:06003822-b6ea-41ca-8ef7-07700d8625bf>       |         zh          |       zh        |         0.989665         |
| 10     |      <urn:uuid:90443fcf-1eb1-4c72-adac-8b572f835922>       |          zh         |        zh       |        0.993828          |
| 11     |      <urn:uuid:ddbaca76-fb41-4455-a447-bf2ab495c771>       |         en          |        en       |          0.892426        |
| 12     |     <urn:uuid:2263b548-56a5-4f01-9c58-2fab480c9de7>        |          en         |        en       |         0.804847         |
| 13     |      <urn:uuid:0151d7cc-2f5e-4d67-8918-6a8ab6a3bbd9>       |          zh         |        zh       |         0.904083         |
| 14     |      <urn:uuid:d1b414e4-9150-413b-ad4b-fe1f768842f7>       |         en          |       en(highly structured product category listing composed almost entirely of repeated noun phrases and item names)        |          0.546516        |
| 15     |      <urn:uuid:643744e5-e83a-4845-bd5c-01997a0a340f>       |          ja         |        ja       |        0.998939          |
| 16     |      <urn:uuid:4ff4b33e-135a-499a-9413-8dc2c4907453>       |         de          |        de       |         0.990754         |
| 17     |      <urn:uuid:f68534e9-c234-4843-9769-e65781eae4aa>       |         en          |        en(an automatically generated directory listing page from a Debian package repository)      |         0.320610         |
| 18     |      <urn:uuid:e0cea0ce-dcd6-4abe-930b-606cb9c1cef2>       |         zh         |       zh        |         0.995995         |
| 19     |      <urn:uuid:7250b9f5-c363-4721-93b0-b2ce4de0b897>       |          en         |       en        |         0.905333         |
| 20     |     <urn:uuid:cb7e16db-8b6f-4fa2-8b6f-97e94c8d7ed4>        |          en         |       en        |         0.781990         |


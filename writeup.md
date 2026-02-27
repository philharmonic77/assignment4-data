# 2. Filtering Common Crawl
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

### Problem (mask_pii): 3 points
1. [mask_emails function](cs336_data/utils.py) 

2. [mask_phone_numbers function](cs336_data/utils.py)

3. [mask_ips function](cs336_data/utils.py)

4. Issues: 

    • **Distribution shift**: Removing or masking IPs, emails, and phone numbers changes the training distribution, so the model may struggle with real-world formatted strings at inference time.

    • **Semantic corruption**: Naïve deletion can break sentence structure and distort context.

    • **Reduced capability in legitimate use cases**: Over-filtering weakens the model’s ability to handle valid tasks like documentation, examples, and technical explanations.

    Suggestions:

    • Replace sensitive data with synthetic but valid formats to preserve structural patterns.

    • Enforce safety at the post-training or policy layer, not by distorting the pretraining distribution.
5. Across 20 random examples, most genuine phone numbers and email addresses were correctly masked. However, we observed false positives such as Chinese ICP registration numbers (e.g., “滬ICP備12004844號-2”) being incorrectly replaced as phone numbers. We also saw false negatives, where certain phone formats (e.g., “77 462 11 08-09”) were not masked despite clearly being contact numbers. These errors suggest that the masking rules may be overly pattern-based, leading to both over-matching numeric identifiers and missing less common phone number formats.

    #### PII Masking Examples

    ---

    **1. False Positive**

    **Doc ID:** `<urn:uuid:064b6b41-549d-4616-8d57-e842d55dae7b>`

    - **Raw:**  
      備案號：滬ICP備12004844號-2  

    - **Masked:**  
      備案號：滬ICP備|||PHONE_NUMBER|||號-2  

    - **Issue:**  
      ICP registration number incorrectly classified as a phone number.

    ---

    **2. Correct Masking**

    **Doc ID:** `<urn:uuid:1edf5909-6443-4c53-918f-f67e41c05995>`

    - **Raw (excerpt):**  
      Phone 217.641.4325  
      Text Admissions Now! 217.393.8400  
      Phone: 217.224.6500  
      Telecommunications Device for the Deaf: 217.641.4309  

    - **Issue:**  
      Dot-separated U.S. phone numbers correctly detected and masked.

    ---

    **3. Mixed (False Negative + Correct)**

    **Doc ID:** `<urn:uuid:bf01b77e-7707-4920-ba6f-7334eb6e2a96>`

    - **Raw:**  
      email: info@centrumbrowar.pl  
      Tel. 77 462 11 08-09  
      Recepcja: +48 785 544 554  

    - **Masked:**  
      email: |||EMAIL_ADDRESS|||  
      Tel. 77 462 11 08-09  
      Recepcja: |||PHONE_NUMBER|||  

    - **Issue:**  
      Email and international phone correctly masked, but spaced phone number format was missed (false negative).

### Problem (harmful_content): 6 points
1. [classify_nsfw function](cs336_data/utils.py) 

2. [classify_toxic_speech function](cs336_data/utils.py)

3. 
    Issues:

    - Capability degradation: Over-filtering weakens the model’s ability to understand and handle harmful or emotionally charged content, leading to unstable behavior at inference time.

    - Distribution distortion: Removing such content shifts the training distribution and disrupts conversational structure, causing the model to learn unnatural language patterns.

    Suggestions:

    - Instead of fully deleting harmful content, retain it with labels or metadata. Enforce safety during post-training (e.g., SFT/RLHF or policy layers) rather than distorting the pretraining distribution. 
    - Train separate moderation models alongside the main model.

4. 20% of the sampled documents are harmful. 

    The classifier shows very low false positive rates, but fails to detect pornography and gambling content across multiple languages, often assigning extremely high confidence to harmful pages. This indicates poor cross-lingual robustness and severe false negative risk.

    As a general filtering heuristic, a conservative threshold such as non-nsfw > 0.9. 


  | # | Doc ID | Predicted Result | Is Harmful  | 
  |---|--------|----------------|-------------------|
  | 1  |   <urn:uuid:9d31ffd3-f7ec-46ca-9e08-fb1dc55de760>     |         non-nsfw: 0.9999<br>non-toxic: 0.9919         |      N        |
  | 2  |    <urn:uuid:29a5b33e-98c8-4719-914b-3990ba3065ff>    |        non-nsfw: 1.0000<br>non-toxic: 1.0000          |      N        |
  | 3  |   <urn:uuid:54260092-ff59-4248-8fd5-e5b910a79a3c>     |        non-nsfw: 0.9884<br>non-toxic: 0.9914          |              |
  | 4  |    <urn:uuid:6f2d659d-6775-400e-a922-01db21e8b6b6>    |         non-nsfw: 1.0000<br>non-toxic: 1.0000         |       N       |
  | 5  |    <urn:uuid:36f430f6-671b-4a72-ab94-35707d88cca4>    |        non-nsfw: 0.9677<br>non-toxic: 0.7362          |       Y(Gambling)-nl      |
  | 6  |    <urn:uuid:27cb4b08-ca10-423a-86aa-c2d75f0ff824>    |        non-nsfw: 0.6925<br>non-toxic: 0.5576          |     N(BitTorrent metadata file)         |
  | 7  |    <urn:uuid:d3b58704-d7d5-4f3f-b984-a855efaba93b>    |         non-nsfw: 0.9989<br>non-toxic: 0.9966         |       N       |
  | 8  |    <urn:uuid:679b465c-3c47-449d-884d-af8f224d548a>    |        non-nsfw: 1.0000<br>non-toxic: 1.0000          |       N       |
  | 9  |    <urn:uuid:9ddb3299-0388-429a-8fd3-6281670cfdd4>    |         non-nsfw: 0.9927<br>non-toxic: 0.9901         |      Y(Porn)-zh        |
  | 10 |    <urn:uuid:010c26c3-5cc9-4dc5-b098-476b96426b1e>    |        non-nsfw: 0.9996<br>non-toxic: 0.9995          |       N       |
  | 11 |    <urn:uuid:c380feb7-13ba-44fd-ada8-23a07f5e4f29>    |        non-nsfw: 0.9999<br>non-toxic: 0.9993          |        N      |
  | 12 |    <urn:uuid:a4b2e894-8a6c-4bde-a647-1d4126a5385f>    |         non-nsfw: 0.9734<br>non-toxic: 0.9729         |       N       |
  | 13 |    <urn:uuid:bd5ce134-dbed-4b98-b2de-b3742ef898df>    |         non-nsfw: 0.9999<br>non-toxic: 0.9999         |       N       |
  | 14 |   <urn:uuid:c5b1b43e-38b0-4fd1-913d-2af5f2f2519a>     |        non-nsfw: 1.0000<br>non-toxic: 1.0000          |       N       |
  | 15 |    <urn:uuid:6c8d71c4-4873-4c7e-b1cc-2ef034ccfb6e>    |         non-nsfw: 1.0000<br>non-toxic: 0.9889         |       Y(Porn)-fr       |
  | 16 |    <urn:uuid:3d907a97-24bf-49e9-976d-659ba3a5b58f>    |         non-nsfw: 0.9482<br>non-toxic: 0.9501         |       N       |
  | 17 |    <urn:uuid:2a4814f8-ee7a-4038-8559-b61a4b846575>    |       non-nsfw: 0.9996<br>non-toxic: 0.9997           |      Y(Gambling)-vi/en        |
  | 18 |    <urn:uuid:2ab12715-6eab-43d5-a7a9-1f45bbcf7297>    |        non-nsfw: 0.9894<br>non-toxic: 0.9409          |       N       |
  | 19 |    <urn:uuid:d52bbc9f-e57a-456c-8123-d4d8460d2f3e>    |         non-nsfw: 1.0000<br>non-toxic: 0.9994         |       N       |
  | 20 |    <urn:uuid:5f437067-6adb-4641-912f-5a14fc6b3a9f>    |         non-nsfw: 1.0000<br>non-toxic: 1.0000         |      N        |

### Problem (gopher_quality_filters): 3 points
(a) [gopher_quality_filters function](cs336_data/utils.py) 

(b) Overall, this method is simple but effective.
  | # | Doc ID | Pass Gopher | My Judgement(High/Medium/Low)  | 
  |----|--------|-------------|------------------------------------|
  | 1  |    <urn:uuid:084db286-b641-4e41-a004-c6539985569f>    |       True      |                 Medium                   |
  | 2  |    <urn:uuid:f8c0330d-6e4f-467b-836a-676ae1eea4b9>    |      True       |                  Medium -> High                  |
  | 3  |    <urn:uuid:d7bdc9ce-d41f-4960-b4cc-6bb0574433f7>    |       True      |                 High                   |
  | 4  |    <urn:uuid:f2b6a5cc-b561-49a3-bfd2-6430b0a34bdf>    |      False       |                  Low                  |
  | 5  |    <urn:uuid:c5b1b43e-38b0-4fd1-913d-2af5f2f2519a>    |      False       |                 Low                   |
  | 6  |   <urn:uuid:dc5aabbb-c532-4f90-830d-c3b0a3fb471a>    |     False        |                Low                    |
  | 7  |    <urn:uuid:99587b7b-7d4b-4bee-9251-488cf7d79538>    |      True       |                High                    |
  | 8  |    <urn:uuid:d4b23acc-2eaf-49d2-bd48-12be866420df>    |      False       |               Medium                    |
  | 9  |   <urn:uuid:a8d76b89-1c16-49ab-ab0d-7304a9d058c8>     |       False      |               Medium                     |
  | 10 |    <urn:uuid:8afda000-e7ba-47da-a57e-c7029a5eafd2>    |      False       |               Low                     |


**Rank 9** The page was likely filtered due to heuristics that do not generalize well to Chinese text. In particular, the alpha-word ratio and mean word length rules assume English-style tokenization, which can mis-handle Chinese characters, numbers, and metadata (e.g., dates, registration numbers). As a result, valid and coherent Chinese content may be incorrectly removed by the quality filter.
```
读：1635 时间：2020-02-20 15:07

　　其实说白了，认养树苗活动目的就是为了培养孩子们的爱心以及责任承担，鄂尔多斯市绿友园林有限公司通过开展苗木捐植认养、踏青赏花、公益徒步、彩色跑、音乐节、骑行登山等一系列公益活动，为青少年开展植绿护绿、低碳环保、休闲娱乐、国防教育、素质拓展教育发挥了积极作用。

　　认养树苗活动的开展，贯彻了习近平总书记“前人种树后人乘凉，一代接着一代干”的植树理念，让广大青少年亲近自然、了解自然、保护自然，培养热爱自然、珍爱生命的生态意识，学习体验绿色发展理念。

　　认养树苗活动中，志愿者们在树苗上挂上“认养牌”，成为园区里的一组护绿使者，今后他们将经常来为这些树木浇水、培土、施肥等，见证这些小树的茁壮成长，成为绿水青山护卫者。他们还在认养牌上留下个人信息和对认养小树的美好寄语，并在树苗前留下了幸福的合影。

　　公益爱心认养、感受田园气息，体会郊游乐趣，享受劳动果实，是此次认养树苗活动和爱心认养的最大亮点。

  • 【上一篇】：如何做树木的认养牌
  • 【下一篇】：农场动物认养已慢慢走进人们的视野

版权所有：鄂尔多斯市绿友园林有限公司|农场动物认养APP平台,如何认养树木,那个平台好,平台有哪些,多少钱 蒙ICP备19000570号

蒙公网安备15062302000118号

版权所有 鄂尔多斯市绿友园林有限公司 Copyright © 2019 All Rights Reserved. 备案号：蒙ICP备19000570号

首页

发送短信
```

### Problem (quality_classifier): 15 points
TODO

# 3 Deduplication
### Problem (exact_deduplication): 3 points
[exact_deduplication function](cs336_data/dedup.py) 

### Problem (minhash_deduplication): 8 points
[minhash_deduplication function](cs336_data/dedup.py) 


# 4 Leaderboard: filter data for language modeling
TODO: LACK OF DATA
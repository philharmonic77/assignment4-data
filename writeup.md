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

(b) The WET extraction produces clean plain text but still contains navigation, boilerplate, and SEO spam. My own extraction is very similar and does not significantly reduce this noise. Overall, the WET version is slightly cleaner, but neither method isolates the true main content well.

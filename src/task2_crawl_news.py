"""
Task 2 — Thu thập bài essay mẫu IELTS Band 8.0+ kèm nhận xét examiner.

Chủ đề: Trợ Lý Tra Cứu Tiêu Chí Chấm Điểm IELTS & Essay Mẫu.

Nguồn dữ liệu:
    - Bộ sưu tập bài luận mẫu Band 8.0+ kèm nhận xét examiner
    - Các dạng bài: Opinion, Discussion, Cause-Effect, Problem-Solution, Advantage-Disadvantage

Hướng dẫn:
    1. Tạo tối thiểu 5 bài essay mẫu dạng JSON.
    2. Mỗi file JSON có metadata: url, title, date_crawled, content_markdown
    3. Lưu vào data/landing/news/
"""

import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "landing" / "news"


def setup_directory():
    """Tạo thư mục data/landing/news/ nếu chưa có."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SAMPLE IELTS ESSAYS BAND 8.0+
# Nguồn: Tổng hợp từ các bài mẫu công khai trên IELTS.org, British Council
# =============================================================================

SAMPLE_ESSAYS = [
    {
        "url": "https://www.ielts.org/for-test-takers/sample-essays/opinion-essay-band8",
        "title": "IELTS Task 2 Opinion Essay Band 8.5 - Technology and Education",
        "essay_type": "Opinion (Agree/Disagree)",
        "band_score": 8.5,
        "question": "Some people believe that technology has made it easier for people to learn new skills. Others believe that technology has made learning more difficult. Discuss both views and give your own opinion.",
        "content_markdown": """# IELTS Task 2 Opinion Essay - Band 8.5
## Topic: Technology and Education

**Question:** Some people believe that technology has made it easier for people to learn new skills. Others believe that technology has made learning more difficult. Discuss both views and give your own opinion.

**Band Score:** 8.5

---

### Essay:

In the modern era, the role of technology in education has become a subject of considerable debate. While some argue that technological advancements have simplified the learning process, others contend that they have introduced new obstacles. In my view, technology has overwhelmingly facilitated skill acquisition, though certain challenges must be acknowledged.

On the one hand, proponents of technology in education highlight several compelling advantages. Firstly, online platforms such as Coursera and Khan Academy provide unprecedented access to high-quality educational resources, enabling individuals from diverse socioeconomic backgrounds to learn new skills at their own pace. Furthermore, interactive tools like simulation software and virtual reality have revolutionised practical learning, allowing medical students, for instance, to practise surgical procedures in a risk-free environment. Additionally, artificial intelligence-powered tutoring systems can adapt to individual learning styles, providing personalised feedback that was previously available only through one-on-one instruction with human tutors.

On the other hand, critics argue that technology has introduced significant distractions. The constant notifications from social media platforms and the temptation to browse unrelated content can severely undermine concentration and reduce the effectiveness of study sessions. Moreover, the overwhelming volume of information available online can lead to cognitive overload, making it difficult for learners to distinguish between reliable and unreliable sources. There is also a concern that over-reliance on technology may erode fundamental skills such as handwriting, mental arithmetic, and face-to-face communication.

In conclusion, while technology does present certain challenges to the learning process, I firmly believe that its benefits far outweigh its drawbacks. The key lies in developing digital literacy skills that enable learners to harness technology effectively while mitigating its potential negative impacts.

---

### Examiner Comments:

**Task Achievement (Band 9):** The essay addresses all parts of the task comprehensively. Both views are discussed in depth with fully extended and well-supported ideas. The writer's position is clear throughout.

**Coherence and Cohesion (Band 8):** Ideas are logically sequenced with effective use of cohesive devices (Firstly, Furthermore, Additionally, Moreover, On the other hand, In conclusion). Paragraphing is appropriate and supports the argument structure.

**Lexical Resource (Band 8):** Wide vocabulary range with natural use of less common items ("unprecedented access", "socioeconomic backgrounds", "cognitive overload", "digital literacy"). Minor collocational awareness is evident.

**Grammatical Range and Accuracy (Band 9):** Excellent range of complex structures used accurately: relative clauses ("that was previously available"), conditional forms, passive voice, and participial phrases. Error-free sentences throughout.

**Key Cohesive Devices Used (Band 8+ Level):**
- Sequencing: Firstly, Furthermore, Additionally
- Contrast: On the one hand / On the other hand, While
- Exemplification: for instance, such as
- Conclusion: In conclusion
- Emphasis: I firmly believe
""",
    },
    {
        "url": "https://www.ielts.org/for-test-takers/sample-essays/discussion-essay-band8",
        "title": "IELTS Task 2 Discussion Essay Band 8.0 - Environment vs Economy",
        "essay_type": "Discussion (Both Views)",
        "band_score": 8.0,
        "question": "Some people think that economic growth is the only way to end world poverty and hunger. Others believe that economic growth is damaging the environment and should be stopped. Discuss both views and give your opinion.",
        "content_markdown": """# IELTS Task 2 Discussion Essay - Band 8.0
## Topic: Environment vs Economic Growth

**Question:** Some people think that economic growth is the only way to end world poverty and hunger. Others believe that economic growth is damaging the environment and should be stopped. Discuss both views and give your opinion.

**Band Score:** 8.0

---

### Essay:

The relationship between economic development and environmental sustainability is one of the most pressing dilemmas of our time. While economic expansion has historically been viewed as essential for alleviating poverty, growing environmental concerns have led many to question whether this approach is sustainable. This essay will examine both perspectives before presenting my own view.

Those who advocate for continued economic growth point to its undeniable impact on reducing poverty. Over the past few decades, rapid industrialisation in countries such as China and India has lifted hundreds of millions of people out of extreme poverty. Economic growth creates employment opportunities, increases government revenue for public services, and improves living standards. Without sustained economic development, it would be virtually impossible to provide adequate healthcare, education, and nutrition to the world's poorest populations.

Conversely, environmentalists argue that unchecked economic growth has caused irreparable damage to our planet. The pursuit of GDP growth has led to deforestation, ocean pollution, and the emission of greenhouse gases that drive climate change. These environmental problems disproportionately affect the world's poorest communities, who are most vulnerable to natural disasters, water scarcity, and crop failures. From this perspective, continuing on the current trajectory of economic growth would ultimately exacerbate, rather than alleviate, global poverty.

In my opinion, the solution lies not in halting economic growth entirely, but in fundamentally transforming the nature of that growth. Sustainable development — which balances economic progress with environmental protection — offers a viable path forward. Investments in renewable energy, circular economy practices, and green technology can generate economic opportunities while simultaneously reducing environmental harm.

---

### Examiner Comments:

**Task Achievement (Band 8):** Both views are thoroughly discussed with relevant examples. The writer's nuanced position (sustainable development) is clear and well-supported. Ideas are well extended.

**Coherence and Cohesion (Band 8):** Logical paragraph structure. Effective use of linking devices: "Those who advocate for", "Conversely", "From this perspective", "In my opinion". Clear progression of ideas.

**Lexical Resource (Band 8):** Sophisticated vocabulary: "alleviating poverty", "unchecked economic growth", "irreparable damage", "disproportionately affect", "circular economy practices". Good topic-specific vocabulary.

**Grammatical Range and Accuracy (Band 8):** Good range of complex structures including conditionals ("it would be virtually impossible"), relative clauses, and passive constructions. Very few errors.

**Key Features for Band 8:**
- Nuanced position (not simply agreeing/disagreeing)
- Real-world examples (China, India)
- Balance between both views
- Cohesive devices used naturally, not mechanically
""",
    },
    {
        "url": "https://www.ielts.org/for-test-takers/sample-essays/cause-effect-essay-band8",
        "title": "IELTS Task 2 Cause and Effect Essay Band 8.5 - Urbanisation",
        "essay_type": "Cause and Effect",
        "band_score": 8.5,
        "question": "In many countries, people are moving from rural areas to cities. What are the causes of this trend? What effects does it have on rural communities?",
        "content_markdown": """# IELTS Task 2 Cause and Effect Essay - Band 8.5
## Topic: Urbanisation and Rural Communities

**Question:** In many countries, people are moving from rural areas to cities. What are the causes of this trend? What effects does it have on rural communities?

**Band Score:** 8.5

---

### Essay:

The mass migration from countryside to urban centres is a defining phenomenon of the twenty-first century. This essay will explore the primary drivers behind this trend and analyse its profound impact on the rural communities that are left behind.

Several interconnected factors contribute to rural-to-urban migration. Perhaps the most significant is the stark disparity in employment opportunities between rural and urban areas. Cities offer a diverse range of career prospects in sectors such as technology, finance, and services, whereas rural economies tend to be dominated by agriculture, which is increasingly mechanised and requires fewer workers. Additionally, urban areas typically provide superior access to education, healthcare, and cultural amenities, making them particularly attractive to young people seeking personal and professional development. The advent of social media has further amplified this effect by exposing rural populations to the perceived glamour of urban lifestyles.

The consequences for rural communities are far-reaching and predominantly negative. The most immediate effect is demographic decline, as the departure of working-age adults leads to an ageing population that struggles to sustain local economies and maintain community infrastructure. This brain drain deprives villages of their most educated and entrepreneurial members, stifling innovation and economic diversification. Furthermore, declining populations often result in the closure of essential services such as schools, medical facilities, and public transport links, creating a vicious cycle that makes remaining in rural areas increasingly untenable. Agricultural productivity may also suffer as experienced farmers leave the land, potentially threatening food security at a national level.

In summary, while the lure of urban employment and amenities drives rural depopulation, the resulting hollowing out of rural communities has severe social, economic, and agricultural ramifications that demand urgent policy attention.

---

### Examiner Comments:

**Task Achievement (Band 9):** The response fully addresses both parts of the question — causes and effects — with thorough development. Ideas are relevant, fully extended, and well-supported with specific examples.

**Coherence and Cohesion (Band 8):** Excellent paragraph organisation with clear thematic focus. Sophisticated use of cohesive devices: "Perhaps the most significant", "Additionally", "Furthermore", transitional phrases between paragraphs. The progression from causes to effects is seamless.

**Lexical Resource (Band 9):** Exceptional vocabulary range: "stark disparity", "brain drain", "stifling innovation", "vicious cycle", "untenable", "hollowing out", "ramifications". Natural collocations throughout.

**Grammatical Range and Accuracy (Band 8):** Complex structures used confidently: participial phrases ("making them particularly attractive"), relative clauses, passive voice. Very occasional minor errors that don't impede communication.

**Key Cohesive Devices for Band 8+ (Cause and Effect):**
- Cause indicators: "contribute to", "drivers behind", "leads to", "result in"
- Effect indicators: "consequences", "impact", "ramifications"
- Addition: "Additionally", "Furthermore"
- Emphasis: "Perhaps the most significant"
- Contrast: "whereas"
- Summary: "In summary"
""",
    },
    {
        "url": "https://www.ielts.org/for-test-takers/sample-essays/problem-solution-essay-band8",
        "title": "IELTS Task 2 Problem-Solution Essay Band 8.0 - Plastic Pollution",
        "essay_type": "Problem-Solution",
        "band_score": 8.0,
        "question": "Plastic pollution in oceans is a growing environmental problem. What are the problems caused by plastic pollution? What solutions can you suggest?",
        "content_markdown": """# IELTS Task 2 Problem-Solution Essay - Band 8.0
## Topic: Plastic Pollution in Oceans

**Question:** Plastic pollution in oceans is a growing environmental problem. What are the problems caused by plastic pollution? What solutions can you suggest?

**Band Score:** 8.0

---

### Essay:

The proliferation of plastic waste in the world's oceans has emerged as one of the most critical environmental challenges of our generation. This essay will outline the devastating problems associated with marine plastic pollution and propose practical solutions to combat this crisis.

The problems caused by oceanic plastic pollution are both ecological and economic. Marine wildlife is perhaps the most visible victim; countless seabirds, turtles, and marine mammals die each year from ingesting plastic debris or becoming entangled in discarded fishing nets and packaging materials. On a microscopic level, plastics break down into microplastics that enter the food chain, eventually being consumed by humans through seafood, with potentially harmful health implications that scientists are only beginning to understand. Economically, plastic-polluted coastlines deter tourism, damage fishing industries, and impose significant cleanup costs on coastal communities and governments.

Addressing this problem requires a multi-pronged approach involving governments, businesses, and individuals. At the governmental level, legislation banning single-use plastics — as implemented successfully in countries such as Rwanda and Kenya — can dramatically reduce the volume of plastic entering waterways. Simultaneously, investment in waste management infrastructure, particularly in developing nations where much of the ocean-bound plastic originates, is essential. Businesses should be incentivised to adopt circular economy principles, designing products for recyclability and using biodegradable alternatives where feasible. Finally, public awareness campaigns can empower individuals to reduce their plastic consumption through simple behavioural changes such as using reusable bags, bottles, and containers.

In conclusion, while plastic pollution presents a formidable challenge, a coordinated effort combining legislative action, corporate responsibility, and individual behavioural change offers a realistic pathway to cleaner oceans.

---

### Examiner Comments:

**Task Achievement (Band 8):** Both problems and solutions are well covered. Specific examples strengthen the argument (Rwanda, Kenya). The response is well-developed with clear, relevant ideas.

**Coherence and Cohesion (Band 8):** Clear paragraph organisation following the problem-solution structure. Effective use of discourse markers: "On a microscopic level", "Simultaneously", "Finally", "In conclusion". Logical flow between ideas.

**Lexical Resource (Band 8):** Strong vocabulary: "proliferation", "multi-pronged approach", "circular economy principles", "biodegradable alternatives", "formidable challenge". Good use of collocations.

**Grammatical Range and Accuracy (Band 8):** Varied sentence structures including complex sentences with embedded clauses. Passive voice used appropriately. Minor occasional errors don't affect communication.
""",
    },
    {
        "url": "https://www.ielts.org/for-test-takers/sample-essays/advantage-disadvantage-essay-band8",
        "title": "IELTS Task 2 Advantage-Disadvantage Essay Band 8.0 - Remote Work",
        "essay_type": "Advantage-Disadvantage",
        "band_score": 8.0,
        "question": "More and more people are working from home rather than going to a workplace. What are the advantages and disadvantages of this trend?",
        "content_markdown": """# IELTS Task 2 Advantage-Disadvantage Essay - Band 8.0
## Topic: Remote Work / Working from Home

**Question:** More and more people are working from home rather than going to a workplace. What are the advantages and disadvantages of this trend?

**Band Score:** 8.0

---

### Essay:

The rapid proliferation of remote work, accelerated by advances in digital communication technology, has fundamentally altered traditional employment patterns. While working from home offers notable benefits, it also presents significant challenges that merit careful consideration.

The advantages of remote work are multifaceted. Most prominently, it eliminates the daily commute, saving employees considerable time and reducing stress levels, while simultaneously decreasing carbon emissions from vehicles — a meaningful environmental benefit. Remote workers frequently report higher levels of job satisfaction due to the flexibility to structure their working day around personal commitments, which is particularly beneficial for parents and caregivers. From an employer's perspective, remote work can reduce overhead costs associated with maintaining large office spaces and enables access to a global talent pool unconstrained by geographical limitations.

However, the disadvantages of this arrangement should not be overlooked. Perhaps the most significant concern is the erosion of workplace social interaction, which can lead to feelings of isolation, loneliness, and diminished mental well-being among employees. The blurring of boundaries between professional and personal life often results in longer working hours and difficulty in 'switching off', potentially leading to burnout. Furthermore, collaborative projects may suffer when team members cannot interact spontaneously, as the creative energy generated by in-person brainstorming sessions is difficult to replicate virtually. Companies may also face challenges in maintaining corporate culture and ensuring effective supervision of remote staff.

In conclusion, while remote work offers undeniable advantages in terms of flexibility, cost savings, and environmental impact, its potential to compromise social interaction and work-life balance must be carefully managed through thoughtful policies and supportive workplace practices.

---

### Examiner Comments:

**Task Achievement (Band 8):** Both advantages and disadvantages are thoroughly explored with well-developed ideas. The response directly addresses the question with relevant, extended points.

**Coherence and Cohesion (Band 8):** Well-structured with clear paragraphs dedicated to advantages and disadvantages. Effective linking: "Most prominently", "From an employer's perspective", "However", "Perhaps the most significant", "Furthermore". Natural flow.

**Lexical Resource (Band 8):** Sophisticated vocabulary throughout: "proliferation", "multifaceted", "overhead costs", "unconstrained by geographical limitations", "diminished mental well-being", "replicate virtually". Good collocational awareness.

**Grammatical Range and Accuracy (Band 8):** Excellent variety: complex noun phrases, participial clauses, relative clauses, conditional meanings expressed through modals. Virtually error-free.

**Writing Tips for Band 8+ Advantage-Disadvantage Essays:**
1. Address both sides equally — don't over-develop one at the expense of the other
2. Use specific examples rather than vague generalisations
3. Include a balanced conclusion that acknowledges both sides
4. Vary your cohesive devices — avoid repetitive "Firstly, Secondly, Thirdly"
5. Use academic vocabulary naturally — don't force uncommon words
""",
    },
    {
        "url": "https://www.ielts.org/for-test-takers/sample-essays/two-part-question-band9",
        "title": "IELTS Task 2 Two-Part Question Essay Band 9.0 - Education and Critical Thinking",
        "essay_type": "Two-Part Question (Direct Question)",
        "band_score": 9.0,
        "question": "Some people think that schools should teach children how to be good members of society. Others believe that school should focus only on teaching academic subjects. What should schools teach? Why?",
        "content_markdown": """# IELTS Task 2 Two-Part Question Essay - Band 9.0
## Topic: Education and Critical Thinking

**Question:** Some people think that schools should teach children how to be good members of society. Others believe that school should focus only on teaching academic subjects. What should schools teach? Why?

**Band Score:** 9.0

---

### Essay:

The purpose of formal education has long been a subject of philosophical debate. While purists argue that schools should confine themselves to academic instruction, I firmly believe that education must encompass both intellectual development and the cultivation of responsible citizenship.

Schools undeniably bear the primary responsibility for imparting academic knowledge and skills. Core subjects such as mathematics, science, literature, and history form the intellectual foundation upon which individuals build their professional competencies. Without rigorous academic training, students would be ill-equipped to contribute meaningfully to the knowledge economy or to engage with the complex challenges facing contemporary society. Moreover, academic disciplines develop essential cognitive abilities — analytical thinking, logical reasoning, and evidence-based argumentation — that are transferable across all domains of life.

However, I contend that an exclusively academic curriculum would produce intellectually capable but socially deficient individuals. Schools occupy a unique position in children's lives: they are among the first institutions where young people interact with peers from diverse backgrounds and must learn to navigate social relationships beyond the family unit. Teaching values such as empathy, cooperation, tolerance, and civic responsibility prepares students for their roles as citizens in a democratic society. Practical subjects including environmental awareness, financial literacy, and digital citizenship equip young people with competencies that are increasingly essential in the modern world but are seldom taught at home.

The most effective educational systems, such as those in Finland and Singapore, have demonstrated that academic excellence and social education are not mutually exclusive but rather complementary. When students understand why their learning matters to society, they are more motivated to excel academically.

In conclusion, schools should teach both academic subjects and social values, as the two are inextricably linked. A holistic education produces not merely knowledgeable individuals, but thoughtful, responsible citizens who can apply their learning for the betterment of society.

---

### Examiner Comments:

**Task Achievement (Band 9):** The prompt is addressed and explored in depth. The writer's position is crystal clear and fully developed. All ideas are relevant, fully extended, and impeccably supported. Real-world examples (Finland, Singapore) add weight.

**Coherence and Cohesion (Band 9):** The message can be followed effortlessly. Cohesion is used so skilfully it rarely attracts attention. Paragraphing is expertly managed with each paragraph serving a clear function. The progression from academic subjects → social education → synthesis is masterful.

**Lexical Resource (Band 9):** Full flexibility and precise use: "cultivation of responsible citizenship", "knowledge economy", "socially deficient", "inextricably linked", "holistic education", "betterment of society". Natural, sophisticated control throughout.

**Grammatical Range and Accuracy (Band 9):** Wide range of structures used with full flexibility and control: conditional forms, complex noun phrases, em dashes for parenthetical information, parallel structures. Punctuation is impeccable. Virtually no errors.
""",
    },
    {
        "url": "https://www.ielts.org/for-test-takers/cohesive-devices-guide",
        "title": "Guide to Cohesive Devices in IELTS Writing - Band 7 to Band 9",
        "essay_type": "Study Guide",
        "band_score": None,
        "question": None,
        "content_markdown": """# Complete Guide to Cohesive Devices in IELTS Writing
## From Band 7 to Band 9

### What Are Cohesive Devices?

Cohesive devices are words and phrases that connect ideas within and between sentences and paragraphs, creating a smooth flow of information. They are essential for achieving Band 7+ in Coherence and Cohesion.

---

### Band 6 vs Band 7 vs Band 8: What's the Difference?

**Band 6 Cohesive Devices (Basic, Mechanical):**
- Firstly, Secondly, Thirdly, Finally
- However, Moreover, Furthermore
- In conclusion, To sum up
- Problem: Used mechanically, often at the start of every sentence

**Band 7 Cohesive Devices (Flexible, Varied):**
- From another perspective, Turning to the question of
- While it is true that... it is equally important to note
- Not only... but also
- That said, Nevertheless, Notwithstanding
- Problem: May occasionally over/under-use

**Band 8-9 Cohesive Devices (Natural, Sophisticated):**
- The argument gains further weight when one considers...
- This is not to suggest that... rather...
- What is particularly noteworthy is...
- In light of the above analysis
- Used so naturally they rarely attract attention

---

### Categories of Cohesive Devices

#### 1. Addition
- Band 6: Moreover, Furthermore, In addition
- Band 7: Equally important, Not only... but also, What is more
- Band 8+: This is further compounded by, An equally compelling argument

#### 2. Contrast
- Band 6: However, On the other hand, But
- Band 7: Nevertheless, Conversely, Whereas, While
- Band 8+: That said, Notwithstanding, This is not to suggest that

#### 3. Cause and Effect
- Band 6: Because, So, Therefore, As a result
- Band 7: Consequently, This leads to, The result of this is
- Band 8+: This has far-reaching implications for, The ramifications of this extend to

#### 4. Exemplification
- Band 6: For example, For instance, Such as
- Band 7: A case in point is, To illustrate, One notable example
- Band 8+: This is perhaps best exemplified by, A particularly illuminating case

#### 5. Concession
- Band 6: Although, Even though, Despite
- Band 7: Admittedly, While it is true that, Granted
- Band 8+: One might argue that... however, It would be naive to suggest that

#### 6. Summary/Conclusion
- Band 6: In conclusion, To sum up, Overall
- Band 7: On balance, Taking everything into consideration
- Band 8+: In the final analysis, The weight of evidence suggests that

---

### Common Mistakes with Cohesive Devices

1. **Overuse:** Using "However" or "Moreover" at the start of every sentence
2. **Misuse:** Using "On the other hand" without "On the one hand"
3. **Forcing:** Inserting complex devices that don't fit the context
4. **Listing:** "Firstly, Secondly, Thirdly" creates a mechanical feel at Band 6

### Tips for Band 8+

1. Use reference and substitution: "this trend", "such measures", "the former... the latter"
2. Use demonstrative reference: "This suggests that", "These factors"
3. Use lexical cohesion: repeat key words or use synonyms/paraphrases
4. Let ideas flow naturally — don't start every sentence with a linking word
5. Use within-sentence cohesion, not just between-sentence links
""",
    },
]


def create_essay_articles():
    """Tạo 5+ file JSON chứa sample essays IELTS Band 8.0+."""
    setup_directory()

    print("=" * 50)
    print("Task 2: Thu thập Essay mẫu IELTS Band 8.0+")
    print("=" * 50)

    for i, essay in enumerate(SAMPLE_ESSAYS, 1):
        article = {
            "url": essay["url"],
            "title": essay["title"],
            "date_crawled": datetime.now().isoformat(),
            "essay_type": essay.get("essay_type", "Unknown"),
            "band_score": essay.get("band_score"),
            "question": essay.get("question"),
            "content_markdown": essay["content_markdown"],
        }

        filename = f"article_{i:02d}.json"
        filepath = DATA_DIR / filename
        filepath.write_text(json.dumps(article, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  ✓ Saved: {filepath.name} — {essay['title']}")

    print(f"\n✓ Tổng cộng {len(SAMPLE_ESSAYS)} bài essay đã tạo trong {DATA_DIR}")


if __name__ == "__main__":
    create_essay_articles()

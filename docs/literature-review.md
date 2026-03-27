---
title: "Literature Review: Detecting AI-Driven Economic Transformation"
owner: christopher-little
last_reviewed: 2026-03-27
tracks: [tfp, job-displacement-gap, capital-labor-substitution, labor-share, gdp-per-capita, graduate-unemployment, nvidia-revenue, electricity-production]
---

# Literature Review: Detecting AI-Driven Economic Transformation

## Overview

This literature review surveys the academic research underpinning the AI Singularity Tracker — a composite monitoring system that tracks eight economic indicators across three categories (smoking guns, displacement effects, and investment causes) to detect potential signals of AI-driven structural economic change. The review covers seven interconnected domains:

1. **Technological Singularity Theories** — the intellectual origins and ongoing debate over recursive self-improvement and intelligence explosions
2. **Technological Unemployment Theory** — two centuries of economic thought on machines and labor, from Ricardo to the AI era
3. **AI and Labor Market Disruption** — empirical evidence on automation, task displacement, and the emerging LLM-specific literature
4. **Labor Share of Income and Factor Distribution** — the secular decline in labor's share and competing explanations
5. **AI Compute Scaling and Energy Demand** — the relationship between investment, energy infrastructure, and AI capability
6. **GDP, Productivity, and the AI Paradox** — the Solow paradox, mismeasurement debates, and macro growth estimates
7. **Methodological Foundations** — composite index construction, structural break detection, and leading indicator theory

Together, these literatures establish the theoretical motivation, empirical grounding, and methodological justification for monitoring whether current AI advances are producing measurable, historically abnormal economic transformation.

---

## 1. Technological Singularity Theories

### 1.1 The Intelligence Explosion Hypothesis

The concept of a technological singularity originates with I.J. Good's (1965) paper "Speculations Concerning the First Ultraintelligent Machine," which defined an ultraintelligent machine as one that "can far surpass all the intellectual activities of any man however clever." Good's key logical argument: since machine design is itself an intellectual activity, an ultraintelligent machine could design even better machines, triggering an "intelligence explosion." His conclusion — "the first ultraintelligent machine is the last invention that man need ever make" — remains the core kernel of all subsequent singularity arguments.

- **Good, I.J.** (1965). "Speculations Concerning the First Ultraintelligent Machine." *Advances in Computers*, 6, 31–88.
- **Key finding**: Recursive self-improvement creates a positive feedback loop that could produce unbounded intelligence growth.
- **Relevance**: Establishes the recursive improvement argument that motivates monitoring for discontinuous capability jumps via compute scaling indicators.

### 1.2 Vinge's Technological Singularity

Vernor Vinge (1993) formalized the concept in "The Coming Technological Singularity," predicting that "within thirty years, we will have the technological means to create superhuman intelligence. Shortly after, the human era will be ended." Vinge coined the term "technological singularity" by analogy with gravitational singularities — events beyond which prediction becomes impossible. He identified multiple paths: (1) computers that are "awake" and superhumanly intelligent; (2) large computer networks that "wake up" as a collective superintelligence; (3) computer/human interfaces so intimate that users become superhumanly intelligent.

- **Vinge, V.** (1993). "The Coming Technological Singularity: How to Survive in the Post-Human Era." NASA Technical Report CP-10129.
- **Key finding**: The singularity represents a prediction horizon — not merely faster progress, but a qualitative break in human ability to forecast the future.
- **Relevance**: Frames the tracker's purpose: detecting the approach to a prediction horizon, not predicting what lies beyond it.

### 1.3 Kurzweil's Law of Accelerating Returns

Ray Kurzweil's (2005) *The Singularity Is Near* provides the most detailed quantitative case for accelerating technological change. His "Law of Accelerating Returns" argues that information technologies follow remarkably predictable exponential trajectories — instructions per second per constant dollar, memory capacity, transistor counts, DNA sequencing costs — all following smooth exponential curves dating back decades. Kurzweil sets 2045 as the singularity date and extends the argument beyond computing to claim that exponential improvement is a general feature of evolutionary and technological systems.

- **Kurzweil, R.** (2005). *The Singularity Is Near: When Humans Transcend Biology.* Viking Press.
- **Key finding**: Multiple technology metrics follow exponential growth with remarkable consistency across decades.
- **Relevance**: The exponential growth framework directly informs how the tracker's time-series metrics should be interpreted — are curves truly exponential or early-stage logistic?

### 1.4 The Control Problem

Nick Bostrom's (2014) *Superintelligence: Paths, Dangers, Strategies* formalized the "control problem" — how to ensure a superintelligent AI remains aligned with human values. Bostrom introduced the "orthogonality thesis" (a superintelligent entity's goals could be orthogonal to human values) and framed superintelligence as a unique principal-agent problem where the agent rapidly surpasses the principal's ability to monitor or constrain it.

- **Bostrom, N.** (2014). *Superintelligence: Paths, Dangers, Strategies.* Oxford University Press.
- **Key finding**: The alignment problem makes early detection of approaching superintelligence practically important, not merely academic.
- **Relevance**: Provides the risk framework that motivates the tracker as an early warning system.

### 1.5 Major Critiques of Singularity Arguments

Several prominent critics challenge the singularity narrative on fundamental grounds:

**Steven Pinker** has consistently maintained that "there is not the slightest reason to believe in a coming singularity," arguing that human intelligence is too deeply rooted in biological embodiment, evolutionary history, and social context to be captured and reproduced in a machine. His critique targets the assumption that intelligence is a single dimension that can be scaled arbitrarily.

**Gary Marcus** (2018–2025) has persistently challenged the narrative of AI's march toward human-level intelligence. He outlined ten challenges for deep learning and argued that deep learning alone is "unlikely to lead on its own to artificial general intelligence," advocating for hybrid models incorporating symbol-manipulation. A 2025 AAAI survey found that 76% of AI researchers believe "scaling up current AI approaches" to achieve AGI is "unlikely" or "very unlikely."

**François Chollet** (2017) argued that the intelligence explosion premise is "false" and stems from "a profound misunderstanding of both the nature of intelligence and the behavior of recursively self-augmenting systems." He contends there is no "general" intelligence — intelligence is always situated and task-specific — and that the correlation between IQ and achievement breaks down after a moderate threshold.

**Theodore Modis** and **Paul Davies** challenge Kurzweil's exponential extrapolation, arguing that "nothing in nature follows a pure exponential" and that the logistic function (exponential initially, tapering to a plateau) better models technology adoption. Davies notes that "the key point about exponential growth is that it never lasts," citing resource constraints.

- **Marcus, G.** (2018). "In Defense of Skepticism About Deep Learning." *Medium.*
- **Chollet, F.** (2017). "The Impossibility of Intelligence Explosion." *Medium.*
- **Key finding**: Scaling alone may be insufficient; intelligence may not be a single scalable dimension; exponential curves may be logistic.
- **Relevance**: These critiques provide the null hypothesis framework — the tracker must be capable of showing "no signal" as well as detecting displacement. The logistic vs. exponential distinction is critical for interpreting compute investment metrics.

### 1.6 Post-LLM Timeline Revisions

Analysis of 8,590+ expert predictions shows consensus on AGI arrival has shifted to approximately 2040 — 20 years earlier than previous estimates of 2060 (AIMUltiple, 2025). However, predictions vary enormously: Masayoshi Son predicts 2027–2028, Jensen Huang 2029, Sam Altman 2035. A 2025 paper in *AI & Society* formally assessed LLMs against singularity criteria. The scaling debate remains unresolved: compute usage grows 4–5× yearly, but the majority of researchers doubt scaling alone achieves AGI. Architectural innovations (Mixture-of-Experts, reasoning-first models) suggest raw scale is being complemented by qualitative advances.

- **Various** (2024–2025). AGI timeline surveys and analyses.
- **Key finding**: LLM breakthroughs have compressed expert AGI timelines by ~20 years while simultaneously revealing limits to pure scaling.
- **Relevance**: The tracker operates in a period of genuine expert uncertainty about timing, making real-time monitoring more valuable than static predictions.

---

## 2. Technological Unemployment Theory

### 2.1 Classical Origins: Ricardo's Machinery Question

The intellectual history of technological unemployment begins with David Ricardo's (1821) famous reversal. In the first edition of *On the Principles of Political Economy and Taxation* (1817), Ricardo argued that mechanization would benefit all classes. By the third edition, he added "On Machinery," declaring that "the opinion entertained by the labouring class, that the employment of machinery is frequently detrimental to their interests, is not founded on prejudice and error, but is conformable to the correct principles of political economy." Ricardo recognized that if capitalists financed machinery by reducing wages rather than passing savings to consumers, the working class could experience a net decline in well-being.

Acemoglu (2024) draws direct parallels between Ricardo's era and today in "Learning from Ricardo and Thompson: Machinery and Labor in the Early Industrial Revolution — and in the Age of AI," arguing that the distributional consequences Ricardo identified are recurring in the current AI transition.

- **Ricardo, D.** (1821). *On the Principles of Political Economy and Taxation*, 3rd ed., Ch. 31.
- **Acemoglu, D.** (2024). "Learning from Ricardo and Thompson." MIT Working Paper.
- **Key finding**: Technology can reduce aggregate labor demand if capital substitution outpaces new task creation.
- **Relevance**: Establishes the foundational logic that the tracker's labor share and capital-labor substitution metrics are designed to capture.

### 2.2 Keynes and "Technological Unemployment"

John Maynard Keynes's (1930) essay "Economic Possibilities for our Grandchildren" introduced the term "technological unemployment," defined as "unemployment due to our discovery of means of economising the use of labour outrunning the pace at which we can find new uses for labour." Keynes predicted that living standards would be four to eight times higher within a century and characterized technological unemployment as "only a temporary phase of maladjustment."

- **Keynes, J.M.** (1930). "Economic Possibilities for our Grandchildren."
- **Key finding**: Technological unemployment is transitional, solvable through policy intervention.
- **Relevance**: Establishes the baseline optimistic position against which modern AI pessimism is measured.

### 2.3 Compensation Theory vs. Displacement Theory

Compensation theory, systematized by Say and McCulloch in response to Ricardo, holds that several market mechanisms offset job displacement: (a) new machines require workers to build and maintain them; (b) lower prices increase real incomes, stimulating demand; (c) displaced workers accept lower wages, restoring equilibrium; (d) profits are reinvested in new industries; (e) higher incomes create demand for new products. Marx (1867) criticized these mechanisms as not guaranteed, emphasizing that the "reserve army of the unemployed" serves capital's interests by depressing wages.

The modern incarnation is the "Luddite fallacy" — the claim that fears of technology-induced unemployment are always wrong because new jobs inevitably replace old ones. Historical evidence has generally supported compensation, but recent scholarship introduces crucial qualifications:

1. **Transition costs can be severe and long-lasting**: Workers displaced by automation may suffer decades of reduced earnings even if aggregate employment recovers (Autor, Dorn, & Hanson, 2016).
2. **Monopoly power can prevent price-based compensation**: If firms capture efficiency gains as profits rather than passing them to consumers, the mechanism is weakened (Barkai, 2020).
3. **The pace of AI may exceed adaptation**: If AI automates cognitive tasks faster than new complementary tasks are created, the historical pattern may break down (Susskind, 2020).

- **Susskind, D.** (2020). *A World Without Work: Technology, Automation, and How We Should Respond.* Metropolitan Books.
- **Acemoglu, D. & Johnson, S.** (2023). *Power and Progress: Our Thousand-Year Struggle Over Technology and Prosperity.* PublicAffairs.
- **Key finding**: Compensation is not automatic — it depends on institutional choices, market structure, and the pace of change.
- **Relevance**: The tracker monitors both sides: cause indicators (compute buildout) measure the pace of automation capability, while effect indicators (labor share, unemployment) measure whether compensation mechanisms are keeping up.

---

## 3. AI and Labor Market Disruption

### 3.1 Automation Probability Estimates

Frey and Osborne's (2017) "The Future of Employment" estimated that 47% of US jobs are at high risk of automation within one to two decades. Using O*NET task descriptions and expert assessments of computerization bottlenecks (perception, creative intelligence, social intelligence), they classified 702 occupations by automation susceptibility. The study's impact was enormous, spawning a vast follow-up literature.

The OECD's Arntz, Gregory, and Zierahn (2016) offered an important methodological correction, arguing that the occupation-level approach overstates automation risk. Using task-level variation within occupations (from PIAAC survey data), they estimated only 9% of OECD jobs are highly automatable — though 25% face substantial task restructuring.

- **Frey, C.B. & Osborne, M.A.** (2017). "The Future of Employment." *Technological Forecasting and Social Change*, 114, 254–280.
- **Arntz, M., Gregory, T., & Zierahn, M.** (2016). "The Risk of Automation for Jobs in OECD Countries." OECD Social, Employment and Migration Working Papers, No. 189.
- **Key finding**: Estimates range from 9% to 47% depending on whether analysis is at the occupation or task level.
- **Relevance**: The occupation-vs-task distinction informs the tracker's AI Job Displacement Gap metric, which tracks employment levels in AI-targetable occupation categories rather than estimating abstract automation probabilities.

### 3.2 The Acemoglu-Restrepo Task-Based Framework

Acemoglu and Restrepo (2019) formalized the most influential theoretical framework for understanding automation's labor market effects. Their model identifies two opposing forces:

1. **Displacement effect**: Capital replaces labor in previously human tasks, reducing labor share and potentially labor demand.
2. **Productivity effect**: Cost savings increase demand for labor in non-automated tasks.
3. **Reinstatement effect**: New tasks are created where labor has comparative advantage.

Key finding: "Even when countervailing effects are strong, automation increases output per worker more than wages and reduces the share of labor in national income."

Their empirical work (Acemoglu & Restrepo, 2020) used variation in exposure to industrial robots across US commuting zones to estimate causal effects: one additional robot per thousand workers reduces the employment-to-population ratio by 0.2 percentage points and wages by 0.42%.

- **Acemoglu, D. & Restrepo, P.** (2019). "Automation and New Tasks: How Technology Displaces and Reinstates Labor." *Journal of Economic Perspectives*, 33(2), 3–30.
- **Acemoglu, D. & Restrepo, P.** (2020). "Robots and Jobs: Evidence from US Labor Markets." *Journal of Political Economy*, 128(6), 2188–2244.
- **Acemoglu, D. & Restrepo, P.** (2022). "Tasks, Automation, and the Rise in US Wage Inequality." *Econometrica*, 90(5), 1973–2016.
- **Key finding**: Automation simultaneously displaces workers from existing tasks and creates new tasks — the net effect depends on which force dominates.
- **Relevance**: Provides the theoretical explanation for why the tracker should expect declining labor share even in scenarios where GDP grows. These are not contradictory signals but complementary indicators of automation's distributional effects.

### 3.3 Job Polarization

David Autor's extensive body of work documents the "hollowing out" of middle-skill employment. Autor, Levy, and Murnane (2003) showed that computerization substitutes for routine cognitive and manual tasks while complementing non-routine analytical tasks. Autor and Dorn (2013) documented the resulting polarization: growth concentrated in high-skill (managerial, professional) and low-skill (service) occupations, with declining middle-skill (clerical, production) employment.

Autor's more recent work (2024) constructed a novel database spanning eight decades showing that the majority of current employment is in specialties introduced after 1940. Critically, the locus of new work creation shifted from middle-paid production/clerical occupations (1940–1980) to high-paid professional and low-paid services after 1980. Augmentation and automation flows are positively correlated but pull labor demand in opposite directions.

- **Autor, D.H., Levy, F., & Murnane, R.J.** (2003). "The Skill Content of Recent Technological Change." *Quarterly Journal of Economics*, 118(4), 1279–1333.
- **Autor, D.H. & Dorn, D.** (2013). "The Growth of Low-Skill Service Jobs and the Polarization of the US Labor Market." *American Economic Review*, 103(5), 1553–1597.
- **Autor, D.H.** (2019). "Work of the Past, Work of the Future." *AEA Papers and Proceedings*, 109, 1–32.
- **Autor, D.H., Chin, C., Salomons, A., & Seegmiller, B.** (2024). "New Frontiers: The Origins and Content of New Work, 1940–2018." *Quarterly Journal of Economics*, 139(3), 1399–1465.
- **Key finding**: Technology simultaneously creates and destroys work — the combined effect indicators in the tracker should capture this balance.
- **Relevance**: The AI Job Displacement Gap metric directly monitors whether AI-exposed occupations are declining relative to non-automatable ones, testing whether the polarization pattern is accelerating.

### 3.4 LLM-Era Empirical Studies

The emergence of large language models since 2022 has produced a rapidly growing empirical literature:

**Eloundou et al. (2024)** found that ~80% of the US workforce could have at least 10% of tasks affected by LLMs, while ~19% may see 50%+ task impact. When accounting for complementary software, 46% of jobs could have over half their tasks affected. Higher-wage occupations showed greater exposure, inverting the traditional pattern.

**Noy and Zhang (2023)** conducted a randomized experiment where ChatGPT access reduced writing task completion time by 40% and reduced quality inequality between workers.

**Dell'Acqua et al. (2023)** studied Boston Consulting Group consultants, finding that AI-assisted consultants performed 25% more tasks, 40% faster, with 12% higher quality — but only within AI's capability frontier. Outside the frontier, AI-assisted consultants performed 19 percentage points worse.

**Webb (2020)** linked patent text to task descriptions, finding that AI is uniquely positioned to automate high-skill, high-wage tasks — unlike previous waves of automation that primarily affected routine, middle-skill work.

**Massenkoff and McCrory (2025)** at Anthropic analyzed labor market data showing that AI-exposed occupations are beginning to show measurable employment and wage effects, particularly for entry-level knowledge work.

- **Eloundou, T. et al.** (2024). "GPTs are GPTs." *Science*.
- **Noy, S. & Zhang, W.** (2023). "Experimental Evidence on the Productivity Effects of Generative AI." *Science*.
- **Dell'Acqua, F. et al.** (2023). "Navigating the Jagged Technological Frontier." Harvard Business School Working Paper.
- **Webb, M.** (2020). "The Impact of Artificial Intelligence on the Labor Market." Stanford Working Paper.
- **Massenkoff, M. & McCrory, M.** (2025). "Labor Market Impacts of AI." Anthropic Research.
- **Key finding**: LLMs disproportionately affect high-skill knowledge work — a reversal from previous automation waves.
- **Relevance**: Validates the tracker's graduate unemployment metric as an early indicator, and supports the AI Job Displacement Gap's focus on cognitive/office occupations as the primary displacement channel.

### 3.5 Scenario Analysis: Gradual vs. Transformative AI

Korinek and Suh (2024) model scenarios where AGI eliminates labor scarcity as a constraint on output. Wages initially rise in all scenarios — but only as long as labor remains scarce — then plummet as the economy approaches AGI. They identify that AI benchmark performance provides "concrete evidence of AI capabilities," while "financial markets are a mirror of expectations" and reflect public AGI expectations.

The IMF (Georgieva, 2024) estimates that AI will affect 40% of global jobs, with advanced economies facing the greatest exposure (~60% of jobs). In half of affected occupations, AI will augment workers; in the other half, it may displace them.

- **Korinek, A. & Suh, D.** (2024). "Scenarios for the Transition to AGI." NBER Working Paper 32255.
- **IMF** (2024). "AI Will Transform the Global Economy."
- **Key finding**: The transition path matters as much as the destination — monitoring the trajectory enables policy preparation.
- **Relevance**: Directly motivates the tracker's three-scenario projection framework (Augmentation, Agent Revolution, Physical AI).

---

## 4. Labor Share of Income and Factor Distribution

### 4.1 The Global Decline of Labor Share

Karabarbounis and Neiman (2014) documented a significant decline in the labor share of national income across most countries and industries since the early 1980s. They attribute roughly half of the decline to the falling relative price of investment goods (including IT equipment), which induced firms to substitute capital for labor. Their framework implies that as AI reduces the cost of automation capital, the labor share decline should accelerate.

- **Karabarbounis, L. & Neiman, B.** (2014). "The Global Decline of the Labor Share." *Quarterly Journal of Economics*, 129(1), 61–103.
- **Key finding**: Declining capital goods prices explain roughly half of the global labor share decline.
- **Relevance**: Directly relevant to the tracker's labor share and capital-labor substitution metrics. If AI dramatically reduces the cost of cognitive automation, the Karabarbounis-Neiman mechanism predicts accelerated labor share decline.

### 4.2 Superstar Firms and Market Concentration

Autor, Dorn, Katz, Patterson, and Van Reenen (2020) propose a "superstar firm" explanation: industries are increasingly dominated by firms with high productivity and low labor shares. As market share concentrates in these firms, the aggregate labor share falls even without changes within firms. The rise of tech giants (whose revenue-to-employee ratios dwarf traditional firms) exemplifies this mechanism.

- **Autor, D. et al.** (2020). "The Fall of the Labor Share and the Rise of Superstar Firms." *Quarterly Journal of Economics*, 135(2), 645–709.
- **Key finding**: Reallocation of activity toward superstar firms drives aggregate labor share decline.
- **Relevance**: AI may accelerate this dynamic by enabling a few firms with superior AI capabilities to capture disproportionate market share, further depressing aggregate labor share.

### 4.3 Rising Markups and Profit Shares

Barkai (2020) challenges the capital-labor substitution narrative by showing that the decline in labor share has not been offset by a rise in capital share — instead, the pure profit share has risen. This suggests increasing market power, not factor substitution, as the primary driver. De Loecker, Eeckhout, and Unger (2020) document a dramatic increase in average markups from 21% above marginal cost in 1980 to 61% by 2016.

- **Barkai, S.** (2020). "Declining Labor and Capital Shares." *Journal of Finance*, 75(5), 2421–2463.
- **De Loecker, J., Eeckhout, J., & Unger, G.** (2020). "The Rise of Market Power." *Quarterly Journal of Economics*, 135(2), 561–644.
- **Key finding**: Rising markups, not just automation, depress labor share — market power is a confounding factor.
- **Relevance**: The tracker must acknowledge that labor share declines have multiple causes. The smoking gun metrics (TFP acceleration, job displacement gap) help distinguish AI-driven displacement from market power effects.

### 4.4 Piketty's Capital Accumulation Thesis

Piketty's (2014) *Capital in the Twenty-First Century* frames inequality through the lens of r > g: when the rate of return on capital exceeds the rate of economic growth, wealth and income concentrate. AI potentially exacerbates this dynamic by creating a new form of "capital" (AI systems) with very high returns and near-zero marginal cost of replication.

- **Piketty, T.** (2014). *Capital in the Twenty-First Century.* Harvard University Press.
- **Key finding**: Structural forces favor capital over labor when r > g; AI may amplify this by creating high-return, low-marginal-cost capital.
- **Relevance**: The tracker's simultaneous monitoring of GDP per capita (total output growth) and labor share (distribution) captures whether the r > g dynamic is accelerating.

### 4.5 Synthesis: Labor Share as a Signal

Grossman and Oberfield (2022) provide a meta-assessment titled "The Elusive Explanation for the Declining Labor Share," concluding that no single explanation fully accounts for the pattern. The ILO (2024) reports that between 2004 and 2024, workers' output per hour increased globally by 58% while income increased by only 53%, creating a persistent wedge. The Philadelphia Fed (2024) specifically examines whether generative AI represents a "turning point" for labor's share.

- **Grossman, G.M. & Oberfield, E.** (2022). "The Elusive Explanation for the Declining Labor Share." *Annual Review of Economics*, 14, 93–124.
- **ILO** (2024). World Employment and Social Outlook.
- **Philadelphia Fed** (2024). "Generative AI: A Turning Point for Labor's Share?"
- **Key finding**: The labor share decline has multiple causes; AI may become the dominant driver if it accelerates capital-labor substitution.
- **Relevance**: The tracker's threshold of 5 percentage points of labor share decline in 3 years represents ~5× the historical rate, which would be difficult to explain without a novel structural force.

---

## 5. AI Compute Scaling and Energy Demand

### 5.1 Neural Scaling Laws

Kaplan et al. (2020) established that model test loss follows smooth power-law relationships with model size (N), dataset size (D), and compute (C), spanning more than seven orders of magnitude. Other architectural details have minimal effects within a wide range. The discovery enabled strategic resource allocation and established the theoretical basis for predicting capability from compute investment.

Hoffmann et al. (2022) — the "Chinchilla" paper — revised these scaling laws, finding that for compute-optimal training, "model size and the number of training tokens should be scaled equally." Their 70B-parameter Chinchilla model outperformed a 280B-parameter model trained on less data, establishing the ~20:1 token-to-parameter ratio guideline.

- **Kaplan, J. et al.** (2020). "Scaling Laws for Neural Language Models." arXiv:2001.08361.
- **Hoffmann, J. et al.** (2022). "Training Compute-Optimal Large Language Models." *NeurIPS 2022.*
- **Key finding**: AI capability scales predictably with compute; how money is spent matters as much as how much.
- **Relevance**: Establishes why NVIDIA revenue and electricity demand are meaningful proxies for AI capability advancement — there is a mathematical relationship between investment and performance.

### 5.2 Compute Trends and Constraints

Epoch AI's systematic tracking (Sevilla et al., 2022, updated through 2025) finds that training compute for frontier models grew at 4–5× per year from 2010 to 2024. LLM context windows have grown 30× per year since 2023. The computing power of the total stock of NVIDIA chips has grown 2.3× per year since 2019. However, the effective stock of quality human-generated training text may be exhausted between 2026 and 2032.

Epoch AI's (2024) analysis "Can AI Scaling Continue Through 2030?" concludes that training runs of 2e29 FLOP are feasible by 2030 — but binding constraints include electric power (frontier runs may require 4–16 GW), chip manufacturing capacity, data availability, and training latency. Whether developers pursue this scaling depends on "willingness to invest hundreds of billions of dollars."

- **Sevilla, J. et al.** (2022). "Compute Trends Across Three Eras of Machine Learning." *IJCNN*.
- **Epoch AI** (2024). "Can AI Scaling Continue Through 2030?"
- **Key finding**: Compute scaling has been remarkably consistent but faces physical constraints (energy, data, manufacturing).
- **Relevance**: Directly maps the relationship between energy infrastructure, semiconductor production, and AI scaling — the three dimensions the tracker monitors on the "cause" side. The data wall and energy constraints set upper bounds on the "cause" indicators.

### 5.3 NVIDIA as an Economic Proxy

NVIDIA's revenue trajectory has become the most widely cited proxy for AI investment: fiscal 2025 revenue of $115.2 billion (up 142% YoY), fiscal 2026 revenue of $215.9 billion (up 65%), with data center revenue surpassing $50 billion per quarter. Goldman Sachs projects total hyperscaler capex from 2025–2027 will reach $1.15 trillion, more than double the $477 billion from 2022–2024. NVIDIA cited "visibility" into $500 billion in chip spending over the next 14 months.

- **Key finding**: At $200B+/quarter, AI compute spending would approach 3–4% of US GDP — historically unprecedented concentration of investment in a single technology.
- **Relevance**: Validates NVIDIA revenue as the strongest available proxy for AI compute investment. The tracker's $200B/quarter threshold represents the inflection point where AI investment becomes macroeconomically significant.

### 5.4 Amodei's "Machines of Loving Grace"

Dario Amodei's (2024) 50+ page essay envisions AI accelerating biological research by a factor of 10 or more, "potentially compressing a century's worth of progress into just 5–10 years." He defines "powerful AI" as smarter than a Nobel Prize winner across most relevant fields, able to work autonomously on multi-week tasks. The essay represents the optimistic industry case for what compute scaling is building toward.

- **Amodei, D.** (2024). "Machines of Loving Grace." Essay.
- **Key finding**: Industry insiders envision transformative outcomes from continued compute scaling, not merely incremental improvement.
- **Relevance**: Provides context for why the tracker's cause indicators matter — they measure investment toward a goal that industry leaders describe as civilization-altering.

### 5.5 Energy Demand from AI Infrastructure

The IEA (2024–2025) estimates global data center electricity consumption at ~415 TWh in 2024 (~1.5% of global electricity), projecting doubling to ~945 TWh by 2030 (~3% of global electricity) — growing at 15% per year, four times faster than all other sectors combined. AI-driven servers grow at 30% annually versus 9% for conventional servers. US data centers consumed 183 TWh in 2024 (>4% of national electricity), with projections of 380–790 TWh by 2030.

Strubell, Ganesh, and McCallum (2019) quantified the environmental cost of AI training — a single large transformer model training produces carbon emissions comparable to the lifetime emissions of five automobiles. Patterson et al. (2021, 2022) at Google identified efficiency measures ("4Ms") that can reduce training energy by up to 100× and emissions by up to 1,000×, arguing that total training emissions may plateau by 2030 with best practices.

Regional concentration creates acute strain: Virginia's data centers consumed 26% of state electricity supply in 2023. Electric utility capex is projected to jump 22% YoY to $212 billion in 2025, with cumulative capex exceeding $1 trillion from 2025–2029. Carnegie Mellon estimates data centers could increase average US electricity bills by 8% by 2030.

- **IEA** (2024–2025). "Energy and AI" report series.
- **Strubell, E., Ganesh, A., & McCallum, A.** (2019). "Energy and Policy Considerations for Deep Learning in NLP." *ACL 2019*.
- **Patterson, D. et al.** (2021/2022). "Carbon Emissions and Large Neural Network Training" / "The Carbon Footprint of Machine Learning Training Will Plateau, Then Shrink."
- **Key finding**: AI scaling requires massive electricity infrastructure buildout; energy is both a constraint on and proxy for AI capability growth.
- **Relevance**: Validates the tracker's use of electricity production indices. The 15% three-year growth threshold represents a dramatic departure from decades of ~1%/year electricity demand growth, detectable only through data center-driven consumption.

---

## 6. GDP, Productivity, and the AI Paradox

### 6.1 The Solow Productivity Paradox

Robert Solow's (1987) observation — "You can see the computer age everywhere but in the productivity statistics" — established the central puzzle. Following transistors and microprocessors, US productivity growth dropped from 2.9% (1948–1973) to 1.1% after 1973. This template is directly relevant: massive AI investment may not immediately appear in aggregate productivity data.

Brynjolfsson (1993) coined the term "productivity paradox" and later applied it specifically to AI (Brynjolfsson, Rock, & Syverson, 2017). He identifies four potential explanations: (1) false hopes (AI is not actually productive); (2) mismeasurement (statistics understate AI's contribution); (3) redistribution (private gains without aggregate improvement); (4) implementation lags (the biggest factor — technology takes decades to reshape organizations).

- **Solow, R.** (1987). "We'd better watch out." *New York Times Book Review*.
- **Brynjolfsson, E.** (1993). "The Productivity Paradox of Information Technology." *Communications of the ACM*.
- **Brynjolfsson, E., Rock, D., & Syverson, C.** (2017). "Artificial Intelligence and the Modern Productivity Paradox." NBER Working Paper 24001.
- **Key finding**: Implementation lags of 10–25 years are typical for transformative technologies; a gap between AI investment and productivity gains is expected, not anomalous.
- **Relevance**: A divergence between the tracker's cause indicators (rising) and GDP per capita (flat) may reflect implementation lags rather than absence of impact. This lag is why the tracker includes both cause and effect indicators with different expected timing.

### 6.2 Growth Skepticism: Gordon's Critique

Robert Gordon's (2016) *The Rise and Fall of American Growth* argues that the life-altering innovations of 1870–1970 (electricity, internal combustion, indoor plumbing) "cannot be repeated." Labor productivity growth fell from 2.82% annually (1920–1970) to 1.62% (1970–2014). He contends the digital revolution generated only a decade-long productivity boost (1996–2006) and that AI will yield "gradual and evolutionary, not sudden and revolutionary" improvements. Additional headwinds — rising inequality, stagnating education, aging population, rising debt — further constrain growth.

- **Gordon, R.J.** (2016). *The Rise and Fall of American Growth.* Princeton University Press.
- **Key finding**: Technology's best contributions to human welfare may be behind us; AI may yield only incremental improvements.
- **Relevance**: Represents the strongest "null hypothesis" for the tracker. If Gordon is right, effect indicators (GDP per capita, labor share) should show no acceleration even as cause indicators rise.

### 6.3 Nordhaus's Formal Test for Economic Singularity

Nordhaus (2015/2021) formally tested whether the economy exhibits accelerating growth characteristic of an approaching singularity. His growth model features a singularity condition and presents several empirical tests. Key finding: "the Singularity is not near." He argues that "continued rapid growth of information technology has no necessary implication for aggregate economic growth, because the economy does not run on bits alone." The critical variable is the substitutability between information and conventional inputs.

- **Nordhaus, W.D.** (2015/2021). "Are We Approaching an Economic Singularity?" NBER Working Paper 21547 / *American Economic Journal: Macroeconomics*.
- **Key finding**: Formal econometric tests find no evidence of singularity-type acceleration in current data.
- **Relevance**: Provides the benchmark quantitative test against which the tracker's TFP acceleration metric can be evaluated. The tracker's 6% TFP rise threshold over 3 years represents the kind of acceleration Nordhaus was testing for and did not find.

### 6.4 Acemoglu's Skeptical Macroeconomic Estimate

Acemoglu's (2024) "The Simple Macroeconomics of AI" provides the most rigorous skeptical estimate: AI's macroeconomic effects are "non-trivial but modest — no more than a 0.66% increase in total factor productivity over 10 years." He argues current AI primarily targets "easy-to-learn tasks" while hard-to-learn tasks remain beyond reach. On distribution: AI is unlikely to increase inequality as much as previous automation technologies but will widen the capital-labor gap.

- **Acemoglu, D.** (2024). "The Simple Macroeconomics of AI." NBER Working Paper 32487 / *Economic Policy*.
- **Key finding**: AI's aggregate GDP impact may be modest (~0.06%/year TFP growth); distributional effects on labor share are more significant.
- **Relevance**: Acemoglu's estimate provides a baseline "no structural change" prediction. If the tracker's TFP metric shows growth exceeding his upper bound (~0.1%/year), this would constitute evidence against the skeptical view.

### 6.5 Optimistic Projections

More optimistic estimates project larger effects: Penn Wharton estimates AI could raise US GDP by ~$2.48 trillion by 2030. Goldman Sachs projects AI could boost US productivity by 1.5% annually over the next decade. The Dallas Fed estimates AI will increase productivity and GDP by 1.5% by 2035, nearly 3% by 2055, and 3.7% by 2075. St. Louis Fed research finds workers using generative AI saved 5.4% of work hours, with 26.4% of workers using generative AI at work in H2 2024.

Aghion, Jones, and Jones (2018) model AI as the latest form of automation spanning 200+ years. Key insight via Baumol's "cost disease": economic growth may be constrained not by what we are good at, but by what is essential and yet hard to improve. However, if AI boosts idea generation (not just production), it could overcome the Baumol constraint.

- **Aghion, P., Jones, B.F., & Jones, C.I.** (2018). "Artificial Intelligence and Economic Growth." In *The Economics of AI: An Agenda*, NBER.
- **Various** (2024–2025). Dallas Fed, Goldman Sachs, Penn Wharton Budget Model projections.
- **Key finding**: Estimates span an order of magnitude — from 0.06%/year (Acemoglu) to 1.5%/year (Goldman Sachs) in productivity impact.
- **Relevance**: The tracker's GDP per capita threshold (12% over 3 years, implying ~4%/year growth) sits well above even the optimistic estimates, representing a genuine structural break if observed.

### 6.6 The GDP-Welfare Disconnect

The ILO (2024) reports a persistent disconnect: between 2004 and 2024, global workers' output per hour increased by 58% while income increased by only 53%. Had the labor share remained unchanged, global labor income would have been $1 trillion higher in 2024. Brookings (2025) analyzes how AI may widen income inequality even while boosting aggregate output.

- **ILO** (2024). World Employment and Social Outlook.
- **Brookings** (2025). "AI's Impact on Income Inequality in the US."
- **Key finding**: GDP can rise while labor welfare stagnates or declines.
- **Relevance**: Validates the tracker's architecture of monitoring both GDP per capita AND labor share. Their divergence — rising GDP with falling labor share — is the signature of automation-driven growth that benefits capital more than labor.

---

## 7. Methodological Foundations

### 7.1 Composite Index Construction

**OECD/JRC Handbook (Nardo et al., 2008)**: The foundational reference for composite indicator methodology, outlining a 10-step process: theoretical framework, data selection, imputation, multivariate analysis, normalization, weighting, aggregation, robustness analysis, decomposition, and visualization. Every methodological choice involves trade-offs that must be made transparent.

**Human Development Index**: The HDI's 2010 shift from arithmetic to geometric mean aggregation was significant — it means poor performance in one dimension is not fully compensated by good performance in another. This parallels the tracker's coherence factor, which penalizes scores where only a few metrics are active.

**Global Innovation Index**: The GII's input-output framework (innovation inputs → outputs) parallels the tracker's cause-effect structure. Its Monte Carlo robustness methodology (confidence intervals via weight perturbation) provides a transferable technique.

- **Nardo, M. et al.** (2008). *Handbook on Constructing Composite Indicators.* OECD/JRC.
- **Saisana, M., Saltelli, A., & Tarantola, S.** (2005). "Uncertainty and Sensitivity Analysis Techniques as Tools for Quality Assessment of Composite Indicators." *Journal of the Royal Statistical Society: Series A*, 168(2), 307–323.
- **Relevance**: The tracker's normalization (progress toward fixed thresholds), weighting (expert-assigned with category hierarchy), and aggregation (weighted average with coherence multiplier) choices should be evaluated against these established frameworks. Monte Carlo sensitivity analysis would strengthen robustness claims.

### 7.2 Time Series Analysis for Structural Breaks

**Bai and Perron (1998, 2003)** developed the framework for estimating multiple structural breaks at unknown dates in linear models. Their dynamic programming algorithm finds globally optimal break dates and provides tests for determining the number of breaks. Directly applicable to detecting when trend parameters shift in labor share or other economic series.

**Hamilton (1989)** introduced Markov regime-switching models where time series alternate between discrete regimes governed by an unobserved Markov chain. Smoothed regime probabilities provide a probabilistic assessment of which regime the economy is in at each date — a natural output for the dashboard.

**Adams and MacKay (2007)** developed Bayesian Online Change-Point Detection (BOCPD), maintaining a posterior distribution over the "run length" (time since last change-point) that updates with each observation. BOCPD is computationally lightweight and suitable for real-time monitoring.

**Brown, Durbin, and Evans (1975)** introduced CUSUM tests that accumulate recursive residuals and test whether the cumulative sum wanders outside expected bounds. As monitoring procedures, they can be applied sequentially as new data arrives.

- **Bai, J. & Perron, P.** (1998/2003). "Estimating and Testing Linear Models with Multiple Structural Changes." *Econometrica* / *Journal of Applied Econometrics*.
- **Hamilton, J.D.** (1989). "A New Approach to the Economic Analysis of Nonstationary Time Series." *Econometrica*, 57(2), 357–384.
- **Adams, R.P. & MacKay, D.J.C.** (2007). "Bayesian Online Changepoint Detection." arXiv:0710.3742.
- **Relevance**: These methods offer more rigorous alternatives to the tracker's current rolling-window trend analysis. BOCPD in particular could provide formally grounded "probability of regime change" metrics, and Markov-switching models could classify whether the economy is in a "normal" or "displacement" regime.

### 7.3 Trend Analysis and Filtering

**Hamilton (2018)** demonstrates that the widely used Hodrick-Prescott filter produces spurious dynamics, creates series with spurious periodicity, and depends undesirably on endpoint observations — the very observations most relevant for real-time monitoring. He proposes an alternative: regress y(t) on y(t-h) using OLS, where h=8 for quarterly data.

**Mann (1945) and Kendall (1975)** provide the non-parametric Mann-Kendall trend test, which is robust to outliers and non-normal distributions. The Sen-Theil slope estimator provides a non-parametric estimate of trend magnitude. Modifications exist for serial correlation and seasonal data.

- **Hamilton, J.D.** (2018). "Why You Should Never Use the Hodrick-Prescott Filter." *Review of Economics and Statistics*, 100(5), 831–843.
- **Relevance**: The tracker's rolling-window approach avoids some HP filter pitfalls but should be evaluated against Hamilton's regression-based alternative. The Mann-Kendall test could supplement the current consistency scoring with formal statistical significance.

### 7.4 Leading Indicator Theory

**Burns and Mitchell (1946)** established the methodology of classifying economic series as leading, coincident, or lagging relative to turning points. **Stock and Watson (1989)** formalized this with dynamic factor models that extract common factors from multiple indicators, handling mixed frequencies and providing optimal signal extraction.

**The Conference Board's LEI** methodology provides interpretation rules directly transferable to the tracker: consecutive declines, threshold-crossing, and diffusion (proportion of components declining). The diffusion concept — measuring breadth of signal rather than magnitude — is a robust complement to composite levels.

- **Burns, A.F. & Mitchell, W.C.** (1946). *Measuring Business Cycles.* NBER.
- **Stock, J.H. & Watson, M.W.** (1989). "New Indexes of Coincident and Leading Economic Indicators." *NBER Macroeconomics Annual*.
- **Stock, J.H. & Watson, M.W.** (2002). "Forecasting Using Principal Components from a Large Number of Predictors." *JASA*, 97(460), 1167–1179.
- **Relevance**: The tracker's cause/effect distinction maps onto leading/lagging indicator theory. A dynamic factor model could formally extract the common "AI displacement signal" from the mixed-frequency data. Reporting diffusion alongside the composite score would provide a breadth-of-signal measure.

### 7.5 Scenario Analysis Frameworks

**Wack (1985)** describes Shell's scenario planning methodology: scenarios are not predictions but alternative narratives about how the future might unfold, designed to challenge mental models. The **IPCC's Shared Socioeconomic Pathways** (O'Neill et al., 2014/2017) provide the gold standard for combining qualitative narratives with quantitative projections, using a modular framework separating development trajectories from policy responses.

**Fan charts** (Britton, Fisher, & Whitley, 1998), introduced by the Bank of England, communicate forecast uncertainty through probability distributions that widen over the horizon — a standard visualization for economic projections.

- **Wack, P.** (1985). "Scenarios: Uncharted Waters Ahead." *Harvard Business Review*.
- **O'Neill, B.C. et al.** (2014/2017). "Shared Socioeconomic Pathways." *Climatic Change* / *Global Environmental Change*.
- **Relevance**: The tracker's three scenarios (Augmentation, Agent Revolution, Physical AI) parallel the IPCC's structured approach. Each should include both qualitative narrative logic and quantitative projections, with fan charts communicating uncertainty.

### 7.6 Causal Inference Limitations

The tracker operates at the macro level where causal identification is fundamentally limited. Granger (1969) causality tests assess predictive content, not true causality. Acemoglu and Restrepo (2020) achieve causal identification by exploiting cross-sectional variation in robot exposure — a strategy unavailable in aggregate time series. Autor and Dorn (2013) use historical instruments interacted with technology trends.

The tracker should be framed as a monitoring tool detecting patterns *consistent with* AI-driven structural change, not proving causality. Multiple confounds (monetary policy, globalization, pandemic effects, demographic shifts) affect all tracked indicators simultaneously.

- **Granger, C.W.J.** (1969). "Investigating Causal Relations by Econometric Models." *Econometrica*, 37(3), 424–438.
- **Autor, D.H.** (2015). "Why Are There Still So Many Jobs?" *Journal of Economic Perspectives*, 29(3), 3–30.
- **Relevance**: The tracker's composite approach (requiring multiple independent indicators to move simultaneously) partially addresses causality concerns — it is unlikely that confounding factors would move all eight metrics in the predicted direction simultaneously. But this is pattern consistency, not causal proof.

### 7.7 Existing AI Impact Dashboards

Several existing efforts provide complementary monitoring:

**Stanford HAI AI Index** (annually since 2017): The most comprehensive annual report on AI trends — R&D, technical performance, economy, education, policy. Provides context indicators but does not construct a composite displacement score.

**OECD AI Policy Observatory** (oecd.ai): Aggregates data on AI policies, research, and impacts across member countries. Provides demand-side adoption data (AI skills in job postings) more granular than the tracker's supply-side proxies.

**McKinsey Global Institute** (various): Estimates 30% of US work hours automatable by 2030; generative AI disproportionately affects knowledge workers. Task-based automation potential framework complements the tracker's time-series approach.

**Felten, Raj, and Seamans (2021/2023)**: Construct an AI Occupational Exposure (AIOE) index linking AI capabilities to occupational abilities. Found that generative AI exposure is highest in high-wage, high-education occupations — inverting the traditional automation pattern.

**TechShock.ai (2024–2025)**: An emerging Technological Shock Index tracking structural labor shifts from technology — methodologically analogous to the tracker's AI Singularity Score.

- **Stanford HAI** (2024). *AI Index Report*.
- **Felten, E., Raj, M., & Seamans, R.** (2021/2023). "Occupational Exposure to Artificial Intelligence." *Strategic Management Journal*.
- **Relevance**: The tracker's distinctive contribution is the composite economic displacement score combining cause and effect indicators with real-time monitoring — which none of these existing efforts provide. They offer complementary data for cross-validation.

---

## 8. Synthesis: Mapping the Literature to the Tracker

### 8.1 Theoretical Grounding by Metric Category

| Tracker Category | Metrics | Primary Literature | Theoretical Basis |
|---|---|---|---|
| **Smoking Guns** | TFP Acceleration | Nordhaus (2015), Acemoglu (2024), Aghion et al. (2018) | Sustained TFP acceleration beyond historical norms would falsify Gordon's stagnation thesis and approach Nordhaus's singularity condition |
| | AI Job Displacement Gap | Autor et al. (2003, 2024), Eloundou et al. (2024), Webb (2020) | Differential employment change between AI-exposed and non-exposed occupations directly tests the task-based displacement framework |
| | Capital-Labor Substitution | Karabarbounis & Neiman (2014), Acemoglu & Restrepo (2019, 2022) | Rising capital-labor ratio at 5× historical rate would indicate firms are actively substituting AI capital for human labor |
| **Displacement Effects** | Labor Share Decline | Karabarbounis & Neiman (2014), Autor et al. (2020), Barkai (2020), Piketty (2014) | Accelerated decline confirms automation's distributional channel; must be distinguished from market power effects |
| | GDP/Capita Growth | Solow (1987), Brynjolfsson et al. (2017), Gordon (2016) | Acceleration above trend — especially diverging from labor share — signals automation-driven growth benefiting capital |
| | College Unemployment Rise | Beaudry et al. (2016), Eloundou et al. (2024), Massenkoff & McCrory (2025) | Structural unemployment in knowledge-work occupations would invert the historical pattern of technology complementing educated workers |
| **Investment Causes** | NVIDIA Revenue | Kaplan et al. (2020), Hoffmann et al. (2022), Sevilla et al. (2022) | Scaling laws establish a mathematical link between compute investment and AI capability |
| | Electricity Production | IEA (2024–2025), Epoch AI (2024), Strubell et al. (2019) | Energy demand is both a necessary condition for and measurable proxy of AI scaling |

### 8.2 Key Academic Debates and Their Implications

**1. Is scaling sufficient for transformative AI?**
Marcus, Chollet, and the 2025 AAAI survey argue no; Kaplan, Hoffmann, and industry scaling efforts suggest yes. *Implication for tracker*: Cause indicators (compute investment) may rise without effect indicators (labor displacement) following, if scaling hits diminishing returns.

**2. Will compensation mechanisms hold?**
Classical theory (Say, McCulloch) says yes; Susskind (2020), Acemoglu & Johnson (2023) say not necessarily. *Implication for tracker*: The reinstatement effect (new task creation) is the key variable. If the AI Job Displacement Gap widens while TFP accelerates, this suggests displacement is outpacing compensation.

**3. How large is the implementation lag?**
Brynjolfsson et al. (2017) estimate 10–25 years based on historical analogies. *Implication for tracker*: Cause indicators may lead effect indicators by years or decades. The three-year rolling window may be too short to detect structural change in its early stages.

**4. Is the labor share decline driven by automation or market power?**
Karabarbounis & Neiman (2014) emphasize automation; Barkai (2020) and De Loecker et al. (2020) emphasize market power. *Implication for tracker*: The smoking gun metrics (TFP, job displacement gap, capital-labor ratio) help distinguish these channels.

**5. Does GDP growth reflect AI's true impact?**
The mismeasurement hypothesis (Brynjolfsson) suggests GDP underestimates AI's contribution; Gordon argues GDP correctly reflects modest impact. *Implication for tracker*: The tracker monitors GDP alongside more direct indicators precisely because GDP alone may be an unreliable measure.

### 8.3 Methodological Enhancements Suggested by the Literature

The review identifies several methodological upgrades that would strengthen the tracker's analytical framework:

1. **Bayesian Online Change-Point Detection** (Adams & MacKay, 2007): Provides formally grounded "probability of regime change" metrics, replacing ad hoc consistency scoring.
2. **Monte Carlo sensitivity analysis** (Saisana et al., 2005): Propagates uncertainty in weighting and normalization choices through to the composite score, producing confidence intervals.
3. **Dynamic factor model** (Stock & Watson, 1989): Extracts a common signal from mixed-frequency data, optimally combining quarterly and monthly indicators.
4. **Diffusion index** (Moore, 1950s): Complements the composite score with a "breadth of signal" measure — how many metrics simultaneously show displacement patterns.
5. **Fan charts** (Bank of England, 1998): Replaces deterministic scenario projections with probabilistic uncertainty visualization.
6. **Hamilton trend extraction** (Hamilton, 2018): Avoids HP filter endpoint distortions that are particularly damaging for real-time monitoring.

### 8.4 The Tracker's Position in the Literature

The AI Singularity Tracker occupies a unique niche in the emerging AI monitoring landscape:

- Unlike **Stanford HAI** and **OECD.AI**, which catalog AI ecosystem trends descriptively, the tracker constructs a composite displacement score with explicit thresholds and scoring methodology.
- Unlike **Frey & Osborne** and **Felten et al.**, which estimate *potential* automation exposure, the tracker monitors *realized* economic outcomes.
- Unlike **Acemoglu** and **Nordhaus**, who estimate aggregate effects in equilibrium models, the tracker is designed for real-time detection of *disequilibrium* — the period before institutional adjustment catches up to technological change.
- Unlike **McKinsey** and other consultancy estimates, the tracker is grounded in publicly available data with transparent methodology.

The tracker's most distinctive contribution is its simultaneous monitoring of cause indicators (compute investment, energy demand) and effect indicators (labor share, unemployment, GDP), combined with smoking gun metrics (TFP, job displacement gap, capital-labor substitution) that can distinguish AI-driven structural change from other macroeconomic forces. This multi-dimensional approach addresses the causal identification problem acknowledged throughout the literature: while no single indicator can prove AI-driven displacement, the simultaneous movement of eight theoretically independent indicators in the predicted direction would constitute strong circumstantial evidence.

---

## References

### Singularity and AI Theory
- Amodei, D. (2024). "Machines of Loving Grace." Essay.
- Bostrom, N. (2014). *Superintelligence: Paths, Dangers, Strategies.* Oxford University Press.
- Chollet, F. (2017). "The Impossibility of Intelligence Explosion." *Medium.*
- Good, I.J. (1965). "Speculations Concerning the First Ultraintelligent Machine." *Advances in Computers*, 6, 31–88.
- Kurzweil, R. (2005). *The Singularity Is Near.* Viking Press.
- Marcus, G. (2018). "In Defense of Skepticism About Deep Learning." *Medium.*
- Vinge, V. (1993). "The Coming Technological Singularity." NASA Technical Report CP-10129.

### Technological Unemployment and Labor Markets
- Acemoglu, D. (2024). "Learning from Ricardo and Thompson." MIT Working Paper.
- Acemoglu, D. & Johnson, S. (2023). *Power and Progress.* PublicAffairs.
- Acemoglu, D. & Restrepo, P. (2019). "Automation and New Tasks." *Journal of Economic Perspectives*, 33(2), 3–30.
- Acemoglu, D. & Restrepo, P. (2020). "Robots and Jobs." *Journal of Political Economy*, 128(6), 2188–2244.
- Acemoglu, D. & Restrepo, P. (2022). "Tasks, Automation, and Wage Inequality." *Econometrica*, 90(5), 1973–2016.
- Arntz, M., Gregory, T., & Zierahn, M. (2016). "The Risk of Automation for Jobs in OECD Countries." OECD Working Papers No. 189.
- Autor, D.H. (2015). "Why Are There Still So Many Jobs?" *Journal of Economic Perspectives*, 29(3), 3–30.
- Autor, D.H. (2019). "Work of the Past, Work of the Future." *AEA Papers and Proceedings*, 109, 1–32.
- Autor, D.H. (2024). "Applying AI to Rebuild Middle Class Jobs." NBER Working Paper 32140.
- Autor, D.H., Chin, C., Salomons, A., & Seegmiller, B. (2024). "New Frontiers." *Quarterly Journal of Economics*, 139(3), 1399–1465.
- Autor, D.H. & Dorn, D. (2013). "The Growth of Low-Skill Service Jobs." *American Economic Review*, 103(5), 1553–1597.
- Autor, D.H., Levy, F., & Murnane, R.J. (2003). "The Skill Content of Recent Technological Change." *Quarterly Journal of Economics*, 118(4), 1279–1333.
- Dell'Acqua, F. et al. (2023). "Navigating the Jagged Technological Frontier." Harvard Business School Working Paper.
- Eloundou, T. et al. (2024). "GPTs are GPTs." *Science*.
- Felten, E., Raj, M., & Seamans, R. (2021/2023). "Occupational Exposure to Artificial Intelligence." *Strategic Management Journal*, 42(12), 2195–2217.
- Frey, C.B. & Osborne, M.A. (2017). "The Future of Employment." *Technological Forecasting and Social Change*, 114, 254–280.
- Keynes, J.M. (1930). "Economic Possibilities for our Grandchildren."
- Korinek, A. & Suh, D. (2024). "Scenarios for the Transition to AGI." NBER Working Paper 32255.
- Massenkoff, M. & McCrory, M. (2025). "Labor Market Impacts of AI." Anthropic Research.
- Noy, S. & Zhang, W. (2023). "Experimental Evidence on Productivity Effects of Generative AI." *Science*.
- Ricardo, D. (1821). *On the Principles of Political Economy and Taxation*, 3rd ed.
- Susskind, D. (2020). *A World Without Work.* Metropolitan Books.
- Webb, M. (2020). "The Impact of Artificial Intelligence on the Labor Market." Stanford Working Paper.

### Labor Share and Factor Distribution
- Autor, D. et al. (2020). "The Fall of the Labor Share and the Rise of Superstar Firms." *Quarterly Journal of Economics*, 135(2), 645–709.
- Barkai, S. (2020). "Declining Labor and Capital Shares." *Journal of Finance*, 75(5), 2421–2463.
- De Loecker, J., Eeckhout, J., & Unger, G. (2020). "The Rise of Market Power." *Quarterly Journal of Economics*, 135(2), 561–644.
- Grossman, G.M. & Oberfield, E. (2022). "The Elusive Explanation for the Declining Labor Share." *Annual Review of Economics*, 14, 93–124.
- ILO (2024). World Employment and Social Outlook.
- Karabarbounis, L. & Neiman, B. (2014). "The Global Decline of the Labor Share." *Quarterly Journal of Economics*, 129(1), 61–103.
- Philadelphia Fed (2024). "Generative AI: A Turning Point for Labor's Share?"
- Piketty, T. (2014). *Capital in the Twenty-First Century.* Harvard University Press.

### Compute Scaling and Energy
- Epoch AI (2024). "Can AI Scaling Continue Through 2030?"
- Hoffmann, J. et al. (2022). "Training Compute-Optimal Large Language Models." *NeurIPS 2022.*
- IEA (2024–2025). "Energy and AI" report series.
- Kaplan, J. et al. (2020). "Scaling Laws for Neural Language Models." arXiv:2001.08361.
- Patterson, D. et al. (2021/2022). "Carbon Emissions and Large Neural Network Training" / "The Carbon Footprint of ML Training."
- Sevilla, J. et al. (2022). "Compute Trends Across Three Eras of Machine Learning." *IJCNN*.
- Strubell, E., Ganesh, A., & McCallum, A. (2019). "Energy and Policy Considerations for Deep Learning in NLP." *ACL 2019*.

### GDP, Productivity, and Growth
- Acemoglu, D. (2024). "The Simple Macroeconomics of AI." NBER Working Paper 32487.
- Aghion, P., Jones, B.F., & Jones, C.I. (2018). "Artificial Intelligence and Economic Growth." NBER.
- Brynjolfsson, E. (1993). "The Productivity Paradox of Information Technology." *Communications of the ACM*.
- Brynjolfsson, E., Rock, D., & Syverson, C. (2017). "AI and the Modern Productivity Paradox." NBER Working Paper 24001.
- Gordon, R.J. (2016). *The Rise and Fall of American Growth.* Princeton University Press.
- IMF (2024). "AI Will Transform the Global Economy."
- Nordhaus, W.D. (2015/2021). "Are We Approaching an Economic Singularity?" NBER Working Paper 21547.
- Solow, R. (1987). "We'd better watch out." *New York Times Book Review*.

### Methodology
- Adams, R.P. & MacKay, D.J.C. (2007). "Bayesian Online Changepoint Detection." arXiv:0710.3742.
- Bai, J. & Perron, P. (1998/2003). "Multiple Structural Changes." *Econometrica* / *Journal of Applied Econometrics*.
- Britton, E., Fisher, P.G., & Whitley, J.D. (1998). "Understanding the Fan Chart." *Bank of England Quarterly Bulletin*.
- Brown, R.L., Durbin, J., & Evans, J.M. (1975). "Techniques for Testing Constancy of Regression Relationships." *JRSS-B*, 37(2), 149–192.
- Burns, A.F. & Mitchell, W.C. (1946). *Measuring Business Cycles.* NBER.
- Granger, C.W.J. (1969). "Investigating Causal Relations." *Econometrica*, 37(3), 424–438.
- Hamilton, J.D. (1989). "A New Approach to Nonstationary Time Series." *Econometrica*, 57(2), 357–384.
- Hamilton, J.D. (2018). "Why You Should Never Use the Hodrick-Prescott Filter." *Review of Economics and Statistics*, 100(5), 831–843.
- Mann, H.B. (1945). "Nonparametric Tests Against Trend." *Econometrica*, 13(3), 245–259.
- Nardo, M. et al. (2008). *Handbook on Constructing Composite Indicators.* OECD/JRC.
- O'Neill, B.C. et al. (2014/2017). "Shared Socioeconomic Pathways." *Climatic Change* / *Global Environmental Change*.
- Saisana, M., Saltelli, A., & Tarantola, S. (2005). "Sensitivity Analysis for Composite Indicators." *JRSS-A*, 168(2), 307–323.
- Stock, J.H. & Watson, M.W. (1989). "New Indexes of Coincident and Leading Economic Indicators." *NBER Macroeconomics Annual*.
- Stock, J.H. & Watson, M.W. (2002). "Forecasting Using Principal Components." *JASA*, 97(460), 1167–1179.
- Wack, P. (1985). "Scenarios: Uncharted Waters Ahead." *Harvard Business Review*.

### Existing AI Indices and Dashboards
- Brookings Institution (2019/2025). "Automation and AI" / "AI's Impact on Income Inequality."
- McKinsey Global Institute (2017/2023). "A Future That Works" / "The Economic Potential of Generative AI."
- OECD AI Policy Observatory (2020–present). oecd.ai.
- Stanford HAI (2024). *AI Index Report*.
- TechShock.ai (2024–2025). Technological Shock Index.

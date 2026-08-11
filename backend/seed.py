from sqlmodel import Session, delete
from .database import engine, create_db_and_tables
from .models import QuestionItem

def seed_data():
    create_db_and_tables()
    questions = []

    # ═══════════════════════════════════════════════════════════
    # READING SECTION — Routing Pool (10 unique items)
    # ═══════════════════════════════════════════════════════════

    # 5x READ_DAILY_LIFE (each with unique passage, question, and options)
    questions.append(QuestionItem(
        section="Reading", task_type="READ_DAILY_LIFE", difficulty_pool="ROUTING",
        content_meta={
            "passage": "NOTICE: The Student Recreation Center will extend its hours during finals week, opening from 6:00 AM to midnight. Free yoga and meditation sessions will be offered daily at 7 PM in Studio B.",
            "question": "What change is being made during finals week?",
            "options": ["The recreation center will close early.", "Operating hours will be extended.", "Yoga sessions are being canceled.", "Studio B is under renovation."]
        },
        correct_answer_key="Operating hours will be extended."
    ))
    questions.append(QuestionItem(
        section="Reading", task_type="READ_DAILY_LIFE", difficulty_pool="ROUTING",
        content_meta={
            "passage": "CAMPUS ALERT: Beginning March 15th, all vehicles must display updated parking permits. Vehicles without valid permits will be subject to towing. New permits can be obtained from the Transportation Office in Building C.",
            "question": "What will happen to vehicles without updated permits?",
            "options": ["They will receive a warning email.", "They may be towed.", "They will be fined $50.", "They must park off-campus."]
        },
        correct_answer_key="They may be towed."
    ))
    questions.append(QuestionItem(
        section="Reading", task_type="READ_DAILY_LIFE", difficulty_pool="ROUTING",
        content_meta={
            "passage": "The Department of Biology is hosting a guest lecture by Dr. Elena Vasquez on marine ecosystem resilience. The talk will take place on Thursday, April 3rd at 4:00 PM in Lecture Hall 200. Attendance is open to all students.",
            "question": "Who is giving the guest lecture?",
            "options": ["A biology student.", "The department chair.", "Dr. Elena Vasquez.", "A marine biologist from NOAA."]
        },
        correct_answer_key="Dr. Elena Vasquez."
    ))
    questions.append(QuestionItem(
        section="Reading", task_type="READ_DAILY_LIFE", difficulty_pool="ROUTING",
        content_meta={
            "passage": "DUE TO CONSTRUCTION: The north entrance of the Science Building will be closed until further notice. Please use the south entrance near the parking garage. We apologize for any inconvenience.",
            "question": "Why is the north entrance closed?",
            "options": ["A security concern.", "An emergency drill.", "Construction work.", "A scheduled inspection."]
        },
        correct_answer_key="Construction work."
    ))
    questions.append(QuestionItem(
        section="Reading", task_type="READ_DAILY_LIFE", difficulty_pool="ROUTING",
        content_meta={
            "passage": "DINING SERVICES UPDATE: Starting next semester, the main cafeteria will offer a plant-based menu option alongside the traditional selections. A survey found that 68% of students wanted more vegetarian choices.",
            "question": "What is the cafeteria adding?",
            "options": ["A new payment system.", "Extended breakfast hours.", "A plant-based menu option.", "A self-service cooking area."]
        },
        correct_answer_key="A plant-based menu option."
    ))

    # 5x COMPLETE_WORDS (each with unique passage content)
    questions.append(QuestionItem(
        section="Reading", task_type="COMPLETE_WORDS", difficulty_pool="ROUTING",
        content_meta={
            "passage": "Photosyn___esis is the process by which green plants convert sun___ght into chemical energy.",
            "question": "Complete the missing word parts.",
            "options": ["th, li", "th, ni", "to, li", "th, ri"]
        },
        correct_answer_key="th, li"
    ))
    questions.append(QuestionItem(
        section="Reading", task_type="COMPLETE_WORDS", difficulty_pool="ROUTING",
        content_meta={
            "passage": "The Industrial Revo___tion fundamentally trans___med the economic landscape of Europe in the 18th century.",
            "question": "Complete the missing word parts.",
            "options": ["lu, for", "lu, sti", "la, for", "lu, for"]
        },
        correct_answer_key="lu, for"
    ))
    questions.append(QuestionItem(
        section="Reading", task_type="COMPLETE_WORDS", difficulty_pool="ROUTING",
        content_meta={
            "passage": "Artifi___al intelli___ce is rapidly changing how businesses approach data analysis and decision-making.",
            "question": "Complete the missing word parts.",
            "options": ["ci, gen", "ti, gen", "ci, gen", "ci, gin"]
        },
        correct_answer_key="ci, gen"
    ))
    questions.append(QuestionItem(
        section="Reading", task_type="COMPLETE_WORDS", difficulty_pool="ROUTING",
        content_meta={
            "passage": "Demo___racy requires active parti___ation from its citizens to function effectively.",
            "question": "Complete the missing word parts.",
            "options": ["c, cip", "cr, cip", "c, cap", "cr, cep"]
        },
        correct_answer_key="c, cip"
    ))
    questions.append(QuestionItem(
        section="Reading", task_type="COMPLETE_WORDS", difficulty_pool="ROUTING",
        content_meta={
            "passage": "Sustain___ility in urban plan___ng involves balancing economic growth with environmental protection.",
            "question": "Complete the missing word parts.",
            "options": ["ab, ni", "ab, ni", "ib, ni", "ab, mi"]
        },
        correct_answer_key="ab, ni"
    ))

    # ═══════════════════════════════════════════════════════════
    # READING — Hard Pool (5 unique academic items)
    # ═══════════════════════════════════════════════════════════
    hard_reading = [
        {
            "passage": "The Cambrian explosion, approximately 541 million years ago, was a pivotal event in the history of life on Earth. Over a geologically brief period, most major animal phyla appeared in the fossil record. Scientists debate whether this was triggered by environmental changes, genetic innovation, or ecological pressures.",
            "question": "What is the main debate about the Cambrian explosion?",
            "options": ["Whether it actually occurred.", "What triggered it.", "How long it lasted.", "Which species survived it."],
            "answer": "What triggered it."
        },
        {
            "passage": "Quantum entanglement is a phenomenon where two particles become interconnected such that the quantum state of one instantly influences the other, regardless of distance. Einstein famously called this 'spooky action at a distance,' questioning its compatibility with the theory of relativity.",
            "question": "Why did Einstein question quantum entanglement?",
            "options": ["It contradicted gravity.", "It seemed incompatible with relativity.", "It was never observed.", "It only worked at short distances."],
            "answer": "It seemed incompatible with relativity."
        },
        {
            "passage": "The Great Oxidation Event, roughly 2.4 billion years ago, marked a dramatic rise in atmospheric oxygen levels. This shift, driven by cyanobacteria, was catastrophic for anaerobic organisms but paved the way for complex aerobic life forms.",
            "question": "What caused the Great Oxidation Event?",
            "options": ["Volcanic activity.", "Cyanobacteria.", "Meteor impacts.", "Tectonic shifts."],
            "answer": "Cyanobacteria."
        },
        {
            "passage": "Behavioral economics challenges the classical economic assumption that humans are perfectly rational agents. Researchers like Daniel Kahneman have shown that cognitive biases—such as loss aversion and anchoring—systematically distort decision-making.",
            "question": "What does behavioral economics challenge?",
            "options": ["The existence of markets.", "The assumption of perfect rationality.", "The value of money.", "The role of government."],
            "answer": "The assumption of perfect rationality."
        },
        {
            "passage": "Epigenetics studies how environmental factors can alter gene expression without changing the underlying DNA sequence. Research has shown that diet, stress, and exposure to toxins can modify epigenetic markers, potentially affecting not only the individual but subsequent generations.",
            "question": "What can modify epigenetic markers?",
            "options": ["Only genetic mutations.", "Diet, stress, and toxins.", "Surgical procedures.", "Physical exercise alone."],
            "answer": "Diet, stress, and toxins."
        }
    ]
    for hr in hard_reading:
        questions.append(QuestionItem(
            section="Reading", task_type="ACADEMIC_PASSAGE", difficulty_pool="HARD",
            content_meta={"passage": hr["passage"], "question": hr["question"], "options": hr["options"]},
            correct_answer_key=hr["answer"]
        ))

    # ═══════════════════════════════════════════════════════════
    # READING — Standard Pool (5 unique items)
    # ═══════════════════════════════════════════════════════════
    std_reading = [
        {
            "passage": "Many universities now offer online degree programs that are fully accredited. These programs allow students to study at their own pace while maintaining employment. However, critics argue that the lack of in-person interaction may reduce the quality of education.",
            "question": "What is a concern about online degree programs?",
            "options": ["They are too expensive.", "They lack in-person interaction.", "They are not accredited.", "They take too long to complete."],
            "answer": "They lack in-person interaction."
        },
        {
            "passage": "Public libraries have evolved significantly over the past two decades. Beyond lending books, many now serve as community technology hubs, offering free Wi-Fi, computer access, and digital literacy workshops to bridge the digital divide.",
            "question": "How have public libraries evolved?",
            "options": ["They stopped lending books.", "They became technology hubs.", "They moved online only.", "They increased membership fees."],
            "answer": "They became technology hubs."
        },
        {
            "passage": "Sleep scientists recommend that adults get between seven and nine hours of sleep per night. Chronic sleep deprivation has been linked to increased risks of cardiovascular disease, obesity, and impaired cognitive function.",
            "question": "What is linked to chronic sleep deprivation?",
            "options": ["Improved memory.", "Better physical health.", "Increased disease risks.", "Enhanced creativity."],
            "answer": "Increased disease risks."
        },
        {
            "passage": "Urban green spaces such as parks and community gardens provide important mental health benefits. Studies show that spending as little as 20 minutes in a natural setting can reduce stress hormones and improve mood.",
            "question": "How much time in green spaces can reduce stress?",
            "options": ["At least one hour.", "As little as 20 minutes.", "A full day.", "30 minutes minimum."],
            "answer": "As little as 20 minutes."
        },
        {
            "passage": "The concept of 'food miles' refers to the distance food travels from farm to consumer. Buying locally grown produce reduces transportation emissions and supports regional economies, though it may limit the variety of available foods.",
            "question": "What does 'food miles' measure?",
            "options": ["The weight of food.", "The distance food travels.", "The cost of shipping.", "The freshness of produce."],
            "answer": "The distance food travels."
        }
    ]
    for sr in std_reading:
        questions.append(QuestionItem(
            section="Reading", task_type="READ_DAILY_LIFE", difficulty_pool="STANDARD",
            content_meta={"passage": sr["passage"], "question": sr["question"], "options": sr["options"]},
            correct_answer_key=sr["answer"]
        ))

    # ═══════════════════════════════════════════════════════════
    # LISTENING SECTION — Routing (5 unique), Hard (5), Standard (5)
    # ═══════════════════════════════════════════════════════════
    listening_routing = [
        {"transcript": "Excuse me, do you know where the financial aid office is? I need to drop off some paperwork before noon.", "question": "What does the speaker need to do?", "options": ["Find a classroom.", "Submit paperwork to financial aid.", "Meet a professor.", "Pick up a textbook."], "answer": "Submit paperwork to financial aid."},
        {"transcript": "I was wondering if the biology lab is open on weekends. I need to finish my experiment before Monday.", "question": "Why does the speaker want lab access?", "options": ["To study for an exam.", "To finish an experiment.", "To meet a lab partner.", "To return equipment."], "answer": "To finish an experiment."},
        {"transcript": "The professor mentioned that the midterm will cover chapters one through eight, but she emphasized that chapter five is particularly important.", "question": "Which chapter did the professor emphasize?", "options": ["Chapter one.", "Chapter three.", "Chapter five.", "Chapter eight."], "answer": "Chapter five."},
        {"transcript": "Have you signed up for the study abroad information session? It's next Tuesday at 3 PM in the international center.", "question": "When is the information session?", "options": ["Next Monday.", "Next Tuesday.", "Next Wednesday.", "Next Friday."], "answer": "Next Tuesday."},
        {"transcript": "I really need to talk to my advisor about changing my major. The engineering courses are much harder than I expected.", "question": "Why does the speaker want to see their advisor?", "options": ["To get a tutor.", "To change their major.", "To drop a class.", "To request extra credit."], "answer": "To change their major."}
    ]
    for lr in listening_routing:
        questions.append(QuestionItem(
            section="Listening", task_type="LISTEN_AND_RESPONSE", difficulty_pool="ROUTING",
            content_meta={"transcript": lr["transcript"], "question": lr["question"], "options": lr["options"]},
            correct_answer_key=lr["answer"]
        ))

    listening_hard = [
        {"transcript": "In today's lecture on plate tectonics, we'll examine how subduction zones create volcanic arcs. The key mechanism involves the release of water from the descending plate, which lowers the melting point of the mantle wedge above.", "question": "What lowers the melting point in subduction zones?", "options": ["Heat from the core.", "Water from the descending plate.", "Pressure from the surface.", "Chemical reactions in the crust."], "answer": "Water from the descending plate."},
        {"transcript": "The dopamine reward system plays a crucial role in motivation and learning. When we achieve a goal, dopamine is released in the nucleus accumbens, reinforcing the behavior that led to the reward.", "question": "Where is dopamine released upon achieving a goal?", "options": ["The hippocampus.", "The amygdala.", "The nucleus accumbens.", "The prefrontal cortex."], "answer": "The nucleus accumbens."},
        {"transcript": "Coral bleaching occurs when rising sea temperatures cause corals to expel their symbiotic algae, called zooxanthellae. Without these algae, the corals lose their primary food source and their vibrant colors.", "question": "What causes coral bleaching?", "options": ["Ocean pollution.", "Rising sea temperatures.", "Overfishing.", "Tidal changes."], "answer": "Rising sea temperatures."},
        {"transcript": "The Sapir-Whorf hypothesis suggests that the language we speak shapes how we perceive and categorize the world. Strong versions of this hypothesis claim that language determines thought entirely.", "question": "What does the strong Sapir-Whorf hypothesis claim?", "options": ["Language reflects thought.", "Language determines thought.", "Thought is independent of language.", "All languages are equal."], "answer": "Language determines thought."},
        {"transcript": "In microeconomics, the concept of opportunity cost refers to the value of the next best alternative that must be forgone when a choice is made. It is a fundamental principle in rational decision-making.", "question": "What is opportunity cost?", "options": ["The price of a product.", "The total cost of production.", "The value of the forgone alternative.", "The profit from a sale."], "answer": "The value of the forgone alternative."}
    ]
    for lh in listening_hard:
        questions.append(QuestionItem(
            section="Listening", task_type="ACADEMIC_TALK", difficulty_pool="HARD",
            content_meta={"transcript": lh["transcript"], "question": lh["question"], "options": lh["options"]},
            correct_answer_key=lh["answer"]
        ))

    listening_standard = [
        {"transcript": "The campus shuttle runs every 15 minutes during the week and every 30 minutes on weekends. You can track the shuttle in real time using the university's mobile app.", "question": "How often does the shuttle run on weekends?", "options": ["Every 10 minutes.", "Every 15 minutes.", "Every 30 minutes.", "Every hour."], "answer": "Every 30 minutes."},
        {"transcript": "Don't forget that the deadline for dropping courses without a 'W' on your transcript is this Friday. After that, a withdrawal will appear on your record.", "question": "When is the drop deadline?", "options": ["Next Monday.", "This Wednesday.", "This Friday.", "Next week."], "answer": "This Friday."},
        {"transcript": "The new student health center offers free flu vaccinations to all enrolled students during October. No appointment is necessary—just bring your student ID.", "question": "What do students need to bring for a flu shot?", "options": ["Insurance card.", "Doctor's note.", "Student ID.", "Proof of enrollment."], "answer": "Student ID."},
        {"transcript": "I heard the bookstore is having a 30% off sale on all used textbooks this week. It might be a good time to pick up the books for next semester.", "question": "What is the bookstore offering?", "options": ["Free shipping.", "New textbook bundles.", "A 30% discount on used books.", "A buyback program."], "answer": "A 30% discount on used books."},
        {"transcript": "The writing center has extended its tutoring hours this semester. They now offer evening sessions until 9 PM on Tuesdays and Thursdays.", "question": "When are the new evening sessions?", "options": ["Mondays and Wednesdays.", "Tuesdays and Thursdays.", "Weekends only.", "Every weekday."], "answer": "Tuesdays and Thursdays."}
    ]
    for ls in listening_standard:
        questions.append(QuestionItem(
            section="Listening", task_type="LISTEN_AND_RESPONSE", difficulty_pool="STANDARD",
            content_meta={"transcript": ls["transcript"], "question": ls["question"], "options": ls["options"]},
            correct_answer_key=ls["answer"]
        ))

    # ═══════════════════════════════════════════════════════════
    # WRITING SECTION — All FIXED pool (12 unique items)
    # ═══════════════════════════════════════════════════════════
    
    # BUILD_SENTENCE (4 unique)
    build_sentences = [
        {"prompt": "Arrange the words to form a grammatically correct sentence about research.", "scrambled_words": ["the", "findings", "suggest", "a", "significant", "correlation"]},
        {"prompt": "Create a sentence describing a historical event.", "scrambled_words": ["revolution", "the", "transformed", "society", "industrial", "dramatically"]},
        {"prompt": "Form a sentence about environmental policy.", "scrambled_words": ["governments", "must", "implement", "sustainable", "energy", "policies"]},
        {"prompt": "Construct a sentence about technological advancement.", "scrambled_words": ["artificial", "intelligence", "is", "reshaping", "modern", "industries"]}
    ]
    for bs in build_sentences:
        questions.append(QuestionItem(
            section="Writing", task_type="BUILD_SENTENCE", difficulty_pool="FIXED",
            content_meta=bs, correct_answer_key=None
        ))

    # WRITE_EMAIL (4 unique)
    emails = [
        {"prompt": "Write a formal email to your professor requesting a deadline extension for your research paper. Explain your circumstances and propose a new submission date.", "bullets": ["State your course and assignment.", "Explain the reason for the request.", "Propose a specific new deadline."]},
        {"prompt": "Compose an email to the campus IT department reporting a persistent login issue with the student portal.", "bullets": ["Describe the problem clearly.", "Include your student ID number.", "Mention any error messages you've seen."]},
        {"prompt": "Write an email to a potential internship supervisor expressing your interest in their summer research program.", "bullets": ["Introduce yourself and your qualifications.", "Explain why you are interested.", "Ask about the application process."]},
        {"prompt": "Draft an email to your academic advisor requesting guidance on selecting elective courses for next semester.", "bullets": ["Mention your major and year.", "List your areas of interest.", "Ask for available meeting times."]}
    ]
    for em in emails:
        questions.append(QuestionItem(
            section="Writing", task_type="WRITE_EMAIL", difficulty_pool="FIXED",
            content_meta=em, correct_answer_key=None
        ))

    # ACADEMIC_DISCUSSION (4 unique)
    discussions = [
        {"prompt": "Should universities require all students to take a course in financial literacy before graduating?", "context": "Professor: Today we're discussing financial education. Some argue it's essential for real-world preparedness, while others say it takes time away from students' chosen disciplines."},
        {"prompt": "Is social media a net positive or negative for democratic discourse?",  "context": "Professor: This week's topic is the role of social media in democracy. Proponents say it amplifies voices; critics warn about misinformation and echo chambers."},
        {"prompt": "Should autonomous vehicles be allowed on public roads before they achieve zero accident rates?", "context": "Professor: Let's discuss the ethics of self-driving cars. The technology isn't perfect, but neither are human drivers. Where do we draw the line?"},
        {"prompt": "Are standardized tests an effective measure of student ability and potential?", "context": "Professor: Standardized testing has been debated for decades. Some educators find them useful for benchmarking, while others argue they disadvantage certain student populations."}
    ]
    for disc in discussions:
        questions.append(QuestionItem(
            section="Writing", task_type="ACADEMIC_DISCUSSION", difficulty_pool="FIXED",
            content_meta=disc, correct_answer_key=None
        ))

    # ═══════════════════════════════════════════════════════════
    # SPEAKING SECTION — All FIXED pool (11 items total)
    # ═══════════════════════════════════════════════════════════
    
    # LISTEN_AND_REPEAT (7 unique sentences)
    phrases = [
        "The cognitive development of children is a complex and multifaceted field of study.",
        "Please submit your laboratory reports to the teaching assistant by Friday afternoon.",
        "Societal norms often dictate individual behavior in surprising and unexpected ways.",
        "The volcanic eruption had a measurable cooling effect on the global climate system.",
        "Effective communication is widely considered the cornerstone of successful leadership.",
        "Renewable energy sources are becoming increasingly cost-effective compared to fossil fuels.",
        "The architecture of the ancient temple reflects the deeply held cultural values of its builders."
    ]
    for phrase in phrases:
        questions.append(QuestionItem(
            section="Speaking", task_type="LISTEN_AND_REPEAT", difficulty_pool="FIXED",
            content_meta={"phrase": phrase}, correct_answer_key=None
        ))

    # TAKE_INTERVIEW (4 unique prompts)
    interviews = [
        "Tell me about a time when you had to work on a team project. What role did you play, and what did you learn from the experience?",
        "Describe a course you took that significantly changed your perspective on a topic. What made it so impactful?",
        "If you could solve one global problem, what would it be, and how would you begin to address it?",
        "What are the most important qualities a university graduate should have, and why?"
    ]
    for iv in interviews:
        questions.append(QuestionItem(
            section="Speaking", task_type="TAKE_INTERVIEW", difficulty_pool="FIXED",
            content_meta={"prompt": iv}, correct_answer_key=None
        ))

    # ═══════════════════════════════════════════════════════════
    # PERSIST
    # ═══════════════════════════════════════════════════════════
    with Session(engine) as session:
        session.exec(delete(QuestionItem))
        session.add_all(questions)
        session.commit()
    return len(questions)

if __name__ == "__main__":
    count = seed_data()
    print(f"Database seeded with {count} unique items.")

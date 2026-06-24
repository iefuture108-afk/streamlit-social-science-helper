import streamlit as st

st.set_page_config(page_title="Social Science Helper", layout="wide")

LESSONS = {
    "map": {
        "title": "Maps And Directions",
        "explanation": "A map is a small drawing of a big place. It helps us find roads, rivers, cities, states, and countries. Directions like north, south, east, and west help us know where things are.",
        "points": ["Maps show places from above.", "Symbols stand for real things.", "A compass shows directions.", "Maps help us travel and learn about places."],
        "example": "If your school is north of your home, a map can help you find the road to reach it.",
        "activity": "Draw a simple map from your home to your school and mark one road, one shop, and one turn.",
        "questions": ["What is a map?", "Name four main directions.", "Why do we use symbols on a map?"],
    },
    "transport": {
        "title": "Transport",
        "explanation": "Transport means ways of moving people and goods from one place to another. Road, rail, water, and air transport help us travel and send things faster.",
        "points": ["Buses and cars move on roads.", "Trains move on railway tracks.", "Ships move on water.", "Aeroplanes move through air."],
        "example": "Milk, fruits, and books reach shops by different types of transport.",
        "activity": "Make four columns: road, rail, water, air. Write two examples in each.",
        "questions": ["What is transport?", "Which transport moves on tracks?", "Why is transport important?"],
    },
    "water": {
        "title": "Water Sources",
        "explanation": "Water is needed by people, plants, and animals. We get water from rain, rivers, lakes, ponds, wells, and taps. We should not waste or dirty water.",
        "points": ["Rain is an important source of water.", "Rivers and lakes store water.", "Clean water keeps us healthy.", "Saving water helps everyone."],
        "example": "We use water for drinking, bathing, cooking, and watering plants.",
        "activity": "List five ways your family uses water in one day.",
        "questions": ["Name two sources of water.", "Why should we save water?", "How can we keep water clean?"],
    },
    "festival": {
        "title": "Festivals",
        "explanation": "Festivals are special days when people celebrate together. They teach us joy, sharing, respect, and unity.",
        "points": ["Festivals bring families together.", "People wear special clothes.", "Many festivals have special food.", "We should respect all festivals."],
        "example": "During Diwali, many people light lamps. During Eid, many people share sweets.",
        "activity": "Write three lines about your favorite festival.",
        "questions": ["What is a festival?", "Why do people celebrate festivals?", "How can we respect all festivals?"],
    },
    "monument": {
        "title": "Historical Places And Monuments",
        "explanation": "Monuments are old and important buildings or places. They tell us about history and the way people lived long ago.",
        "points": ["Monuments are part of our heritage.", "They teach us about the past.", "We should keep them clean.", "Many people visit monuments to learn."],
        "example": "The Taj Mahal, Red Fort, and Qutub Minar are famous monuments in India.",
        "activity": "Pick one monument and write its name, city, and one fact.",
        "questions": ["What is a monument?", "Why should we protect monuments?", "Name one monument in India."],
    },
    "environment": {
        "title": "Our Environment",
        "explanation": "The environment means the air, water, land, plants, animals, and people around us. We should keep it clean.",
        "points": ["Trees give us clean air.", "Pollution makes air and water dirty.", "We should reduce waste.", "Clean surroundings keep us healthy."],
        "example": "Throwing waste in a dustbin helps keep streets and parks clean.",
        "activity": "Plant a seed or clean one small area with an adult.",
        "questions": ["What is environment?", "Why are trees important?", "How can we reduce pollution?"],
    },
    "general": {
        "title": "Easy Social Science Study Help",
        "explanation": "Social Science helps us learn about people, places, history, nature, rules, and how we live together.",
        "points": ["Look carefully at the picture.", "Find the main topic.", "Ask what, where, why, and how.", "Connect it with daily life."],
        "example": "If the picture shows a market, think about buyers, sellers, goods, money, and transport.",
        "activity": "Write the topic name, draw the picture, and label three important things.",
        "questions": ["What do you see in the picture?", "What is the topic about?", "Where do we see this in real life?"],
    },
}

MATCHES = {
    "map": ["map", "direction", "north", "south", "east", "west", "globe"],
    "transport": ["transport", "bus", "train", "car", "ship", "aeroplane", "vehicle"],
    "water": ["water", "river", "rain", "lake", "sea", "well", "pond"],
    "festival": ["festival", "diwali", "eid", "christmas", "holi"],
    "monument": ["monument", "fort", "taj", "temple", "historical"],
    "environment": ["environment", "pollution", "tree", "forest", "clean", "nature"],
}

def detect_topic(text):
    text = text.lower()
    for topic, words in MATCHES.items():
        if any(word in text for word in words):
            return topic
    return "general"

st.title("Social Science Helper")
st.write("Free app for Class 3 to 5. Upload image, type topic hint, and get easy explanation.")

grade = st.radio("Choose class", ["3", "4", "5"], horizontal=True)
topic_hint = st.text_input("Topic hint", placeholder="Example: map, transport, water, festival, monument")
image = st.file_uploader("Upload Social Science image", type=["png", "jpg", "jpeg", "webp"])

if image:
    st.image(image, caption="Uploaded image", use_container_width=True)

if st.button("Explain Simply", type="primary"):
    lesson = LESSONS[detect_topic(topic_hint)]

    st.subheader(lesson["title"])
    st.info(f"Class {grade} topic: {topic_hint if topic_hint else 'General Social Science'}")

    st.markdown("### Easy Explanation")
    st.write(lesson["explanation"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Key Points")
        for point in lesson["points"]:
            st.write("- " + point)

        st.markdown("### Quick Activity")
        st.write(lesson["activity"])

    with col2:
        st.markdown("### Real Life Example")
        st.write(lesson["example"])

        st.markdown("### Practice Questions")
        for i, question in enumerate(lesson["questions"], 1):
            st.write(f"{i}. {question}")

    st.success("Parent tip: Ask the child to explain this answer in their own words.")

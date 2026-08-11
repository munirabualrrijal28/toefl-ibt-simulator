# toefl-ibt-simulator
A dynamic, multi-stage TOEFL iBT test simulator built with FastAPI. [Work in Progress]

# 🎓 TOEFL iBT Test Simulator [Work in Progress]

## 📝 Overview
A dynamic, multi-stage TOEFL iBT test simulator designed to replicate the official exam environment. Currently focusing on the **Reading Section**, this backend application is built to handle complex, time-sensitive testing logic, asynchronous operations, and dynamic content delivery. 

## 🚀 Tech Stack
* **Backend Framework:** FastAPI (Python)
* **Architecture:** RESTful API design & Modular structure
* **Data Handling:** Pydantic (Data validation) & JSON/Relational Database

## ⚙️ Key Features
* **Asynchronous Performance:** Built utilizing FastAPI's async capabilities for high-performance, non-blocking API requests.
* **Reading Module (Active):** Fully functional reading comprehension engine with real-time logical evaluation.
* **Scalable System Design:** Architected with a clean, modular structure to seamlessly integrate upcoming sections (Listening, Speaking, Writing).
* **Robust Routing:** Efficient endpoint routing to manage multi-stage test states and user sessions.

## 🛠️ Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/munirabualrrijal28/toefl-ibt-simulator.git](https://github.com/munirabualrrijal28/toefl-ibt-simulator.git)
2. **Navigate to the project directory:**
  ```bash
  cd toefl-ibt-simulator

```
3. **Install dependencies:**
  ```bash
  pip install -r requirements.txt
```
4. **Run the FastAPI server:**
  ```bash
  uvicorn main:app --reload
```
## 🚧 Roadmap
[x] Core Backend Architecture ,
[x] Reading Section Logic & API Endpoints , 
[ ] Listening Section Integration ,
[ ] Database Migration & User Authentication

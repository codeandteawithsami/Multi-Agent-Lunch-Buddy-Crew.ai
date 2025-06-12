# 🍽️ Lunch Buddy Crew

**Lunch Buddy Crew** is a multi-agent system that helps users find the perfect lunch spot based on their mood, cravings, dietary preferences, and location.

![Lunch Buddy UI](./frontend-preview.png)

Lunch Buddy Crew uses an intelligent multi-agent backend to analyze your inputs and suggest personalized restaurants based on mood, cravings, dietary filters, and location. The frontend is a simple, clean HTML/JS interface designed to collect user preferences and display recommendations.

---

## 🔁 Clone the Repository

```bash
git clone https://github.com/your-username/Multi-Agent-Lunch-Buddy-Crew.git
cd Multi-Agent-Lunch-Buddy-Crew
```

# Backend Setup


```bash
pip install -r requirements.txt
```

```bash
python main.py
```

This launches the multi-agent backend server that processes user mood, cravings, and preferences to generate recommendations.

# Frontend Setup

Navigate to the `frontend/` folder and open `index.html`:

* Recommended: Use **Live Server** (e.g., VS Code Live Server extension).
* Alternative: Open `index.html` directly in your browser (some features may require a local server).# Project Structure

  ```bash
  Multi-Agent-Lunch-Buddy-Crew/
  │
  ├── main.py               # API
  ├── Lunch_Buddy.py        # Backend logic (multi-agent reasoning system)
  ├── tools                 # Backend logic (multi-agent reasoning system)
  ├── utils.py              # Backend logic (multi-agent reasoning system)
  ├── requirements.txt      # Clean list of used Python packages
  │
  ├── frontend/
  │   ├── index.html          # Main user interface

  ```
  ## Example Input

  Example user input:


  * Mood: “I’m feeling energetic and happy today. Looking for something special to celebrate my promotion!”
  * Cravings: `butter chicken`, `pizza`
  * Location: `New York`
  * Dietary: `Halal`, `Gluten-Free`

  🧠 The system will return a list of suitable restaurants tailored to your mood and preferences.

  ## Technologies Used

  * **Python** (multi-agent backend)
  * **HTML/CSS/JS** (frontend UI)
  * **pipreqs** to generate minimal `requirements.txt`

  ## 🙌 Author

  Developed by [Samiullah Saleem](https://github.com/codeandteawithsami). Contributions welcome!

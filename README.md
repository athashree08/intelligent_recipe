# Snap2Serve – Intelligent Recipe Generator

**Smart cooking made simple: From photo to feast in seconds.**

## Project Overview

Snap2Serve is an AI-powered web application designed to solve the common household dilemma of "what to cook?" by generating personalized recipes based on ingredients already available at home. The system leverages computer vision to automatically detect ingredients from user-uploaded images and utilizes natural language processing (LLMs) to craft detailed, step-by-step cooking instructions.

This solution reduces food waste, saves time on meal planning, and encourages home cooking through an intuitive and modern web interface.

## Core Features

- **Ingredient Detection**: Instantly identifies ingredients from photos using advanced image processing (MobileNetV2/Food-101) and OCR technology.
- **AI Recipe Generation**: Generates complete, unique recipes with cooking steps, nutritional information, and dietary tags using OpenAI's GPT models.
- **Nutrition Analysis**: improved accuracy for calorie and nutrient tracking using USDA FoodData Central integration.
- **Smart Search & Filters**: Allows users to manually add ingredients and filter recipes by cuisine, dietary restrictions (Vegan, Gluten-Free), and cooking time.
- **User Dashboard**: Personalized experience for saving favorite recipes and managing dietary preferences.
- **Responsive Design**: Modern, distinct aesthetics featuring an organic "La Petite Cuisine" theme with seamless navigation.

## System Architecture

The application follows a modular client-server architecture:

1.  **Frontend**: Built with React and Tailwind CSS, handling user interactions, image uploads, and data visualization.
2.  **Backend API**: A Flask-based RESTful API that manages authentication, image processing requests, and external API integrations.
3.  **AI/ML Service**: 
    -   **Vision Layer**: Processes images to extract ingredient labels.
    -   **LLM Layer**: Synthesizes ingredients into cohesive recipes.
4.  **Database**: MongoDB stores user profiles, saved recipes, and cached ingredient data to minimize API costs and latency.

## Folder Structure

```
intelligent_recipe/
├── backend/                # Flask API and core logic
│   ├── app.py              # Application entry point
│   ├── routes/             # API endpoints (auth, recipes, images)
│   ├── models/             # Database models and ML binaries
│   ├── utils/              # Helper functions (OCR, Nutrition API)
│   ├── image_processing/   # Vision processing logic
│   └── requirements.txt    # Python dependencies
├── frontend/               # React application
│   ├── src/                # Components, pages, and hooks
│   ├── public/             # Static assets
│   └── tailwind.config.js  # Styling configuration
└── README.md               # Project documentation
```

## Setup & Installation

Follow these steps to set up the project locally.

### Prerequisites
- Python 3.8+
- Node.js 14+ and npm
- MongoDB installed and running locally

### 1. Clone the Repository
```bash
git clone https://github.com/athashree08/intelligent_recipe.git
cd intelligent_recipe
```

### 2. Backend Setup
Create a virtual environment and store your API keys safely.

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Environment Configuration**:
Create a `.env` file in the `backend/` directory:
```env
MONGO_URI=mongodb://localhost:27017/intelligent_recipe
JWT_SECRET_KEY=your_secure_random_key
OPENAI_API_KEY=your_openai_api_key
USDA_API_KEY=your_usda_api_key
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

### 4. Running the Application
Open two terminal windows:

**Terminal 1 (Backend):**
```bash
cd backend
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

The application will be accessible at `http://localhost:5173`.

## How It Works

1.  **Image Input**: The user takes a photo of their pantry or fridge.
2.  **Processing**: The backend receives the image. Specialized OCR and classification algorithms analyze the visual data to list detected ingredients (e.g., "Tomato," "Eggs," "Basil").
3.  **Recipe Synthesis**: This list is augmented with user preferences and sent to the LLM (Large Language Model), which constructs a valid recipe.
4.  **Nutrition Calculation**: Use the USDA database to calculate precise nutritional values based on ingredient quantities.
5.  **Output**: The user sees a beautiful recipe card with instructions, time estimates, and match percentages.

## Security & API Key Management

-   **Environment Variables**: All sensitive keys (OpenAI, JWT, USDA) are stored strictly in `.env` files which are git-ignored.
-   **No Hardcoding**: The codebase contains no hardcoded secrets.
-   **Authentication**: User sessions are secured using JWT (JSON Web Tokens) with secure HTTP-only practices.

## Future Scope

-   **Mobile App**: Development of a native React Native application for easier camera access.
-   **Pantry Tracking**: Persistent inventory management to track expiration dates.
-   **Social Features**: Ability to share creations and cook with friends.
-   **Fine-tuned Models**: Training a custom LLaMA model specifically for culinary tasks to reduce API dependency.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
